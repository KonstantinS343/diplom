import logging
from typing import Optional
import re

import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM
from fastapi import HTTPException, Depends

from rules import unwanted_chars, patterns


class AutocomplateService:
    _tokenizer: Optional[AutoTokenizer] = None
    _model: Optional[AutoModelForMaskedLM] = None

    @classmethod
    async def preload_model(cls):
        try:
            logging.warning(f"Loading model 'Kanstantsin/bert_eli5_mlm_model'")
            cls._tokenizer = AutoTokenizer.from_pretrained(
                "google-bert/bert-base-multilingual-cased"
            )
            cls._model = AutoModelForMaskedLM.from_pretrained("Kanstantsin/bert_eli5_mlm_model")
            logging.warning(f"Model 'Kanstantsin/bert_eli5_mlm_model' loaded successfully")
        except HTTPException as e:
            logging.warning(f"Failed to load model 'Kanstantsin/bert_eli5_mlm_model': {e.detail}")

    async def predict(self, text: str, cursor_position: int, language: str) -> str:
        text = text[:cursor_position] + " [MASK] " + text[cursor_position:]

        if text.rstrip().endswith("[MASK]"):
            text = text.rstrip() + "."
            
        logging.info(text)

        inputs = self._tokenizer(text, return_tensors="pt")
        mask_token_index = torch.where(inputs["input_ids"] == self._tokenizer.mask_token_id)[1]

        logits = self._model(**inputs).logits
        mask_token_logits = logits[0, mask_token_index]

        top_k = 100
        top_token_ids = torch.topk(mask_token_logits, top_k, dim=-1).indices[0]
        
        lang_pattern = patterns.get(language, r'^[a-zA-Z]+$')
        for token_id in top_token_ids:
            predicted_token = self._tokenizer.decode([token_id]).strip()
            if not re.search(unwanted_chars, predicted_token) and re.match(lang_pattern, predicted_token):
                return predicted_token

        return ""
