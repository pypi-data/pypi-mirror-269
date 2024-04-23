import json
import os
import shutil

from pydantic import BaseModel
from step_machine.types import HistoryBackend, StepMeta, ScriptType, StepStatus


class FileProgressBackendConfig(BaseModel):
    history_folder: str


class FileHistoryBackend(HistoryBackend):
    def __init__(self, config: FileProgressBackendConfig):
        super().__init__()
        self.config = config

    def reset(self, project_name):
        hb = self._project_history_folder(project_name)
        shutil.rmtree(hb)

    def rename_project(self, project_name, new_project_name):
        s = self._project_folder(project_name)
        t = self._project_folder(new_project_name)
        shutil.move(s, t)

    def get_status(self, project_name, step: StepMeta) -> StepStatus:
        fp = self._project_step_status_file(project_name, step)
        if os.path.exists(fp):
            with open(fp) as file_content:
                return StepStatus(**json.load(file_content))
        return StepStatus.ready_to_run()

    def set_status(self, project_name, step: StepMeta, status: StepStatus):
        fp = self._project_step_status_file(project_name, step)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'w') as out:
            json.dump(
                status.model_dump(mode='json'),
                out
            )

    def rename_step(self, project_name, step: StepMeta, new_step: StepMeta):
        s = self._project_step_history_folder(project_name, step)
        t = self._project_step_history_folder(project_name, new_step)
        shutil.move(s, t)

    def delete_status(self, project_name, index: int):
        base = self._project_history_folder(project_name)
        for hist in os.listdir(base):
            parts = hist.split('_')[0]
            if parts >= 3 and int(parts) == index:
                shutil.rmtree(
                    os.path.join(base, hist)
                )
                return

    def init_backend(self):
        os.makedirs(self.config.history_folder, exist_ok=True)

    def _project_folder(self, project_name):
        return os.path.join(self.config.history_folder, f"{project_name}")

    def _project_history_folder(self, project_name):
        return os.path.join(
            self._project_folder(project_name),
            'run_history'
        )

    def _project_step_history_folder(self, project_name, step: StepMeta):
        return os.path.join(
            self._project_history_folder(project_name),
            f"{step.fullname()}"
        )

    def _project_step_status_file(self, project_name, step: StepMeta):
        return os.path.join(
            self._project_step_history_folder(project_name, step),
            f"status.json"
        )

    def _project_step_script_output(self, project_name, step: StepMeta, script_type: ScriptType):
        return os.path.join(
            self._project_step_history_folder(project_name, step),
            f'log-{script_type}.json'
        )
