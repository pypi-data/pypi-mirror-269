from typing import Optional

from pydantic import BaseModel

from step_machine.types import HistoryBackend, StepMeta, ScriptType, StepExecutionOutput, StepStatus


class PgProgressBackendConfig(BaseModel):
    host: str = 'localhost'
    port: int = 5432
    username: str = 'postgres'
    password: str = 'password'
    db_name: str = 'uptd_history'


class PgHistoryBackend(HistoryBackend):
    def init_backend(self):
        pass

    def reset(self, project_name):
        pass

    def rename_project(self, project_name, new_project_name):
        pass

    def rename_step(self, project_name, step: StepMeta, new_step: StepMeta):
        pass

    def get_status(self, project_name, step: StepMeta) -> StepStatus:
        pass

    def set_status(self, project_name, step: StepMeta, status: StepStatus):
        pass

    def __init__(self, config: PgProgressBackendConfig):
        super().__init__()
        self.config = config
