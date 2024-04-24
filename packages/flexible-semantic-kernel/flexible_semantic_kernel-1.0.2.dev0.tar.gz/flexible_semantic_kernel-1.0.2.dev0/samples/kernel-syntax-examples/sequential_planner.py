# Copyright (c) Microsoft. All rights reserved.

import flexible_semantic_kernel as sk
from flexible_semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from flexible_semantic_kernel.core_plugins import (
    FileIOPlugin,
    MathPlugin,
    TextPlugin,
    TimePlugin,
)
from flexible_semantic_kernel.planning import SequentialPlanner


async def main():
    kernel = sk.Kernel()
    api_key, org_id = sk.openai_settings_from_dot_env()

    kernel.add_chat_service("gpt-3.5", OpenAIChatCompletion("gpt-3.5-turbo", api_key=api_key, org_id=org_id))
    kernel.import_plugin(MathPlugin(), "math")
    kernel.import_plugin(FileIOPlugin(), "fileIO")
    kernel.import_plugin(TimePlugin(), "time")
    kernel.import_plugin(TextPlugin(), "text")

    # create an instance of sequential planner.
    planner = SequentialPlanner(kernel)

    # the ask for which the sequential planner is going to find a relevant function.
    ask = "What day of the week is today, all uppercase?"

    # ask the sequential planner to identify a suitable function from the list of functions available.
    plan = await planner.create_plan_async(goal=ask)

    # ask the sequential planner to execute the identified function.
    result = await plan.invoke_async()

    for step in plan._steps:
        print(step.description, ":", step._state.__dict__)

    print("Expected Answer:")
    print(result)
    """
    Output:
    SUNDAY
    """


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
