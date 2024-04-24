from typing import TypedDict, List, Dict, Optional


class PropertySchema(TypedDict):
    bsonType: str
    description: Optional[str]  # Optional
    required: Optional[List[str]]  # Optional
    properties: Optional[Dict[str, 'PropertySchema']]  # Optional


class ModelSchema(TypedDict):
    bsonType: str
    title: Optional[str]  # Optional
    required: Optional[List[str]]  # Optional
    properties: Dict[str, PropertySchema | dict]  # Optional
