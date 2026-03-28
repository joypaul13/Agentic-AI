# Assignment 2: Autonomous Research Agent - Implementation Requirements

## Objective
Build an AI Agent that can automatically research a topic and generate a structured report.

## Requirements Checklist

### ✅ 1. Take a Topic as Input
**Requirement**: Accept a research topic as input
- **Example**: "Impact of AI in Healthcare"

**Implementation**:
- ✓ Command-line interface in `main.py`: `python main.py "Your Topic"`
- ✓ Interactive input if no argument provided
- ✓ Direct API in `agent.py` and `advanced_agent.py`

**Usage Examples**:
```bash
# Method 1: Command line argument
python main.py "Impact of AI in Healthcare"

# Method 2: Interactive prompt
python main.py
# Then enter topic when prompted

# Method 3: Python API
from agent import ResearchAgent
agent = ResearchAgent()
result = agent.research("Your Topic")
```

---

### ✅ 2. Agent Capabilities
**Requirements**:
- ✓ Search relevant information
- ✓ Extract key insights  
- ✓ Organize content
- ✓ Generate final report

**Implementation Details**:

#### 2.1 Search Information (`tools.py`)
```python
# Web Search Tool
search_web(query: str) -> List[dict]
- Searches internet for current information
- Returns titles, links, snippets
- Supports SerpAPI for enhanced results

# Wikipedia Tool  
search_wikipedia(topic: str) -> str
- Retrieves detailed information
- Handles disambiguation
- Provides comprehensive summaries
```

#### 2.2 Extract & Analyze (`agent.py`)
```python
ResearchAgent.research(topic: str)
- Iteratively queries tools
- Analyzes responses
- Identifies key insights
- Tracks findings across iterations
```

#### 2.3 Organize Content
```python
ResearchAgent.generate_report()
- Organizes findings by category
- Creates structured sections:
  * Executive Summary
  * Key Findings
  * Analysis
  * Implications
  * Sources
```

#### 2.4 Generate Report
```python
# Final report includes:
- Research topic
- Comprehensive findings
- Analysis and insights
- Metadata (iterations, tools used)
- Source information
```

---

### ✅ 3. Technology Stack

#### 3.1 LangChain ✓
**Files**: `agent.py`, `advanced_agent.py`
```python
# Tool Integration
from langchain_core.tools import tool
@tool
def search_web(query: str) -> str: ...

# Prompt Templates
from langchain_core.prompts import ChatPromptTemplate

# Message Handling
from langchain_core.messages import (
    HumanMessage, AIMessage, ToolMessage
)

# Agent Framework
from langchain.agents import initialize_agent, AgentType
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    max_iterations=15
)
```

#### 3.2 LLM Integration ✓
**Files**: `config.py`, `agent.py`

**OpenAI Support**:
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4",
    temperature=0.7,
    max_tokens=4000
)
```

**Anthropic Support**:
```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(
    api_key=ANTHROPIC_API_KEY,
    model="claude-3-opus",
    temperature=0.7,
    max_tokens=4000
)
```

---

### ✅ 4. Required Tools (2+)

#### 4.1 Web Search Tool ✓
**File**: `tools.py` → `WebSearchTool`
```python
class WebSearchTool:
    - search(query, num_results=5) -> List[dict]
    - _serpapi_search(query, num_results)
    - _simple_search(query, num_results)
    - Callable interface: tool(query)
```

**Capabilities**:
- Multi-result retrieval
- SerpAPI integration (optional)
- Wikipedia fallback
- Formatted output

**Used For**:
- Finding current information
- Latest news and developments
- Diverse perspectives
- Recent statistics

#### 4.2 Wikipedia/Knowledge Tool ✓
**File**: `tools.py` → `WikipediaTool`
```python
class WikipediaTool:
    - search(topic, sentences) -> str
    - get_related_topics(topic) -> List[str]
    - Handle disambiguation
    - Callable interface: tool(topic)
```

**Capabilities**:
- Comprehensive summaries
- Related topic discovery
- Disambiguation handling
- Structured information

**Used For**:
- Background information
- Detailed explanations
- Historical context
- Definitions and concepts

#### 4.3 Bonus Tool ✓
**File**: `tools.py` → `KnowledgeBaseTool`
```python
class KnowledgeBaseTool:
    - add_knowledge(key, value)
    - query(query) -> str
    - Extensible knowledge base
    - Callable interface: tool(query)
```

---

### ✅ 5. Agent Implementation (ReAct Pattern)

**File**: `agent.py` → `ResearchAgent`

#### Workflow Implementation:

```python
# ============================================
# THINK Phase
# ============================================
- Agent analyzes research topic
- Identifies information needs
- Plans search strategy
- Determines relevant queries

# ============================================
# ACT Phase (Execute Tools)
# ============================================
- search_web(topic)
- search_wikipedia(topic)
- query_knowledge(topic)
- Multiple tool calls per iteration

# ============================================
# OBSERVE Phase
# ============================================
- Analyzes tool outputs
- Extracts key information
- Evaluates relevance
- Identifies gaps

# ============================================
# DECIDE Phase
# ============================================
- If information sufficient:
    → Generate report (EXIT)
- If gaps remain:
    → Continue research (ITERATE)
- Max iterations: 15

# ============================================
# REPORT Phase
# ============================================
- Synthesize findings
- Organize by category
- Generate structured report
```

#### ReAct Implementation Details:

**Reasoning**: 
```python
_build_agent_prompt() -> ChatPromptTemplate
- System prompt guides ReAct workflow
- Clear instructions for THINK-ACT-OBSERVE
- Examples of tool usage
- Expected output format
```

**Acting**:
```python
_execute_tools(agent_response) -> List[tuple]
- Extracts search queries from response
- Executes appropriate tools
- Collects results
- Returns (tool_name, output) pairs
```

**Iteration**:
```python
research(topic) -> Dict
- Main loop: while iterations < MAX_ITERATIONS
- For each iteration:
  1. Send prompt to LLM
  2. Parse response
  3. Execute tools if needed
  4. Add findings to history
  5. Continue or finish
```

---

## File Structure

```
assignment 2/
├── main.py                 # Entry point (CLI)
├── agent.py               # Core ResearchAgent (ReAct)
├── advanced_agent.py      # Advanced implementation
├── tools.py               # Tool implementations
├── config.py              # Configuration
├── setup.py               # Setup & validation
├── test_agent.py          # Unit & integration tests
├── demo.py                # Demo scenarios
├── requirements.txt       # Dependencies
├── .env.example           # Configuration template
├── README.md              # Documentation
└── REQUIREMENTS.md        # This file
```

---

## How to Run

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
copy .env.example .env
# Edit .env with your API keys

# Verify setup
python setup.py
```

### 2. Run Research
```bash
# Default topic
python main.py

# Custom topic  
python main.py "Your Research Topic"

# Advanced implementation
python advanced_agent.py
```

### 3. View Results
```bash
# Reports saved in reports/ folder
# - report_*.txt (human-readable)
# - findings_*.json (structured data)
```

---

## Key Features

### 1. Iterative Research ✓
- Multiple research iterations (default: 15)
- Evaluates when to stop vs. continue
- Adjusts queries based on findings

### 2. Tool Integration ✓
- Automatic tool selection
- Query extraction from responses
- Result tracking

### 3. Flexible LLM Support ✓
- OpenAI (GPT-4, GPT-3.5-turbo)
- Anthropic (Claude 3 models)
- Easy switching via config

### 4. Structured Output ✓
- Organized reports
- Key findings extraction
- Metadata tracking
- JSON export

### 5. Error Handling ✓
- Graceful fallbacks
- Configuration validation
- Tool error recovery
- Clear error messages

---

## Testing

### Run Tests
```bash
# All tests
python test_agent.py

# Quick validation
python test_agent.py --quick
```

### Test Coverage
- ✓ Tool initialization
- ✓ Tool functionality
- ✓ Agent workflow
- ✓ Configuration
- ✓ Integration tests
- ✓ Mock scenarios

---

## Example Output

```
Research Report: Impact of AI in Healthcare
============================================================

EXECUTIVE SUMMARY
- AI is transforming healthcare delivery...
- Machine learning improving diagnostics...
- Automation reducing costs...

KEY FINDINGS
1. Diagnostic Accuracy
   - ML models achieving 95%+ accuracy
   - Faster detection of diseases
   - Reduced human error

2. Operational Efficiency
   - Automating routine tasks
   - Reducing administrative burden
   - Improving resource allocation

3. Challenges & Concerns
   - Data privacy issues
   - Regulatory compliance
   - Need for explainability

IMPLICATIONS & RECOMMENDATIONS
- Continue investment in AI research
- Establish ethical guidelines
- Train healthcare professionals
- Ensure data security

Research Metadata
- Iterations: 8
- Tools used: 3
- Sources consulted: 12
- Status: Success
```

---

## Compliance Summary

| Requirement | Implementation | Status |
|------------|-----------------|--------|
| Input topic | main.py, agent.py | ✅ |
| Search information | WebSearchTool | ✅ |
| Analyze data | ResearchAgent logic | ✅ |
| Extract insights | Finding tracking | ✅ |
| Organize content | Report generation | ✅ |
| Generate report | generate_report() | ✅ |
| Use LangChain | agent.py, advanced_agent.py | ✅ |
| LLM support | OpenAI & Anthropic | ✅ |
| Web search tool | WebSearchTool | ✅ |
| Knowledge tool | WikipediaTool | ✅ |
| ReAct agent | ResearchAgent full impl. | ✅ |
| 2+ tools | 3 tools (web, wiki, kb) | ✅ |

---

## Assignment Completed ✅

All requirements have been implemented and tested:
- ✓ Autonomous research agent built
- ✓ Web search capability
- ✓ Knowledge base integration (Wikipedia)
- ✓ LangChain framework used
- ✓ Multiple LLM support
- ✓ ReAct pattern implemented
- ✓ Structured report generation
- ✓ Full documentation
- ✓ Test suite included
