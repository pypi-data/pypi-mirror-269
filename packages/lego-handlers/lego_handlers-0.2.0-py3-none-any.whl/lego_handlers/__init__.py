"""Lego handlers."""

import asyncio

from result import Ok, Result
from typing_extensions import assert_never

from lego_handlers.components import (
    AsyncCommandComponent,
    CommandComponent,
    DomainEvent,
    E,
    R,
)


async def run_and_publish(
    cmd: AsyncCommandComponent[E, R] | CommandComponent[E, R],
) -> Result[R, E]:
    domain_events: list[DomainEvent] = []
    cmd_result: Result[R, E]
    if isinstance(cmd, AsyncCommandComponent):
        cmd_result = await cmd.run(events=domain_events)
    elif isinstance(cmd, CommandComponent):
        cmd_result = cmd.run(events=domain_events)
    else:
        assert_never(cmd)

    if isinstance(cmd_result, Ok):
        await publish_events(events=domain_events)
    return cmd_result


async def publish_events(events: list[DomainEvent]) -> None:
    """Publish events."""
    await asyncio.gather(
        *(event.publish() for event in events), return_exceptions=False
    )
