import litellm
from litellm import acompletion
from typing import List, Dict
import asyncio
from tqdm.asyncio import tqdm_asyncio


async def acompletion_batch(
        message_batch: List[List[Dict[str, str]]],
        model: str,
        progress: bool = False,
        **kwargs
    ) -> List[litellm.ModelResponse]:
    """
    Process a batch of message completions asynchronously.

    Args:
        message_batch (List[List[Dict[str, str]]]): A list of message lists, where each inner list
            contains message dictionaries for a single completion request.
        model (str): The language model to use for completions.
        progress (bool, optional): Whether to display a progress bar during processing. Defaults to False.
        **kwargs: Additional arguments to pass to the litellm.acompletion function.

    Returns:
        List[litellm.ModelResponse]: A list of model responses corresponding to each message in the batch.
    """
    tasks = [
        acompletion(model=model, messages=message, **kwargs)
        for message in message_batch
    ]

    if progress:
        return await tqdm_asyncio.gather(*tasks)

    return await asyncio.gather(*tasks)


def completion_cost_batch(result_batch: List[litellm.ModelResponse]):
    """
    Calculate the total cost of a batch of completion results.

    Args:
        result_batch (List[litellm.ModelResponse]): A list of model responses to calculate costs for.

    Returns:
        float: The total cost of all completions in the batch.
    """
    total_cost = 0
    for result in result_batch:
        total_cost += litellm.completion_cost(result)

    return total_cost


async def process_batch(message_batch: List[List[Dict[str, str]]], model: str, **kwargs):
    """
    Process a batch of messages, get completions, calculate costs, and extract responses.

    This function combines the functionality of acompletion_batch and completion_cost_batch
    to provide a complete processing pipeline for batch completions.

    Args:
        message_batch (List[List[Dict[str, str]]]): A list of message lists for batch processing.
        model (str): The language model to use for completions.
        **kwargs: Additional arguments to pass to the acompletion_batch function.

    Returns:
        tuple: A tuple containing:
            - responses (List[str]): The extracted text content from each completion
            - result_batch (List[litellm.ModelResponse]): The raw model responses
            - total_cost (float): The total cost of all completions
    """
    result_batch = await acompletion_batch(message_batch, model, **kwargs)
    total_cost = completion_cost_batch(result_batch)
    try:
        responses = [result.choices[-1].message.content for result in result_batch]
    except Exception as e:
        print(f"Error processing batch: {e}")
        responses = [""] * len(message_batch)

    return responses, result_batch, total_cost