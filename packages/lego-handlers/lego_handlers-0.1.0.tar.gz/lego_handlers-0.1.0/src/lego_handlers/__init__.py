"""Lego handlers."""

import asyncio

from lego_handlers.components import DomainEvent


async def publish_events(events: list[DomainEvent]) -> None:
    """Publish events."""
    await asyncio.gather(
        *(event.publish() for event in events), return_exceptions=False
    )
