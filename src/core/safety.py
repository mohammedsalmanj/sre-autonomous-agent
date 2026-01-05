import time
from collections import deque
from structlog import get_logger

log = get_logger()

class SafetyCircuitBreaker:
    """
    The Safety Valve.
    Prevents the agent from causing cascading failures by executing too many actions too quickly.
    
    Principles:
    1. Rate Limiting: Don't execute more than X actions in Y seconds.
    2. Backoff: (Future) If an action keeps failing, stop trying.
    3. Global Lock: (Future) Prevent multiple agents from acting on the same resource.
    """
    def __init__(self, max_actions_per_window=5, window_seconds=60):
        self.max_actions = max_actions_per_window
        self.window = window_seconds
        # Stores history of executed actions: {'timestamp': float, 'action': str}
        self.history = deque()

    def allow_action(self, action_name: str) -> bool:
        """
        Checks if an action is safe to execute based on rate limits.
        """
        now = time.time()
        
        # 1. Prune history (remove events older than the window)
        while self.history and self.history[0]['timestamp'] < now - self.window:
            self.history.popleft()
            
        # 2. Check Global Rate Limit
        if len(self.history) >= self.max_actions:
            log.warning("safety_valve_triggered", 
                        reason="global_rate_limit_exceeded",
                        desired_action=action_name, 
                        limit=self.max_actions, 
                        window_seconds=self.window)
            return False
            
        # 3. Update History (optimistic, assuming the action will happen)
        # Note: In a stricter system, we might update this only AFTER execution, 
        # but for safety, we count the *attempt*.
        self.history.append({'timestamp': now, 'action': action_name})
        log.info("safety_check_passed", action=action_name)
        return True
