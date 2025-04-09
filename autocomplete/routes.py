from schemas import AutocompleteRequest
from fastapi import APIRouter

router = APIRouter(tags=["autocomplete"], prefix="/autocomplete")


@router.post("/")
async def autocomplete(request: AutocompleteRequest):
    return {"suggestions": "test"}
