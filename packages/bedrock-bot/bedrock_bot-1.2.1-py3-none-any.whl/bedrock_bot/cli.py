import logging
import sys

import boto3
import click
from botocore.config import Config

from . import model_list
from .util import formatted_print

CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])
LOG_FORMATTER = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
log = None


def configure_logger(verbose):
    global log
    log_level = logging.ERROR
    if verbose:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)
    log = logging.getLogger()
    log.handlers[0].setFormatter(LOG_FORMATTER)
    log.info(f"Log level set to {logging.getLevelName(log_level)}")


def available_models():
    return [x.name for x in model_list]


def model_class_from_input(value):
    try:
        return [x for x in model_list if x.name.lower() == value.lower()][0]
    except IndexError:
        raise click.BadParameter(
            f"Invalid value: {value}. Allowed values are: {available_models}"
        )


def generate_boto_config(region):
    boto_config = Config()
    if region:
        boto_config = Config(region_name=region)
    elif boto3.setup_default_session() and not boto3.DEFAULT_SESSION.region_name:
        boto_config = Config(region_name="us-east-1")
    return boto_config


def get_user_input(instance, args):
    if instance.messages == [] and not sys.stdin.isatty():
        user_input = sys.stdin.read()
        print(f"> {user_input}")
    elif instance.messages == [] and args:
        user_input = " ".join(args)
        print(f"> {user_input}")
    elif not sys.stdin.isatty():
        print(
            "Note that you can only do one-shot requests when providing input via stdin"
        )
        exit()
    else:
        user_input = input("> ")

    return user_input


def handle_input_files(input_file) -> list:
    output = []
    if input_file:
        for file in input_file:
            output.append(file.read())
    return output


@click.command()
@click.argument("args", nargs=-1)
@click.option(
    "-r",
    "--region",
    help="The AWS region to use for requests. If no default region is specified, defaults to us-east-1",
)
@click.option("--raw-output", help="Don't interpret markdown in the AI response")
@click.option(
    "-m",
    "--model",
    type=click.Choice(available_models(), case_sensitive=False),
    default="Claude-3-Haiku",
    help="The model to use for requests",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable verbose logging messages",
)
@click.option(
    "-i",
    "--input-file",
    multiple=True,
    type=click.File(),
    help="Read in file(s) to be used in your queries",
)
def main(model, region, raw_output, args, verbose, input_file):
    configure_logger(verbose)

    model = model_class_from_input(model)
    boto_config = generate_boto_config(region)
    instance = model(boto_config=boto_config)

    print(
        f"Hello! I am an AI assistant powered by Amazon Bedrock and using the model {instance.name}. Enter 'quit' or"
        + " 'exit' at any time to exit. How may I help you today?"
    )
    print(
        "(You can clear existing context by starting a query with 'new>' or 'reset>')"
    )

    while True:
        print()
        user_input = get_user_input(instance, args)

        if not user_input:
            continue
        if user_input.lower() == "quit" or user_input.lower() == "exit":
            print("\nGoodbye!")
            sys.exit()
        if user_input.lower().startswith("new>") or user_input.lower().startswith(
            "reset>"
        ):
            print("\nResetting...")
            instance.reset()
            continue

        if not instance.messages:
            user_input += "\n"
            user_input += "\n".join(handle_input_files(input_file))

        response = instance.invoke(user_input)

        if raw_output:
            print(response)
        else:
            formatted_print(response)

        print()
