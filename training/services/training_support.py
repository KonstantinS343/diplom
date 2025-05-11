from typing import Sequence, Mapping
from fastapi import Depends, HTTPException

from repositories import MongoService, TranslatorRepository


class TranslatorSupportService:
    def __init__(
        self,
        respository: MongoService = Depends(),
        translator_repo: TranslatorRepository = Depends(),
    ) -> None:
        self.respository = respository
        self.translator_repo = translator_repo

    async def check_user_file(
        self, dataset: Sequence[Mapping[str, str]], source_lang, target_lang
    ) -> bool:
        if not isinstance(dataset, list):
            return False

        for i in dataset:
            if not isinstance(i, dict):
                return False

            if source_lang not in i.keys() or target_lang not in i.keys():
                return False
        return True

    async def user_file_upload(
        self, dataset: Sequence[Mapping[str, str]], source_lang: str, target_lang: str
    ) -> str:
        if not await self.check_user_file(dataset, source_lang, target_lang):
            raise HTTPException(status_code=400, detail="Invalid dataset format")

        return await self.respository.insert_many(f"{source_lang}-{target_lang}", dataset)

    async def get_language_pairs(self) -> Mapping[str, str]:
        supported_langs = (await self.translator_repo.get_languages()).keys()

        dataset_pairs = await self.respository.get_collections()
        dataset_pairs = {i.split("-")[0]: i.split("-")[1] for i in dataset_pairs if "-" in i}

        language_pairs = {"old": {}, "new": {}}

        for source, target in dataset_pairs.items():
            if source in supported_langs and target in supported_langs:
                language_pairs["old"][source] = target
            else:
                language_pairs["new"][source] = target

        return language_pairs

    async def create_language_pair(self, source_lang: str, target_lang: str) -> bool:
        if source_lang == target_lang:
            raise HTTPException(
                status_code=400, detail="Source and target languages cannot be the same"
            )

        dataset_pairs = await self.respository.get_collections()

        if f"{source_lang}-{target_lang}" in dataset_pairs:
            raise HTTPException(status_code=400, detail="Language pair already exists")

        return await self.respository.create_collection(f"{source_lang}-{target_lang}")

    async def get_language_dataset(self, source_lang: str, target_lang: str, user_id: str) -> Mapping[str, str]:
        supported_langs = (await self.translator_repo.get_languages()).keys()

        if source_lang not in supported_langs or target_lang not in supported_langs:
            raise HTTPException(status_code=400, detail="Unsupported language pair")

        collection = f"{source_lang}-{target_lang}"
        cards = await self.respository.get(collection)
        
        # Получаем голоса пользователя
        user_votes = await self.respository.get_user_votes(user_id)
        
        # Добавляем информацию о голосе пользователя к каждой карточке
        for card in cards:
            card_id = card["_id"]
            if card_id in user_votes:
                card["user_vote"] = user_votes[card_id]
            else:
                card["user_vote"] = None

        return cards

    async def add_like(self, card_id: str, collection: str, user_id: str) -> bool:
        return await self.respository.add_like(collection, card_id, user_id)

    async def add_dislike(self, card_id: str, collection: str, user_id: str) -> bool:
        return await self.respository.add_dislike(collection, card_id, user_id)
