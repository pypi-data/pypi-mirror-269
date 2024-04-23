from dataclasses import dataclass

import click

from step_machine.core import StepMachineProject


@dataclass
class CliContext:
    project_base: str

    def get_project(self):
        return StepMachineProject(project_base=self.project_base)


@click.group()
@click.option('-t', '--target', default='./', help='Location of the step_machine project.')
@click.pass_context
def cli(ctx, target):
    ctx.obj = CliContext(
        project_base=target,
    )


@cli.command(name='init')
@click.option('-n', '--name', default=None, help='Project name for bookkeeping purposes.')
@click.option('-b', '--backend',
              default='file',
              type=click.Choice(['file']),
              help='Which history backend to use.')
@click.pass_context
def cmd_init(ctx, name, backend):
    """Initialize step_machine project."""
    StepMachineProject.create(ctx.obj.project_base, name, backend)


@cli.command(name='clone')
@click.argument('source')
@click.option('-t', '--target', default='./', help='Where to create the step_machine project.')
@click.option('-n', '--name', default='default', help='Project name.')
@click.option('-b', '--backend',
              default='file',
              type=click.Choice(['file', 'pg']),
              help='Type of history backend.')
def cmd_clone(source, target, name, backend):
    """Initialize step_machine project."""
    raise NotImplemented()
    # StepMachineProject.create(target, name, backend)
    # TODO: sync source.


# Step group


@cli.command(name='create')
@click.argument('step_name')
@click.pass_context
def cmd_step_create(ctx, step_name):
    """Create a new step."""
    click.echo("Creating a new step...")
    proj: StepMachineProject = ctx.obj.get_project()
    proj.create_new_step(step_name)


@cli.command(name='remove')
@click.argument('step_query')
@click.option('--force', is_flag=True, default=False, help='Force remove without confirmation')
@click.pass_context
def cmd_step_remove(ctx, step_query, force):
    """Remove a step."""
    click.echo(f"Removing step: {step_query}")
    proj: StepMachineProject = ctx.obj.get_project()
    found_step = proj.get_step(query=step_query)
    if found_step:
        resp = 'y'

        if not force:
            resp = input('Do you want to remove step script? (y/N) ').lower().strip()
            if resp == '':
                resp = 'n'

        if resp == 'y':
            proj.delete_step(found_step)
    else:
        raise ValueError(f'No step matching query: {step_query}.')


@cli.command(name='list')
@click.pass_context
def cmd_step_list(ctx):
    """Remove a step."""
    proj: StepMachineProject = ctx.obj.get_project()
    steps = proj.get_steps()
    if len(steps) > 0:
        print('Steps:')
        for s in steps:
            print(s.meta.fullname())
    else:
        print('Project is currently empty.')


@cli.command(name='status')
@click.pass_context
def cmd_status(ctx):
    """Check status of current project."""
    proj: StepMachineProject = ctx.obj.get_project()
    steps = proj.get_steps_with_status()
    header_line = 'Status'.rjust(18, ' ') + ' | ' + 'Step'.ljust(35, ' ')
    print('-----------------------------------------------------------')
    print(f"|  {header_line}  ")
    print('-----------------------------------------------------------')
    for step in steps:
        print(f"|  {step.to_line()}  ")
    print('-----------------------------------------------------------')


@cli.command(name='up')
@click.option('-t', '--to', default=None, help='Run all steps to this one (including this step).')
@click.option('--force', is_flag=True, default=False, help='Force re-run all steps (until failure.).')
@click.option('--pre/--no-pre', default=True, help='Run pre check script before executing first step.')
@click.option('--post/--no-post', default=True, help='Run post validation script after the last step.')
@click.pass_context
def cmd_up(ctx, to, force, pre, post):
    """Run all steps to latest or the given step (including this step)"""
    click.echo("")
    proj: StepMachineProject = ctx.obj.get_project()
    target = None
    if to:
        target = proj.get_step(query=to)
    proj.execute_all(
        target=target,
        force_run_all=force,
        run_pre_check=pre,
        run_post_validate=post,
    )


# Progress group
@cli.group()
def progress():
    """Commands related to progress tracking."""
    pass


@progress.command(name='print')
@click.argument('query')
@click.pass_context
def cmd_progress_print(ctx, query):
    """Print all recorded progresses."""
    proj: StepMachineProject = ctx.obj.get_project()
    step = proj.get_step(query)
    print(step.status.output)


@progress.command(name='remove')
@click.argument('index')
@click.pass_context
def cmd_progress_remove(ctx, index):
    """Remove progress of the given step."""
    click.echo(f"Removing progress step of index: {index}")
    proj: StepMachineProject = ctx.obj.get_project()
    proj.delete_step(index)
    proj.get_backend().delete_status(proj)


if __name__ == '__main__':
    cli(obj={})
