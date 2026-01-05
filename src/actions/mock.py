import time
from typing import Dict, Any
from .base import Action
from structlog import get_logger

log = get_logger()

class MockRemediation(Action):
    """
    A placeholder action that simulates doing work (e.g., restarting a pod).
    """
    @property
    def name(self) -> str:
        return "mock_remediation_action"

    def execute(self, context: Dict[str, Any]) -> bool:
        log.info("executing_action", action=self.name, context=context)
        # Simulate work
        time.sleep(0.5)
        log.info("action_completed", action=self.name, status="success")
        return True
