import abc
import enum
import os.path
from typing import Optional

from pydantic import BaseModel


class StatusCode:
    NA = 5
    OK = 0


class StepStatusState(str, enum.Enum):
    READY_TO_RUN = 'READY_TO_RUN'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'

    def is_ok(self):
        return self in [StepStatusState.READY_TO_RUN, StepStatusState.FINISHED]


class ScriptType(str, enum.Enum):
    UP = 'UP'
    PRE = 'PRE'
    POST = 'POST'


class StepMeta(BaseModel):
    name: str
    index: int
    time_str: int

    def filename(self):
        index_str = str(self.index).zfill(5)
        return f"{index_str}_{self.name}_{self.time_str}.py"

    def fullname(self):
        index_str = str(self.index).zfill(5)
        return f"{index_str}_{self.name}_{self.time_str}"

    def short_name(self):
        index_str = str(self.index).zfill(5)
        return f"{index_str}_{self.name}"

    @staticmethod
    def match_name_format(fullname: str):
        fullname = os.path.basename(fullname)

        if '.' not in fullname:
            return False

        name, extension = os.path.basename(fullname).split('.', 1)

        if extension.lower() != 'py':
            return False

        parts = name.split('_')
        if len(parts) < 3:
            return False

        if not parts[0].isnumeric():
            return False

        if not parts[-1].isnumeric():
            return False

        return (
            int(parts[0]),
            "_".join(parts[1: -1]),
            int(parts[-1])
        )

    @staticmethod
    def parse_from_name(fullname: str) -> Optional['StepMeta']:
        parsed_ = StepMeta.match_name_format(fullname)

        if parsed_ is None or parsed_ is False:
            return None

        index, name, timestamp = parsed_
        return StepMeta(name=name, index=index, time_str=timestamp)

    def rename(self, new_name, new_index=None) -> 'StepMeta':
        if new_index is None:
            new_index = self.index
        return StepMeta(name=new_name, index=new_index, time_str=self.time_str)


class StepExecutionOutput(BaseModel):
    signature: str
    timestamp: int
    exit_code: int
    stdout: str
    stderr: str

    def is_ok(self):
        return self.exit_code == 0


class RuntimeScriptInfo(BaseModel):
    script_path: str
    entry_point: str


class StepStatus(BaseModel):
    state: StepStatusState = StepStatusState.READY_TO_RUN
    timestamp: Optional[int] = None
    output: Optional[StepExecutionOutput] = None

    @staticmethod
    def ready_to_run():
        return StepStatus(status=StepStatusState.READY_TO_RUN, timestamp=None)


class Step(BaseModel):
    meta: StepMeta
    location: str
    status: Optional[StepStatus] = None

    def to_line(self):
        status = '---'
        if self.status is not None:
            status = self.status.state
        return status.rjust(18, ' ') + ' | ' + self.meta.fullname()

    @staticmethod
    def load_from_file_or_none(location):
        meta = StepMeta.parse_from_name(os.path.basename(location))
        if meta:
            return Step(
                meta=meta,
                location=location,
            )
        return None

    def load_progress(
            self,
            backend: 'HistoryBackend',
            project_name
    ):
        self.status = backend.get_status(project_name, self.meta)


class HistoryBackend:

    @abc.abstractmethod
    def init_backend(self):
        raise NotImplemented()

    @abc.abstractmethod
    def reset(self, project_name):
        raise NotImplemented()

    @abc.abstractmethod
    def rename_project(self, project_name, new_project_name):
        raise NotImplemented()

    @abc.abstractmethod
    def rename_step(self, project_name, step: StepMeta, new_step: StepMeta):
        raise NotImplemented()

    @abc.abstractmethod
    def get_status(self, project_name, step: StepMeta) -> StepStatus:
        raise NotImplemented()

    @abc.abstractmethod
    def set_status(self, project_name, step: StepMeta, status: StepStatus):
        raise NotImplemented()

    @abc.abstractmethod
    def delete_status(self, project_name, index: int):
        raise NotImplemented()
