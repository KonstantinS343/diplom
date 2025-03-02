from schemas import AutocompleteRequest
from entrypoint import app

@app.post("/autocomplete/")
async def autocomplete(request: AutocompleteRequest):
    return {"suggestions": [f"{request.text}1", f"{request.text}2"]}