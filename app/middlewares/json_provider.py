import json
from datetime import datetime
from typing import Any

from flask.json.provider import DefaultJSONProvider

from app.core.base_model import BaseModel
from app.utils.dttm_utils import DateUtils


class ComplexJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to handle complex types like datetime, custom objects,
    and nested structures (lists and dictionaries).
    """

    def default(self, obj: Any) -> Any:
        # print(f"{obj=}, {type(obj)=}")
        if isinstance(obj, BaseModel):
            return obj.to_dict()
        elif isinstance(obj, datetime):
            return DateUtils.serialize_to_iso(obj)
        elif hasattr(obj, '__dict__'):
            return {k: self.default(v) for k, v in vars(obj).items()}
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}
        return super().default(obj)


class AppJSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=ComplexJSONEncoder)
