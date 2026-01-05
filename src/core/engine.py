import time
import signal
import sys
from structlog import get_logger

log = get_logger()

from monitors.system import SystemMonitor
from core.safety import SafetyCircuitBreaker
from actions.mock import MockRemediation

class AgentEngine:
    """
    The main control loop for the SRE Agent.
    It manages the lifecycle of the agent: Start -> Monitor -> Act -> Stop.
    """
    def __init__(self, interval_seconds=10, monitors=None):
        self.interval = interval_seconds
        self.running = False
        self._setup_signals()
        
        # 1. Monitors (The Eyes)
        if monitors:
            self.monitors = monitors
        else:
            self.monitors = [SystemMonitor()]
        
        # 2. Safety (The Guardrails)
        # Allow max 3 actions per minute
        self.safety = SafetyCircuitBreaker(max_actions_per_window=3, window_seconds=60)
        
        # 3. Actions Registry (The Hands)
        # Mapping Alert Type -> Action to take
        self.action_registry = {
            "high_cpu": MockRemediation(),
            "high_memory": MockRemediation()
        }

    def _setup_signals(self):
        """
        Setup signal handlers for graceful shutdown.
        Captures SIGINT (Ctrl+C) and SIGTERM so we can finish current tasks before exiting.
        """
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    def start(self):
        """
        Starts the main control loop.
        """
        self.running = True
        log.info("agent_started", interval=self.interval)
        
        while self.running:
            start_time = time.time()
            try:
                self.tick()
            except Exception as e:
                # Catch-all to prevent the agent from crashing due to a transient error
                log.exception("agent_tick_failed", error=str(e))
            
            # Calculate sleep to maintain a consistent cadence
            elapsed = time.time() - start_time
            sleep_time = max(0, self.interval - elapsed)
            time.sleep(sleep_time)
        
        log.info("agent_stopped")

    def tick(self):
        """
        The Heartbeat.
        Executes one full cycle of: Observe -> Decide -> Act.
        """
        log.debug("heartbeat_check", status="ok")
        
        # 1. Observe
        all_alerts = []
        for monitor in self.monitors:
            try:
                alerts = monitor.check()
                if alerts:
                    log.info("alerts_detected", monitor=monitor.name, count=len(alerts))
                    all_alerts.extend(alerts)
            except Exception as e:
                log.error("monitor_failed", monitor=monitor.name, error=str(e))

        # 2. Decide & Act
        if all_alerts:
            self.handle_alerts(all_alerts)

    def handle_alerts(self, alerts):
        """
        Process alerts and determine actions.
        """
        for alert in alerts:
            alert_type = alert['type']
            log.info("analyzing_alert", alert_type=alert_type, severity=alert['severity'])
            
            # Find matching action
            action = self.action_registry.get(alert_type)
            if not action:
                log.warning("no_remediation_defined", alert_type=alert_type)
                continue
                
            # Check Safety Valve
            if not self.safety.allow_action(action.name):
                log.error("remediation_blocked_by_safety", action=action.name, reason="rate_limit")
                continue
                
            # Execute Action
            log.info("initiating_remediation", action=action.name)
            try:
                success = action.execute(context=alert)
                if success:
                    log.info("remediation_success", action=action.name)
                else:
                    log.error("remediation_failed", action=action.name)
            except Exception as e:
                log.exception("remediation_crashed", action=action.name, error=str(e))



    def stop(self, signum=None, frame=None):
        """
        Signal handler to stop the loop.
        """
        log.info("shutdown_signal_received", signal=signum)
        self.running = False
