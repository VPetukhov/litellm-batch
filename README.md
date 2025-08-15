# LiteLLM Batch

A Python package for batch processing of LLM completions using [LiteLLM](https://github.com/BerriAI/litellm).

## Installation

```bash
pip install git+https://github.com/VPetukhov/litellm-batch.git
```

## Usage

```python
import asyncio
from litellm_batch import acompletion_batch, completion_cost_batch, process_batch

# Example batch of messages
message_batch = [
    [{"role": "user", "content": "Hello, how are you?"}],
    [{"role": "user", "content": "What is the capital of France?"}],
    [{"role": "user", "content": "Explain quantum computing briefly."}]
]

# Basic batch completion
results = await acompletion_batch(
    message_batch=message_batch,
    model="gpt-5",
    progress=True  # Show progress bar
)

# Calculate total cost
total_cost = completion_cost_batch(results)
print(f"Total cost: ${total_cost:.6f}")

# Process batch and get responses, results, and cost
responses, results, cost = await process_batch(
    message_batch=message_batch,
    model="gpt-5"
)

# Print the responses
for i, response in enumerate(responses):
    print(f"Response {i+1}: {response[:100]}...")
```

## License

MIT
