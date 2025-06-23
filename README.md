# LangGraph Chatbot - Debug Version

> ⚠️ **Note**: This is a debug version and first attempt at building a LangGraph-based conversational AI agent. Expect rough edges and experimental features.

A conversational AI agent built with LangGraph that can:
- Search the web using Tavily
- Request human assistance when needed
- Execute command line operations
- Maintain conversation memory

## Prerequisites

- Python 3.8+
- [UV](https://docs.astral.sh/uv/) package manager
- API Keys for:
  - Google Gemini API (for LLM)
  - Tavily API (for web search)

## Setup with UV

### 1. Install UV (if not already installed)

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Clone and Initialize Project

```bash
git clone <your-repo-url>
cd line

# Initialize UV environment and install dependencies
uv sync

# Or if you don't have pyproject.toml yet:
uv init
uv add langchain-tavily python-dotenv langchain-core langgraph langchain-google-genai
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Getting API Keys:**
- **Gemini API**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Tavily API**: Get from [Tavily](https://tavily.com/)

### 4. Make Scripts Executable (Linux/macOS)

```bash
chmod +x activate.sh run.sh
```

## Running the Project

### Option 1: Using UV directly

```bash
# Activate UV environment and run
uv run python src/main.py
```

### Option 2: Using provided scripts

```bash
# Activate environment
./activate.sh

# Run the project
./run.sh
```

### Option 3: Manual activation

```bash
# Activate UV environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Run the project
python src/main.py
```

## Available Tools

The chatbot has access to these tools:

1. **Web Search** - Search the internet using Tavily
2. **Human Assistance** - Request help from a human operator
3. **Command Execution** - Run command line operations

## Usage

Once running, you can:

```
User: What's the weather like today?
# Uses web search tool

User: help me decide between these options
# May trigger human assistance tool

User: list files in current directory
# May use command execution tool

User: quit
# Exit the application
```

## Project Structure

```
line/
├── src/
│   ├── main.py              # Main application entry point
│   └── tools/
│       └── local_tools.py   # Custom tool definitions
├── .env                     # Environment variables (create this)
├── pyproject.toml          # UV project configuration
├── activate.sh             # Environment activation script
├── run.sh                  # Run script
├── graph.png              # Generated graph visualization
└── README.md              # This file
```

## Development with UV

### Adding new dependencies

```bash
uv add package-name
```

### Updating dependencies

```bash
uv sync --upgrade
```


### Running in development mode

```bash
uv run --reload python src/main.py
```

## Troubleshooting

### Common Issues

1. **"No module named" errors**: Make sure you're in the UV environment
   ```bash
   uv sync
   uv run python src/main.py
   ```

2. **API Key errors**: Check your `.env` file has the correct keys

3. **Permission denied on scripts**: 
   ```bash
   chmod +x activate.sh run.sh
   ```

4. **UV not found**: Install UV following the setup instructions above

### Debug Mode

This is a debug version - you may encounter:
- Verbose logging
- Experimental features
- Potential crashes or unexpected behavior
- Graph visualization generation attempts

## Contributing

This is a first attempt/debug version. Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Test edge cases

## License

See LICENSE file for details.

---

**Note**: This project is in active development and debugging phase. Use at your own discretion.
