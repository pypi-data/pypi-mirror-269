from pydantic import BaseModel


class Metadata(BaseModel):
    name: str


class ConfigMap(BaseModel):
    metadata: Metadata
    data: dict
    apiVersion: str = 'v1'
    kind: str = 'ConfigMap'


configMap = ConfigMap(
    metadata=Metadata(name='the-map'),
    data={'altGreeting': 'Good Morning!', 'enableRisky': 'false'},
)
