"""Lego handlers."""

import asyncio

from result import Err, Ok, Result

from lego_handlers.components import (
    AsyncCommandComponent,
    CommandComponent,
    DomainEvent,
    E,
    R,
)


async def run_and_collect_events(
    cmd: AsyncCommandComponent[E, R] | CommandComponent[E, R],
) -> Result[tuple[R, list[DomainEvent]], E]:
    domain_events: list[DomainEvent] = []

    cmd_result: Result[R, E]
    match cmd:
        case AsyncCommandComponent():
            cmd_result = await cmd.run(events=domain_events)
        case CommandComponent():
            cmd_result = cmd.run(events=domain_events)

    match cmd_result:
        case Ok(result):
            return Ok((result, domain_events))
        case Err(error):
            return Err(error)


async def publish_events(events: list[DomainEvent]) -> None:
    """Publish events."""
    await asyncio.gather(
        *(event.publish() for event in events), return_exceptions=False
    )
