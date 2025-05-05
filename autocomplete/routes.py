from fastapi import APIRouter, Depends

from schemas import AutocompleteRequest
from services import AutocomplateService

router = APIRouter(tags=["autocomplete"], prefix="/v1/api/autocomplete")


@router.post("/")
async def autocomplete(request: AutocompleteRequest, service: AutocomplateService = Depends()):
    return await service.predict(request.text, request.position, request.language)
