from abc import ABC, abstractmethod
from typing import Dict, Any

class Action(ABC):
    """
    Abstract base class for all Remediation Actions (The 'Hands' of the agent).
    """

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Executes the remediation action.
        Returns True if successful, False otherwise.
        
        context: A dictionary containing details about the alert and environment.
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the action."""
        pass
        
    @property
    def description(self) -> str:
        """Human-readable description of what this action does."""
        return self.name
