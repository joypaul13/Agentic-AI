# Autonomous Research Agent - Deployment Guide

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Git cloned or files downloaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] API keys obtained
- [ ] .env file configured
- [ ] Setup validation passed
- [ ] First research completed

## Pre-Deployment Setup

### Step 1: System Requirements

**Minimum Requirements**:
- Python 3.8+
- 4GB RAM
- 500MB disk space
- Internet connection
- Modern web browser (optional)

**Recommended**:
- Python 3.10+
- 8GB RAM
- SSD for faster I/O
- Stable internet connection

### Step 2: Clone/Download Project

```bash
# Navigate to project directory
cd "e:\6 semester\agentic AI\assignment 2"

# Verify files exist
dir
```

### Step 3: Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Activate (Linux/Mac)
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 5: Configure API Keys

```bash
# Copy template
copy .env.example .env

# Edit .env with your editor
# Add your API keys
```

### Step 6: Validate Setup

```bash
# Run setup validation
python setup.py

# Expected output: "✓ All checks passed!"
```

## Deployment Scenarios

### Scenario 1: Personal Development

**Setup**:
1. Create virtual environment
2. Install dependencies locally
3. Configure .env with API keys
4. Run main.py for research

**Cost**: Minimal (shared API account)

### Scenario 2: Integration with Other Tools

**Setup**:
```python
# Import in your script
from agent import ResearchAgent

agent = ResearchAgent()
result = agent.research("Your Topic")
report = agent.generate_report(result)
```

**Integration Points**:
- CLI: `main.py`
- API: `agent.py` classes
- Advanced: `advanced_agent.py`

### Scenario 3: Docker Container

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "main.py"]
```

**Build & Run**:
```bash
docker build -t research-agent .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY \
           -v reports:/app/reports \
           research-agent "Your Topic"
```

### Scenario 4: Cloud Deployment

**AWS Lambda**:
```python
def lambda_handler(event, context):
    os.environ['OPENAI_API_KEY'] = event['api_key']
    
    agent = ResearchAgent()
    result = agent.research(event['topic'])
    report = agent.generate_report(result)
    
    return {
        'statusCode': 200,
        'body': json.dumps(report)
    }
```

**Azure Function**:
```python
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    topic = req.params.get('topic')
    
    agent = ResearchAgent()
    result = agent.research(topic)
    
    return func.HttpResponse(
        json.dumps(result),
        status_code=200
    )
```

## Configuration for Production

### config.py Optimization

```python
# Production settings
TEMPERATURE = 0.3           # More focused responses
MAX_TOKENS = 2000          # Faster responses
MAX_ITERATIONS = 10        # Balanced depth
REPORT_LENGTH = "medium"   # Concise reports
```

### Error Handling

```python
# Add to main.py
try:
    agent = ResearchAgent()
    result = agent.research(topic)
    report = agent.generate_report(result)
except APIError as e:
    log_error(f"API Error: {e}")
    # Retry logic
except ConfigError as e:
    log_error(f"Config Error: {e}")
    # Configuration check
```

## Performance Optimization

### Cache Results

```python
import json
from pathlib import Path

class CachedResearchAgent(ResearchAgent):
    def __init__(self, cache_dir="cache"):
        super().__init__()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def research(self, topic):
        cache_file = self.cache_dir / f"{topic}.json"
        
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        
        result = super().research(topic)
        
        with open(cache_file, 'w') as f:
            json.dump(result, f)
        
        return result
```

### Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor

topics = ["AI", "ML", "NLP"]
agent = ResearchAgent()

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(agent.research, topic)
        for topic in topics
    ]
    
    results = [f.result() for f in futures]
```

## Monitoring & Logging

### Add Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('research_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# In agent.py
logger.info(f"Starting research on: {topic}")
logger.debug(f"Tool executed: {tool_name}")
logger.error(f"Error: {error}")
```

### Health Check

```python
def health_check():
    """Verify system is ready"""
    checks = [
        ("Python Version", check_python()),
        ("Dependencies", check_dependencies()),
        ("API Keys", check_api_keys()),
        ("Network", check_network()),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = "✓" if check_func() else "✗"
        except Exception as e:
            results[name] = f"✗ ({e})"
    
    return results
```

## Troubleshooting Deployment

### Issue: Module Not Found

```
ModuleNotFoundError: No module named 'langchain'
```

**Solution**:
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: API Key Invalid

```
AuthenticationError: Invalid API key
```

**Solution**:
```bash
# Verify .env file exists and has content
cat .env

# Check formatting: no quotes around keys
OPENAI_API_KEY=sk-...123
# NOT: OPENAI_API_KEY="sk-...123"
```

### Issue: Rate Limited

```
RateLimitError: Rate limit exceeded
```

**Solution**:
```python
# Add retry logic
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(), stop=stop_after_attempt(3))
def research_with_retry(agent, topic):
    return agent.research(topic)
```

### Issue: Timeout

```
TimeoutError: Request timed out
```

**Solution**:
```python
# Increase timeout in config.py
TIMEOUT = 120  # 2 minutes

# Or add to specific calls
llm = ChatOpenAI(request_timeout=120)
```

## Post-Deployment

### Monitoring

1. **Check logs regularly**:
   ```bash
   cat research_agent.log
   ```

2. **Monitor API usage**:
   - OpenAI: https://platform.openai.com/usage
   - Anthropic: https://console.anthropic.com

3. **Track reports**:
   ```bash
   dir reports
   ```

### Maintenance

1. **Keep dependencies updated**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Regular backups**:
   ```bash
   # Backup reports
   tar -czf reports_backup.tar.gz reports/
   ```

3. **Rotate API keys** regularly for security

## Scaling Considerations

### Batch Processing

```python
# Process multiple topics efficiently
def batch_research(topics, batch_size=5):
    agent = ResearchAgent()
    results = []
    
    for i in range(0, len(topics), batch_size):
        batch = topics[i:i+batch_size]
        for topic in batch:
            result = agent.research(topic)
            results.append(result)
        
        # Cool down between batches
        time.sleep(10)
    
    return results
```

### Multi-Agent System

```python
# Use multiple agent instances
from multiprocessing import Pool

def research_topic(topic):
    agent = ResearchAgent()
    return agent.research(topic)

if __name__ == '__main__':
    topics = ["AI", "ML", "DL"]
    with Pool(3) as pool:
        results = pool.map(research_topic, topics)
```

## Security Considerations

1. **Never commit .env files**:
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use environment variables in production**:
   ```python
   import os
   API_KEY = os.getenv('OPENAI_API_KEY')
   ```

3. **Rotate API keys regularly**

4. **Use IAM roles for cloud deployment**

5. **Encrypt sensitive data**

## Rollback Plan

If issues occur:

1. **Identify the issue**:
   ```bash
   python setup.py --trouble
   ```

2. **Check recent changes**:
   ```bash
   git diff HEAD~1
   ```

3. **Rollback if needed**:
   ```bash
   git revert HEAD
   ```

4. **Restart with last known good**:
   ```bash
   python main.py
   ```

---

**Deployment Complete! Happy Researching! 🚀**
