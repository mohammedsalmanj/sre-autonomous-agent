from abc import ABC, abstractmethod
from typing import Dict, Any, List

class Monitor(ABC):
    """
    Abstract base class for all Monitors (The 'Eyes' of the agent).
    """

    @abstractmethod
    def check(self) -> List[Dict[str, Any]]:
        """
        Performs a check of the monitored resource.
        Returns a list of alerts. An empty list means everything is healthy.
        
        Alert Structure:
        {
            "source": "monitor_name",
            "type": "alert_type",
            "severity": "info|warning|critical",
            "message": "Human readable description",
            "context": { ... extra data ... }
        }
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the monitor for logging purposes."""
        pass
