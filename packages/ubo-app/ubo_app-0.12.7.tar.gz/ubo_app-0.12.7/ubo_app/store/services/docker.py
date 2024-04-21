"""Docker store types."""

from __future__ import annotations

from dataclasses import field
from enum import StrEnum, auto

from immutable import Immutable
from redux import BaseAction, BaseCombineReducerState, BaseEvent


class DockerStatus(StrEnum):
    """Docker status."""

    UNKNOWN = auto()
    NOT_INSTALLED = auto()
    INSTALLING = auto()
    NOT_RUNNING = auto()
    RUNNING = auto()
    ERROR = auto()


class ImageStatus(StrEnum):
    """Image status."""

    NOT_AVAILABLE = auto()
    FETCHING = auto()
    AVAILABLE = auto()
    CREATED = auto()
    RUNNING = auto()
    ERROR = auto()


class DockerAction(BaseAction):
    """Docker action."""


class DockerSetStatusAction(DockerAction):
    """Docker set status action."""

    status: DockerStatus


class DockerImageAction(DockerAction):
    """Docker image action."""

    image: str


class DockerImageSetStatusAction(DockerImageAction):
    """Docker image set status action."""

    status: ImageStatus
    ports: list[str] | None = None
    ip: str | None = None


class DockerImageSetDockerIdAction(DockerImageAction):
    """Docker image set docker id action."""

    docker_id: str


class DockerEvent(BaseEvent):
    """Docker event."""


class DockerServiceState(Immutable):
    """Docker service state."""

    status: DockerStatus = DockerStatus.UNKNOWN


class DockerImageEvent(DockerEvent):
    """Docker image event."""

    image: str


class ImageState(Immutable):
    """Image state."""

    id: str
    label: str
    icon: str
    path: str
    status: ImageStatus = ImageStatus.NOT_AVAILABLE
    container_ip: str | None = None
    docker_id: str | None = None
    ports: list[str] = field(default_factory=list)
    ip_addresses: list[str] = field(default_factory=list)

    @property
    def is_fetching(self: ImageState) -> bool:
        """Check if image is available."""
        return self.status == ImageStatus.FETCHING

    @property
    def is_available(self: ImageState) -> bool:
        """Check if image is available."""
        return self.status in [ImageStatus.AVAILABLE, ImageStatus.RUNNING]

    @property
    def is_running(self: ImageState) -> bool:
        """Check if image is running."""
        return self.status == ImageStatus.RUNNING


class DockerState(BaseCombineReducerState):
    """Docker state."""

    service: DockerServiceState

    def __getattribute__(self: DockerState, name: str) -> ImageState:
        """Set type for random attributes of DockerState."""
        return super().__getattribute__(name)
