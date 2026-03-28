"""
Examples of using the Research Agent in various scenarios
"""

# ============================================================
# EXAMPLE 1: Basic Research on a Topic
# ============================================================

def example_basic_research():
    """Simple research on a single topic"""
    from agent import ResearchAgent
    
    agent = ResearchAgent()
    result = agent.research("Impact of Artificial Intelligence in Healthcare")
    report = agent.generate_report(result)
    
    print(report)


# ============================================================
# EXAMPLE 2: Research with Custom Configuration
# ============================================================

def example_custom_config():
    """Research with custom settings"""
    import os
    os.environ['LLM_PROVIDER'] = 'anthropic'
    os.environ['TEMPERATURE'] = '0.5'
    os.environ['MAX_ITERATIONS'] = '20'
    
    from agent import ResearchAgent
    from importlib import reload
    import config
    reload(config)
    
    agent = ResearchAgent()
    result = agent.research("Quantum Computing Future")


# ============================================================
# EXAMPLE 3: Advanced Agent with Tool Tracking
# ============================================================

def example_advanced_agent():
    """Use advanced agent with detailed tracking"""
    from advanced_agent import AdvancedResearchAgent
    
    agent = AdvancedResearchAgent()
    result = agent.research("Renewable Energy Technologies", verbose=True)
    report = agent.generate_detailed_report(result)
    
    print(report)


# ============================================================
# EXAMPLE 4: Interactive Session
# ============================================================

def example_interactive_session():
    """Conduct multiple research tasks in a session"""
    from advanced_agent import InteractiveResearchSession
    
    session = InteractiveResearchSession()
    
    # Research multiple topics
    topics = [
        "Machine Learning in Finance",
        "Blockchain Technology",
        "5G Networks"
    ]
    
    print("Starting interactive research session...")
    for topic in topics:
        print(f"\nResearching: {topic}")
        result = session.research(topic)
        print(f"✓ Completed in {result['status']}")
    
    # Export entire session
    session.export_session("my_research_session.json")


# ============================================================
# EXAMPLE 5: Batch Research with Reports
# ============================================================

def example_batch_research():
    """Research multiple topics and save reports"""
    from agent import ResearchAgent
    import json
    from datetime import datetime
    
    topics = [
        "AI in Education",
        "Cybersecurity Threats",
        "Climate Change Solutions"
    ]
    
    agent = ResearchAgent()
    all_results = {}
    
    for topic in topics:
        print(f"Researching: {topic}...")
        result = agent.research(topic)
        all_results[topic] = {
            "report": result['report'],
            "findings_count": len(result['findings']),
            "iterations": result['iterations']
        }
        print(f"✓ Completed")
    
    # Save batch results
    with open("reports/batch_results.json", "w") as f:
        json.dump(all_results, f, indent=2)


# ============================================================
# EXAMPLE 6: Research with Custom Knowledge Base
# ============================================================

def example_custom_knowledge():
    """Add custom knowledge before research"""
    from agent import ResearchAgent
    
    agent = ResearchAgent()
    
    # Add domain-specific knowledge
    agent.toolkit.knowledge_base.add_knowledge(
        "AI in Healthcare",
        "Key applications include diagnostic imaging, drug discovery, and patient monitoring"
    )
    agent.toolkit.knowledge_base.add_knowledge(
        "ML challenges",
        "Common challenges: data quality, interpretability, scalability, and bias"
    )
    
    # Research will use this knowledge
    result = agent.research("AI in Healthcare")


# ============================================================
# EXAMPLE 7: Extract and Analyze Findings
# ============================================================

def example_analyze_findings():
    """Deep analysis of research findings"""
    from agent import ResearchAgent
    
    agent = ResearchAgent()
    result = agent.research("Neural Networks")
    
    print(f"Topic: {result['topic']}")
    print(f"Total Iterations: {result['iterations']}")
    print(f"Total Searches: {len(result['findings'])}\n")
    
    # Analyze findings by tool
    tool_usage = {}
    for finding in result['findings']:
        tool = finding['tool']
        tool_usage[tool] = tool_usage.get(tool, 0) + 1
    
    print("Tool Usage:")
    for tool, count in tool_usage.items():
        print(f"  {tool}: {count} times")


# ============================================================
# EXAMPLE 8: Comparing Research Results
# ============================================================

def example_compare_topics():
    """Compare research on similar topics"""
    from agent import ResearchAgent
    from advanced_agent import AdvancedResearchAgent
    
    comparison_topics = [
        ("Machine Learning", "Deep Learning"),
        ("Cloud Computing", "Edge Computing"),
        ("AI Ethics", "AI Bias")
    ]
    
    session = AdvancedResearchAgent()
    
    for topic1, topic2 in comparison_topics:
        print(f"\nComparing: {topic1} vs {topic2}")
        
        result1 = session.research(topic1)
        result2 = session.research(topic2)
        
        print(f"{topic1}: {result1['iterations']} iterations")
        print(f"{topic2}: {result2['iterations']} iterations")


# ============================================================
# EXAMPLE 9: Error Handling and Retry Logic
# ============================================================

def example_error_handling():
    """Handle errors gracefully"""
    from agent import ResearchAgent
    from tenacity import retry, wait_exponential, stop_after_attempt
    
    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(3)
    )
    def research_with_retry(topic):
        agent = ResearchAgent()
        return agent.research(topic)
    
    try:
        result = research_with_retry("Complex Topic")
    except Exception as e:
        print(f"Research failed after retries: {e}")


# ============================================================
# EXAMPLE 10: Caching Research Results
# ============================================================

def example_cached_research():
    """Cache results to avoid re-research"""
    from agent import ResearchAgent
    import json
    from pathlib import Path
    
    class CachedAgent(ResearchAgent):
        def __init__(self, cache_dir="research_cache"):
            super().__init__()
            self.cache_dir = Path(cache_dir)
            self.cache_dir.mkdir(exist_ok=True)
        
        def research(self, topic):
            # Check cache
            cache_file = self.cache_dir / f"{topic}.json"
            if cache_file.exists():
                print(f"Using cached result for: {topic}")
                with open(cache_file) as f:
                    return json.load(f)
            
            # Research and cache
            print(f"Researching: {topic}")
            result = super().research(topic)
            
            with open(cache_file, 'w') as f:
                json.dump(result, f, default=str)
            
            return result
    
    agent = CachedAgent()
    result1 = agent.research("AI")  # Researches
    result2 = agent.research("AI")  # Uses cache


# ============================================================
# EXAMPLE 11: Pipe Results to Other Systems
# ============================================================

def example_pipeline():
    """Chain research into other processes"""
    from agent import ResearchAgent
    import requests
    import json
    
    agent = ResearchAgent()
    result = agent.research("API Integration")
    
    # Send to external API
    response = requests.post(
        "https://api.example.com/research",
        json=result,
        headers={"Content-Type": "application/json"}
    )
    
    # Or save to database
    # db.research_reports.insert_one(result)


# ============================================================
# EXAMPLE 12: Custom Report Format
# ============================================================

def example_custom_report():
    """Generate custom formatted report"""
    from agent import ResearchAgent
    
    agent = ResearchAgent()
    result = agent.research("Topic")
    
    # Custom formatting
    custom_report = f"""
    # Executive Report: {result['topic']}
    
    ## Summary
    {result['report'][:500]}...
    
    ## Statistics
    - Research Iterations: {result['iterations']}
    - Total Findings: {len(result['findings'])}
    - Status: {result['status']}
    
    ## Findings Details
    """
    
    for i, finding in enumerate(result['findings'], 1):
        custom_report += f"\n### Finding {i}: {finding['tool']}"
        custom_report += f"\n{finding['output'][:200]}...\n"
    
    print(custom_report)


# ============================================================
# Main Demo Runner
# ============================================================

if __name__ == "__main__":
    examples = [
        ("Basic Research", example_basic_research),
        ("Custom Config", example_custom_config),
        ("Advanced Agent", example_advanced_agent),
        ("Interactive Session", example_interactive_session),
        ("Batch Research", example_batch_research),
        ("Custom Knowledge", example_custom_knowledge),
        ("Analyze Findings", example_analyze_findings),
        ("Compare Topics", example_compare_topics),
        ("Error Handling", example_error_handling),
        ("Cached Research", example_cached_research),
        ("Pipeline", example_pipeline),
        ("Custom Report", example_custom_report),
    ]
    
    print("="*60)
    print("RESEARCH AGENT - EXAMPLES")
    print("="*60)
    print("\nAvailable Examples:")
    
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. Exit")
    
    choice = input("\nSelect example to run (0-12): ").strip()
    
    if choice == "0":
        print("Exiting...")
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                print(f"\nRunning: {examples[idx][0]}\n")
                examples[idx][1]()
            else:
                print("Invalid choice!")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
