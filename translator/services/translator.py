import logging
from typing import Mapping, Sequence
import nltk
nltk.download('punkt_tab')

from transformers import MarianTokenizer, MarianMTModel
from fastapi import HTTPException, Depends

from repositories.translator import TranslatorRepository


class TranslationService:
    _tokenizers: Mapping[str, MarianTokenizer] = {}
    _models: Mapping[str, MarianMTModel] = {}
    respository: TranslatorRepository

    def __init__(self, respository: TranslatorRepository = Depends()):
        self.respository = respository

    async def _get_model_key(self, source_lang: str, target_lang: str) -> str:
        """Генерирует ключ для модели на основе языковой пары"""
        return f"{source_lang}-{target_lang}"

    async def _load_translation_tools(self, source_lang: str, target_lang: str) -> tuple:
        """Загружает или возвращает из кэша токенизатор и модель"""
        model_key = await self._get_model_key(source_lang, target_lang)

        if model_key not in self._tokenizers:
            try:
                model_name = f"Kanstantsin/trans-{source_lang}-{target_lang}"
                self._tokenizers[model_key] = MarianTokenizer.from_pretrained(model_name)
                self._models[model_key] = MarianMTModel.from_pretrained(model_name)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Translation model for {source_lang} to {target_lang} is unavailable: {str(e)}",
                )

        return self._tokenizers[model_key], self._models[model_key]

    async def preload_models(self):
        """Предзагрузка всех возможных языковых пар"""
        languages = await self.respository.get_languages()

        supported_pairs = [
            (source, target)
            for source in languages.keys()
            for target in languages.keys()
            if source != target
        ]

        for source_lang, target_lang in supported_pairs:
            try:
                logging.warning(f"Loading model for {source_lang} -> {target_lang}")
                await self._load_translation_tools(source_lang, target_lang)
                logging.warning(f"Model for {source_lang} -> {target_lang} loaded successfully")
            except HTTPException as e:
                logging.warning(
                    f"Failed to load model for {source_lang} -> {target_lang}: {e.detail}"
                )
                
    async def _chunk_separator(self, text: str, tokenizer: MarianTokenizer, max_tokens: int) -> Sequence[str]:
        sentences = nltk.sent_tokenize(text)
        
        chunks = []
        current_chunk = []
        current_token_count = 0

        for sentence in sentences:
            tokens = tokenizer.encode(sentence, add_special_tokens=False)
            token_count = len(tokens)

            if current_token_count + token_count <= max_tokens:
                current_chunk.append(sentence)
                current_token_count += token_count
            else:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))

                current_chunk = [sentence]
                current_token_count = token_count
                
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks

    async def translate(self, source_lang: str, target_lang: str, text: str, max_tokens: int = 32) -> str:
        """
        Переводит текст с одного языка на другой

        Args:
            source_lang: код исходного языка (напр. 'de', 'en', 'aa')
            target_lang: код целевого языка (напр. 'de', 'en', 'aa')
            text: текст для перевода

        Returns:
            переведенный текст
        Raises:
            HTTPException: если язык не поддерживается или возникла ошибка
        """
        languages = await self.respository.get_languages()

        if source_lang not in languages or target_lang not in languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language code. Supported codes: {', '.join(languages.keys())}",
            )

        tokenizer, model = await self._load_translation_tools(source_lang, target_lang)
        
        chunks = await self._chunk_separator(text, tokenizer, max_tokens)
        translated_chunks = []

        for chunk in chunks:
            input_ids = tokenizer(
                chunk,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_tokens
            )

            output_ids = model.generate(
                **input_ids,
                max_length=max_tokens
            )

            translated_chunk = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            translated_chunks.append(translated_chunk)
        translated_text = " ".join(translated_chunks)

        return translated_text
