import logging
from typing import Mapping, Sequence

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import HTTPException, Depends

from repositories.translator import TranslatorRepository


class TranslationService:
    _tokenizers: Mapping[str, AutoTokenizer] = {}
    _models: Mapping[str, AutoModelForSeq2SeqLM] = {}
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
                model_name = f"Kanstantsin/t5-trans-small-{source_lang}-{target_lang}"
                self._tokenizers[model_key] = AutoTokenizer.from_pretrained(model_name)
                self._models[model_key] = AutoModelForSeq2SeqLM.from_pretrained(model_name)
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

    def _split_text_with_overlap(
        self, text: str, tokenizer: AutoTokenizer, max_length: int, overlap: int = 50
    ) -> Sequence[str]:
        """Разбивает текст на части с перекрытием."""
        tokens = tokenizer.encode(text, add_special_tokens=False)
        if len(tokens) <= max_length:
            return [text]

        chunks = []
        start = 0

        while start < len(tokens):
            end = min(start + max_length, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True).strip()
            chunks.append(chunk_text)
            start += max_length - overlap
            if end == len(tokens):
                break

        return chunks

    def _merge_translated_chunks(self, translated_chunks: Sequence[str]) -> str:
        """Простое объединение переведённых кусков с минимальной обработкой."""
        return " ".join(chunk.strip() for chunk in translated_chunks)

    async def translate(self, source_lang: str, target_lang: str, text: str) -> str:
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

        source_lang_name = languages[source_lang]
        target_lang_name = languages[target_lang]
        prompt_prefix = f"translate {source_lang_name} to {target_lang_name}: "
        overlap = 16

        max_model_length = 512 - len(tokenizer.encode(prompt_prefix))

        text_chunks = self._split_text_with_overlap(
            text, tokenizer, max_length=max_model_length, overlap=overlap
        )

        translated_chunks = []
        for chunk in text_chunks:
            input_text = prompt_prefix + chunk
            input_ids = tokenizer.encode(input_text, return_tensors="pt")
            output_ids = model.generate(input_ids, max_length=512)
            translated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            translated_chunks.append(translated_text)

        return self._merge_translated_chunks(translated_chunks)
