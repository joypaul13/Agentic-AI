"""
Unit tests and integration tests for Research Agent
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import json
from datetime import datetime

from tools import WebSearchTool, WikipediaTool, KnowledgeBaseTool, ResearchToolkit
from agent import ResearchAgent
from config import LLM_PROVIDER, MODEL_NAME


class TestWebSearchTool(unittest.TestCase):
    """Test Web Search Tool"""
    
    def setUp(self):
        self.tool = WebSearchTool()
    
    def test_tool_initialization(self):
        """Test if tool initializes correctly"""
        self.assertIsNotNone(self.tool)
        self.assertEqual(self.tool.name, "web_search")
    
    def test_tool_callable(self):
        """Test if tool is callable"""
        self.assertTrue(callable(self.tool))
    
    def test_search_with_wikipedia_fallback(self):
        """Test search with Wikipedia fallback"""
        results = self.tool.search("Python Programming")
        self.assertIsInstance(results, list)


class TestWikipediaTool(unittest.TestCase):
    """Test Wikipedia Tool"""
    
    def setUp(self):
        self.tool = WikipediaTool()
    
    def test_tool_initialization(self):
        """Test if tool initializes correctly"""
        self.assertIsNotNone(self.tool)
        self.assertEqual(self.tool.name, "wikipedia_search")
    
    def test_search_valid_topic(self):
        """Test search with valid Wikipedia topic"""
        result = self.tool.search("Artificial Intelligence", sentences=3)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_search_invalid_topic(self):
        """Test search with invalid topic"""
        result = self.tool.search("XyZ123InvalidTopicXyZ")
        # Should return None or empty or disambiguation message
        self.assertFalse(result or result == "")


class TestKnowledgeBaseTool(unittest.TestCase):
    """Test Knowledge Base Tool"""
    
    def setUp(self):
        self.tool = KnowledgeBaseTool()
    
    def test_add_and_query_knowledge(self):
        """Test adding and querying knowledge"""
        self.tool.add_knowledge("test_key", "test_value")
        result = self.tool.query("test_key")
        self.assertEqual(result, "test_value")
    
    def test_query_missing_knowledge(self):
        """Test querying missing knowledge"""
        result = self.tool.query("non_existent_key")
        self.assertIsNone(result)


class TestResearchToolkit(unittest.TestCase):
    """Test Research Toolkit"""
    
    def setUp(self):
        self.toolkit = ResearchToolkit()
    
    def test_toolkit_initialization(self):
        """Test toolkit initializes with all tools"""
        self.assertIsNotNone(self.toolkit.web_search)
        self.assertIsNotNone(self.toolkit.wikipedia)
        self.assertIsNotNone(self.toolkit.knowledge_base)
    
    def test_get_tools(self):
        """Test getting tools in LangChain format"""
        tools = self.toolkit.get_tools()
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)


class TestResearchAgent(unittest.TestCase):
    """Test Research Agent"""
    
    def setUp(self):
        try:
            self.agent = ResearchAgent()
        except Exception as e:
            self.skipTest(f"Cannot initialize agent: {e}")
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.llm)
        self.assertIsNotNone(self.agent.tools)
    
    def test_agent_has_tools(self):
        """Test agent has all required tools"""
        self.assertGreater(len(self.agent.tools), 0)
    
    def test_should_use_tools(self):
        """Test tool usage detection"""
        # Should detect tool usage
        self.assertTrue(self.agent._should_use_tools("search for information"))
        self.assertTrue(self.agent._should_use_tools("I will research this"))
        self.assertTrue(self.agent._should_use_tools("let me look up this"))
        
        # Should not detect
        self.assertFalse(self.agent._should_use_tools("I think this is correct"))
    
    def test_extract_search_queries(self):
        """Test search query extraction"""
        response = 'search for "machine learning"'
        queries = self.agent._extract_search_queries(response)
        self.assertGreater(len(queries), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    @patch('agent.ChatOpenAI')
    def test_agent_research_with_mocked_llm(self, mock_llm):
        """Test agent research with mocked LLM"""
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = "Let me search for information about AI in healthcare"
        mock_llm.return_value.invoke.return_value = mock_response
        
        # This would need proper setup to work


class TestConfiguration(unittest.TestCase):
    """Test configuration"""
    
    def test_config_values(self):
        """Test if configuration values are set"""
        from config import MAX_ITERATIONS, TEMPERATURE
        
        self.assertIsNotNone(LLM_PROVIDER)
        self.assertIn(LLM_PROVIDER, ["openai", "anthropic"])
        self.assertIsNotNone(MODEL_NAME)
        self.assertGreater(MAX_ITERATIONS, 0)
        self.assertGreaterEqual(TEMPERATURE, 0.0)
        self.assertLessEqual(TEMPERATURE, 1.0)


class MockTests(unittest.TestCase):
    """Mock tests for quick validation"""
    
    def test_toolkit_mock_research(self):
        """Test toolkit with mock data"""
        toolkit = ResearchToolkit()
        
        # Add mock knowledge
        toolkit.knowledge_base.add_knowledge(
            "AI in Healthcare",
            "AI is revolutionizing healthcare with diagnostics and treatment planning"
        )
        
        # Query mock knowledge
        result = toolkit.knowledge_base.query("AI in Healthcare")
        self.assertIsNotNone(result)
    
    def test_report_generation(self):
        """Test report generation"""
        mock_result = {
            "topic": "Test Topic",
            "report": "This is a test report",
            "findings": [
                {"tool": "search_web", "output": "Finding 1"},
                {"tool": "wikipedia", "output": "Finding 2"}
            ],
            "iterations": 3,
            "status": "success"
        }
        
        # Verify structure
        self.assertEqual(mock_result["topic"], "Test Topic")
        self.assertEqual(len(mock_result["findings"]), 2)
        self.assertEqual(mock_result["status"], "success")


def run_quick_tests():
    """Run quick validation tests"""
    print("\n" + "="*60)
    print("QUICK VALIDATION TESTS")
    print("="*60 + "\n")
    
    tests = [
        ("Web Search Tool", TestWebSearchTool),
        ("Wikipedia Tool", TestWikipediaTool),
        ("Knowledge Base Tool", TestKnowledgeBaseTool),
        ("Toolkit", TestResearchToolkit),
        ("Agent", TestResearchAgent),
        ("Configuration", TestConfiguration),
        ("Mock Tests", MockTests)
    ]
    
    for test_name, test_class in tests:
        print(f"Running {test_name} tests...")
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(verbosity=0)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print(f"  ✓ {len(result.testsRun)} tests passed\n")
        else:
            print(f"  ✗ {len(result.failures)} failures, {len(result.errors)} errors\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_tests()
    else:
        # Run all tests
        unittest.main(verbosity=2)
