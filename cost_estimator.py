#!/usr/bin/env python3
"""llm-cost-estimator: estimate token counts and dollar cost of a prompt
across common LLMs, so you can compare before you pay.

Token counts are approximations only. Prices are illustrative USD per 1K
tokens -- update the PRICING table with current figures before relying on it.
"""

import argparse
import math
import sys

# Illustrative USD per 1,000 tokens. Replace with live prices as needed.
PRICING = {
    "gpt-4o":            {"input": 0.005,    "output": 0.015},
    "gpt-4o-mini":       {"input": 0.00015,  "output": 0.0006},
    "claude-3.5-sonnet": {"input": 0.003,    "output": 0.015},
    "claude-3-haiku":    {"input": 0.00025,  "output": 0.00125},
    "gemini-1.5-pro":    {"input": 0.00125,  "output": 0.005},
    "gemini-1.5-flash":  {"input": 0.000075, "output": 0.0003},
    "llama-3.1-70b":     {"input": 0.00059,  "output": 0.00079},
}


def estimate_tokens(text):
    """Rough token estimate: ~4 characters per token, rounded up."""
    return max(1, math.ceil(len(text) / 4))


def read_prompt(args):
    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            return fh.read()
    if args.prompt:
        return args.prompt
    if not sys.stdin.isatty():
        return sys.stdin.read()
    sys.exit("error: provide a prompt as an argument, --file, or via stdin")


def main():
    parser = argparse.ArgumentParser(
        description="Estimate prompt token count and cost across LLMs."
    )
    parser.add_argument("prompt", nargs="?", help="prompt text")
    parser.add_argument("--file", "-f", help="read prompt from a file")
    parser.add_argument(
        "--output-tokens", "-o", type=int, default=300,
        help="assumed output tokens for the estimate (default: 300)",
    )
    args = parser.parse_args()

    text = read_prompt(args)
    in_tokens = estimate_tokens(text)
    out_tokens = args.output_tokens

    print("Input characters : {:,}".format(len(text)))
    print("Est. input tokens: {:,}".format(in_tokens))
    print("Assumed output   : {:,} tokens\n".format(out_tokens))
    header = "{:<22} {:>10} {:>10} {:>10}".format("Model", "Input $", "Output $", "Total $")
    print(header)
    print("-" * len(header))
    for model, price in PRICING.items():
        in_cost = in_tokens / 1000 * price["input"]
        out_cost = out_tokens / 1000 * price["output"]
        total = in_cost + out_cost
        print("{:<22} {:>10.6f} {:>10.6f} {:>10.6f}".format(model, in_cost, out_cost, total))


if __name__ == "__main__":
    main()
