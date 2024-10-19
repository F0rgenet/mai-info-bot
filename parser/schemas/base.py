from pydantic import BaseModel


class NamedEntityBase(BaseModel):
    name: str


class NamedEntityCreate(NamedEntityBase):
    pass


class NamedEntityUpdate(BaseModel):
    name: str | None = None


class NamedEntity(NamedEntityBase):
    id: int

    class Config:
        from_attributes = True
