# Changelog

All notable changes to this project will be documented in this file.

## [0.0.6] - April 24, 2024

- Add keyword argument `fallback_to_default` to `build_messages` function to allow for defaulting to the CL100k token encoder and minimum GPT token limit if the model is not found.
- Fixed usage of `past_messages` argument of `build_messages` to not skip the last past message. (New user message should *not* be passed in)

## [0.0.5] - April 24, 2024

- Add keyword argument `default_to_cl100k` to `count_tokens_for_message` function to allow for defaulting to the CL100k token limit if the model is not found.
- Add keyword argument `default_to_minimum` to `get_token_limit` function to allow for defaulting to the minimum token limit if the model is not found.

## [0.0.4] - April 21, 2024

- Rename to openai-messages-token-helper from llm-messages-token-helper to reflect library's current OpenAI focus.

## [0.0.3] - April 21, 2024

- Fix for `count_tokens_for_message` function to match OpenAI output precisely, particularly for calls with images to GPT-4  vision.
