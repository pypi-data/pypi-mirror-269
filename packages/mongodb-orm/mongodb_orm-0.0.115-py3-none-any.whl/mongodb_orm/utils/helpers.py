from uuid import UUID
from bson import ObjectId
from django.db.models import Model
from datetime import datetime, date


class Helper:
    @classmethod
    def standardize_dict(cls, dct: dict, underscore=False) -> dict:
        standard_dct = {}
        for key, value in dct.items():
            if key == '_id':
                standard_dct['id'] = str(value)
            if key.startswith('_') and not underscore:
                continue
            if isinstance(value, dict):
                standard_dct[key] = cls.standardize_dict(value)
                continue
            if isinstance(value, UUID):
                standard_dct[key] = value.hex
                continue
            if isinstance(value, ObjectId):
                standard_dct[key] = str(value)
                continue
            if isinstance(value, (datetime, date)):
                standard_dct[key] = value.isoformat()
                continue
            if isinstance(value, Model):
                standard_dct[key] = value.pk if not isinstance(value.pk, UUID) else value.pk.hex
                continue
            standard_dct[key] = value

        return standard_dct
