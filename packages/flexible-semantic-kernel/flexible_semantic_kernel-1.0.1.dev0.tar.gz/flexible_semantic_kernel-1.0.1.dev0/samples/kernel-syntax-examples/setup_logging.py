# Copyright (c) Microsoft. All rights reserved.
import logging

import flexible_semantic_kernel as sk
from flexible_semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from flexible_semantic_kernel.utils.logging import setup_logging


async def main():
    setup_logging()

    # Set the logging level for  flexible_semantic_kernel.kernel to DEBUG.
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    kernel = sk.Kernel()

    api_key, org_id = sk.openai_settings_from_dot_env()

    kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))

    plugin = kernel.import_semantic_plugin_from_directory("../../samples/plugins", "FunPlugin")

    joke_function = plugin["Joke"]

    print(joke_function("time travel to dinosaur age"))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
