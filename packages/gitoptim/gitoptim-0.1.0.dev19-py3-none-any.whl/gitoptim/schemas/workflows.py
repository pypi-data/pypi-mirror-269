from pydantic import BaseModel


class AnalyseLogsSchema(BaseModel):
    logs: str
    pipeline_id: int
    job_id: int
    event_type: str = "gitlab-job-logs"
