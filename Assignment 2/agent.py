"""
Research Agent implementation using LangChain
"""
from typing import Any, List, Optional, Dict
from langchain_core.tools import tool, Tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
import json

from config import (
    LLM_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY, 
    MODEL_NAME, TEMPERATURE, MAX_TOKENS, MAX_ITERATIONS, SERPAPI_KEY
)
from tools import ResearchToolkit


class ResearchAgent:
    """Autonomous Research Agent using ReAct pattern"""
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.toolkit = ResearchToolkit(SERPAPI_KEY)
        self.tools = self.toolkit.get_tools()
        self.research_history = []
        self.findings = []
        self.iteration_count = 0
    
    def _initialize_llm(self):
        """Initialize the LLM based on configuration"""
        if LLM_PROVIDER == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                api_key=OPENAI_API_KEY,
                model=MODEL_NAME,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
        elif LLM_PROVIDER == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                api_key=ANTHROPIC_API_KEY,
                model=MODEL_NAME,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
        else:
            raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")
    
    def _build_agent_prompt(self) -> ChatPromptTemplate:
        """Build the ReAct prompt for the agent"""
        system_prompt = """You are an expert research agent tasked with thoroughly researching topics and generating comprehensive reports.

Your workflow:
1. THINK: Identify what information you need to find
2. ACT: Use available tools to search for information
3. OBSERVE: Analyze the results
4. REPEAT: Continue until you have enough information
5. CONCLUDE: Generate a comprehensive report

Available tools:
- search_web: Search the internet for current information
- search_wikipedia: Get detailed information from Wikipedia
- query_knowledge: Query your knowledge base

Instructions:
- Be thorough in your research
- Gather information from multiple angles and sources
- Organize findings into clear categories
- When you have sufficient information, generate a final report
- Format your response with clear sections and key insights

After gathering research, provide a structured report with:
- Executive Summary
- Key Findings
- Analysis
- Implications and Recommendations
- Sources"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            ("user", "{input}")
        ])
        
        return prompt
    
    def research(self, topic: str) -> Dict[str, Any]:
        """
        Conduct research on a topic
        
        Args:
            topic: The research topic
            
        Returns:
            Dictionary containing research findings and generated report
        """
        print(f"\n{'='*60}")
        print(f"Starting Research on: {topic}")
        print(f"{'='*60}\n")
        
        self.iteration_count = 0
        messages = []
        research_input = f"""Please conduct a comprehensive research on the following topic and generate a detailed report:

Topic: {topic}

Search for:
1. Key definitions and background
2. Current developments and recent news
3. Main issues and challenges
4. Opportunities and benefits
5. Future trends and predictions
6. Notable experts and organizations

Then provide a well-structured final report."""
        
        # Main research loop
        while self.iteration_count < MAX_ITERATIONS:
            self.iteration_count += 1
            print(f"\n--- Iteration {self.iteration_count} ---")
            
            # Prepare messages for LLM
            prompt = self._build_agent_prompt()
            
            # Invoke the LLM
            response = self.llm.invoke(
                prompt.format_messages(
                    messages=messages,
                    input=research_input if self.iteration_count == 1 else "Continue your research or provide the final report."
                )
            )
            
            assistant_message = response.content
            print(f"\nAgent Response:\n{assistant_message[:500]}...\n")
            
            messages.append(HumanMessage(content=research_input if self.iteration_count == 1 else "Continue research"))
            messages.append(AIMessage(content=assistant_message))
            
            # Check if agent wants to use tools
            if self._should_use_tools(assistant_message):
                tool_outputs = self._execute_tools(assistant_message)
                for tool_name, output in tool_outputs:
                    messages.append(ToolMessage(
                        content=output,
                        tool_call_id=tool_name
                    ))
                self.findings.append({
                    "iteration": self.iteration_count,
                    "tool": tool_name,
                    "output": output
                })
            else:
                # Agent finished research and generated report
                print("\n" + "="*60)
                print("RESEARCH COMPLETE")
                print("="*60 + "\n")
                
                return {
                    "topic": topic,
                    "report": assistant_message,
                    "findings": self.findings,
                    "iterations": self.iteration_count,
                    "status": "success"
                }
        
        # Max iterations reached
        return {
            "topic": topic,
            "report": assistant_message,
            "findings": self.findings,
            "iterations": self.iteration_count,
            "status": "max_iterations_reached"
        }
    
    def _should_use_tools(self, response: str) -> bool:
        """Determine if the agent should use tools based on response"""
        tool_indicators = ["search", "find", "research", "investigate", "look", "check", "query"]
        response_lower = response.lower()
        return any(indicator in response_lower for indicator in tool_indicators)
    
    def _extract_search_queries(self, response: str) -> List[str]:
        """Extract search queries from agent's response"""
        import re
        
        # Look for patterns like "search for [query]" or "search [query]"
        patterns = [
            r"search(?:\s+(?:for|about))?\s+['\"]?([^'\".\n]+)['\"]?",
            r"look\s+up\s+['\"]?([^'\".\n]+)['\"]?",
            r"search:\s*['\"]?([^'\".\n]+)['\"]?",
            r"query:\s*['\"]?([^'\".\n]+)['\"]?"
        ]
        
        queries = []
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            queries.extend(matches)
        
        return queries[:3]  # Limit to 3 searches per iteration
    
    def _execute_tools(self, agent_response: str) -> List[tuple]:
        """Execute tools based on agent's response"""
        results = []
        queries = self._extract_search_queries(agent_response)
        
        if not queries:
            # If no specific queries found, extract topic from agent's intent
            queries = self._infer_queries(agent_response)
        
        for query in queries:
            # Try different tools
            if "wikipedia" in agent_response.lower():
                print(f"  Executing: search_wikipedia('{query}')")
                result = self.toolkit.wikipedia(query)
                results.append(("search_wikipedia", result if result else f"No results for '{query}'"))
            else:
                print(f"  Executing: search_web('{query}')")
                result = self.toolkit.web_search(query)
                results.append(("search_web", result if result else f"No results for '{query}'"))
        
        return results
    
    def _infer_queries(self, response: str) -> List[str]:
        """Infer search queries from agent's general response"""
        # Extract noun phrases that might be search queries
        import re
        
        # Simple heuristic: look for capitalized phrases
        phrases = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', response)
        return phrases[:3]
    
    def generate_report(self, research_result: Dict[str, Any]) -> str:
        """Format and return the final report"""
        report = research_result["report"]
        
        formatted_report = f"""
{'='*70}
RESEARCH REPORT: {research_result['topic'].upper()}
{'='*70}

{report}

{'='*70}
Research Metadata:
- Iterations Completed: {research_result['iterations']}
- Total Findings: {len(research_result['findings'])}
- Status: {research_result['status']}
{'='*70}
"""
        return formatted_report
