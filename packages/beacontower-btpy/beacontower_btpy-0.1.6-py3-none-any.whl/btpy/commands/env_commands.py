import asyncio

import typer
from colorama import Fore
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.spinner import Spinner
from rich.table import Table

from btpy.core.envs import env_desc_loader
from btpy.core.envs.env_client import EnvClient
from btpy.core.resource_clients.resource_client import ResourceStatus
from btpy.print_utility import print_status

app = typer.Typer()


@app.command("list")
def list_envs_cmd():
    asyncio.run(_list_envs())


async def _list_envs():
    env_list = await env_desc_loader.list_envs()

    for env in env_list:
        print(env)


@app.command("status")
def env_status_cmd(env_name: str):
    asyncio.run(_get_env_status(env_name))


async def _get_env_status(env_name: str):
    env_desc = await env_desc_loader.load_env_desc(env_name)

    if env_desc is None:
        print("Env not found")
        return

    env_client = EnvClient(env_desc)
    resource_clients = env_client.get_resource_clients()

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), TextColumn("{task.fields[result]}")) as table:
        loop = asyncio.get_event_loop()
        tasks = [(resource_client, loop.create_task(_get_formatted_status(resource_client.client)),
                  table.add_task(f"[blue]{resource_client.name}[/blue]", result="")) for resource_client in
                 resource_clients]

        while not table.finished:
            for (resource_client, task, table_task) in tasks:
                if task.done():
                    table.update(table_task, total=100, completed=100, result=task.result())

            await asyncio.sleep(0.1)

    [await resource_client.client.close() for resource_client in resource_clients]


async def _get_formatted_status(resource_client):
    status = await resource_client.status()
    return print_status(status)
