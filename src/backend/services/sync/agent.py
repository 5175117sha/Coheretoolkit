from backend.config.tools import ToolName
from backend.crud.agent import get_agent_by_id
from backend.crud.agent_tool_metadata import get_all_agent_tool_metadata_by_agent_id
from backend.database_models.database import db_sessionmaker
from backend.tools.google_drive import (
    handle_google_drive_activity_event,
    query_google_drive_activity,
)


# @app.task(time_limit=120)
def sync_agent(agent_id: str):
    agent_tool_metadata = []
    session = db_sessionmaker()
    agent = get_agent_by_id(session, agent_id)
    agent_tool_metadata = get_all_agent_tool_metadata_by_agent_id(session, agent_id)
    for metadata in agent_tool_metadata:
        match metadata.tool_name:
            case ToolName.Google_Drive:
                activities = query_google_drive_activity(
                    session=session, agent=agent, agent_artifacts=metadata.artifacts
                )
                for _artifact_id, activity in activities.items():
                    for activity_item in activity:
                        event_type = list(activity_item["primaryActionDetail"].keys())[0]
                        # NOTE: This is an unfortunate hack because the Google APi
                        # does not provide consistency over the request and response
                        # format of this action
                        if event_type == "permissionChange":
                            event_type = "permission_change"

                        handle_google_drive_activity_event(
                            event_type=event_type, activity=activity_item, agent_id=agent_id, user_id=agent.user_id
                        )
            case _:
                continue
