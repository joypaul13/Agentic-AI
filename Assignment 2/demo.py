"""
Demo script showing various uses of the Research Agent
"""
from agent import ResearchAgent
import json


def demo_basic_research():
    """Demo: Basic research on a topic"""
    print("\n" + "="*70)
    print("DEMO 1: Basic Research")
    print("="*70)
    
    agent = ResearchAgent()
    topic = "Impact of Artificial Intelligence in Healthcare"
    
    print(f"Researching: {topic}\n")
    result = agent.research(topic)
    
    report = agent.generate_report(result)
    print(report)
    
    return result


def demo_multiple_topics():
    """Demo: Research multiple topics"""
    print("\n" + "="*70)
    print("DEMO 2: Research Multiple Topics")
    print("="*70)
    
    topics = [
        "Machine Learning in Finance",
        "Renewable Energy Future",
        "Space Exploration Developments"
    ]
    
    agent = ResearchAgent()
    results = {}
    
    for topic in topics:
        print(f"\nResearching: {topic}")
        result = agent.research(topic)
        results[topic] = result
        print(f"✓ Completed with {result['iterations']} iterations")
    
    # Save combined results
    with open("reports/batch_research.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results


def demo_detailed_analysis():
    """Demo: Detailed analysis with findings"""
    print("\n" + "="*70)
    print("DEMO 3: Detailed Analysis")
    print("="*70)
    
    agent = ResearchAgent()
    topic = "Blockchain Technology"
    
    result = agent.research(topic)
    
    print(f"\nDetailed Findings for: {topic}")
    print(f"Total Iterations: {result['iterations']}")
    print(f"Total Searches: {len(result['findings'])}\n")
    
    print("Search History:")
    for i, finding in enumerate(result['findings'], 1):
        print(f"\n{i}. Tool: {finding['tool']}")
        print(f"   Iteration: {finding['iteration']}")
        print(f"   Output Preview: {finding['output'][:200]}...")
    
    return result


def demo_custom_workflow():
    """Demo: Custom workflow with agent"""
    print("\n" + "="*70)
    print("DEMO 4: Custom Workflow")
    print("="*70)
    
    agent = ResearchAgent()
    
    # Custom research flow
    print("\nStep 1: Initial research")
    result = agent.research("Quantum Computing")
    
    print("\nStep 2: Extract key findings")
    findings_count = len(result['findings'])
    iterations = result['iterations']
    
    print(f"  - Number of findings: {findings_count}")
    print(f"  - Iterations completed: {iterations}")
    
    print("\nStep 3: Generate insights")
    report = agent.generate_report(result)
    
    # Save with metadata
    metadata = {
        "topic": result['topic'],
        "timestamp": str(__import__('datetime').datetime.now()),
        "iterations": result['iterations'],
        "findings_count": len(result['findings']),
        "status": result['status']
    }
    
    with open("reports/custom_workflow_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print("\n✓ Report and metadata saved")
    return result


def run_all_demos():
    """Run all demo scenarios"""
    print("\n" + "="*70)
    print("AUTONOMOUS RESEARCH AGENT - DEMO SUITE")
    print("="*70)
    print("\nThis script demonstrates various use cases of the Research Agent.")
    print("Note: Each demo will consume API credits.\n")
    
    demos = [
        ("Basic Research", demo_basic_research),
        ("Multiple Topics", demo_multiple_topics),
        ("Detailed Analysis", demo_detailed_analysis),
        ("Custom Workflow", demo_custom_workflow)
    ]
    
    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print(f"  {len(demos)+1}. Run All Demos")
    print(f"  0. Exit")
    
    choice = input("\nSelect demo to run (0-5): ").strip()
    
    if choice == "0":
        print("Exiting...")
        return
    elif choice == str(len(demos) + 1):
        # Run all demos
        for name, demo_func in demos:
            try:
                demo_func()
            except Exception as e:
                print(f"Error in {name}: {e}")
    else:
        try:
            demo_idx = int(choice) - 1
            if 0 <= demo_idx < len(demos):
                demos[demo_idx][1]()
        except (ValueError, IndexError):
            print("Invalid choice!")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("RESEARCH AGENT - DEMO SUITE")
    print("="*70)
    print("\nChoose an option:")
    print("  1. Run Interactive Demos")
    print("  2. Basic Research (default topic)")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        run_all_demos()
    elif choice == "2":
        agent = ResearchAgent()
        result = agent.research("Impact of AI in Healthcare")
        report = agent.generate_report(result)
        print(report)
    else:
        print("Exiting...")
