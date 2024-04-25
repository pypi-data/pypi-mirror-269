"""
Module to generate images based on provided input prompts using the DeepAI API.

The module uses the DeepAI API to create images based on provided text prompts.
It supports generating images in both High Definition (HD) and Standard Definition (SD).
It also supports running the image generation process in an asynchronous manner using asyncio.

The module reads the input prompts from src/promptsets.json and uses environment 
variables to get the API key, endpoint, and generator model for the DeepAI API.
"""

import argparse
import asyncio
import itertools
import json
import logging
import os
import time
from typing import Tuple, Union

import httpx
from dotenv import load_dotenv
from tqdm.asyncio import tqdm

load_dotenv()

RETRY_ATTEMPTS = 2
APIKEY: str = os.environ.get("DEEPAIKEY", "No_API_KEY")
BASE_URL: str = os.environ.get("ENDPOINT", "https://api.deepai.org/api/text2img")
MODEL: str = os.environ.get("GENERATOR_MODEL", 'hd')
DEBUG_MODE = False
ERROR_COUNT = (
    0
)


LOG_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGING_LEVEL = logging.INFO

FILE_HANDLER = logging.FileHandler("app.log", mode="a")
FILE_HANDLER.setLevel(LOGGING_LEVEL)
FILE_FORMATTER = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
FILE_HANDLER.setFormatter(FILE_FORMATTER)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(LOGGING_LEVEL)
STREAM_FORMATTER = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
STREAM_HANDLER.setFormatter(STREAM_FORMATTER)

ROOT_LOGGER = logging.getLogger()
ROOT_LOGGER.setLevel(LOGGING_LEVEL)
ROOT_LOGGER.addHandler(FILE_HANDLER)
ROOT_LOGGER.addHandler(STREAM_HANDLER)

GOOD_RESOLUTIONS: list[dict[str, Tuple[int, int]|float]] = [
    {"size": (1024, 1024), "aspect_ratio": 1.0},
    {"size": (1032, 1016), "aspect_ratio": 1.016},
    {"size": (1040, 1008), "aspect_ratio": 1.032},
    {"size": (1048, 1000), "aspect_ratio": 1.048},
    {"size": (1120, 936), "aspect_ratio": 1.197},
    {"size": (1160, 904), "aspect_ratio": 1.283},
    {"size": (1192, 880), "aspect_ratio": 1.355},
    {"size": (1224, 856), "aspect_ratio": 1.43},
]


def make_payload(input_prompt: Union[str, dict[str, str]], version: int=0, square: bool=False) -> dict[str, str]:
    """
    Constructs the payload to be sent to the DeepAI API.

    Args:
    - input_prompt (Union[str, dict]): The prompt based on which the image should be generated.
    - version (int, optional): Version of the generator model. Defaults to 0.
    - square (bool, optional): If True, generates a square image. Defaults to False.

    Returns:
    - dict: Payload for the API request.
    """
    __prompt: str = ""
    if type(input_prompt) is dict:
        __prompt = input_prompt["prompt"]
    if type(input_prompt) is str:
        __prompt = input_prompt
    w = "1024" if square else str(1224 / (2 - version))
    l = "1024" if square else str(856 / (2 - version))
    payload: dict[str, str] = {
        "text": __prompt,
        "grid_size": "1",
        "width": "1224" if version == 0 else "612",
        "height": "856" if version == 0 else "428",
    }
    if version == 0:
        payload["image_generator_version"] = MODEL
    return payload


async def generate_image(
    prompt_data: dict,
    client: httpx.AsyncClient = httpx.AsyncClient(),
    version=0,
    setname=None,
    semaphore=None,
    pbar=None,
):
    """
    Asynchronously generates an image based on the provided prompt data.

    Args:
    - prompt_data (dict): Dictionary containing the name and prompt for image generation.
    - client (httpx.AsyncClient, optional): HTTP client for making API requests. If not provided, a new one is created.
    - version (int, optional): Version of the generator model. Defaults to 0.
    - setname (str, optional): Name of the set to which the prompt belongs. Used for organizing saved images.
    - semaphore (asyncio.Semaphore, optional): Semaphore for controlling concurrency.

    Returns:
    - None
    """
    global ERROR_COUNT
    if semaphore is None:
        return
    async with semaphore:
        outpath = "../images" if version == 0 else "../images_sd"
        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        if setname is not None and not os.path.isdir(os.path.join(outpath, setname)):
            os.mkdir(os.path.join(outpath, setname))
        outpath = os.path.join(outpath, setname) if setname is not None else outpath
        payload = make_payload(prompt_data["prompt"], version=version)
        headers = {"api-key": APIKEY}

        if DEBUG_MODE:
            logging.info(
                f"Prompt: {prompt_data}, payload: {payload}, version: {version}, outpath: {outpath}, headers: {headers}".replace(
                    ",", "\n"
                )
            )
            input("paused")

        _url = BASE_URL if version == 0 else "https://api.deepai.org/api/text2img"

        attempt = 0
        while attempt < RETRY_ATTEMPTS:
            response = await client.post(_url, headers=headers, data=payload)
            if response.status_code < 300:
                await asyncio.sleep(1)
                break
            logging.warning(
                f"Attempt {attempt + 1}/{RETRY_ATTEMPTS} failed for prompt '{prompt_data['name']}': {response.text}"
            )
            attempt += 1
            ERROR_COUNT += 1
            if attempt < RETRY_ATTEMPTS:
                await asyncio.sleep(5)
        else:
            logging.error(
                f"All {RETRY_ATTEMPTS} attempts failed for prompt '{prompt_data['name']}'"
            )
            return

        image_url = response.json()["output_url"]
        attempt = 0
        while attempt < RETRY_ATTEMPTS:
            image_response = await client.get(image_url)
            if image_response.status_code < 300:
                break
            logging.warning(
                f"Attempt {attempt + 1}/{RETRY_ATTEMPTS} failed to fetch output image for prompt '{prompt_data['name']}': {image_response.text}"
            )
            attempt += 1
            ERROR_COUNT += 1
            if attempt < RETRY_ATTEMPTS:
                await asyncio.sleep(5)
        else:
            logging.error(
                f"All {RETRY_ATTEMPTS} attempts failed to fetch output image for prompt '{prompt_data['name']}'"
            )
            if pbar:
                pbar.update(1)
            return

        base_filename = f"{outpath}/{prompt_data['name'].replace(' ', '_').lower()}_{int(time.time())}.{'SD' if version == 1 else 'HD'}"
        filename = f"{base_filename}.jpg"
        file_index = 1

        while os.path.isfile(filename):
            logging.warning(f"File {filename} already exists, incrementing index")
            filename = f"{base_filename}_{file_index}.jpg"
            file_index += 1

        with open(filename, "wb") as f:
            f.write(image_response.content)
        if pbar:
            pbar.update(1)
        logging.info(f"Saved image for prompt '{prompt_data['name']}' as {filename}")


def do_HD(data, itrs=2, setname=None):
    """
    Synchronously generates HD images based on the provided data.

    Args:
    - data (Union[dict, List[dict]]): Data containing the prompts for image generation.
    - itrs (int, optional): Number of iterations to generate images. Defaults to 2.
    - setname (str, optional): Name of the set to which the prompt belongs. Used for organizing saved images.

    Returns:
    - None
    """
    with httpx.Client(timeout=None) as client:
        if type(data) is list:
            for itr, prompt_data in itertools.product(range(itrs), data):
                if not all([ea in prompt_data for ea in ["name", "prompt"]]):
                    raise ValueError(
                        "Each prompt dict must have a 'name' and 'prompt' key."
                    )
                logging.info(
                    f"Running inference {itr+1}/{itrs} for prompt:\nName: {prompt_data['name']}\nPrompt: {prompt_data['prompt']}"
                )
                generate_image(prompt_data, client, 0, setname)
        elif isinstance(data, dict):
            generate_image(data, client, 0, setname)
        else:
            raise TypeError(
                "Unsupported data type. Please provide a dict or list of dicts."
            )


def do_SD(data, itrs=2, setname=None):
    """
    Synchronously enerates SD images based on the provided data.

    Args:
    - data (Union[dict, List[dict]]): Data containing the prompts for image generation.
    - itrs (int, optional): Number of iterations to generate images. Defaults to 2.
    - setname (str, optional): Name of the set to which the prompt belongs. Used for organizing saved images.

    Returns:
    - None
    """
    with httpx.Client(timeout=None) as client:
        if type(data) is list:
            for itr, prompt_data in itertools.product(range(itrs), data):
                if not all([ea in prompt_data for ea in ["name", "prompt"]]):
                    raise ValueError(
                        "Each prompt dict must have a 'name' and 'prompt' key."
                    )
                logging.info(
                    f"Running inference {itr+1}/{itrs} for prompt:\nName: {prompt_data['name']}\nPrompt: {prompt_data['prompt']}"
                )
                generate_image(prompt_data, client, 1, setname)
        elif isinstance(data, dict):
            generate_image(data, client, 1, setname)
        else:
            raise TypeError(
                "Unsupported data type. Please provide a dict or list of dicts."
            )


async def async_do_HD(data, itrs=2, setname=None, semaphore=None, pbar=None):
    """
    Asynchronously generates HD images based on the provided data.

    Args:
    - data (List[dict]): Data containing the prompts for image generation.
    - itrs (int, optional): Number of iterations to generate images. Defaults to 2.
    - setname (str, optional): Name of the set to which the prompt belongs. Used for organizing saved images.
    - semaphore (asyncio.Semaphore, optional): Semaphore for controlling concurrency.

    Returns:
    - None
    """
    async with httpx.AsyncClient(timeout=None) as client:
        tasks = [
            generate_image(prompt_data, client, 0, setname, semaphore, pbar)
            for itr, prompt_data in itertools.product(range(itrs), data)
            if all([ea in prompt_data for ea in ["name", "prompt"]])
        ]
        await asyncio.gather(*tasks)


async def async_do_SD(data, itrs=2, setname=None, semaphore=None, pbar=None):
    """
    Asynchronously generates SD images based on the provided data.

    Args:
    - data (List[dict]): Data containing the prompts for image generation.
    - itrs (int, optional): Number of iterations to generate images. Defaults to 2.
    - setname (str, optional): Name of the set to which the prompt belongs. Used for organizing saved images.
    - semaphore (asyncio.Semaphore, optional): Semaphore for controlling concurrency.

    Returns:
    - None
    """
    async with httpx.AsyncClient(timeout=None) as client:
        tasks = [
            generate_image(prompt_data, client, 1, setname, semaphore, pbar)
            for itr, prompt_data in itertools.product(range(itrs), data)
            if all([ea in prompt_data for ea in ["name", "prompt"]])
        ]
        await asyncio.gather(*tasks)


async def generate_both(data, itrs=2, setname=None, semaphore=None, pbar=None):
    """
    Asynchronously generates both HD and SD images based on the provided data.

    Args:
    - data (List[dict]): Data containing the prompts for image generation.
    - itrs (int, optional): Number of iterations to generate images. Defaults to 2.
    - setname (str, optional): Name of the set to which the prompt belongs. Used for organizing saved images.
    - semaphore (asyncio.Semaphore, optional): Semaphore for controlling concurrency.

    Returns:
    - None
    """
    tasks = [
        async_do_HD(data, itrs, setname, semaphore, pbar),
        async_do_SD(data, itrs, setname, semaphore, pbar),
    ]
    await asyncio.gather(*tasks)


def main():
    ROOT_LOGGER.removeHandler(STREAM_HANDLER)
    parser = argparse.ArgumentParser(
        description="Generate images based on command line arguments."
    )
    parser.add_argument("-n", "--num", type=int, default=2, help="Number of images to generate for each prompt/quality")
    parser.add_argument(
        "-p",
        "--prompts",
        type=str,
        default="promptsets.example.json",
        help="File path to the promptsets file. (JSON, List[Dict[str, str]])",
    )
    parser.add_argument(
        "-q",
        "--quality",
        choices=["both", "hd", "sd"],
        default="hd",
        help="Quality of the image to generate.",
    )
    parser.add_argument(
        "-c",
        "--concurrency",
        default=4,
        help="Number of concurrent image generation tasks to run. Default: 4",
    )

    args = parser.parse_args()

    async def _main(args: argparse.Namespace) -> None:
        """
        Asynchronous main function to handle the entire image generation process based on command-line arguments.

        This function reads the prompts from the promptsets file and processes them based (af)
        on the arguments provided. It supports generating HD and/or SD images based on the
        quality argument and runs the generation process with controlled concurrency using a semaphore.

        Returns:
        - None
        """
        semaphore = asyncio.Semaphore(args.concurrency)
        with open(args.prompts) as f:
            _prompt_data = json.load(f)

        total_tasks = sum(len(prompts) for prompts in _prompt_data.values()) * args.num
        with tqdm(total=total_tasks, desc="Generating Images", leave=True) as _progress_bar:
            for _prompt_set in _prompt_data.keys():
                if args.quality == "both":
                    logging.info(
                        f"Running both HD and SD prompts (concurrency: {args.concurrency}): {_prompt_set}"
                    )
                    await generate_both(
                        _prompt_data.get(_prompt_set),
                        itrs=args.num,
                        setname=_prompt_set,
                        semaphore=semaphore,
                        pbar=_progress_bar,
                    )
                elif args.quality == "hd":
                    logging.info(f"Running only HD prompts (concurrency: {args.concurrency}): {_prompt_set}")
                    await async_do_HD(
                        _prompt_data.get(_prompt_set),
                        itrs=args.num,
                        setname=_prompt_set,
                        semaphore=semaphore,
                        pbar=_progress_bar,
                    )
                elif args.quality == "sd":
                    logging.info(f"Running only HD prompts (concurrency: {args.concurrency}): {_prompt_set}")
                    await async_do_SD(
                        _prompt_data.get(_prompt_set),
                        itrs=args.num,
                        setname=_prompt_set,
                        semaphore=semaphore,
                        pbar=_progress_bar,
                    )

        logging.info(f"Finished processing. Total errors encountered: {ERROR_COUNT}")

    asyncio.run(_main(args))


if __name__ == "__main__":
    main()