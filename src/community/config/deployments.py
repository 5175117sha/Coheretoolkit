from enum import StrEnum
from community.model_deployments.hugging_face import HuggingFaceDeployment
from backend.schemas.deployment import Deployment

class ModelDeploymentName(StrEnum):
    HuggingFace = "HuggingFace"


AVAILABLE_MODEL_DEPLOYMENTS = {
    ModelDeploymentName.HuggingFace: Deployment(
        name=ModelDeploymentName.HuggingFace,
        deployment_class=HuggingFaceDeployment,
        models=HuggingFaceDeployment.list_models(),
        is_available=HuggingFaceDeployment.is_available(),
        env_vars=[]
    ),
}