from .base import CRUDBase
from backend.database.models import Entry, Subject, Type


class CRUDEntry(CRUDBase):
    pass


class CRUDSubject(CRUDBase):
    pass


class CRUDType(CRUDBase):
    pass


crud_entry = CRUDEntry(Entry)
crud_subject = CRUDSubject(Subject)
crud_type = CRUDType(Type)
