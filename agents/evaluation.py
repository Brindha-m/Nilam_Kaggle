"""
Agent Evaluation Framework
Evaluates agent performance and quality
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging
from dataclasses import dataclass, asdict


@dataclass
class EvaluationResult:
    """Result of agent evaluation"""
    agent_id: str
    evaluation_type: str
    score: float
    timestamp: datetime
    details: Dict[str, Any] = None
    
    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "evaluation_type": self.evaluation_type,
            "score": self.score,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details or {}
        }


class AgentEvaluator:
    """
    Evaluates agent performance using various metrics
    """
    
    def __init__(self):
        self.evaluations: List[EvaluationResult] = []
        self.logger = logging.getLogger("evaluator")
    
    def evaluate_response_quality(
        self,
        agent_id: str,
        user_query: str,
        agent_response: str,
        expected_keywords: Optional[List[str]] = None
    ) -> EvaluationResult:
        """
        Evaluate response quality based on:
        - Relevance to query
        - Completeness
        - Presence of expected keywords
        """
        score = 0.0
        details = {}
        
        # Check relevance (simple keyword matching)
        query_lower = user_query.lower()
        response_lower = agent_response.lower()
        
        query_words = set(query_lower.split())
        response_words = set(response_lower.split())
        
        overlap = len(query_words.intersection(response_words))
        relevance_score = min(overlap / len(query_words) if query_words else 0, 1.0)
        score += relevance_score * 0.4
        details["relevance_score"] = relevance_score
        
        # Check completeness (response length)
        completeness_score = min(len(agent_response) / 200, 1.0)  # Normalize to 200 chars
        score += completeness_score * 0.3
        details["completeness_score"] = completeness_score
        
        # Check expected keywords
        if expected_keywords:
            found_keywords = [kw for kw in expected_keywords if kw.lower() in response_lower]
            keyword_score = len(found_keywords) / len(expected_keywords) if expected_keywords else 0
            score += keyword_score * 0.3
            details["keyword_score"] = keyword_score
            details["found_keywords"] = found_keywords
        else:
            details["keyword_score"] = 0.5  # Neutral if no keywords specified
        
        result = EvaluationResult(
            agent_id=agent_id,
            evaluation_type="response_quality",
            score=min(score, 1.0),
            timestamp=datetime.now(),
            details=details
        )
        
        self.evaluations.append(result)
        return result
    
    def evaluate_tool_usage(
        self,
        agent_id: str,
        tools_used: List[str],
        expected_tools: Optional[List[str]] = None
    ) -> EvaluationResult:
        """Evaluate tool usage effectiveness"""
        score = 0.0
        details = {}
        
        # Check if tools were used
        if tools_used:
            score += 0.5
            details["tools_used"] = tools_used
            details["tool_count"] = len(tools_used)
        else:
            details["tools_used"] = []
            details["tool_count"] = 0
        
        # Check if expected tools were used
        if expected_tools:
            used_expected = [t for t in expected_tools if t in tools_used]
            tool_match_score = len(used_expected) / len(expected_tools)
            score += tool_match_score * 0.5
            details["expected_tools"] = expected_tools
            details["used_expected"] = used_expected
            details["tool_match_score"] = tool_match_score
        
        result = EvaluationResult(
            agent_id=agent_id,
            evaluation_type="tool_usage",
            score=min(score, 1.0),
            timestamp=datetime.now(),
            details=details
        )
        
        self.evaluations.append(result)
        return result
    
    def evaluate_performance(
        self,
        agent_id: str,
        response_time_ms: float,
        success: bool,
        error_count: int = 0
    ) -> EvaluationResult:
        """Evaluate performance metrics"""
        score = 0.0
        details = {}
        
        # Success rate
        if success:
            score += 0.6
            details["success"] = True
        else:
            details["success"] = False
        
        # Response time (faster is better, normalized to 5 seconds)
        time_score = max(0, 1.0 - (response_time_ms / 5000))
        score += time_score * 0.3
        details["response_time_ms"] = response_time_ms
        details["time_score"] = time_score
        
        # Error count (fewer is better)
        error_score = max(0, 1.0 - (error_count / 10))
        score += error_score * 0.1
        details["error_count"] = error_count
        details["error_score"] = error_score
        
        result = EvaluationResult(
            agent_id=agent_id,
            evaluation_type="performance",
            score=min(score, 1.0),
            timestamp=datetime.now(),
            details=details
        )
        
        self.evaluations.append(result)
        return result
    
    def evaluate_agent(
        self,
        agent_id: str,
        user_query: str,
        agent_response: str,
        response_time_ms: float,
        success: bool,
        tools_used: List[str] = None,
        expected_keywords: List[str] = None
    ) -> Dict[str, EvaluationResult]:
        """Comprehensive agent evaluation"""
        results = {}
        
        # Response quality
        results["quality"] = self.evaluate_response_quality(
            agent_id, user_query, agent_response, expected_keywords
        )
        
        # Tool usage
        results["tool_usage"] = self.evaluate_tool_usage(
            agent_id, tools_used or [], expected_keywords
        )
        
        # Performance
        results["performance"] = self.evaluate_performance(
            agent_id, response_time_ms, success
        )
        
        # Overall score (weighted average)
        overall_score = (
            results["quality"].score * 0.5 +
            results["tool_usage"].score * 0.2 +
            results["performance"].score * 0.3
        )
        
        results["overall"] = EvaluationResult(
            agent_id=agent_id,
            evaluation_type="overall",
            score=overall_score,
            timestamp=datetime.now(),
            details={
                "quality_score": results["quality"].score,
                "tool_usage_score": results["tool_usage"].score,
                "performance_score": results["performance"].score
            }
        )
        
        self.evaluations.append(results["overall"])
        
        return results
    
    def get_evaluation_history(
        self,
        agent_id: Optional[str] = None,
        evaluation_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get evaluation history with optional filtering"""
        filtered = self.evaluations
        
        if agent_id:
            filtered = [e for e in filtered if e.agent_id == agent_id]
        
        if evaluation_type:
            filtered = [e for e in filtered if e.evaluation_type == evaluation_type]
        
        return [e.to_dict() for e in filtered[-limit:]]
    
    def get_agent_scores(self, agent_id: str) -> Dict[str, float]:
        """Get average scores for an agent"""
        agent_evals = [e for e in self.evaluations if e.agent_id == agent_id]
        
        if not agent_evals:
            return {}
        
        scores_by_type = {}
        for eval_type in ["response_quality", "tool_usage", "performance", "overall"]:
            type_evals = [e for e in agent_evals if e.evaluation_type == eval_type]
            if type_evals:
                scores_by_type[eval_type] = sum(e.score for e in type_evals) / len(type_evals)
        
        return scores_by_type
    
    def export_evaluations(self, filepath: str):
        """Export evaluations to JSON file"""
        with open(filepath, 'w') as f:
            json.dump([e.to_dict() for e in self.evaluations], f, indent=2)
