"""Agent CLI entry point"""

import asyncio
import logging
import sys
from pathlib import Path

from .agent import EchoDeskAgent
from .config import AgentConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "register":
        # Manual registration mode
        config = AgentConfig()
        asyncio.run(register_agent(config))
    else:
        # Normal run mode
        config_file = Path("/etc/echodesk-agent/config.yml")
        if config_file.exists():
            config = AgentConfig.load(config_file)
        else:
            logger.warning(f"Config file not found at {config_file}, using defaults")
            config = AgentConfig()

        agent = EchoDeskAgent(config)
        asyncio.run(agent.start())


async def register_agent(config: AgentConfig):
    """Register agent and save config"""
    agent = EchoDeskAgent(config)
    await agent.register()
    print(f"\nAgent registered successfully!")
    print(f"Agent ID: {config.agent_id}")
    print(f"Config saved to: {config.config_file}")


if __name__ == "__main__":
    main()
