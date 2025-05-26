from pydantic import BaseModel



class FolderSchema(BaseModel):
    id: int
    name: str
    is_root: bool
