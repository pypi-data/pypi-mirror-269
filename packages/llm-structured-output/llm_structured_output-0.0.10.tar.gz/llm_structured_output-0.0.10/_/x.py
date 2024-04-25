import json
import mlx.core as mx
from mlx_lm.utils import load  # Needs pip import mlx_lm
from src.llm_structured_output import (
    JsonSchemaAcceptorDriver,
    HuggingfaceTokenizerHelper,
    bias_logits,
)


MODEL_PATH = "mistralai/Mistral-7B-Instruct-v0.2"
SCHEMA = {
    "type": "object",
    "properties": {
        "streetNumber": {"type": "number"},
        "streetName": {"type": "string"},
        "city": {"type": "string"},
        "state": {"type": "string"},
        "zipCode": {"type": "number"},
    },
}
PROMPT = f"""
[INST] Parse the following address into a JSON object: "27 Barrow St, New York, NY 10014".
Your answer should be only a JSON object according to this schema: {json.dumps(SCHEMA)}
Do not explain the result, just output it. Do not add any additional information. [/INST]
"""


# Load the model as usual.
model, tokenizer = load(MODEL_PATH)

# Instantiate a token acceptor
tokenizer_helper = HuggingfaceTokenizerHelper(tokenizer)
vocabulary, eos_id = tokenizer_helper.extract_vocabulary()
token_acceptor_factory = JsonSchemaAcceptorDriver.driver_factory_for_model(vocabulary, eos_id)
token_acceptor = token_acceptor_factory(SCHEMA)

cache = None
tokens = tokenizer_helper.encode_prompt(PROMPT)

mx_fast_scaled_dot_product_attention = mx.fast.scaled_dot_product_attention
def mock_fast_scaled_dot_product_attention(q, k, v, *, scale, mask = None, stream = None):
    result = mx_fast_scaled_dot_product_attention(q, k, v, scale=scale, mask=mask, stream=stream)
    print("MOCK", result.shape)
    return result
mx.fast.scaled_dot_product_attention = mock_fast_scaled_dot_product_attention

while tokens[-1] != eos_id:
    # Evaluate the model as usual.
    logits, cache = model(mx.array(tokens)[None], cache)

    # Set probability to -inf for invalid tokens.
    accepted_token_bitmap = token_acceptor.select_valid_tokens()
    logits = bias_logits(mx, logits[0, -1, :], accepted_token_bitmap)

    # Sample as usual, e.g.:
    token = mx.argmax(logits, axis=-1).item()

    if token == eos_id:
        break

    # Store or use the generated token.
    tokens = [token]
    text = tokenizer_helper.no_strip_decode(tokens)
    print(text, end="")

    # Advance the acceptor to the next state.
    token_acceptor.advance_token(token)
