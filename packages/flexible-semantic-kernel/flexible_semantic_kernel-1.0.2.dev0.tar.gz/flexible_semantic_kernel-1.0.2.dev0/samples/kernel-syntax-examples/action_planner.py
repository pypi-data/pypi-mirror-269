# Copyright (c) Microsoft. All rights reserved.

import flexible_semantic_kernel as sk
from flexible_semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion,
)
from flexible_semantic_kernel.core_plugins import (
    FileIOPlugin,
    MathPlugin,
    TextPlugin,
    TimePlugin,
)
from flexible_semantic_kernel.planning import ActionPlanner


async def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()

    kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))
    kernel.import_plugin(MathPlugin(), "math")
    kernel.import_plugin(FileIOPlugin(), "fileIO")
    kernel.import_plugin(TimePlugin(), "time")
    kernel.import_plugin(TextPlugin(), "text")

    # create an instance of action planner.
    planner = ActionPlanner(kernel)

    # the ask for which the action planner is going to find a relevant function.
    ask = "What is the sum of 110 and 990?"

    # ask the action planner to identify a suitable function from the list of functions available.
    plan = await planner.create_plan_async(goal=ask)

    # ask the action planner to execute the identified function.
    result = await plan.invoke_async()
    print(result)
    """
    Output:
    1100
    """


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
