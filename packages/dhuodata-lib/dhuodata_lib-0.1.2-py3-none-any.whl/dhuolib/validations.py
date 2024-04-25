from pydantic import BaseModel, Field


class FileBody(BaseModel):
    bucket: str = Field(..., description="Bucket")
    namespace: str = Field(..., description="Namespace")
    filepath: str = Field(..., description="Filepath")


class RunExperimentBody(BaseModel):
    modelname: str = Field(..., description="DEPENDENCY|PREDICT")
    modeltag: str = Field(..., description="Tag")
    experiment_id: str = Field(..., description="Id")
    stage: str = Field(..., description="STAGING|PRODUCTION")
    file: FileBody = Field(None, description="FAIL/SUCESS")


class ExperimentBody(BaseModel):
    experiment_name: str = Field(..., description="Id")
    experiment_tags: dict = Field(None, description="Tags")
