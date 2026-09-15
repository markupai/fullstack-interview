from temporalio import activity


@activity.defn
async def compose_greeting(name: str) -> str:
    activity.logger.info("composing greeting for %s", name)
    return f"Hello, {name}!"
