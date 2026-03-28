"""
Tool implementations for Research Agent
"""
import wikipedia
import requests
from typing import Optional, List
from bs4 import BeautifulSoup


class WebSearchTool:
    """Tool for searching information from the web"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.name = "web_search"
        self.description = "Search for information on the web. Use this to find recent and relevant information about topics."
    
    def search(self, query: str, num_results: int = 5) -> List[dict]:
        """
        Search the web using Google Search Results API or fallback to requests
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            List of search results with title, link, and snippet
        """
        try:
            if self.api_key:
                # Using SerpAPI
                results = self._serpapi_search(query, num_results)
            else:
                # Fallback to basic search
                results = self._simple_search(query, num_results)
            return results
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    def _serpapi_search(self, query: str, num_results: int) -> List[dict]:
        """Search using SerpAPI"""
        from serpapi import GoogleSearch
        
        params = {
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        formatted_results = []
        if "organic_results" in results:
            for result in results["organic_results"][:num_results]:
                formatted_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", "")
                })
        return formatted_results
    
    def _simple_search(self, query: str, num_results: int) -> List[dict]:
        """Fallback simple search using Wikipedia snippets and basic web search"""
        results = []
        
        # Try to get Wikipedia summary
        try:
            summary = wikipedia.summary(query, sentences=3)
            results.append({
                "title": f"Wikipedia: {query}",
                "link": f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}",
                "snippet": summary
            })
        except:
            pass
        
        return results
    
    def __call__(self, query: str) -> str:
        """Make tool callable"""
        results = self.search(query)
        if not results:
            return "No results found."
        
        formatted = "Web Search Results:\n"
        for i, result in enumerate(results, 1):
            formatted += f"\n{i}. {result['title']}\n"
            formatted += f"   Link: {result['link']}\n"
            formatted += f"   Snippet: {result['snippet']}\n"
        return formatted


class WikipediaTool:
    """Tool for retrieving information from Wikipedia"""
    
    def __init__(self):
        self.name = "wikipedia_search"
        self.description = "Search Wikipedia for detailed information about topics. Use this to get comprehensive background information."
    
    def search(self, topic: str, sentences: int = 5) -> Optional[str]:
        """
        Search Wikipedia for a topic
        
        Args:
            topic: The topic to search
            sentences: Number of sentences to return
            
        Returns:
            Wikipedia summary or None if not found
        """
        try:
            # Search for the topic
            result = wikipedia.page(topic, auto_suggest=True)
            summary = wikipedia.summary(topic, sentences=sentences)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            # Return first option from disambiguation
            options = e.options[:3]
            try:
                summary = wikipedia.summary(options[0], sentences=sentences)
                return f"(Searched for '{options[0]}' instead)\n\n{summary}"
            except:
                return f"Found disambiguation. Options: {', '.join(options[:5])}"
        except wikipedia.exceptions.PageError:
            return None
    
    def get_related_topics(self, topic: str) -> List[str]:
        """Get related Wikipedia topics"""
        try:
            page = wikipedia.page(topic)
            # Extract links from the page
            links = page.links[:10]
            return links
        except:
            return []
    
    def __call__(self, topic: str) -> str:
        """Make tool callable"""
        result = self.search(topic, sentences=7)
        if result:
            return f"Wikipedia Information:\n{result}"
        else:
            return f"No Wikipedia page found for '{topic}'. Try a different search term."


class KnowledgeBaseTool:
    """Tool for accessing structured knowledge"""
    
    def __init__(self):
        self.name = "knowledge_base"
        self.description = "Query the knowledge base for specific facts and information."
        self.knowledge_base = {}
    
    def add_knowledge(self, key: str, value: str):
        """Add knowledge to the base"""
        self.knowledge_base[key] = value
    
    def query(self, query: str) -> Optional[str]:
        """Query the knowledge base"""
        for key, value in self.knowledge_base.items():
            if key.lower() in query.lower():
                return value
        return None
    
    def __call__(self, query: str) -> str:
        """Make tool callable"""
        result = self.query(query)
        if result:
            return f"Knowledge Base Result:\n{result}"
        else:
            return "No relevant information found in knowledge base."


class ResearchToolkit:
    """Collection of all research tools"""
    
    def __init__(self, serpapi_key: Optional[str] = None):
        self.web_search = WebSearchTool(serpapi_key)
        self.wikipedia = WikipediaTool()
        self.knowledge_base = KnowledgeBaseTool()
        self.tools = [
            self.web_search,
            self.wikipedia,
            self.knowledge_base
        ]
    
    def get_tools(self) -> List:
        """Get all tools as LangChain tools"""
        from langchain_core.tools import tool
        
        @tool
        def search_web(query: str) -> str:
            """Search the web for information about a topic."""
            return self.web_search(query)
        
        @tool
        def search_wikipedia(topic: str) -> str:
            """Search Wikipedia for detailed information about a topic."""
            return self.wikipedia(topic)
        
        @tool
        def query_knowledge(question: str) -> str:
            """Query the knowledge base for information."""
            return self.knowledge_base(question)
        
        return [search_web, search_wikipedia, query_knowledge]
