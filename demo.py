import sys
import os
import time

# Add src to path so imports work
sys.path.append(os.path.join(os.getcwd(), 'src'))

from core.engine import AgentEngine
from monitors.system import SystemMonitor
from logger import configure_logging

def main():
    configure_logging(log_level="INFO")
    
    print("\n" + "="*60)
    print(" SRE AGENT DEMO: SELF-HEALING & SAFETY RAILS")
    print("="*60)
    print(" 1. DETECT:  CPU Threshold set to 0.1% (Simulating Incident)")
    print(" 2. REACT:   Agent will attempt 'Mock Remediation' (Restart)")
    print(" 3. SAFETY:  Agent should STOP after 3 attempts (Circuit Breaker)")
    print("="*60 + "\n")
    
    # Create a monitor that will definitely fire (Threshold 0.1%)
    aggressive_monitor = SystemMonitor(cpu_threshold=0.1, memory_threshold=0.1)
    
    # Run loop fast (every 2 seconds) to demonstrate the safety valve quickly
    engine = AgentEngine(interval_seconds=2, monitors=[aggressive_monitor])
    
    try:
        engine.start()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
