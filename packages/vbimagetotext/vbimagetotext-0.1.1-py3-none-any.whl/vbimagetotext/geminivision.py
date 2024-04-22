import PIL.Image
import os
import google.generativeai as genai
import click
import sys
from rich.console import Console
from .prompts import switch_prompt
from .choice_option import ChoiceOption
import pyperclip


@click.command(
    help="Process images using Google's Gemini Vision model and extract the response."
)
@click.option(
    "-i",
    "--image",
    type=click.Path(exists=True),
    required=True,
    multiple=True,
    help="Path to the image file",
)
@click.option(
    "-p",
    "--prompt",
    cls=ChoiceOption,
    type=click.Choice(
        [
            "assertion_reason",
            "mcq",
            "mcq_solution",
            "subjective",
            "match",
            "comprehension",
            "answer",
            "prompt",
        ],
        case_sensitive=False),
    prompt=True,
    default=2,
    show_default=True,
    help="Prompt to use for the completion",
)
def geminivision(image, prompt):
    """
    Generates text content based on an image and a prompt using the Gemini Pro Vision model.

    Args:
        image (list): A list of image file paths.
        prompt (str): The prompt to be used for generating the text content.

    Returns:
        None

    Raises:
        SystemExit: If the GOOGLE_API_KEY environment variable is not set.

    """
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    if GOOGLE_API_KEY is None:
        console = Console()
        console.print(
            "Google_api_key error.", style="bold red")
        sys.exit(1)

    if prompt == "prompt":
        prompt = click.prompt("Please enter your custom prompt", type=str)

    prompt = switch_prompt(prompt)

    model = genai.GenerativeModel('gemini-pro-vision')

    images = [PIL.Image.open(image_name) for image_name in image]
    response = model.generate_content(
        [prompt, *images], stream=True, max_tokens=1000)
    response.resolve()

    try:
        pyperclip.copy(response.text)
    except Exception as e:
        print(
            f"An error occurred while copying the text to clipboard: {str(e)}")

    Console().print(response.text, style="deep_pink3")
