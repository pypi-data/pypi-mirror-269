from decimal import Decimal
from typing import Union, Literal, List, Optional, Any, Set

from pydantic import Field, model_validator

from ..common import *


class ServicePlan(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    GROWTH = "GROWTH"


class Spec(BaseModel):
    config: ScaleTorchConfig
    type: JobType
    productType: Optional[ProductType] = ProductType.SCALETORCH

    class Config:
        use_enum_values = False


class Job(BaseModel):
    name: str
    spec: Spec
    id: str
    user_id: str
    status: JobStatus = JobStatus.QUEUED
    viz_page: str = ""
    stage: str = ""
    start_time: str
    end_time: str = ""
    cost: float = 0.0
    compute_used: dict = {}
    last_cost_updated_time: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        use_enum_values = False


class Workstation(BaseModel):
    id: str
    user_id: str
    config: WorkstationConfig
    stage: str = ""
    status: str
    prev_status: str = ""
    start_time: str = ""
    cost: float = 0.0
    viz_page: Optional[str] = None
    nodes: Optional[List[Node]] = []
    last_cost_updated_time: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        populate_by_name = True
        use_enum_values = False


class WorkstationAction(str, Enum):
    RESTART = "RESTART"
    STOP = "STOP"


class CommonOut(BaseModel):
    success: bool
    message: Optional[Any] = None


class CreateJobOut(CommonOut):
    warning: Optional[Any] = None
    info: Optional[Any] = None


class gDriveOut(BaseModel):
    success: bool
    refresh_token: Optional[Any] = None
    access_token: Optional[Any] = None
    error: Optional[Any] = None


class Trial(BaseModel):
    trial_id: str
    status: str
    user_id: Optional[str] = None
    job_id: str
    hyperparameters: dict
    host: Optional[str] = None
    is_dapp_trial: Optional[bool] = False
    gpu_indices: Optional[str] = None
    monitor_status: Optional[str] = None
    start_time: str = ""
    end_time: str = ""
    timestamp: Optional[str] = None


class JobOut(BaseModel):
    job_id: str


class UserMetadata(BaseModel):
    ns: str
    gt2: dict
    dev_user: bool = False
    is_admin: bool = False
    plan: Optional[ServicePlan] = ServicePlan.GROWTH
    admin_user_id: Optional[str] = None
    client_ids: Optional[List[str]] = None
    launch_jc: Optional[bool] = True
    member_users: List[str] = []  # List of emails
    created_from_backend: Optional[bool] = True
    st_slack_webhook_url: Optional[str] = None
    sg_slack_webhook_url: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class User(BaseModel):
    email: str
    user_id: str
    email_verified: bool
    user_metadata: UserMetadata

    class Config:
        arbitrary_types_allowed = True


class SecretOut(BaseModel):
    secret: dict
    success_status: bool


class SecretIn(BaseModel):
    secret_key: str
    secret_value: str
    typed: bool = False


class CloudDetails(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    cloud_provider: ProviderEnum
    bucket_name: Optional[str] = None
    primary: bool = False
    regions: List[str] = []

    class Config:
        use_enum_values = False


class CloudDetailsIn(CloudDetails):
    creds: dict

    class Config:
        use_enum_values = False


class UserRegisterIn(BaseModel):
    email: str
    productType: ProductType = ProductType.SCALETORCH


class Checkpoint(BaseModel):
    id: str
    job_id: str
    trial_id: str
    filename: str
    user_id: str
    metadata: dict
    timestamp: str
    copied_to_bucket: bool
    source: str
    timestamp: str

    class Config:
        populate_by_name = True


class Metrics(BaseModel):
    user_id: str
    job_id: str
    trial_id: str
    metrics: dict
    epoch: int
    timestamp: Optional[str] = None


class Telemetry(BaseModel):
    source: str
    # filename: str
    # filesize: int
    data: int
    timestamp: Optional[str] = None
    job_id: str
    trial_id: str


class Credentials(BaseModel):
    client_id: str
    client_secret: str


class ArtifactsStorageIn(BaseModel):
    name: str
    path: str
    credentials: dict = {}


class ArtifactsStorage(ArtifactsStorageIn):
    id: Optional[str] = None
    user_id: Optional[str] = None


class VirtualMountIn(BaseModel):
    name: str
    src: str
    dest: Optional[str] = None
    filter: Optional[str] = None
    prefetch: Optional[bool] = False
    unravelArchives: Optional[bool] = False
    credentials: dict = {}


class VirtualMountDB(VirtualMountIn):
    id: Optional[str] = None
    user_id: Optional[str] = None


class Entity(str, Enum):
    ARTIFACTS_STORAGE = "ARTIFACTS_STORAGE"
    SECRET = "SECRET"
    CLOUD_PROVIDER = "CLOUD_PROVIDER"
    VIRTUAL_MOUNT = "VIRTUAL_MOUNT"
    GT2 = "GT2"


class UserAssignRevokeIn(BaseModel):
    member_email: str
    entity_type: Entity
    entity_ids: List[str]


class UserPermissionsOut(BaseModel):
    ARTIFACTS_STORAGE: List[str]
    SECRET: List[str]
    CLOUD_PROVIDER: List[str]
    VIRTUAL_MOUNT: List[str] = []
    GT2: List[str]


class UserPermissionsIn(UserPermissionsOut):
    member_email: str


class VisualisationDetails(BaseModel):
    type: VisualisationType
    key: str


class TemplateType(str, Enum):
    EXPERIMENT = "EXPERIMENT"
    HPTOPT = "HPTOPT"
    WORKSTATION = "WORKSTATION"
    SIMPLE_JOB = "SIMPLE_JOB"


class Template(BaseModel):
    id: Optional[str] = None
    name: str
    config: Union[ScaleTorchConfig, WorkstationConfig]
    type: TemplateType
    user_id: Optional[str] = None

    class Config:
        use_enum_values = False


class EventDB(Event):
    pass


class NodeUsage(BaseModel):
    id: str
    entity_id: str
    gpu_type: Optional[GPUType] = None
    gpu_count: Optional[int] = 0
    hours: Decimal
    cost: Decimal

    class Config:
        arbitrary_types_allowed = True


class JobUsage(BaseModel):
    id: str
    job_id: str
    job_type: JobType
    user_id: str
    timestamp: str
    nodes: List[NodeUsage]
    platform_cost: float
    last_status: str


class Invoice(BaseModel):
    id: str
    timestamp: str
    amount: float
    payment_status: str
    user_id: str


# OAuth Models


class Token(BaseModel):
    access_token: str
    expires_in: int


class OAuth2In(BaseModel):
    client_id: str
    client_secret: str
    grant_type: str
    audience: str


class AccessKeyRecord(BaseModel):
    access_key_id: str
    access_key_secret_hashed: str
    user_id: str
    timestamp: str


# On-prem models


class OnPremNodeIn(BaseModel):
    ip: str
    username: str
    ssh_private_key: str
    port: int
    private_ip: Optional[str] = None
    cpu_only: bool


class OnPremNodeDB(OnPremNodeIn):
    id: str
    ssh_key_id: str
    role: Optional[VMRole] = None
    vcpus: int
    memory: int
    verified: bool
    verification_message: str
    gpu_type: GPUType
    gpu_count: int
    user_id: str


class OnPremNodeCandidate(OnPremNodeDB):
    available_resources: List[str]


class OnPremJournalStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class OnPremNodeJournal(BaseModel):
    id: str
    user_id: str
    timestamp: str
    status: OnPremJournalStatus
    role: VMRole
    on_prem_node_id: str
    job_id: str
    gpu_ids: Set[str]


class OnPremNodeEditIn(OnPremNodeIn):
    id: str


# Inference Models


class InferenceDeploymentInitialWorkersConfig(BaseModel):
    min_workers: int = 0
    initial_workers_gpu: Optional[GPUType] = None
    initial_workers_gpu_num: Optional[int] = None
    use_other_gpus: Optional[bool] = False
    instance_types: Optional[List[str]] = None
    use_on_prem: Optional[bool] = False
    use_cloudburst: Optional[bool] = False
    on_prem_node_ids: Optional[List[str]] = None


class InferenceDeploymentAutoscalingConfig(BaseModel):
    scale_up_time_window_sec: Optional[int] = 5 * 60
    scale_down_time_window_sec: Optional[int] = 5 * 60
    upper_allowed_latency_sec: Optional[float] = 1
    lower_allowed_latency_sec: Optional[float] = 0.2
    scaling_up_timeout_sec: Optional[int] = 20 * 60
    scaling_down_timeout_sec: Optional[int] = 20 * 60
    scale_to_zero_timeout_sec: Optional[int] = 30 * 60
    enable_speedup_shared: Optional[bool] = False
    scale_to_zero: Optional[bool] = False


class InferenceDeploymentGatewayCloudChoice(BaseModel):
    name: ProviderEnum
    region: str


class InferenceDeploymentIn(BaseModel):
    name: str
    model: str
    base_model: Optional[str] = None
    inf_type: InferenceDeploymentType = InferenceDeploymentType.llm
    hf_token: Optional[str] = None
    allow_spot_instances: bool = False
    logs_store: Optional[str] = None
    cloud_providers: Optional[List[CloudProviderChoice]] = []
    gateway_config: InferenceDeploymentGatewayCloudChoice
    initial_worker_config: Optional[InferenceDeploymentInitialWorkersConfig] = None
    autoscaling_config: Optional[InferenceDeploymentAutoscalingConfig] = (
        InferenceDeploymentAutoscalingConfig()
    )
    max_price_per_hour: Optional[float] = None
    min_throughput_rate: Optional[float] = None


class GpuTypeCount(BaseModel):
    type: GPUType
    count: int = Field(1, gt=0)


class InferenceDeploymentPriceEstimationIn(BaseModel):
    cloud: Optional[List[ProviderEnum]] = None
    gpu: Optional[List[GpuTypeCount]] = None
    region: Optional[List[str]] = None

    number_of_workers: int = Field(1, gt=0)

    @model_validator(mode="after")
    def check_fields(self):
        fields = ["cloud", "gpu", "region"]
        if all(not getattr(self, field) for field in fields):
            raise ValueError("At least one of the fields must be provided.")
        return self


class SpotDemandDB(BaseModel):
    on_demand: float
    spot: float


class MinMaxPrice(BaseModel):
    min: float
    max: float


class EstimatedPrice(BaseModel):
    on_demand_price: MinMaxPrice
    spot_price: MinMaxPrice


class InferenceDeploymentUpdateIn(BaseModel):
    # Initial worker params
    initial_worker_config: Optional[InferenceDeploymentInitialWorkersConfig] = None

    # Auto scaling parameters
    autoscaling_config: Optional[InferenceDeploymentAutoscalingConfig] = None
    imidiate_scale_down: Optional[bool] = False

    max_price_per_hour: Optional[float] = None
    min_throughput_rate: Optional[float] = None
    allow_spot_instances: Optional[bool] = None


class InferenceDeploymentGpuNodesIn(BaseModel):
    gpu_nodes_ids: List[str]


class InferenceDeploymentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PROVISIONING = "PROVISIONING"
    DELETED = "DELETED"
    FAILED = "FAILED"
    DELETING = "DELETING"
    SCALING = "SCALING"


class InferenceDeploymentAPIGatewayData(BaseModel):
    provider: ProviderEnum
    api_id: str
    hash_value: str
    endpoint: str
    region: str


class InferenceDeploymentDB(InferenceDeploymentIn):
    id: str
    user_id: str
    status: InferenceDeploymentStatus
    current_price_per_hour: float
    cost: Decimal = Decimal(0.00)
    last_cost_updated_time: Optional[str] = None
    timestamp: str
    link: Optional[str] = None
    metadata: Optional[dict] = {}
    api_gateway_data: Optional[InferenceDeploymentAPIGatewayData] = None


class InferenceSupportedModelOut(BaseModel):
    model: str
    type: InferenceDeploymentType


class NodeIP(BaseModel):
    ip: str
    id: str
    tailscale_ip: Optional[str] = None


# Finetuning


class AutotrainParams(BaseModel):
    use_peft: Optional[Literal["lora", "adalora", "ia3", "llama_adapter"]] = None
    quantization: Optional[Literal["fp4", "nf4", "int8"]] = None
    mixed_precision: Optional[Literal["fp16", "bf16"]] = None
    disable_gradient_checkpointing: Optional[bool] = None
    use_flash_attention_2: Optional[bool] = None
    lora_r: Optional[int] = None
    lora_alpha: Optional[int] = None
    lora_dropout: Optional[float] = None
    lr: float = Field(0.00003, title="Learning rate")
    batch_size: int = Field(1, title="Batch size for training")
    epochs: int = Field(1, title="Number of training epochs")
    train_subset: Optional[str] = None
    text_column: Optional[str] = None
    gradient_accumulation: Optional[int] = None
    max_model_length: Optional[int] = Field(
        2048, title="Model input max context length"
    )
    block_size: str = Field("-1", title="Block size")
    torch_dtype: Optional[Literal["auto", "bfloat16", "float16", "float32"]] = Field(
        None, title="Load the model under this dtype"
    )


class FinetuningIn(BaseModel):
    job_name: Optional[str] = None
    model: str

    data_path: str
    user_dataset: Optional[str] = None
    hf_token: Optional[str] = None
    project_name: Optional[str] = Field(None, title="Project name in HF hub")

    push_to_hub: Optional[bool] = False
    username: Optional[str] = None
    repo_id: Optional[str] = Field(None, title="Repo id")

    use_spot: bool = False
    cloud_providers: Optional[List[CloudProviderChoice]] = []

    wandb_key: Optional[str] = None
    artifacts_storage: Optional[str] = None

    autotrain_params: Optional[AutotrainParams] = None


class FinetuningRecipe(BaseModel):
    id: str
    model: str
    gpu_type: GPUType
    gpu_count: int
    autotrain_params: AutotrainParams


class CheckKeyIn(BaseModel):
    key_id: str
    key_secret: str


# Openai datamodels


class OpenaiFinetuningHyperparameters(BaseModel):
    batch_size: Optional[Union[str, int]] = "auto"
    learning_rate_multiplier: Optional[Union[str, float]] = "auto"
    n_epochs: Optional[Union[str, int]] = "auto"


class OpenaiFinetuningIn(BaseModel):
    model: str  # The name of the model to fine-tune
    training_file: str  # The ID of an uploaded file that contains training data.
    hyperparameters: Optional[OpenaiFinetuningHyperparameters] = (
        OpenaiFinetuningHyperparameters()
    )
    suffix: Optional[str] = (
        ""  # A string of up to 18 characters that will be added to your fine-tuned model name.
    )
    validation_file: Optional[Union[str, None]] = (
        None  # The ID of an uploaded file that contains validation data.
    )


class OpenaiFinetuningJobError(BaseModel):
    code: str  # A machine-readable error code.
    message: str  # A human-readable error message.
    param: Union[str, None] = (
        None  # The parameter that was invalid, usually training_file or validation_file. This
    )
    # field will be null if the failure was not parameter-specific.


class OpenaiFinetuningJobStatus(str, Enum):
    VALIDATING_FILES = "validating_files"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OpenaiFinetuningJob(BaseModel):
    id: str  # The object identifier, which can be referenced in the API endpoints.
    created_at: (
        int  # The Unix timestamp (in seconds) for when the fine-tuning job was created.
    )
    error: Optional[Union[OpenaiFinetuningJobError, None]] = (
        None  # For fine-tuning jobs that have failed, this will
    )
    # contain more information on the cause of the failure.

    fine_tuned_model: Optional[Union[str, None]] = (
        None  # The name of the fine-tuned model that is being created.
    )
    # The value will be null if the fine-tuning job is still running.
    finished_at: Optional[Union[int, None]] = (
        None  # The Unix timestamp (in seconds) for when the fine-tuning job
    )
    # was finished. The value will be null if the fine-tuning job is still running.

    hyperparameters: OpenaiFinetuningHyperparameters  # The hyperparameters used for the fine-tuning job.
    model: str  # The base model that is being fine-tuned.
    object: str = (
        "fine_tuning.job"  # The object type, which is always "fine_tuning.job".
    )
    organization_id: str = (
        "scaletorch"  # The organization that owns the fine-tuning job.
    )

    result_files: List[str] = (
        []
    )  # The compiled results file ID(s) for the fine-tuning job. You can retrieve the
    # results with the Files API.

    status: OpenaiFinetuningJobStatus  # The current
    # status of the fine-tuning job, which can be either validating_files, queued, running, succeeded, failed, or
    # cancelled.

    trained_tokens: Optional[Union[int, None]] = (
        None  # The total number of billable tokens processed by this
    )
    # fine-tuning job. The value will be null if the fine-tuning job is still running.
    training_file: str  # The file ID used for training. You can retrieve the training data with the Files API.
    validation_file: Optional[Union[str, None]] = (
        None  # The file ID used for validation. You can retrieve the
    )
    # validation results with the Files API.


class OpenaiFinetuningJobDB(OpenaiFinetuningJob):
    user_id: str


class OpenaiFinetuningJobEvent(BaseModel):
    id: str
    created_at: int
    level: str
    message: str
    object: str = "fine_tuning.job.event"


class OpenaiFile(BaseModel):
    id: str  # The file identifier, which can be referenced in the API endpoints.
    bytes: int  # The size of the file, in bytes.
    created_at: int  # The Unix timestamp (in seconds) for when the file was created.
    filename: str  # The name of the file.
    object: str = "file"  # The object type, which is always file.
    purpose: Literal[
        "fine-tune", "fine-tune-results", "assistants", "assistants_output"
    ]  # The intended purpose of
    # the file. Supported values are fine-tune, fine-tune-results, assistants, and assistants_output.


class OpenaiFileActualPath(BaseModel):
    filename: str
    storage_name: str


class OpenaiFileDB(OpenaiFile):
    actual_path: Optional[Union[None, OpenaiFileActualPath]] = None
    user_id: str


class OpenaiListFilesResponse(BaseModel):
    data: List[OpenaiFile]
    object: str = "list"


class OpenaiPaginatedResponse(BaseModel):
    object: str = "list"
    data: List[Union[OpenaiFinetuningJob, OpenaiFinetuningJobEvent]] = []
    has_more: bool = False


class OpenaiDeleteFileResponse(BaseModel):
    id: str
    object: str = "file"
    deleted: bool


class OpenaiFinishJobIn(BaseModel):
    result_model: Optional[Union[str, None]] = (
        None  # An openai file with resulting lora weights after finetuning
    )
    result_files: List[str] = []  # other resulting files, like logs
    trained_tokens: Optional[int] = 0  # Number of total consumed tokens (if possible)
