# llm-cost-estimator

A tiny Python CLI that estimates the token count and dollar cost of running a prompt across common LLMs, so you can compare prices before you spend. I built it because trying out models gets expensive fast and I wanted a quick way to see what a prompt would cost.

## Install

Python 3.8+, standard library only -- no dependencies.

    python cost_estimator.py --help

## Usage

Estimate a single prompt:

    python cost_estimator.py "Summarise the following article in three bullets"

From a file, assuming 500 output tokens:

    python cost_estimator.py --file prompt.txt --output-tokens 500

Piped from stdin:

    cat prompt.txt | python cost_estimator.py

It prints a table of estimated input/output/total cost per model.

## Notes

- Token counts are a rough approximation (~4 characters per token), not an exact tokenizer. Good enough for budgeting, not for billing.
- Prices in the PRICING table inside cost_estimator.py are illustrative USD per 1,000 tokens and go stale -- update them with current figures before relying on the numbers.
- Only the input side is estimated from your text; output is whatever you pass via --output-tokens.

## License

MIT -- see LICENSE.
