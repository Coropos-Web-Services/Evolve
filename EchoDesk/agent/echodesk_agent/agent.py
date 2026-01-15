"""Main agent class"""

import asyncio
import logging
from typing import Any

import httpx

from .config import AgentConfig
from .metrics import MetricsCollector

logger = logging.getLogger(__name__)


class EchoDeskAgent:
    """EchoDesk Agent - manages connection to server and executes commands"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.metrics_collector = MetricsCollector()
        self.running = False
        self.client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        """Start the agent"""
        logger.info("Starting EchoDesk Agent...")

        # Ensure we're registered
        if not self.config.agent_id or not self.config.api_key:
            logger.info("Agent not registered. Registering with server...")
            await self.register()

        self.running = True

        # Create HTTP client
        self.client = httpx.AsyncClient(
            base_url=self.config.server_url,
            verify=self.config.verify_ssl,
            timeout=30.0,
        )

        # Start background tasks
        metrics_task = asyncio.create_task(self._metrics_loop())
        heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        logger.info(f"Agent started. ID: {self.config.agent_id}")

        try:
            # Wait for tasks
            await asyncio.gather(metrics_task, heartbeat_task)
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Stop the agent"""
        logger.info("Stopping EchoDesk Agent...")
        self.running = False
        if self.client:
            await self.client.aclose()

    async def register(self) -> None:
        """Register agent with server"""
        async with httpx.AsyncClient(verify=self.config.verify_ssl) as client:
            try:
                response = await client.post(
                    f"{self.config.server_url}/api/v1/agents/register",
                    json={
                        "name": self.config.name,
                        "hostname": self.config.hostname,
                        "os": self.config.os,
                        "os_version": self.config.os_version,
                        "architecture": self.config.architecture,
                        "capabilities": self.config.capabilities,
                    },
                )
                response.raise_for_status()
                data = response.json()

                self.config.agent_id = str(data["agent_id"])
                self.config.api_key = data["api_key"]

                # Save config
                self.config.save()

                logger.info(f"Agent registered successfully. ID: {self.config.agent_id}")
                logger.info(f"API key saved to {self.config.config_file}")

            except httpx.HTTPError as e:
                logger.error(f"Failed to register agent: {e}")
                raise

    async def _metrics_loop(self) -> None:
        """Send metrics to server periodically"""
        while self.running:
            try:
                await self._send_metrics()
            except Exception as e:
                logger.error(f"Error sending metrics: {e}")

            await asyncio.sleep(self.config.metrics_interval)

    async def _heartbeat_loop(self) -> None:
        """Send heartbeat to server periodically"""
        while self.running:
            try:
                await self._send_heartbeat()
            except Exception as e:
                logger.error(f"Error sending heartbeat: {e}")

            await asyncio.sleep(self.config.heartbeat_interval)

    async def _send_metrics(self) -> None:
        """Send metrics to server"""
        if not self.client:
            return

        metrics = self.metrics_collector.collect_all()
        logger.debug(f"Sending metrics: {metrics}")

        # TODO: Implement metrics endpoint on server
        # For now, just log
        logger.info(f"CPU: {metrics['cpu']['percent']}% | Memory: {metrics['memory']['percent']}%")

    async def _send_heartbeat(self) -> None:
        """Send heartbeat to server"""
        if not self.client:
            return

        logger.debug("Sending heartbeat")

        # TODO: Implement heartbeat endpoint on server
        # For now, just log
        logger.debug("Heartbeat sent")
