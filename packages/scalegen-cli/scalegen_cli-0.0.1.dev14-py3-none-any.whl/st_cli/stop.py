import click
from rich.console import Console

from .client import send_request


@click.command()
@click.argument("job_id", type=click.STRING, required=True)
# @click.argument("trial_id", type=click.STRING, required=False)
def stop(job_id):
    """
    Stop a job
    """
    console = Console()
    # if not trial_id:
    with console.status("[bold green]Stopping job...") as status:
        resp = send_request("DELETE", f"/job/{job_id}")

    if resp.status_code == 201:
        click.echo(click.style(f"{resp.json()['message']}", fg="green"))
        return

    if resp.status_code != 202:
        click.echo(click.style("\nCouldn't find the requested job", fg="red"))
        return

    click.echo(
        click.style(f"\nSuccessfully requested to stop job: {job_id}", fg="green")
    )

    # else:
    #     resp = send_request('DELETE', f'/job/{job_id}/trial/{trial_id}')

    #     if resp.status_code != 202:
    #         click.echo(click.style("Couldn't find the requested trial", fg='red'))
    #         return

    #     click.echo(click.style(f"Stopping trial: {trial_id}", fg='blue'))
