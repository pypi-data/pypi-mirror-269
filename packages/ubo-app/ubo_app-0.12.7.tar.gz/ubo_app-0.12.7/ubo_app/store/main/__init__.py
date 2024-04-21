# ruff: noqa: D100, D101, D102, D103, D104, D107
from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from immutable import Immutable
from redux import BaseAction, BaseEvent, FinishAction, InitAction

from ubo_app.store.services.keypad import KeypadAction
from ubo_app.store.status_icons import StatusIconsAction

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import TypeAlias

    from ubo_gui.menu.types import Item, Menu


class InitEvent(BaseEvent): ...


class RegisterAppAction(BaseAction):
    menu_item: Item


class UpdateLightDMState(BaseAction):
    is_active: bool
    is_enable: bool


class RegisterRegularAppAction(RegisterAppAction): ...


class RegisterSettingAppAction(RegisterAppAction): ...


class PowerOffAction(BaseAction): ...


class PowerOffEvent(BaseEvent): ...


class MainState(Immutable):
    menu: Menu | None = None
    path: Sequence[str] = field(default_factory=list)


class SetMenuPathAction(BaseAction):
    path: Sequence[str]


MainAction: TypeAlias = (
    InitAction
    | FinishAction
    | PowerOffAction
    | StatusIconsAction
    | KeypadAction
    | RegisterAppAction
    | SetMenuPathAction
)
