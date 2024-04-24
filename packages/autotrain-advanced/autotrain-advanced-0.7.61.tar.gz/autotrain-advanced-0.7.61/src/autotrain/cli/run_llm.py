from argparse import ArgumentParser

from autotrain import logger
from autotrain.cli.utils import common_args, llm_munge_data
from autotrain.project import AutoTrainProject
from autotrain.trainers.clm.params import LLMTrainingParams

from . import BaseAutoTrainCommand


def run_llm_command_factory(args):
    return RunAutoTrainLLMCommand(args)


class RunAutoTrainLLMCommand(BaseAutoTrainCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        arg_list = [
            {
                "arg": "--text_column",
                "help": "Text column to use",
                "required": False,
                "type": str,
                "default": "text",
                "alias": ["--text-column"],
            },
            {
                "arg": "--rejected_text_column",
                "help": "Rejected text column to use",
                "required": False,
                "type": str,
                "default": "rejected",
                "alias": ["--rejected-text-column"],
            },
            {
                "arg": "--prompt-text-column",
                "help": "Prompt text column to use",
                "required": False,
                "type": str,
                "default": "prompt",
                "alias": ["--prompt-text-column"],
            },
            {
                "arg": "--model-ref",
                "help": "Reference model to use for DPO when not using PEFT",
                "required": False,
                "type": str,
            },
            {
                "arg": "--warmup_ratio",
                "help": "Warmup proportion to use",
                "required": False,
                "type": float,
                "default": 0.1,
                "alias": ["--warmup-ratio"],
            },
            {
                "arg": "--optimizer",
                "help": "Optimizer to use",
                "required": False,
                "type": str,
                "default": "adamw_torch",
            },
            {
                "arg": "--scheduler",
                "help": "Scheduler to use",
                "required": False,
                "type": str,
                "default": "linear",
            },
            {
                "arg": "--weight_decay",
                "help": "Weight decay to use",
                "required": False,
                "type": float,
                "default": 0.0,
                "alias": ["--weight-decay"],
            },
            {
                "arg": "--max_grad_norm",
                "help": "Max gradient norm to use",
                "required": False,
                "type": float,
                "default": 1.0,
                "alias": ["--max-grad-norm"],
            },
            {
                "arg": "--add_eos_token",
                "help": "Add EOS token to use",
                "required": False,
                "action": "store_true",
                "alias": ["--add-eos-token"],
            },
            {
                "arg": "--block_size",
                "help": "Block size to use",
                "required": False,
                "type": str,
                "default": "-1",
                "alias": ["--block-size"],
            },
            {
                "arg": "--peft",
                "help": "Use PEFT",
                "required": False,
                "action": "store_true",
                "alias": ["--use-peft"],
            },
            {
                "arg": "--lora_r",
                "help": "Lora r to use",
                "required": False,
                "type": int,
                "default": 16,
                "alias": ["--lora-r"],
            },
            {
                "arg": "--lora_alpha",
                "help": "Lora alpha to use",
                "required": False,
                "type": int,
                "default": 32,
                "alias": ["--lora-alpha"],
            },
            {
                "arg": "--lora_dropout",
                "help": "Lora dropout to use",
                "required": False,
                "type": float,
                "default": 0.05,
                "alias": ["--lora-dropout"],
            },
            {
                "arg": "--logging_steps",
                "help": "Logging steps to use",
                "required": False,
                "type": int,
                "default": -1,
                "alias": ["--logging-steps"],
            },
            {
                "arg": "--evaluation_strategy",
                "help": "Evaluation strategy to use",
                "required": False,
                "type": str,
                "default": "epoch",
                "alias": ["--evaluation-strategy"],
            },
            {
                "arg": "--save_total_limit",
                "help": "Save total limit to use",
                "required": False,
                "type": int,
                "default": 1,
                "alias": ["--save-total-limit"],
            },
            {
                "arg": "--save_strategy",
                "help": "Save strategy to use",
                "required": False,
                "type": str,
                "default": "epoch",
                "alias": ["--save-strategy"],
            },
            {
                "arg": "--auto_find_batch_size",
                "help": "Auto find batch size True/False",
                "required": False,
                "action": "store_true",
                "alias": ["--auto-find-batch-size"],
            },
            {
                "arg": "--mixed-precision",
                "help": "fp16, bf16, or None",
                "required": False,
                "type": str,
                "default": None,
                "alias": ["--mixed-precision", "--mp"],
            },
            {
                "arg": "--quantization",
                "help": "int4, int8, or None",
                "required": False,
                "type": str,
                "default": None,
                "alias": ["--quantization"],
            },
            {
                "arg": "--model_max_length",
                "help": "Model max length to use",
                "required": False,
                "type": int,
                "default": 1024,
                "alias": ["--model-max-length"],
            },
            {
                "arg": "--max_prompt_length",
                "help": "Prompt length to use, for orpo",
                "required": False,
                "type": int,
                "default": 128,
                "alias": ["--max-prompt-length"],
            },
            {
                "arg": "--max_completion_length",
                "help": "Completion length to use, for orpo: encoder-decoder models only",
                "required": False,
                "type": int,
                "default": None,
                "alias": ["--max-completion-length"],
            },
            {
                "arg": "--trainer",
                "help": "Trainer type to use",
                "required": False,
                "type": str,
                "default": "default",
            },
            {
                "arg": "--target_modules",
                "help": "Target modules to use",
                "required": False,
                "type": str,
                "default": None,
                "alias": ["--target-modules"],
            },
            {
                "arg": "--merge_adapter",
                "help": "Use this flag to merge PEFT adapter with the model",
                "required": False,
                "action": "store_true",
                "alias": ["--merge-adapter"],
            },
            {
                "arg": "--use_flash_attention_2",
                "help": "Use flash attention 2",
                "required": False,
                "action": "store_true",
                "alias": ["--use-flash-attention-2", "--use-fa2"],
            },
            {
                "arg": "--dpo-beta",
                "help": "Beta for DPO trainer",
                "required": False,
                "type": float,
                "default": 0.1,
                "alias": ["--dpo-beta"],
            },
            {
                "arg": "--chat_template",
                "help": "Apply chat template",
                "required": False,
                "default": None,
                "alias": ["--chat-template"],
                "choices": ["tokenizer", "chatml", "zephyr"],
            },
            {
                "arg": "--padding",
                "help": "Padding side",
                "required": False,
                "type": str,
                "default": None,
                "alias": ["--padding"],
            },
        ]
        arg_list.extend(common_args())
        run_llm_parser = parser.add_parser("llm", description="✨ Run AutoTrain LLM")
        for arg in arg_list:
            names = [arg["arg"]] + arg.get("alias", [])
            if "action" in arg:
                run_llm_parser.add_argument(
                    *names,
                    dest=arg["arg"].replace("--", "").replace("-", "_"),
                    help=arg["help"],
                    required=arg.get("required", False),
                    action=arg.get("action"),
                    default=arg.get("default"),
                )
            else:
                run_llm_parser.add_argument(
                    *names,
                    dest=arg["arg"].replace("--", "").replace("-", "_"),
                    help=arg["help"],
                    required=arg.get("required", False),
                    type=arg.get("type"),
                    default=arg.get("default"),
                )
        run_llm_parser.set_defaults(func=run_llm_command_factory)

    def __init__(self, args):
        self.args = args

        store_true_arg_names = [
            "train",
            "deploy",
            "inference",
            "add_eos_token",
            "peft",
            "auto_find_batch_size",
            "push_to_hub",
            "merge_adapter",
            "use_flash_attention_2",
            "disable_gradient_checkpointing",
        ]
        for arg_name in store_true_arg_names:
            if getattr(self.args, arg_name) is None:
                setattr(self.args, arg_name, False)

        block_size_split = self.args.block_size.strip().split(",")
        if len(block_size_split) == 1:
            self.args.block_size = int(block_size_split[0])
        elif len(block_size_split) > 1:
            self.args.block_size = [int(x.strip()) for x in block_size_split]
        else:
            raise ValueError("Invalid block size")

        if self.args.train:
            if self.args.project_name is None:
                raise ValueError("Project name must be specified")
            if self.args.data_path is None:
                raise ValueError("Data path must be specified")
            if self.args.model is None:
                raise ValueError("Model must be specified")
            if self.args.push_to_hub:
                # must have project_name, username and token OR project_name, repo_id, token
                if self.args.username is None and self.args.repo_id is None:
                    raise ValueError("Username or repo id must be specified for push to hub")
                if self.args.token is None:
                    raise ValueError("Token must be specified for push to hub")

            if self.args.backend.startswith("spaces") or self.args.backend.startswith("ep-"):
                if not self.args.push_to_hub:
                    raise ValueError("Push to hub must be specified for spaces backend")
                if self.args.username is None and self.args.repo_id is None:
                    raise ValueError("Repo id or username must be specified for spaces backend")
                if self.args.token is None:
                    raise ValueError("Token must be specified for spaces backend")

        if self.args.deploy:
            raise NotImplementedError("Deploy is not implemented yet")
        if self.args.inference:
            raise NotImplementedError("Inference is not implemented yet")

    def run(self):
        logger.info("Running LLM")
        if self.args.train:
            params = LLMTrainingParams(**vars(self.args))
            params = llm_munge_data(params, local=self.args.backend.startswith("local"))
            project = AutoTrainProject(params=params, backend=self.args.backend)
            _ = project.create()
