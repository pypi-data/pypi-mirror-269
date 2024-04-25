from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID, uuid4

import lego_handlers
from lego_handlers.components import (
    CommandComponent,
    DomainError,
    DomainEvent,
    ResponseComponent,
)
from result import Err, Ok, Result


@dataclass(frozen=True)
class ResponseCreateAccount(ResponseComponent):
    account_id: UUID
    initial_balance: int


@dataclass(frozen=True)
class AccountCreated(DomainEvent):
    async def publish(self) -> None: ...


class NegativeInitialBalanceError(DomainError):
    def __init__(self) -> None:
        super().__init__(
            "Not possible to create account with negative initial balance."
        )


class ZeroInitialBalanceError(DomainError):
    def __init__(self) -> None:
        super().__init__("Not possible to create account with zero initial balance.")


CreateAccountErrors: TypeAlias = NegativeInitialBalanceError | ZeroInitialBalanceError


@dataclass(frozen=True)
class CreateAccount(CommandComponent[CreateAccountErrors, ResponseCreateAccount]):
    initial_balance: int

    def run(
        self, events: list[DomainEvent]
    ) -> Result[ResponseCreateAccount, CreateAccountErrors]:
        if self.initial_balance < 0:
            return Err(NegativeInitialBalanceError())

        if self.initial_balance == 0:
            return Err(ZeroInitialBalanceError())

        events.append(AccountCreated())

        return Ok(
            ResponseCreateAccount(
                account_id=uuid4(), initial_balance=self.initial_balance
            )
        )


async def test_run_command() -> None:
    intial_balance = 10
    create_account_events: list[DomainEvent] = []
    command_result = CreateAccount(
        initial_balance=intial_balance,
    ).run(
        events=create_account_events,
    )
    assert isinstance(command_result, Ok)
    assert command_result.unwrap().initial_balance == intial_balance
    assert len(create_account_events) == 1
    await lego_handlers.publish_events(events=create_account_events)
