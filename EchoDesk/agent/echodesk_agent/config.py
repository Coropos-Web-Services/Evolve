"""Agent configuration"""

import platform
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseSettings):
    """Agent configuration"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ECHODESK_",
        case_sensitive=False,
    )

    # Server connection
    server_url: str = Field(
        default="http://localhost:8000",
        description="EchoDesk server URL",
    )
    verify_ssl: bool = True

    # Agent identity
    agent_id: str | None = None
    api_key: str | None = None
    name: str = Field(default_factory=platform.node)

    # System info
    hostname: str = Field(default_factory=platform.node)
    os: str = Field(default_factory=platform.system)
    os_version: str = Field(default_factory=platform.release)
    architecture: str = Field(default_factory=platform.machine)

    # Capabilities
    capabilities: list[str] = Field(
        default_factory=lambda: [
            "system.metrics",
        ]
    )

    # Behavior
    metrics_interval: int = 60  # seconds
    heartbeat_interval: int = 30  # seconds
    reconnect_delay: int = 5  # seconds

    # Paths
    config_file: Path = Path("/etc/echodesk-agent/config.yml")
    log_file: Path | None = None

    def save(self, path: Path | None = None) -> None:
        """Save configuration to file"""
        import yaml

        save_path = path or self.config_file
        save_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "server_url": self.server_url,
            "agent_id": self.agent_id,
            "api_key": self.api_key,
            "name": self.name,
            "capabilities": self.capabilities,
        }

        with open(save_path, "w") as f:
            yaml.dump(data, f)

    @classmethod
    def load(cls, path: Path) -> "AgentConfig":
        """Load configuration from file"""
        import yaml

        if not path.exists():
            return cls()

        with open(path) as f:
            data = yaml.safe_load(f) or {}

        return cls(**data)
