# Copyright (c) Microsoft. All rights reserved.

import asyncio

from flexible_semantic_kernel.plugin_definition import sk_function
from flexible_semantic_kernel.sk_pydantic import SKBaseModel


class WaitPlugin(SKBaseModel):
    """
    WaitPlugin provides a set of functions to wait for a certain amount of time.

    Usage:
        kernel.import_plugin(WaitPlugin(), plugin_name="wait")

    Examples:
        {{wait.seconds 5}} => Wait for 5 seconds
    """

    @sk_function(description="Wait for a certain number of seconds.")
    async def wait(self, seconds_text: str) -> None:
        try:
            seconds = max(float(seconds_text), 0)
        except ValueError:
            raise ValueError("seconds text must be a number")
        await asyncio.sleep(seconds)
