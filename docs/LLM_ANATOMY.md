# LLM Anatomy — Project Example

Project prompt:

> I know Python Basics. What should I learn before Agentic AI?

## Prompt journey

1. **Tokenization** — the text is split into tokens that the model can process.
2. **Token IDs** — tokens are mapped to numerical identifiers.
3. **Embeddings** — token IDs are represented as vectors.
4. **Positional information** — information about token order is represented.
5. **Transformer layers** — representations are repeatedly refined.
6. **Q/K/V** — attention uses queries, keys and values to determine which contextual information is useful.
7. **Self-attention** — tokens exchange contextual information.
8. **Residual connection** — earlier information is retained while new information is added.
9. **FFN** — each token representation is further transformed.
10. **Multiple layers** — the process is repeated through the model.
11. **Logits** — the model produces scores for possible next tokens.
12. **Softmax** — scores can be converted to probabilities.
13. **Decoding** — a next token is selected according to the decoding strategy.
14. **Repeat** — generation continues until the response is complete.

## Q/K/V intuition

For:

> What should I learn after Python?

- Query: what information is being sought?
- Key: which token/context information is relevant?
- Value: what information should be passed forward?

## Causal masking

During training, the complete sequence is available. Future tokens must be hidden when predicting the next token; otherwise the model could see information it is supposed to predict.

## Attention vs FFN

- Attention: communication/mixing of information between token representations.
- FFN: further transformation of each token representation.

## Temperature

Temperature changes variation/randomness in token selection. Higher temperature does not make an LLM more intelligent.
