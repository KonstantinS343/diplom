import aiohttp

from fastapi import HTTPException


class TranslationService:
    def __init__(self, translator_url: str):
        self.translator_url = translator_url

    async def translate(self, text: str, target_lang: str, source_lang: str) -> str:
        """
        Translate the given text using the specified translation service.
        """
        model_translation = await self._translation_request(text, target_lang, source_lang)
        if not model_translation:
            raise HTTPException(
                status_code=500, detail="Translation service not available or failed"
            )

        return model_translation

    async def _translation_request(self, text: str, target_lang: str, source_lang: str) -> str:
        """
        Send a translation request to the translation service.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.translator_url,
                json={"text": text, "target_lang": target_lang, "source_lang": source_lang},
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Translation service failed with status code {response.status}",
                    )
                data = await response.json()
                return data.get("text")
