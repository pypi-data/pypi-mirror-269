import transformers
from _typeshed import Incomplete
from tlc.client.helpers import active_run as active_run
from tlc.client.session import Session as Session
from tlc.core.builtins.types import MetricData as MetricData
from tlc.core.exceptions import TLCException as TLCException
from tlc.core.objects.table import Table as Table
from tlc.core.writers import MetricsTableWriter as MetricsTableWriter
from torch import Tensor, nn as nn
from torch.utils.data import Dataset as Dataset
from transformers.trainer_utils import EvalPrediction as EvalPrediction, IntervalStrategy as IntervalStrategy
from typing import Any, Callable

logger: Incomplete

class TLCTrainer(transformers.Trainer):
    '''A drop-in replacement for the 🤗 transformers Trainer.

    Adds per-sample metrics collection on both the train and eval datasets every time .evaluate() is called.

    To specify what metrics to collect, pass in a function to the compute_tlc_metrics argument that takes in a batch
    of data and returns a dictionary of per-sample metrics for the batch.

    :param compute_hf_metrics: The function that will be used to compute metrics at evaluation. Must take a
        [`EvalPrediction`] and return a dictionary string to metric values. Also called compute_metrics in HF Trainer.
    :param compute_tlc_metrics: A function that takes in a batch of data and returns a dictionary of metrics.
    :param compute_tlc_metrics_on_train_begin: Whether to collect metrics before training starts.
    :param compute_tlc_metrics_on_train_end: Whether to collect metrics after training ends.
    :param tlc_metrics_collection_start: The iteration or epoch to start collecting metrics on. Can be use with
        eval_strategy as "epochs" or "steps". If eval_strategy is "steps", tlc_metrics_collection_start needs
        to be a multiple of eval_steps.
    :param tlc_metrics_collection_epoch_frequency: The epoch frequency with which to collect metrics. Must be greater
        than 0 for metrics to be collected during training. Please use eval_steps for "steps" evaluation strategy.
    '''
    compute_tlc_metrics: Incomplete
    compute_tlc_metrics_on_train_begin: Incomplete
    compute_tlc_metrics_on_train_end: Incomplete
    tlc_metrics_collection_start: Incomplete
    tlc_metrics_collection_epoch_frequency: Incomplete
    def __init__(self, *args: Any, compute_hf_metrics: Callable[[EvalPrediction], dict] | None = None, compute_tlc_metrics: Callable[..., dict[str, MetricData]] | None = None, compute_tlc_metrics_on_train_begin: bool = False, compute_tlc_metrics_on_train_end: bool = False, tlc_metrics_collection_start: int = 0, tlc_metrics_collection_epoch_frequency: int = -1, **kwargs: Any) -> None: ...
    def get_current_epoch(self) -> int: ...
    def get_current_global_step(self) -> int: ...
    def train(self, *args: Any, **kwargs: Any) -> Any: ...
    def prediction_step(self, model: nn.Module, inputs: dict[str, Tensor | Any], prediction_loss_only: bool, ignore_keys: list[str] | None = None) -> tuple[Tensor | None, Tensor | None, Tensor | None]: ...
    def collect_metrics_with_tlc(self, ignore_keys: list[str] | None = None, metric_key_prefix: str = 'eval') -> dict[str, float]: ...
    def run_default_evaluate_based_on_evaluation_strategy(self, evaluation_strategy: IntervalStrategy | str) -> bool: ...
    def evaluate(self, eval_dataset: Dataset | None = None, ignore_keys: list[str] | None = None, metric_key_prefix: str = 'eval', on_train_begin: bool = False, on_train_end: bool = False) -> dict[str, float]: ...
