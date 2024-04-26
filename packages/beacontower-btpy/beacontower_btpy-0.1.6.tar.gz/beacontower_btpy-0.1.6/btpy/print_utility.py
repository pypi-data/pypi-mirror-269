from btpy.core.resource_clients.resource_client import ResourceStatus


def print_status(status: ResourceStatus):
    if status == ResourceStatus.Running:
        color = "[green]"
    elif status == ResourceStatus.Stopped:
        color = "[red]"
    elif status == ResourceStatus.Restarting or status == ResourceStatus.Unknown or status == ResourceStatus.Mixed:
        color = "[yellow]"
    else:
        raise ValueError(f"Unknown status: {status}")

    return f"{color}{status.name}"
