from pydantic import BaseModel


class TaskDetailsSchema(BaseModel):
    name: str
    status: str


class ProjectCreateSchema(BaseModel):
    project_name: str
    location: str


class ProjectDetailsSchema(BaseModel):
    id: int
    project_name: str
    location: str
    status: str
    tasks: list[TaskDetailsSchema]
