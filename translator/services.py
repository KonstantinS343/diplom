from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Mapping, Sequence
from models import TranslatorDAO

class TranslationService:
    # Кэш для токенизаторов и моделей
    _tokenizers: Mapping[str, AutoTokenizer] = {}
    _models: Mapping[str, AutoModelForSeq2SeqLM] = {}
    
    @classmethod
    async def _get_model_key(cls, source_lang: str, target_lang: str) -> str:
        """Генерирует ключ для модели на основе языковой пары"""
        return f"{source_lang}-{target_lang}"
    
    @classmethod
    async def _load_translation_tools(cls, source_lang: str, target_lang: str) -> tuple:
        """Загружает или возвращает из кэша токенизатор и модель"""
        model_key = await cls._get_model_key(source_lang, target_lang)
        
        if model_key not in cls._tokenizers:
            try:
                # Предполагаем, что модели следуют шаблону Kanstantsin/t5-trans-small-{source}-{target}
                model_name = f"Kanstantsin/t5-trans-small-{source_lang}-{target_lang}"
                cls._tokenizers[model_key] = AutoTokenizer.from_pretrained(model_name)
                cls._models[model_key] = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            except Exception as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Translation model for {source_lang} to {target_lang} is unavailable: {str(e)}"
                )
        
        return cls._tokenizers[model_key], cls._models[model_key]
    
    @classmethod
    async def preload_models(cls, translator_dao: TranslatorDAO, db: AsyncSession):
        """Предзагрузка всех возможных языковых пар"""
        languages = await translator_dao.get_languages(db)

        supported_pairs = [
            (source, target)
            for source in languages.keys()
            for target in languages.keys()
            if source != target  # Исключаем перевод с языка на тот же язык
        ]
        
        for source_lang, target_lang in supported_pairs:
            try:
                print(f"Loading model for {source_lang} -> {target_lang}")
                await cls._load_translation_tools(source_lang, target_lang)
                print(f"Model for {source_lang} -> {target_lang} loaded successfully")
            except HTTPException as e:
                print(f"Failed to load model for {source_lang} -> {target_lang}: {e.detail}")
                
    @classmethod
    def _split_text_with_overlap(cls, text: str, tokenizer: AutoTokenizer, max_length: int, overlap: int = 50) -> Sequence[str]:
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

    @classmethod
    def _merge_translated_chunks(cls, translated_chunks: Sequence[str]) -> str:
        """Простое объединение переведённых кусков с минимальной обработкой."""
        return " ".join(chunk.strip() for chunk in translated_chunks)

    @classmethod
    async def translate(cls, source_lang: str, target_lang: str, text: str, translator_dao: TranslatorDAO, db: AsyncSession) -> str:
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
        languages = await translator_dao.get_languages(db)
        
        if source_lang not in languages or target_lang not in languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language code. Supported codes: {", ".join(languages.keys())}"
            )

        # Получаем токенизатор и модель для данной языковой пары
        tokenizer, model = await cls._load_translation_tools(source_lang, target_lang)
        
        # Формируем промпт для перевода
        source_lang_name = languages[source_lang]
        target_lang_name = languages[target_lang]
        prompt_prefix = f"translate {source_lang_name} to {target_lang_name}: "
        overlap = 16
        
        # Вычисляем максимальную длину с учётом промпта
        max_model_length = 512 - len(tokenizer.encode(prompt_prefix))
        
        # Разбиваем текст на куски с перекрытием
        text_chunks = cls._split_text_with_overlap(text, tokenizer, max_length=max_model_length, overlap=overlap)
        
        # Переводим каждый кусок
        translated_chunks = []
        for chunk in text_chunks:
            input_text = prompt_prefix + chunk
            input_ids = tokenizer.encode(input_text, return_tensors='pt')
            output_ids = model.generate(input_ids, max_length=512)
            translated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            translated_chunks.append(translated_text)
        
        # Объединяем переведённые куски с учётом перекрытия
        return cls._merge_translated_chunks(translated_chunks, overlap, tokenizer)