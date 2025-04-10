import logging

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import HTTPException, Depends


class AutocomplateService:
    _model = None
    _tokenizer = None

    async def preload_model(self):
        try:
            logging.warning(f"Loading model 'Kanstantsin/bert_eli5_mlm_model'")
            self._tokenizer = AutoTokenizer.from_pretrained(
                "google-bert/bert-base-multilingual-cased"
            )
            self._model = AutoModelForSeq2SeqLM.from_pretrained("Kanstantsin/bert_eli5_mlm_model")
            logging.warning(f"Model 'Kanstantsin/bert_eli5_mlm_model' loaded successfully")
        except HTTPException as e:
            logging.warning(f"Failed to load model 'Kanstantsin/bert_eli5_mlm_model': {e.detail}")

    async def predics(self, text: str, cursor_position: int) -> str:
        text = text[:cursor_position] + " [MASK] " + text[cursor_position:]

        inputs = self._tokenizer(text, return_tensors="pt")
        mask_token_index = torch.where(inputs["input_ids"] == self._tokenizer.mask_token_id)[1]

        logits = self._model(**inputs).logits
        mask_token_logits = logits[0, mask_token_index, :]

        return torch.topk(mask_token_logits, 3, dim=1).indices[0].tolist()[0]
