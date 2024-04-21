# Standard modules
import os
from typing import Any, Dict, List
from datetime import datetime

# Third-party modules
import click
from rich import box
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import yaml

# Product modules
from .client import get_garb, send_request
from .datamodels.datamodels.api import (
    InferenceDeploymentIn,
    InferenceDeploymentStatus,
    InferenceDeploymentAutoscalingConfig,
)
from .utils import CategorizedMutuallyExclusiveOption, PatchedCommand

DEFAULT_AUTOSCALING_CONFIG = InferenceDeploymentAutoscalingConfig()


def get_deployment(inf_id: str) -> Dict[str, Any]:
    console = Console()

    with console.status(
        f"[bold green]Getting deployment with inf_id {inf_id}..."
    ) as status:

        resp = send_request("GET", f"/sg_inf/{inf_id}")

    if resp.status_code == 204:
        click.echo(
            click.style(f"Deployment with inf_id {inf_id} not found", fg="red"),
            err=True,
        )
        exit()

    elif resp.status_code != 200:
        click.echo(click.style(f"Could not fetch deployment", fg="red"), err=True)
        exit()

    deployment = resp.json()
    return deployment


def get_deployments(should_exist: bool = True):
    console = Console()

    with console.status("[bold green]Getting existing deployments...") as status:

        resp = send_request("GET", "/sg_inf/list")

    if resp.status_code == 204:
        if should_exist:
            click.echo(
                click.style(
                    f"No deployments found. Create one with 'scalegen infer create'",
                    fg="blue",
                ),
                err=should_exist,
            )
        return []

    elif resp.status_code != 200:
        click.echo(click.style(f"Could not fetch deployments", fg="red"), err=True)
        exit()

    deployments = resp.json()
    deployments.sort(key=lambda dep: dep["name"])

    return deployments


def print_inference_deployments(
    deployments: List[Dict[str, Any]],
    table_title: str = "Inference Deployments",
    plain: bool = False,
):
    table = Table(
        show_header=True,
        # header_style='bold #2070b2',
        # title='[bold] Jobs',
        title=table_title,
        box=None if plain else box.DOUBLE_EDGE,
    )

    col_names = [
        "Inference ID",
        "Name",
        "Model",
        "Allow Spot Instances",
        "Current Price Per Hour",
        "Status",
        # "API Gateway",
    ]

    for col in col_names:
        table.add_column(col)

    provisioning = sorted(
        [
            d
            for d in deployments
            if d["status"] == InferenceDeploymentStatus.PROVISIONING
        ],
        key=lambda dep: datetime.strptime(dep["timestamp"], "%Y-%m-%d %H:%M:%S.%f"),
        reverse=True,
    )
    active = sorted(
        [d for d in deployments if d["status"] == InferenceDeploymentStatus.ACTIVE],
        key=lambda dep: datetime.strptime(dep["timestamp"], "%Y-%m-%d %H:%M:%S.%f"),
        reverse=True,
    )
    inactive = sorted(
        [d for d in deployments if d["status"] == InferenceDeploymentStatus.INACTIVE],
        key=lambda dep: datetime.strptime(dep["timestamp"], "%Y-%m-%d %H:%M:%S.%f"),
        reverse=True,
    )
    deleted = sorted(
        [
            d
            for d in deployments
            if d["status"]
            not in [
                InferenceDeploymentStatus.PROVISIONING,
                InferenceDeploymentStatus.ACTIVE,
                InferenceDeploymentStatus.INACTIVE,
            ]
        ],
        key=lambda dep: datetime.strptime(dep["timestamp"], "%Y-%m-%d %H:%M:%S.%f"),
        reverse=True,
    )

    deployments = provisioning + active + inactive + deleted

    for depl in deployments:
        row = [
            depl["id"],
            depl["name"],
            depl["model"],
            str(depl["allow_spot_instances"]),
            str(depl["current_price_per_hour"]),
            depl["status"],
            # depl["link"],
        ]
        # if row[-1] is None:
        #     row[-1] = "Unavailable"
        # else:
        #     row[-1] = print_to_string(
        #         f"[link={depl['link'] + '/inference'}]Inference link[/link]\n"
        #         f"[link={depl['link'] + '/metrics'}]Metrics link[/link]",
        #         end="",
        #     )

        table.add_row(*row)

    console = Console()

    if table.row_count <= 15 or plain:
        console.print(table, justify="left")
    else:
        with console.pager():
            console.print(table, justify="left")


@click.group(name="infer", chain=True)
def infer():
    """
    ScaleGen commands for managing inference deployments
    """
    pass


def create_inf_dep(
    inf_dep_req_data: InferenceDeploymentIn, quiet: bool = False, force: bool = False
):

    console = Console()

    with console.status("[bold green]Creating new deployment...") as status:
        resp = send_request(
            "POST", "/sg_inf/create", data=inf_dep_req_data.model_dump(mode="json")
        )
        inf_id = ""

    if resp.status_code == 200:
        resp_data = resp.json()
        inf_id = resp_data["message"]["inf_id"]  # P-API returns dict for CREATE request
        click.echo(click.style(f"Created deployment - Id: {inf_id}", fg="green"))

    elif resp.status_code == 500:
        resp_data = resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"Something went wrong: {resp_data}. Please try creating deployment later",
                fg="red",
            ),
            err=True,
        )
        exit()

    else:
        try:
            resp_data = resp.json()
            click.echo(
                click.style(f"Couldn't not create deployment: {resp_data}", fg="red"),
                err=True,
            )
        except Exception as e:
            click.echo(
                click.style(f"Couldn't not create deployment", fg="red"), err=True
            )
        exit()

    # Exit if quiet was passed
    if not quiet:
        print_inference_deployments(
            [get_deployment(inf_id)],
            table_title="New Deployment Added",
        )


@infer.command(
    "create",
    cls=PatchedCommand,
    context_settings=dict(max_content_width=150),
)
# ******************************* COMMON OPTIONS *******************************
@click.option(
    "--name", type=click.STRING, required=True, help="Deployment name to use."
)
@click.option("--model", type=click.STRING, required=True, help="Model to use.")
@click.option(
    "--base_model", type=click.STRING, required=False, help="Base model to use."
)
@click.option(
    "--inf_type",
    type=click.Choice(["embedding", "llm"]),
    required=True,
    help="Inference deployment type to use.",
)
@click.option(
    "--hf_token",
    type=click.STRING,
    required=False,
    help="Hugging Face token to use.",
)
@click.option(
    "--allow_spot_instances",
    is_flag=True,
    required=False,
    help="Use spot instances.",
)
@click.option(
    "--logs_store", type=click.STRING, required=False, help="Logs store to use."
)
@click.option(
    "--max_price_per_hour",
    type=click.INT,
    required=True,
    help="The maximum price you are willing to spend per hour.",
)
# ******************************* CLOUD PROVIDER OPTIONS *******************************
@click.option(
    "--cloud_providers",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    multiple=True,
    help="Specify cloud provider in upper case. "
    + click.style("Example: AWS.", italic=True),
    category="Cloud options",
)
@click.option(
    "--cloud_regions",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    multiple=True,
    help="Specify cloud region in following style <PROVIDER>:<region>. "
    + click.style("Example: AWS:us-east-1.", italic=True),
    category="Cloud options",
)
# ******************************* AUTO-SCALING OPTIONS *******************************
@click.option(
    "--enable_speedup_shared",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    required=False,
    help="Enable fast auto scaling using shared capacity.",
    category="Auto-scaling options",
)
@click.option(
    "--scale_to_zero",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    required=False,
    help="Enable scaling to zero.",
    category="Auto-scaling options",
)
@click.option(
    "--lower_allowed_latency_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.lower_allowed_latency_sec,
    help="Lower allowed latency in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--upper_allowed_latency_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.upper_allowed_latency_sec,
    help="Upper allowed latency in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scale_to_zero_timeout_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scale_to_zero_timeout_sec,
    help="Scaling down to zero timeout in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scaling_down_timeout_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scaling_down_timeout_sec,
    help="Scaling down timeout in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scaling_up_timeout_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scaling_up_timeout_sec,
    help="Scaling up timeout in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scale_down_time_window_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scale_down_time_window_sec,
    help="Scaling down time window in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
@click.option(
    "--scale_up_time_window_sec",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.FLOAT,
    required=False,
    default=DEFAULT_AUTOSCALING_CONFIG.scale_up_time_window_sec,
    help="Scaling up time window in seconds to use.",
    category="Auto-scaling options",
    show_default=True,
)
# ******************************* MIN THROUGHPUT CONFIGURATION OPTIONS *******************************
@click.option(
    "--min_throughput_rate",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    help="The minimum throughput rate you need to.",
    mutually_exclusive=[
        "min_workers",
        "use_same_gpus_when_scaling",
        "initial_workers_gpu_num",
        "initial_workers_gpu_type",
        "instance_types",
    ],
    category="Options responsible for minimum throughput configuration",
)
# ******************************* OPTIMAL WORKER CONFIGURATION OPTIONS *******************************
@click.option(
    "--min_workers",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    default=0,
    help="The minimum number of workers to scale down to.",
    category="Options responsible for optimal worker configuration",
    mutually_exclusive=["min_throughput_rate"],
    show_default=True,
)
@click.option(
    "--use_same_gpus_when_scaling",
    cls=CategorizedMutuallyExclusiveOption,
    is_flag=True,
    required=False,
    help="Enable to use same GPU type when scaling up.",
    category="Options responsible for optimal worker configuration",
    mutually_exclusive=["min_throughput_rate"],
)
@click.option(
    "--initial_workers_gpu_num",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    help="Initial number of GPUs per worker.",
    category="Options responsible for optimal worker configuration",
    mutually_exclusive=["min_throughput_rate"],
)
@click.option(
    "--initial_workers_gpu_type",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    help="Initial number of GPUs per worker.",
    category="Options responsible for optimal worker configuration",
    mutually_exclusive=["min_throughput_rate"],
)
@click.option(
    "--instance_types",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.INT,
    required=False,
    multiple=True,
    help="Provide space-separated list of instance types.",
    category="Options responsible for optimal worker configuration",
    mutually_exclusive=[
        "min_throughput_rate",
        "initial_workers_gpu_type",
        "initial_workers_gpu_num",
        "use_same_gpus_when_scaling",
    ],
)
# ******************************* API GATEWAY OPTIONS *******************************
@click.option(
    "--api_gateway_cloud",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    default="AWS",
    help="Specify API gateway cloud provider in upper case. "
    + click.style("Example: AWS.", italic=True),
    category="API gateway options",
    show_default=True,
)
@click.option(
    "--api_gateway_region",
    cls=CategorizedMutuallyExclusiveOption,
    type=click.STRING,
    required=False,
    default="us-east-1",
    help="Specify API gateway cloud provider region. "
    + click.style("Example: us-east-1.", italic=True),
    category="API gateway options",
    show_default=True,
)
@click.option("-f", "--force", is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
def create_impl(**inference_kwargs):
    """
    Create an inference deployment
    """

    # Get existing deployments
    deployments = get_deployments(should_exist=False)

    # Check if there is already a deployment with the same model
    similar_deployments = list(
        map(
            lambda x: x["id"],
            filter(lambda x: x["model"] == inference_kwargs["model"], deployments),
        )
    )
    if similar_deployments and not inference_kwargs["force"]:
        # If exists, Warn the user
        if not click.confirm(
            click.style(
                f"This model is already deployed with id(s): {similar_deployments}. Do you want to continue?",
                fg="yellow",
            )
        ):
            exit()

    # Make request to P-API
    if not inference_kwargs["inf_type"] in ["llm", "embedding"]:
        click.echo(
            click.style(
                f"\nType value must be one of [ llm , embedding ]",
                fg="red",
            ),
            err=True,
        )
        exit()

    if inference_kwargs["cloud_providers"]:
        cloud_providers_dict = dict.fromkeys(inference_kwargs["cloud_providers"], [])
        for region in inference_kwargs["cloud_regions"]:
            cloud, region = region.split(":")
            cloud_providers_dict[cloud].append(region)
        cloud_providers = [
            {"name": key, "regions": value}
            for key, value in cloud_providers_dict.items()
        ]
    else:
        cloud_providers = []

    data = {
        "name": inference_kwargs["name"],
        "model": inference_kwargs["model"],
        "inf_type": inference_kwargs["inf_type"],
        "hf_token": inference_kwargs["hf_token"],
        "allow_spot_instances": inference_kwargs["allow_spot_instances"],
        "logs_store": inference_kwargs["logs_store"],
        "cloud_providers": cloud_providers,
        "initial_worker_config": {
            "min_workers": inference_kwargs["min_workers"],
            "initial_workers_gpu": inference_kwargs["initial_workers_gpu_type"],
            "initial_workers_gpu_num": inference_kwargs["initial_workers_gpu_num"],
            "use_same_gpus_when_scaling": inference_kwargs[
                "use_same_gpus_when_scaling"
            ],
            "instance_types": inference_kwargs["instance_types"],
        },
        "autoscaling_config": {
            "enable_speedup_shared": inference_kwargs["enable_speedup_shared"],
            "scale_to_zero": inference_kwargs["scale_to_zero"],
            "scale_up_time_window_sec": inference_kwargs["scale_up_time_window_sec"],
            "scale_down_time_window_sec": inference_kwargs[
                "scale_down_time_window_sec"
            ],
            "upper_allowed_latency_sec": inference_kwargs["upper_allowed_latency_sec"],
            "lower_allowed_latency_sec": inference_kwargs["lower_allowed_latency_sec"],
            "scaling_up_timeout_sec": inference_kwargs["scaling_up_timeout_sec"],
            "scaling_down_timeout_sec": inference_kwargs["scaling_down_timeout_sec"],
            "scale_to_zero_timeout_sec": inference_kwargs["scale_to_zero_timeout_sec"],
        },
        "gateway_config": {
            "name": inference_kwargs["api_gateway_cloud"],
            "region": inference_kwargs["api_gateway_region"],
        },
        "max_price_per_hour": inference_kwargs["max_price_per_hour"],
        "min_throughput_rate": inference_kwargs["min_throughput_rate"],
    }

    inf_dep_req_data = InferenceDeploymentIn(**data)
    create_inf_dep(
        inf_dep_req_data,
        quiet=inference_kwargs["quiet"],
        force=inference_kwargs["force"],
    )


@infer.command("launch")
@click.argument("config_file", type=click.STRING, required=True)
@click.option("-f", "--force", is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
def launch_impl(config_file, force, quiet):
    """
    Launch an inference deployment using a config YAML file
    """
    # check if config_file is an absolute path
    if not os.path.isabs(config_file):
        config_path = os.path.join(os.getcwd(), config_file)

    if not os.path.exists(config_path):
        click.echo(
            click.style(
                f"{config_path} not found. Please specify a valid config file path",
                fg="red",
            ),
            err=True,
        )
        return

    with open(config_path, "r") as fp:
        config_yaml = fp.read()
        dict_from_yaml = yaml.safe_load(config_yaml)

    try:
        inf_dep_create_req = InferenceDeploymentIn(**dict_from_yaml)  # Valid config
    except Exception as e:
        click.echo(click.style(f"Validation Error: {e}", fg="red"), err=True)
        exit()

    create_inf_dep(inf_dep_create_req, quiet, force)


@infer.command("start")
@click.option("--inf_id", type=click.STRING, required=True)
@click.option("-f", "--force", is_flag=True)
@click.option("-q", "--quiet", is_flag=True)
def start_impl(inf_id, force, quiet):
    """
    Allows user to make the InferenceDeployment Active in case
    its been scaled to zero because of no-requests (status is INACTIVE)
    """

    def _check_if_deployment_already_started(inf_id: str):
        console = Console()

        with console.status(
            f"[bold green]Getting deployment with inf_id {inf_id}..."
        ) as status:

            resp = send_request("GET", f"/sg_inf/{inf_id}/gpu_nodes_ips")
            resp_json = ""

        if resp.status_code == 200:
            # Fetched GPU nodes successfully
            resp_data = resp.json()
            # return True
        elif resp.status_code == 500:
            resp_data = resp.content.decode("utf-8")
            click.echo(
                click.style(
                    f"\nSomething went wrong: {resp_data}. Please try fetching deployment GPU nodes later",
                    fg="red",
                ),
                err=True,
            )
            return False
        else:
            try:
                resp_data = resp.json()
                click.echo(
                    click.style(
                        f"\nCould not fetch deployment GPU nodes: {resp_data}", fg="red"
                    ),
                    err=True,
                )
            except Exception as e:
                click.echo(
                    click.style(f"\nCould not fetch deployment GPU nodes", fg="red"),
                    err=True,
                )
            return False

        if (len(resp_json) > 0) and not force:
            # If there are already existing GPU nodes, Warn the user
            if not click.confirm(
                click.style(
                    f"Deployment {inf_id} already running with {len(resp_json)} GPU nodes. Do you want to continue scaling up?",
                    fg="yellow",
                )
            ):
                exit()

    if not _check_if_deployment_already_started(inf_id):
        exit()

    console = Console()

    with console.status(
        f"[bold green]Scaling deployment with inf_id {inf_id}..."
    ) as status:

        resp = send_request("POST", f"/sg_inf/{inf_id}/scale/up")

    if resp.status_code == 200:
        resp_data = resp.json()
        click.echo(
            click.style(
                f"\nScaled deployment up with Id: {inf_id} successfully", fg="green"
            )
        )
    elif resp.status_code == 500:
        resp_data = resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"\nSomething went wrong: {resp_data}. Please try scaling deployment later",
                fg="red",
            ),
            err=True,
        )
        exit()
    else:
        try:
            resp_data = resp.json()
            click.echo(
                click.style(f"\nCould not scale up deployment: {resp_data}", fg="red"),
                err=True,
            )
        except Exception as e:
            click.echo(
                click.style(f"\nCould not scale up deployment", fg="red"), err=True
            )
        exit()

    # Exit if quiet was passed
    if not quiet:
        print_inference_deployments(
            [get_deployment(inf_id)],
            table_title="Deployment started!",
        )


@infer.command("delete")
@click.argument("inf_id", type=click.STRING, required=True)
@click.option("-q", "--quiet", is_flag=True)
def delete_impl(inf_id, quiet):
    """
    Delete an inference deployment
    """

    console = Console()

    with console.status(
        f"[bold green]Deleting deployment with inf_id {inf_id}..."
    ) as status:

        resp = send_request("DELETE", f"/sg_inf/{inf_id}")

    if resp.status_code == 200:
        resp_data = resp.json()
        click.echo(
            click.style(
                f"\nDelete request for deployment with id: {inf_id} is successful",
                fg="green",
            )
        )
    elif resp.status_code == 500:
        resp_data = resp.content.decode("utf-8")
        click.echo(
            click.style(
                f"\nSomething went wrong: {resp_data}. Please try deleting deployment later",
                fg="red",
            ),
            err=True,
        )
        exit()
    else:
        try:
            resp_data = resp.json()
            click.echo(
                click.style(f"\nCould not delete deployment: {resp_data}", fg="red"),
                err=True,
            )
        except Exception as e:
            click.echo(
                click.style(f"\nCould not delete deployment", fg="red"), err=True
            )
        exit()

    if not quiet:
        print_inference_deployments(
            [get_deployment(inf_id)],
            table_title="Deployment deleted!",
        )


@infer.command("list")
@click.option("-p", "--plain", is_flag=True)
def list_impl(plain):
    """
    Print the list of existing inference deployments
    """

    # Get existing deployments
    deployments = get_deployments(should_exist=True)

    print_inference_deployments(deployments, plain=plain)


@infer.command("view")
@click.argument("inf_id", type=click.STRING, required=True)
def view_impl(inf_id):
    """
    Print information about a single inference deployment
    """

    console = Console()
    inf_dep = get_deployment(inf_id)

    markdown_content = (
        f"[bold][orange_red1]ID[/orange_red1] : [cyan]{inf_dep['id']}[/cyan]\n"
    )
    markdown_content += (
        f"[orange_red1]Name[/orange_red1] : [yellow]{inf_dep['name']}[/yellow]\n"
    )
    markdown_content += (
        f"[orange_red1]Status[/orange_red1] : [yellow]{inf_dep['status']}[/yellow]\n"
    )
    markdown_content += f"[orange_red1]Cost[/orange_red1] : [yellow]$ {round(inf_dep['current_price_per_hour'], 3)}[/yellow]\n"
    markdown_content += (
        f"[orange_red1]Model[/orange_red1] : [yellow]{inf_dep['model']}[/yellow]\n"
    )

    url = inf_dep.get("link", "")
    if url:
        if inf_dep["inf_type"] == "llm":
            url += "/inference"
        else:
            url += "inference/embed"
    markdown_content += (
        f"[orange_red1]Endpoint[/orange_red1] : [yellow]{url}[/yellow]\n"
    )
    markdown_content += f"[orange_red1]APIKey[/orange_red1] : [yellow]{get_garb('AUTH_ENDPOINT_KEY_' + inf_id)}[/yellow]\n"

    console.print(Panel(markdown_content))
