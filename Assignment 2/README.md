# Autonomous Research Agent - LangChain

An intelligent AI-powered research agent that automatically searches the web, analyzes data, and generates comprehensive reports on any topic using LangChain's ReAct (Reasoning + Acting) pattern.

## Features

✅ **Autonomous Research** - Automatically searches and gathers information without user intervention
✅ **Multiple Tools** - Web search and Wikipedia integration for comprehensive data collection
✅ **ReAct Agent Pattern** - Implements reasoning and action loops for intelligent research
✅ **Flexible LLM Support** - Works with OpenAI (GPT-4) or Anthropic (Claude) models
✅ **Structured Reports** - Generates well-organized reports with key findings and analysis
✅ **Iterative Research** - Conducts multiple research iterations to ensure comprehensive coverage

## Project Structure

```
assignment 2/
├── main.py              # Entry point and orchestration
├── agent.py             # Research agent implementation (ReAct pattern)
├── tools.py             # Tool implementations (Web Search, Wikipedia, Knowledge Base)
├── config.py            # Configuration and environment variables
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── reports/             # Generated research reports (auto-created)
```

## Requirements

- Python 3.8+
- LangChain 0.1.0+
- OpenAI API Key OR Anthropic API Key
- (Optional) SerpAPI Key for enhanced web search

## Installation

### 1. Clone/Setup the Project

```bash
cd "e:\6 semester\agentic AI\assignment 2"
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project directory:

```env
# LLM Configuration (choose one)
LLM_PROVIDER=openai
# LLM_PROVIDER=anthropic

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4

# OR Anthropic Configuration
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# MODEL_NAME=claude-3-opus-20240229

# Optional: For enhanced web search
SERPAPI_KEY=your_serpapi_key_here
```

## Getting API Keys

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and add to `.env`

### Anthropic API Key
1. Go to [Anthropic Console](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and add to `.env`

### SerpAPI Key (Optional)
1. Go to [SerpAPI](https://serpapi.com)
2. Sign up for free
3. Get your API key from dashboard
4. Add to `.env` for enhanced web search

## Usage

### Basic Usage

```bash
# Default topic (Impact of AI in Healthcare)
python main.py

# Search a specific topic
python main.py "Impact of AI in Healthcare"

# Multi-word topic
python main.py "Climate Change and Global Warming"
```

### Example 1: AI in Healthcare

```bash
python main.py "Impact of AI in Healthcare"
```

Expected output:
- Searches for AI applications in healthcare
- Gathers information on machine learning in diagnostics
- Analyzes benefits and challenges
- Generates comprehensive report with key findings

### Example 2: Climate Change

```bash
python main.py "Climate Change Effects on Ocean Ecosystems"
```

### Example 3: Technology Trends

```bash
python main.py "Quantum Computing Future"
```

## How It Works

### Agent Workflow (ReAct Pattern)

1. **THINK** 🤔
   - Agent analyzes the research topic
   - Identifies information gaps
   - Plans search strategy

2. **ACT** 🔍
   - Executes web searches
   - Queries Wikipedia for details
   - Retrieves information from knowledge base

3. **OBSERVE** 📊
   - Analyzes collected information
   - Identifies key insights
   - Evaluates data quality

4. **ITERATE** 🔄
   - Continues research if more information needed
   - Refines search queries
   - Gathers additional perspectives

5. **REPORT** 📋
   - Synthesizes findings
   - Generates structured report
   - Provides recommendations

## Available Tools

### 1. Web Search Tool (`search_web`)
- Searches the internet for current information
- Uses SerpAPI for enhanced results (if configured)
- Returns links, titles, and snippets
- Best for: Recent news, current developments, latest trends

### 2. Wikipedia Tool (`search_wikipedia`)
- Retrieves detailed information from Wikipedia
- Handles disambiguation automatically
- Provides comprehensive summaries
- Best for: Background information, definitions, historical context

### 3. Knowledge Base Tool (`query_knowledge`)
- Queries structured knowledge base
- Extensible for custom knowledge
- Best for: Specific facts, structured information

## Report Output

Generated reports include:

```
RESEARCH REPORT: [TOPIC]
═══════════════════════════

Executive Summary
- Brief overview of the topic
- Key takeaways

Key Findings
- Main insights discovered
- Important facts and statistics

Analysis
- Deep dive into findings
- Context and implications

Implications and Recommendations
- Future trends
- Actionable insights
- Suggested next steps

Sources
- Referenced sources
- Tools used

Research Metadata
- Number of iterations
- Sources consulted
- Processing time
```

Reports are saved in the `reports/` folder with:
- `.txt` file: Human-readable report
- `.json` file: Structured findings data

## Configuration Options

Edit `config.py` to customize:

```python
# LLM Settings
LLM_PROVIDER = "openai"  # or "anthropic"
MODEL_NAME = "gpt-4"
TEMPERATURE = 0.7        # 0.0-1.0 (lower = more focused)
MAX_TOKENS = 4000        # Maximum response length

# Agent Settings
MAX_ITERATIONS = 15      # Maximum research iterations
TIMEOUT = 60             # Request timeout in seconds

# Report Settings
REPORT_LENGTH = "detailed"  # "brief", "medium", "detailed"
```

## Advanced Usage

### Custom Research Script

```python
from agent import ResearchAgent

# Initialize agent
agent = ResearchAgent()

# Research a topic
result = agent.research("Your Topic Here")

# Get formatted report
report = agent.generate_report(result)
print(report)

# Access raw findings
for finding in result['findings']:
    print(f"Tool: {finding['tool']}")
    print(f"Output: {finding['output']}")
```

### Batch Research

```python
topics = [
    "AI in Healthcare",
    "Quantum Computing",
    "Climate Change"
]

agent = ResearchAgent()
for topic in topics:
    result = agent.research(topic)
    report = agent.generate_report(result)
    # Save or process report
```

## Troubleshooting

### Issue: "API key not found"
**Solution**: Ensure `.env` file exists and contains valid API keys

### Issue: "No results found"
**Solution**: 
- Check internet connectivity
- Try a different search term
- Verify SerpAPI key (if using)

### Issue: "Max iterations reached"
**Solution**: 
- Increase `MAX_ITERATIONS` in `config.py`
- The agent needs more time for complex topics

### Issue: Rate limit error
**Solution**: 
- Wait before running next search
- Reduce `MAX_ITERATIONS`
- Check API rate limits

## Project Architecture

```
ResearchAgent (Main Agent)
├── LLM (OpenAI/Anthropic)
├── Tools
│   ├── WebSearchTool
│   ├── WikipediaTool
│   └── KnowledgeBaseTool
└── ReAct Loop
    ├── Think Phase
    ├── Act Phase (Execute Tools)
    ├── Observe Phase
    └── Iterate/Report
```

## Performance Tips

1. **Reduce MAX_ITERATIONS** for faster results
2. **Use specific topic names** for better results
3. **Configure SERPAPI_KEY** for better web search
4. **Use gpt-4** for better reasoning (if available)
5. **Run during off-peak hours** for API calls

## Limitations

- Requires active internet connection
- Depends on LLM API availability
- Wikipedia/web search quality varies by topic
- Some topics may require multiple iterations
- API costs apply to LLM usage

## Future Enhancements

🚀 Planned features:
- PDF extraction and analysis
- Academic paper search integration
- Real-time news feed integration
- Custom data source support
- Multi-language research support
- Visualization of research findings
- Collaborative research with multiple agents

## License

MIT License - Free to use and modify

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Verify API keys and configuration
4. Check internet connectivity

## Requirements Summary

- **Python**: 3.8+
- **RAM**: 4GB minimum
- **Internet**: Required for web search
- **APIs**: OpenAI or Anthropic (required)
- **Optional**: SerpAPI for enhanced search

---

**Happy Researching! 🔍📚**
