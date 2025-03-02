from pydantic import BaseModel


class AutocompleteRequest(BaseModel):
    text: str