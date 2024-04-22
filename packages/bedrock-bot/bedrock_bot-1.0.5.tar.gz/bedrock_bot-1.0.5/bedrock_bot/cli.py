import sys

import click
from botocore.config import Config

from . import model_list
from .util import formatted_print


def available_models():
    return [x.name for x in model_list]


def model_class_from_input(value):
    try:
        return [x for x in model_list if x.name.lower() == value.lower()][0]
    except IndexError:
        raise click.BadParameter(
            f"Invalid value: {value}. Allowed values are: {available_models}"
        )


@click.command()
@click.argument("args", nargs=-1)
@click.option("-r", "--region", help="The AWS region to use for requests")
@click.option("--raw-output", help="Don't interpret markdown in the AI response")
@click.option(
    "-m",
    "--model",
    type=click.Choice(available_models(), case_sensitive=False),
    default="Claude-3-Haiku",
    help="The model to use for requests",
)
def main(model, region, raw_output, args):
    model = model_class_from_input(model)

    boto_config = Config()
    if region:
        boto_config = Config(region_name=region)

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

        response = instance.invoke(user_input)

        if raw_output:
            print(response)
        else:
            formatted_print(response)

        print()
