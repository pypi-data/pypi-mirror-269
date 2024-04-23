import json
import os
import shutil
import uuid
import warnings
from datetime import datetime

from typing import Optional

from step_machine.config import SMConfig
from step_machine.script import run_script
from step_machine.backend import get_backend, get_default_config
from step_machine.types import StepMeta, Step, StepStatus, StepStatusState, StepExecutionOutput, HistoryBackend
import pkgutil


def copy_to_target(package_data_path, target):
    if os.path.exists(target):
        raise ValueError(f'file {target} already exists.')
    data = pkgutil.get_data('step_machine.templates', package_data_path)
    with open(target, 'wb') as out:
        out.write(data)


def create_default_config(project_name, backend_type, target):
    if os.path.exists(target):
        warnings.warn(f'file already exists: {target}')
        return

    config = get_default_config(backend_type)

    ret = {
        'project_name': project_name,
        'history_backend': {
            'type': backend_type,
            'config': config,
        }
    }

    with open(target, 'w') as out:
        json.dump(ret, out, indent=4)


def get_current_time_str() -> int:
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y%m%d%H%M%S')
    return int(formatted_time)


class StepMachineProject:
    STEP_FOLDER_NAME = '_steps'
    STEP_CFG_FILE_NAME = 'step_machine_config.json'

    project_base: str
    config: SMConfig

    steps: list[Step]
    pre_check: str
    post_validate: str

    _loaded_backend: Optional[HistoryBackend]

    def __init__(self, project_base='./'):
        self.project_base = project_base

        self.steps_base = os.path.join(project_base, StepMachineProject.STEP_FOLDER_NAME)
        self.config_path = os.path.join(project_base, StepMachineProject.STEP_CFG_FILE_NAME)

        with open(self.config_path) as fd:
            cfg = json.load(fd)
            self.config = SMConfig(**cfg)

        self._loaded_backend = None

    @staticmethod
    def create(project_base, project_name=None, backend_type='file') -> 'StepMachineProject':
        steps_base = os.path.join(project_base, StepMachineProject.STEP_FOLDER_NAME)
        config_path = os.path.join(project_base, StepMachineProject.STEP_CFG_FILE_NAME)

        os.makedirs(steps_base, exist_ok=True)
        copy_to_target(f'pre_check.py', os.path.join(steps_base, 'pre_check.py'))
        copy_to_target(f'post_validate.py', os.path.join(steps_base, 'post_validate.py'))

        if project_name is None:
            project_name = str(uuid.uuid4())
        create_default_config(project_name, backend_type, config_path)
        return StepMachineProject(project_base=project_base)

    def get_backend(self):
        if self._loaded_backend is None:
            self._loaded_backend = get_backend(
                self.config.history_backend.type,
                self.config.history_backend.config,
            )
        return self._loaded_backend

    def get_steps_with_status(self) -> list[Step]:
        steps = self.get_steps()
        for step in steps:
            step.load_progress(self.get_backend(), self.config.project_name)
        return steps

    def _get_steps(self) -> list[Step]:
        """
        Return a list of migration files by returning all .sh or .py files directly under base_folder.

        :return: A list of strings, where each string is the path to a migration file.
        """
        steps = []

        # Iterate over each item in the base folder
        for full_step_name in os.listdir(self.steps_base):
            step_script = os.path.join(self.steps_base, full_step_name)
            rs = Step.load_from_file_or_none(step_script)
            if rs:
                steps.append(rs)
        steps = sorted(steps, key=lambda x: x.meta.index)
        return steps

    def get_steps(self, ensure_order=True):
        steps = self._get_steps()
        if not ensure_order:
            return steps

        total_steps = len(steps)

        for i in range(1, total_steps + 1):
            step = steps[i - 1]
            if step.meta.index != i:
                raise ValueError(f'Step out of order: {step.meta.fullname()}')

        return steps

    def delete_step(self, step: Step):
        step_base = os.path.join(self.steps_base, step.meta.filename())
        os.remove(step_base)

    def search_steps(self, query: str):
        steps = self.get_steps(ensure_order=False)
        ret = []
        for step in steps:
            if query.isnumeric() and int(query) == step.meta.index:
                ret.append(step)
            if query == step.meta.name:
                ret.append(step)
            if query == step.meta.short_name():
                ret.append(step)
            if query == step.meta.fullname():
                ret.append(step)
            if query == step.meta.filename():
                ret.append(step)
        return ret

    def get_step(self, query) -> Optional[Step]:
        results = self.search_steps(query)
        if len(results) == 0:
            return None
        if len(results) > 1:
            fullnames = '\n'.join(
                [r.meta.fullname() for r in results]
            )
            raise ValueError(
                f'Found more than one steps match query. Use full step name to select one from: \n{fullnames}')
        return results[0]

    def rename_step(self, step: Step, new_name: str):
        step_base = os.path.join(self.steps_base, step.meta.filename())
        new_meta = step.meta.rename(new_name)
        dest = os.path.join(self.steps_base, new_meta.filename())
        shutil.move(step_base, dest)

    def reorder_step(self, step: Step, new_index: int):
        step_base = os.path.join(self.steps_base, step.meta.filename())

        new_meta = step.meta.rename(step.meta.name, new_index=new_index)
        dest = os.path.join(self.steps_base, new_meta.filename())

        shutil.move(step_base, dest)

    def reorder_all_steps(self):
        steps = self.get_steps(ensure_order=False)
        sorted_steps = sorted(steps, key=lambda x: x.meta.timestr)
        for idx, step in enumerate(sorted_steps):
            if idx + 1 != step.meta.index:
                self.reorder_step(step, idx + 1)

    def create_new_step(
            self,
            step_name,
    ):
        step = StepMeta(
            name=step_name,
            index=len(self.get_steps()) + 1,
            time_str=get_current_time_str()
        )

        out_file_base = os.path.join(self.steps_base, step.filename())
        os.makedirs(os.path.dirname(out_file_base), exist_ok=True)
        copy_to_target(f'up.py', out_file_base)
        return Step.load_from_file_or_none(out_file_base)

    def execute_single_step(
            self,
            step: Step,
            record_output=True
    ) -> StepStatus:
        output = run_script('python', step.location)
        if output.exit_code == 0:
            status_state = StepStatusState.FINISHED
        else:
            status_state = StepStatusState.FAILED
        new_status = StepStatus(state=status_state, timestamp=output.timestamp, output=output)

        if record_output:
            self.get_backend().set_status(self.config.project_name, step.meta, new_status)
        return new_status

    def execute_pre_check(self) -> StepStatus:
        p = os.path.join(self.steps_base, 'pre_check.py')
        if os.path.exists(p):
            output = run_script('python', p)
            if output.exit_code == 0:
                status_state = StepStatusState.FINISHED
            else:
                status_state = StepStatusState.FAILED
            new_status = StepStatus(state=status_state, timestamp=output.timestamp, output=output)
            return new_status

    def execute_post_validate(self) -> StepStatus:
        p = os.path.join(self.steps_base, 'post_validate.py')
        if os.path.exists(p):
            output = run_script('python', p)
            if output.exit_code == 0:
                status_state = StepStatusState.FINISHED
            else:
                status_state = StepStatusState.FAILED
            new_status = StepStatus(state=status_state, timestamp=output.timestamp, output=output)
            return new_status

    def execute_all(
            self,
            target=None,
            force_run_all=False,
            run_pre_check=True,
            run_post_validate=True,
            ignore_first_error=True
    ):
        if run_pre_check:
            new_status = self.execute_pre_check()
            if not new_status.state.is_ok():
                raise ValueError('Pre-check failed.')
            else:
                print('--\n[OK] Pre Check: Success')
        else:
            print(' -- Skipping pre check')

        print('---- ' * 12)

        err_count = 0
        steps = self.get_steps_with_status()

        print(f' -- Checking {len(steps)} steps before execution.')

        for step in steps:

            ok_to_run = False
            already_finished = False
            if force_run_all:
                ok_to_run = True
            else:
                if step.status.state == StepStatusState.FINISHED:
                    already_finished = True
                else:
                    if step.status.state == StepStatusState.READY_TO_RUN:
                        ok_to_run = True
                    else:
                        if ignore_first_error and err_count == 0:
                            ok_to_run = True
                            err_count += 1
            if ok_to_run:
                print(f' -- Executing step: {step.meta.fullname()}.')
                new_status = self.execute_single_step(step)
                if not new_status.state.is_ok():
                    raise ValueError(f' -- Step {step.meta.fullname()} failed.')
            else:
                if not already_finished:
                    raise ValueError(f'Cannot run step {step.meta.fullname()}.')
                else:
                    print(f' -- Step is already finished: {step.meta.fullname()}.')
            if target == step:
                break

        print('---- ' * 12)

        if run_post_validate:
            new_status = self.execute_post_validate()
            if not new_status.state.is_ok():
                raise ValueError('Post validation failed.')
            else:
                print('--\n[OK] Post Validation: Success')
        else:
            print(' -- Skipping post validation')

    def delete_all_progress(self):
        self.get_backend().reset(self.config.project_name)

    def delete_progress(self, index: int):
        self.get_backend().delete_status(self.config.project_name, index)
