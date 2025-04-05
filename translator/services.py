from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
from fastapi import HTTPException
from typing import Mapping

# Загрузка языкового mapping из JSON
with open('languages.json', 'r', encoding='utf-8') as f:
    LANGUAGE_MAP = json.load(f)

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
    async def preload_models(cls):
        """Предзагрузка всех возможных языковых пар"""
        supported_pairs = [
            (source, target)
            for source in LANGUAGE_MAP.keys()
            for target in LANGUAGE_MAP.keys()
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
    async def translate(cls, source_lang: str, target_lang: str, text: str) -> str:
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
        if source_lang not in LANGUAGE_MAP or target_lang not in LANGUAGE_MAP:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language code. Supported codes: {", ".join(LANGUAGE_MAP.keys())}"
            )

        # Получаем токенизатор и модель для данной языковой пары
        tokenizer, model = await cls._load_translation_tools(source_lang, target_lang)
        
        # Формируем промпт для перевода
        source_lang_name = LANGUAGE_MAP[source_lang]
        target_lang_name = LANGUAGE_MAP[target_lang]
        input_text = f"translate {source_lang_name} to {target_lang_name}: {text}"
        
        # Кодируем и генерируем перевод
        input_ids = tokenizer.encode(input_text, return_tensors='pt')
        output_ids = model.generate(input_ids)
        translated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        return translated_text