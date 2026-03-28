"""
Main entry point for the Autonomous Research Agent
"""
import sys
import json
from datetime import datetime
from agent import ResearchAgent


def save_report(topic: str, report: str, findings: list):
    """Save the research report to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/report_{topic.replace(' ', '_')}_{timestamp}.txt"
    
    # Create reports directory if it doesn't exist
    import os
    os.makedirs("reports", exist_ok=True)
    
    with open(filename, "w") as f:
        f.write(report)
    
    # Also save findings as JSON
    json_filename = f"reports/findings_{topic.replace(' ', '_')}_{timestamp}.json"
    with open(json_filename, "w") as f:
        json.dump(findings, f, indent=2)
    
    print(f"✓ Report saved to: {filename}")
    print(f"✓ Findings saved to: {json_filename}")
    
    return filename


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("AUTONOMOUS RESEARCH AGENT - Powered by LangChain")
    print("="*70 + "\n")
    
    # Get topic from user or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        print("Enter the research topic (or press Enter for default):")
        topic = input("Topic: ").strip()
        if not topic:
            topic = "Impact of AI in Healthcare"
    
    print(f"\nResearching: {topic}")
    print("This may take a minute...\n")
    
    # Initialize and run agent
    try:
        agent = ResearchAgent()
        research_result = agent.research(topic)
        
        # Generate formatted report
        final_report = agent.generate_report(research_result)
        
        # Display report
        print(final_report)
        
        # Save report
        save_report(topic, final_report, research_result["findings"])
        
        print("\n✓ Research completed successfully!")
        
    except KeyError as e:
        print(f"\n✗ Configuration Error: Missing API key - {e}")
        print("Please set the required environment variables:")
        print("  - OPENAI_API_KEY (for OpenAI)")
        print("  - ANTHROPIC_API_KEY (for Anthropic)")
        print("  - SERPAPI_KEY (optional, for web search)")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error during research: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
