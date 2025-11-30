"""
Observability System: Logging, Tracing, and Metrics
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import json
from collections import defaultdict
from dataclasses import dataclass, asdict


@dataclass
class TraceEvent:
    """Trace event for observability"""
    agent_id: str
    event_type: str
    timestamp: datetime
    duration_ms: Optional[float] = None
    metadata: Dict[str, Any] = None
    
    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "metadata": self.metadata or {}
        }


@dataclass
class Metric:
    """Metric for tracking agent performance"""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = None
    
    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "tags": self.tags or {}
        }


class ObservabilitySystem:
    """
    Centralized observability system for logging, tracing, and metrics
    """
    
    def __init__(self, log_level: str = "INFO"):
        self.logger = logging.getLogger("observability")
        self.traces: List[TraceEvent] = []
        self.metrics: List[Metric] = []
        self.logs: List[Dict[str, Any]] = []
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def log(
        self,
        level: str,
        message: str,
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log a message"""
        log_entry = {
            "level": level,
            "message": message,
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.logs.append(log_entry)
        
        # Also log to standard logging
        log_func = getattr(self.logger, level.lower(), self.logger.info)
        log_func(f"[{agent_id}] {message}", extra=metadata)
    
    def trace(
        self,
        agent_id: str,
        event_type: str,
        duration_ms: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record a trace event"""
        trace = TraceEvent(
            agent_id=agent_id,
            event_type=event_type,
            timestamp=datetime.now(),
            duration_ms=duration_ms,
            metadata=metadata
        )
        
        self.traces.append(trace)
        self.log("DEBUG", f"Trace: {event_type}", agent_id=agent_id, metadata=metadata)
    
    def record_metric(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ):
        """Record a metric"""
        metric = Metric(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {}
        )
        
        self.metrics.append(metric)
        self.log("DEBUG", f"Metric: {name}={value}", metadata={"tags": tags})
    
    def get_traces(
        self,
        agent_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get traces with optional filtering"""
        filtered = self.traces
        
        if agent_id:
            filtered = [t for t in filtered if t.agent_id == agent_id]
        
        if event_type:
            filtered = [t for t in filtered if t.event_type == event_type]
        
        return [t.to_dict() for t in filtered[-limit:]]
    
    def get_metrics(
        self,
        name: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get metrics with optional filtering"""
        filtered = self.metrics
        
        if name:
            filtered = [m for m in filtered if m.name == name]
        
        return [m.to_dict() for m in filtered[-limit:]]
    
    def get_aggregated_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics across all agents"""
        aggregated = defaultdict(list)
        
        for metric in self.metrics:
            aggregated[metric.name].append(metric.value)
        
        result = {}
        for name, values in aggregated.items():
            result[name] = {
                "count": len(values),
                "sum": sum(values),
                "avg": sum(values) / len(values) if values else 0,
                "min": min(values) if values else 0,
                "max": max(values) if values else 0
            }
        
        return result
    
    def get_logs(
        self,
        level: Optional[str] = None,
        agent_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get logs with optional filtering"""
        filtered = self.logs
        
        if level:
            filtered = [l for l in filtered if l["level"] == level]
        
        if agent_id:
            filtered = [l for l in filtered if l.get("agent_id") == agent_id]
        
        return filtered[-limit:]
    
    def export_traces(self, filepath: str):
        """Export traces to JSON file"""
        with open(filepath, 'w') as f:
            json.dump([t.to_dict() for t in self.traces], f, indent=2)
    
    def export_metrics(self, filepath: str):
        """Export metrics to JSON file"""
        with open(filepath, 'w') as f:
            json.dump([m.to_dict() for m in self.metrics], f, indent=2)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for observability dashboard"""
        return {
            "traces_count": len(self.traces),
            "metrics_count": len(self.metrics),
            "logs_count": len(self.logs),
            "aggregated_metrics": self.get_aggregated_metrics(),
            "recent_traces": self.get_traces(limit=10),
            "recent_metrics": self.get_metrics(limit=10),
            "recent_logs": self.get_logs(limit=10)
        }
