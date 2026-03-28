"""
Visual Quick Reference Guide
"""

QUICK_REFERENCE = """
╔════════════════════════════════════════════════════════════════════╗
║        AUTONOMOUS RESEARCH AGENT - QUICK REFERENCE GUIDE          ║
╚════════════════════════════════════════════════════════════════════╝

┌─ INSTALLATION ────────────────────────────────────────────────────┐
│                                                                    │
│  1. Create Virtual Environment:                                   │
│     python -m venv venv                                           │
│     venv\\Scripts\\activate                                         │
│                                                                    │
│  2. Install Dependencies:                                         │
│     pip install -r requirements.txt                               │
│                                                                    │
│  3. Configure API Keys:                                           │
│     copy .env.example .env                                        │
│     # Edit .env with your OpenAI/Anthropic key                    │
│                                                                    │
│  4. Verify Setup:                                                 │
│     python setup.py                                               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ USAGE ────────────────────────────────────────────────────────────┐
│                                                                    │
│  Basic:                                                           │
│    python main.py                                                 │
│                                                                    │
│  Custom Topic:                                                    │
│    python main.py "AI in Healthcare"                              │
│                                                                    │
│  Run Demos:                                                       │
│    python demo.py                                                 │
│                                                                    │
│  Try Examples:                                                    │
│    python examples.py                                             │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ KEY FILES ────────────────────────────────────────────────────────┐
│                                                                    │
│  ENTRY POINTS:                                                    │
│  • main.py .......................... Command line interface       │
│  • demo.py .......................... Demo scenarios              │
│  • examples.py ...................... Usage examples              │
│                                                                    │
│  CORE:                                                            │
│  • agent.py ......................... Main ReAct agent            │
│  • advanced_agent.py ................ Advanced features           │
│  • tools.py ......................... Tool implementations        │
│  • config.py ........................ Configuration              │
│                                                                    │
│  DOCUMENTATION:                                                   │
│  • README.md ........................ Full guide                   │
│  • REQUIREMENTS.md .................. All requirements met         │
│  • DEPLOYMENT.md .................... Deploy to production        │
│  • PROJECT_SUMMARY.md ............... This project               │
│                                                                    │
│  TESTING:                                                         │
│  • test_agent.py .................... Unit tests                  │
│  • setup.py ......................... Validation                  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ AGENT WORKFLOW ──────────────────────────────────────────────────┐
│                                                                    │
│  THINK (Reasoning)                                                │
│    ↓                                                              │
│  Analyze topic and plan research strategy                         │
│    ↓                                                              │
│  ACT (Taking Actions)                                             │
│    ↓                                                              │
│  Execute tools:                                                   │
│    • search_web() → Get current information                       │
│    • search_wikipedia() → Get detailed background                 │
│    • query_knowledge() → Query knowledge base                     │
│    ↓                                                              │
│  OBSERVE (Analyzing)                                              │
│    ↓                                                              │
│  Analyze findings and extract insights                            │
│    ↓                                                              │
│  DECIDE (Continue or Stop)                                        │
│    ↓                                                              │
│  If sufficient info → Generate Report (EXIT)                      │
│  If need more → Go back to THINK (ITERATE)                        │
│    ↓                                                              │
│  REPORT (Output)                                                  │
│    ↓                                                              │
│  Generate formatted comprehensive report                          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ CONFIGURATION OPTIONS ────────────────────────────────────────────┐
│                                                                    │
│  LLM_PROVIDER = "openai" or "anthropic"                           │
│  MODEL_NAME = "gpt-4", "gpt-3.5-turbo", "claude-3-opus"          │
│  TEMPERATURE = 0.0 (focused) to 1.0 (creative)                   │
│  MAX_ITERATIONS = 5-15 (default: 15)                             │
│  MAX_TOKENS = 1000-4000 (default: 4000)                          │
│                                                                    │
│  In config.py or .env file                                       │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ TROUBLESHOOTING ──────────────────────────────────────────────────┐
│                                                                    │
│  Problem: "API key not found"                                     │
│  Solution: Check .env file has OPENAI_API_KEY or ANTHROPIC_API_KEY│
│                                                                    │
│  Problem: "ModuleNotFoundError"                                   │
│  Solution: pip install -r requirements.txt                        │
│                                                                    │
│  Problem: "Rate limit exceeded"                                   │
│  Solution: Wait a few minutes, increase MAX_ITERATIONS           │
│                                                                    │
│  Problem: "Connection error"                                      │
│  Solution: Check internet, verify API status                      │
│                                                                    │
│  Get help:                                                        │
│    python setup.py --trouble                                      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ OUTPUT FILES ─────────────────────────────────────────────────────┐
│                                                                    │
│  Reports are saved in reports/ folder:                            │
│                                                                    │
│  report_[topic]_[timestamp].txt                                   │
│    → Human-readable comprehensive report                          │
│                                                                    │
│  findings_[topic]_[timestamp].json                                │
│    → Structured findings data                                     │
│                                                                    │
│  View reports:                                                    │
│    type reports\\report_*.txt                                      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ QUICK EXAMPLES ──────────────────────────────────────────────────┐
│                                                                    │
│  1. Basic API Usage:                                              │
│     from agent import ResearchAgent                               │
│     agent = ResearchAgent()                                       │
│     result = agent.research("Your Topic")                         │
│     print(agent.generate_report(result))                          │
│                                                                    │
│  2. Advanced Features:                                            │
│     from advanced_agent import AdvancedResearchAgent              │
│     agent = AdvancedResearchAgent()                               │
│     result = agent.research("Topic", verbose=True)                │
│                                                                    │
│  3. Batch Research:                                               │
│     topics = ["AI", "ML", "DL"]                                   │
│     from examples import example_batch_research                   │
│     example_batch_research()                                      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ REQUIREMENTS MET ────────────────────────────────────────────────┐
│                                                                    │
│  ✅ Topic input (CLI + API)                                       │
│  ✅ Web search capability                                         │
│  ✅ Data analysis                                                 │
│  ✅ Key insight extraction                                        │
│  ✅ Content organization                                          │
│  ✅ Report generation                                             │
│  ✅ LangChain integration                                         │
│  ✅ Multi-LLM support                                             │
│  ✅ Web Search Tool                                               │
│  ✅ Knowledge Tool (Wikipedia)                                    │
│  ✅ ReAct Agent Implementation                                    │
│                                                                    │
│  BONUS:                                                           │
│  ✅ Third Tool (Knowledge Base)                                   │
│  ✅ Full Documentation                                            │
│  ✅ Test Suite                                                    │
│  ✅ Working Examples                                              │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

╔════════════════════════════════════════════════════════════════════╗
║                    READY TO START RESEARCHING!                    ║
║                                                                    ║
║  1. Get API key (https://platform.openai.com)                    ║
║  2. Add to .env file                                              ║
║  3. Run: python main.py "Your Topic"                              ║
║                                                                    ║
║  Documentation: README.md                                         ║
║  Quick Help: python setup.py                                      ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(QUICK_REFERENCE)
