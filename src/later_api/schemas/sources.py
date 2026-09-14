from sqlmodel import SQLModel


class SourceRead(SQLModel):
    id: int
    name: str
