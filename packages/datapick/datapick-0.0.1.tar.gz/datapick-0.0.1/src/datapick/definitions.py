from pydantic import BaseModel
from typing import List, Union, Optional

class Example(BaseModel):
    input: str
    output: str

class GetWorkflowResponse(BaseModel):
    name: str
    description: str
    examples: List[Example]

class RecordExampleResponse(BaseModel):
    success: bool
    message: Optional[str] = None

class CreateWorkflowResponse(BaseModel):
    success: bool
    message: Optional[str] = None