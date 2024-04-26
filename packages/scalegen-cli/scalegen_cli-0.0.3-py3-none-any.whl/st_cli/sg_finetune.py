from typing import Optional
import click
from rich import box
from rich.console import Console
from rich.table import Table

from .client import send_request
from .utils import display_event_logs
from .stop import stop
from .view import view
from .launch import launch


def find_next_word_in_string(input_: str, target: str) -> Optional[str]:
    list_of_words = input_.split()
    try:
        next_word = list_of_words[list_of_words.index(target) + 1]
    except ValueError:
        next_word = None
    return next_word


@click.group(name="finetune")
def finetune():
    """
    ScaleGen commands for managing fine-tuning deployments
    """
    pass


finetune.add_command(stop, name="stop")
finetune.add_command(view, name="view")
finetune.add_command(launch, name="launch")


@finetune.command(name="create")
# ******************************* JOB ARGS *******************************
@click.option("-q", "--quiet", is_flag=True, help="Display status updates of workload")
@click.option(
    "--task",
    type=click.Choice(
        ["llm", "seq2seq", "text_classification", "token_classification"]
    ),
    required=False,
    default="llm",
)
@click.option("--job_name", type=click.STRING, required=False)
@click.option("--artifacts_storage", type=click.STRING, required=False)
@click.option("--allow_spot_instances", is_flag=True, required=False)
# ******************************* FINETUNE ARGS *******************************
@click.option("--model", required=True, type=click.STRING, help="Model to use")
@click.option(
    "--data_path",
    required=True,
    type=click.STRING,
    help="Data path to use. Can be a hugging face dataset or name of a virtual mount (filename is set with user_dataset)",
)
@click.option(
    "--user_dataset",
    required=False,
    type=click.STRING,
    help="Filename of a dataset on virtual mount to use",
)
@click.option(
    "--train_subset",
    required=False,
    type=click.STRING,
    help="Training data subset to use",
)
@click.option(
    "--text_column",
    required=False,
    type=click.STRING,
    default="text",
    help="Text column to use",
)
@click.option(
    "--lr", required=False, type=click.FLOAT, default=3e-5, help="Learning rate to use"
)
@click.option(
    "--epochs",
    required=False,
    type=click.INT,
    default=1,
    help="Number of training epochs to use",
)
@click.option(
    "--use_peft",
    required=False,
    type=click.Choice(["lora", "adalora", "ia3", "llama_adapter"]),
    help="PEFT method to use",
)
@click.option(
    "--wandb_key", required=False, type=click.STRING, help="Use experiment tracking"
)
@click.option(
    "--mixed_precision",
    required=False,
    type=click.Choice(["fp16", "bf16"], case_sensitive=True),
    help="Mixed precision type to use",
)
@click.option(
    "--quantization",
    required=False,
    type=click.Choice(["nf4", "fp4", "int8"], case_sensitive=True),
    help="Quantization type to use",
)
@click.option(
    "--disable_gradient_checkpointing",
    required=False,
    is_flag=True,
    help="Disable gradient checkpointing",
)
@click.option(
    "--use_flash_attention_2",
    required=False,
    is_flag=True,
    help="Use flash attention 2",
)
@click.option(
    "--lora_r", required=False, type=click.INT, default=16, help="Lora r to use"
)
@click.option(
    "--lora_alpha", required=False, type=click.INT, default=32, help="Lora alpha to use"
)
@click.option(
    "--lora_dropout",
    required=False,
    type=click.FLOAT,
    default=0.05,
    help="Lora dropout to use",
)
@click.option(
    "--gradient_accumulation_steps",
    required=False,
    type=click.INT,
    default=1,
    help="Gradient accumulation steps to use",
)
@click.option(
    "--batch_size",
    required=False,
    type=click.INT,
    default=2,
    help="Training batch size to use",
)
@click.option(
    "--block_size",
    required=False,
    type=click.STRING,
    default="-1",
    help="Block size to use",
)
@click.option(
    "--project_name",
    required=False,
    type=click.STRING,
    help="Project name in Hugging Face hub",
)
@click.option(
    "--model_max_length",
    required=False,
    type=click.INT,
    default=1024,
    help="Model max length to use",
)
@click.option(
    "--repo_id",
    required=False,
    type=click.STRING,
    help="Repo id for hugging face hub. Format is username/repo_name",
)
@click.option(
    "--hf_token", required=False, type=click.STRING, help="Hugging Face token to use"
)
@click.option(
    "--torch_dtype",
    required=False,
    type=click.Choice(["auto", "bfloat16", "float16", "float32"]),
    help="Load the model under specified dtype",
)
@click.option(
    "--username", required=False, type=click.STRING, help="Hugging Face username to use"
)
@click.option(
    "--push_to_hub",
    required=False,
    is_flag=True,
    help="Push to hub True/False. In case you want to push the trained model to Hugging Face hub",
)
# @click.option("--use_deepspeed", required=False, type=click.Choice(['stage_2', 'stage_3'], case_sensitive=True), help="DeepSpeed stage to use")
# @click.option("--prompt_text_column", required=False, type=click.STRING, default="prompt", help="Prompt text column to use")
# @click.option("--model_ref", required=False, type=click.STRING, help="Reference model to use for DPO when not using PEFT")
# @click.option("--warmup_ratio", required=False, type=click.FLOAT, default=0.1, help="Warmup proportion to use")
# @click.option("--optimizer", required=False, type=click.STRING, help="Optimizer to use")
# @click.option("--scheduler", required=False, type=click.STRING, default="linear", help="Scheduler to use")
# @click.option("--weight_decay", required=False, type=click.FLOAT, default=0.0, help="Weight decay to use")
# @click.option("--max_grad_norm", required=False, type=click.FLOAT, default=1.0, help="Max gradient norm to use")
# @click.option("--seed", required=False, type=click.INT, default=42, help="Seed to use")
# @click.option("--add_eos_token", required=False, is_flag=True, help="Add EOS token to use")
# @click.option("--logging_steps", required=False, type=click.INT, defaulf=-1, help="Logging steps to use")
# @click.option("--evaluation_strategy", required=False, type=click.STRING, defaulf="epoch", help="Evaluation strategy to use")
# @click.option("--save_total_limit", required=False, type=click.INT, defaulf=1, help="Save total limit to use")
# @click.option("--save_strategy", required=False, type=click.STRING, defaulf="epoch", help="Save strategy to use")
# @click.option("--auto_find_batch_size", required=False, is_flag=True, help="Auto find batch size True/False")
# @click.option("--push_to_hub", required=False, is_flag=True, help="Push to hub True/False. In case you want to push the trained model to huggingface hub")
# @click.option("--trainer", required=False, type=click.STRING, default="default", help="Trainer type to use")
# @click.option("--target_modules", required=False, type=click.STRING, default=None, help="Target modules to use")
# @click.option("--merge_adapter", required=False, is_flag=True, help="Use this flag to merge PEFT adapter with the model")
# @click.option("--beta", required=False, type=click.FLOAT, default=0.1, help="Beta for DPO trainer")
def create(**finetune_kwargs):
    """
    Function responsible for launching a scalegen finetune workload from the CLI
    """

    # Make request to P-API
    data = {
        "use_spot": finetune_kwargs["allow_spot_instances"],
        "wandb_key": finetune_kwargs["wandb_key"],
        "model": finetune_kwargs["model"],
        "data_path": finetune_kwargs["data_path"],
        "job_name": finetune_kwargs["job_name"],
        "user_dataset": finetune_kwargs["user_dataset"],
        "hf_token": finetune_kwargs["hf_token"],
        "artifacts_storage": finetune_kwargs["artifacts_storage"],
        "autotrain_params": {
            "use_peft": finetune_kwargs["use_peft"],
            "quantization": finetune_kwargs["quantization"],
            "mixed_precision": finetune_kwargs["mixed_precision"],
            "disable_gradient_checkpointing": finetune_kwargs[
                "disable_gradient_checkpointing"
            ],
            "gradient_accumulation_steps": finetune_kwargs[
                "gradient_accumulation_steps"
            ],
            "use_flash_attention_2": finetune_kwargs["use_flash_attention_2"],
            "lora_r": finetune_kwargs["lora_r"],
            "lora_alpha": finetune_kwargs["lora_alpha"],
            "lora_dropout": finetune_kwargs["lora_dropout"],
            "lr": finetune_kwargs["lr"],
            "batch_size": finetune_kwargs["batch_size"],
            "epochs": finetune_kwargs["epochs"],
            "train_subset": finetune_kwargs["train_subset"],
            "text_column": finetune_kwargs["text_column"],
        },
    }

    console = Console()
    with console.status("[bold green]Launching fine-tuning job...") as status:

        resp = send_request("POST", "/finetune/create", data=data)

    if resp.status_code != 500:
        resp_data = resp.json()
        if resp_data["warning"] is not None:
            warnings_ = resp_data["warning"].split("[\\r\\n]+")
            for w in warnings_:
                click.echo(click.style(f"Warning: {w}", fg="yellow"), nl=False)
        if resp_data["info"] is not None:
            info_ = resp_data["info"].split("[\\r\\n]+")
            for i in info_:
                click.echo(click.style(f"Info: {i}", fg="cyan"), nl=False)
    else:
        resp_data = resp.content.decode("utf-8")

    if resp.status_code == 200:
        job_id = resp_data["message"]["job_id"]
        click.echo(click.style(f"\nLaunched job - Id: {job_id}", fg="green"))
    elif resp.status_code == 400:
        click.echo(
            click.style(f"Bad request: {resp_data['message']}", fg="red"), err=True
        )
        return
    elif resp.status_code == 500:
        click.echo(
            click.style(
                f"\nSomething went wrong: {resp_data}. Please try launch job later",
                fg="red",
            ),
            err=True,
        )
        return
    else:
        click.echo(
            click.style(f"\nCouldn't create workload: {resp_data}", fg="red"), err=True
        )
        return

    if not finetune_kwargs["quiet"]:
        display_event_logs(job_id)


@finetune.command()
@click.option("-a", "--all", is_flag=True)
def list(all):
    """
    List all your finetune workloads
    """
    """
    - Status of the Workload
    - Status of the trials:
        - Trial Name
        - Trial latest metrics
        - Trial Status
    """
    console = Console()

    with console.status("[bold green]Fetching fine-tuning jobs...") as status:

        resp = send_request("GET", f"/job")

        if resp.status_code == 204:
            click.echo(click.style(f"\nNo finetune jobs found", fg="red"))
            return
        elif resp.status_code != 200:
            err = (
                resp.json() if resp.status_code != 500 else resp.content.decode("utf-8")
            )
            click.echo(
                click.style(f"\nCouldn't list the finetune jobs: {err}", fg="red")
            )
            return

        resp_data = resp.json()

        table = Table(
            show_header=True,
            header_style="bold #2070b2",
            title="[bold] Jobs",
            box=box.DOUBLE_EDGE,
        )

        for col in ["ID", "Name", "Model", "Data", "Status"]:
            table.add_column(col, justify="left")

        for job in resp_data:
            if all or (
                not all and (job["status"] == "RUNNING" or job["status"] == "QUEUED")
            ):
                model = find_next_word_in_string(
                    job["spec"]["config"]["entrypoint"], "--model"
                )
                data = find_next_word_in_string(
                    job["spec"]["config"]["entrypoint"], "--data_path"
                )
                table.add_row(job["id"], job["name"], model, data, job["status"])

    if table.row_count <= 15:
        console.print(table, justify="left")
    else:
        with console.pager():
            console.print(table, justify="left")
