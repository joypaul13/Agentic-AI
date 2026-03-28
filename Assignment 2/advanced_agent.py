"""
Advanced Research Agent with improved ReAct implementation and error handling
"""
from typing import Any, List, Optional, Dict, Tuple
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool as LangChainTool
from langchain_core.callbacks import CallbackManager, BaseCallbackHandler
import json
from datetime import datetime

from config import (
    LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY,
    MODEL_NAME, TEMPERATURE, MAX_TOKENS, MAX_ITERATIONS, SERPAPI_KEY
)
from tools import ResearchToolkit


class ResearchLogger(BaseCallbackHandler):
    """Custom callback handler to log agent actions"""
    
    def __init__(self):
        self.logs = []
    
    def on_llm_start(self, serialized: Dict, prompts: List[str], **kwargs):
        self.logs.append({
            "type": "llm_start",
            "timestamp": datetime.now().isoformat()
        })
    
    def on_tool_start(self, serialized: Dict, input_str: str, **kwargs):
        self.logs.append({
            "type": "tool_start",
            "tool": serialized.get("name"),
            "input": input_str,
            "timestamp": datetime.now().isoformat()
        })
    
    def on_tool_end(self, output: str, **kwargs):
        self.logs.append({
            "type": "tool_end",
            "output_length": len(output),
            "timestamp": datetime.now().isoformat()
        })


class AdvancedResearchAgent:
    """Advanced Research Agent with better tool integration"""
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.toolkit = ResearchToolkit(SERPAPI_KEY)
        self.agent = None
        self.logger = ResearchLogger()
        self.research_findings = []
    
    def _initialize_llm(self):
        """Initialize the LLM with callbacks"""
        if LLM_PROVIDER == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model=MODEL_NAME,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                callbacks=CallbackManager([self.logger])
            )
        elif LLM_PROVIDER == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                api_key=ANTHROPIC_API_KEY,
                model=MODEL_NAME,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                callbacks=CallbackManager([self.logger])
            )
        else:
            raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")
    
    def _create_tools(self) -> List[LangChainTool]:
        """Create LangChain tools for the agent"""
        
        @tool
        def search_web(query: str) -> str:
            """Search the web for information"""
            return self.toolkit.web_search(query)
        
        @tool
        def search_wikipedia(topic: str) -> str:
            """Search Wikipedia for information"""
            return self.toolkit.wikipedia(topic)
        
        @tool
        def get_related_topics(topic: str) -> str:
            """Get topics related to the search term"""
            related = self.toolkit.wikipedia.get_related_topics(topic)
            return f"Related topics: {', '.join(related[:5])}"
        
        return [search_web, search_wikipedia, get_related_topics]
    
    def research(self, topic: str, verbose: bool = True) -> Dict[str, Any]:
        """
        Conduct research using LangChain agent framework
        
        Args:
            topic: Research topic
            verbose: Print agent actions
            
        Returns:
            Research results dictionary
        """
        try:
            from langchain.agents import initialize_agent, AgentType
        except ImportError:
            print("Using standard research implementation...")
            return self._fallback_research(topic)
        
        print(f"\n{'='*60}")
        print(f"Advanced Research on: {topic}")
        print(f"{'='*60}\n")
        
        try:
            tools = self._create_tools()
            
            # Initialize agent
            self.agent = initialize_agent(
                tools=tools,
                llm=self.llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=verbose,
                max_iterations=MAX_ITERATIONS,
                handle_parsing_errors=True,
                early_stopping_method="generate"
            )
            
            # Run agent
            research_query = f"""Conduct a thorough research on: {topic}
            
Please:
1. Search for key information using web_search
2. Get detailed information using search_wikipedia
3. Find related topics using get_related_topics
4. Synthesize all findings into a comprehensive summary

Provide your findings organized by topic with clear insights."""
            
            result = self.agent.invoke({"input": research_query})
            
            final_report = result.get("output", result)
            
            return {
                "topic": topic,
                "report": final_report,
                "findings": self.research_findings,
                "logs": self.logger.logs,
                "status": "success"
            }
        
        except Exception as e:
            print(f"Advanced agent error: {e}")
            print("Falling back to standard implementation...\n")
            return self._fallback_research(topic)
    
    def _fallback_research(self, topic: str) -> Dict[str, Any]:
        """Fallback implementation using direct LLM calls"""
        from agent import ResearchAgent
        
        basic_agent = ResearchAgent()
        return basic_agent.research(topic)
    
    def generate_detailed_report(self, research_result: Dict[str, Any]) -> str:
        """Generate a detailed formatted report"""
        
        report = f"""
{'='*70}
COMPREHENSIVE RESEARCH REPORT
{'='*70}

TOPIC: {research_result['topic'].upper()}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*70}
MAIN FINDINGS
{'='*70}

{research_result['report']}

{'='*70}
RESEARCH METADATA
{'='*70}

Processing Information:
  - Total API Calls: {len(research_result['logs'])}
  - Research Status: {research_result['status']}
  - Timestamp: {datetime.now().isoformat()}

Tool Usage:
"""
        
        # Count tool usages
        tool_counts = {}
        for log in research_result['logs']:
            if log.get('type') == 'tool_start':
                tool_name = log.get('tool')
                tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
        
        for tool_name, count in tool_counts.items():
            report += f"\n  - {tool_name}: {count} calls"
        
        report += f"\n\n{'='*70}\n"
        
        return report


class InteractiveResearchSession:
    """Interactive session for conducting multiple research tasks"""
    
    def __init__(self):
        self.agent = AdvancedResearchAgent()
        self.history = []
    
    def research(self, topic: str) -> Dict[str, Any]:
        """Conduct research and add to history"""
        result = self.agent.research(topic)
        self.history.append({
            "topic": topic,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        return result
    
    def get_history(self) -> List[Dict]:
        """Get research history"""
        return self.history
    
    def compare_topics(self, topics: List[str]) -> Dict[str, Any]:
        """Research multiple topics and compare findings"""
        results = {}
        for topic in topics:
            print(f"\nResearching: {topic}")
            results[topic] = self.research(topic)
        
        return {
            "comparison_topics": topics,
            "results": results,
            "total_searches": sum(1 for r in results.values() for _ in r.get('findings', [])),
            "timestamp": datetime.now().isoformat()
        }
    
    def export_session(self, filename: str = None) -> str:
        """Export entire session to JSON"""
        if filename is None:
            filename = f"research_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        session_data = {
            "session_timestamp": datetime.now().isoformat(),
            "total_research_tasks": len(self.history),
            "research_history": self.history
        }
        
        with open(f"reports/{filename}", "w") as f:
            json.dump(session_data, f, indent=2, default=str)
        
        print(f"Session exported to: reports/{filename}")
        return f"reports/{filename}"


if __name__ == "__main__":
    # Example usage
    agent = AdvancedResearchAgent()
    result = agent.research("Quantum Computing Applications")
    report = agent.generate_detailed_report(result)
    print(report)
