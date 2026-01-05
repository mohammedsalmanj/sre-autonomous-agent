import time
import pytest
from src.core.safety import SafetyCircuitBreaker

def test_circuit_breaker_allows_within_limit():
    # Allow 2 actions per minute
    safety = SafetyCircuitBreaker(max_actions_per_window=2, window_seconds=60)
    
    assert safety.allow_action("test_action") is True
    assert safety.allow_action("test_action") is True

def test_circuit_breaker_blocks_exceeded_limit():
    # Allow 1 action per minute
    safety = SafetyCircuitBreaker(max_actions_per_window=1, window_seconds=60)
    
    assert safety.allow_action("test_action") is True
    assert safety.allow_action("test_action") is False  # Should block

def test_circuit_breaker_resets_after_window():
    # Allow 1 action per 1 second
    safety = SafetyCircuitBreaker(max_actions_per_window=1, window_seconds=1)
    
    assert safety.allow_action("test_action") is True
    time.sleep(1.1)
    assert safety.allow_action("test_action") is True  # Should be allowed again
