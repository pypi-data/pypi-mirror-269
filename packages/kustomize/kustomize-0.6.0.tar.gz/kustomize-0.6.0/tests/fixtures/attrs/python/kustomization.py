from typing import List

from pydantic import BaseModel


class CommonLabels(BaseModel):
    app: str


class MyKustomization(BaseModel):
    commonLabels: CommonLabels
    resources: List[str]


kustomization = MyKustomization(
    commonLabels=CommonLabels(app='hello'),
    resources=[
        'deployment',
        'service',
        'configMap',
    ],
)
