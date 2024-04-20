from os.path import join
import json
import click as ck
from daily_tasks.commands import utilities
from daily_tasks.commands.main_commands import add


@ck.command
@ck.option(
    '-p', '--export-path',
    type=ck.Path(exists=True, dir_okay=True, resolve_path=True),
    required=True
)
def export_tasks(export_path):
    """Export your tasks."""

    with open(utilities.TASKS_FILE_PATH, 'r', encoding='utf-8') as tasks_file:
        tasks = json.load(tasks_file)

    with open(join(export_path, utilities.EXPORTED_TASKS_FILE), 'w', encoding='utf-8') as exported_tasks_file:
        json.dump(tasks, exported_tasks_file, indent=2) 

@ck.command
@ck.option(
    '-a', '--add-tasks',
    is_flag=True,
    required=False,
    help="To add tasks from a json file."
)
@ck.option(
    '-f', '--file-name',
    required=False,
    help="Name of the json file where tasks you want add are."
)
@ck.option(
    '-d', '--description-key',
    required=False,
    help="Key that contains the descriptions for your tasks."
)
@ck.option(
    '-p', '--import-path',
    type=ck.Path(exists=True, dir_okay=True, resolve_path=True),
    required=True,
    help=f'Directory/Folder where your {utilities.EXPORTED_TASKS_FILE} is, \n Or where your json file with tasks that you want add is (to pass this json file use -a flag).'
)
@ck.pass_context
def import_tasks(ctx, import_path, file_name: str | None , description_key: str | None, add_tasks=False):
    """Import your tasks."""

    with open(utilities.TASKS_FILE_PATH, 'r', encoding='utf-8') as tasks_file:
        existing_tasks = json.load(tasks_file)

    if add_tasks is False:
        with open(join(import_path, utilities.EXPORTED_TASKS_FILE), 'r', encoding='utf-8') as imported_tasks_file:
            tasks = json.load(imported_tasks_file)

        for task in tasks:
            existing_tasks.append(task)

        with open(utilities.TASKS_FILE_PATH, 'w', encoding='utf-8') as tasks_file:
            json.dump(existing_tasks, tasks_file, indent=2)
    else:
        with open(join(import_path, f'{file_name}.json'), 'r', encoding='utf-8') as new_tasks_file:
            new_tasks = json.load(new_tasks_file)

        new_tasks_descriptions = []

        for new_task in new_tasks:
            new_tasks_descriptions.append(new_task[description_key])

        for new_task_description in new_tasks_descriptions:
            ctx.invoke(add, description=new_task_description)
            