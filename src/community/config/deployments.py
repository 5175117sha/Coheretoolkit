from enum import StrEnum

from backend.schemas.deployment import Deployment
from community.model_deployments.hugging_face import HuggingFaceDeployment
from community.model_deployments.local_model import LocalModelDeployment


class ModelDeploymentName(StrEnum):
    HuggingFace = "HuggingFace"
    LocalModel = "LocalModel"


AVAILABLE_MODEL_DEPLOYMENTS = {
    ModelDeploymentName.HuggingFace: Deployment(
        name=ModelDeploymentName.HuggingFace,
        deployment_class=HuggingFaceDeployment,
        models=HuggingFaceDeployment.list_models(),
        is_available=HuggingFaceDeployment.is_available(),
        env_vars=[],
    ),
    ModelDeploymentName.LocalModel: Deployment(
        name=ModelDeploymentName.LocalModel,
        deployment_class=LocalModelDeployment,
        models=LocalModelDeployment.list_models(),
        is_available=LocalModelDeployment.is_available(),
        env_vars=[],
        kwargs={
            "model_path": "path/to/model",  # Note that the model needs to be in the src directory
        },
    ),
}
