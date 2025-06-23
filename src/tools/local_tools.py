import os
import subprocess
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langchain_core.tools import tool
from langgraph.types import Command, interrupt
load_dotenv()

os.environ["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY")

@tool(
    "human_assistance",
    description=(
        "Request assistance from a human when you need help with tasks that require "
        "human judgment, creativity, access to real-time information, or clarification "
        "of ambiguous requirements. Use this when you encounter limitations in your "
        "capabilities or need human input to proceed effectively."
    )
)
def human_assistance(query: str) -> str:
    """
    Request assistance from a human when you need help with tasks that require:
    - Human judgment, creativity, or subjective decision-making
    - Access to information not available in your knowledge base
    - Clarification of ambiguous requirements or instructions
    - Real-time information or current events
    - Complex problem-solving that benefits from human insight
    
    Use this tool when you encounter limitations in your capabilities or need 
    human input to proceed effectively with a task.
    
    Args:
        query (str): A clear, specific question or request for human assistance.
                    Include context about what you've tried and why you need help.
    
    Returns:
        str: The human's response to your query.
    """
    print("human assistance tool called")
    human_response = interrupt({"query": query})
    return human_response["data"]


@tool(
    "execute_command",
    description=(
        "Execute a command line/shell command and return its output. "
        "Use this tool to run system commands, scripts, or utilities. "
        "Be cautious with destructive commands. Commands run in the current working directory."
    )
)
def execute_command(command: str) -> str:
    """
    Execute a command line command and return its output.
    
    Use this tool when you need to:
    - Run system utilities or commands
    - Execute scripts or programs
    - Check system status or information
    - Perform file operations via command line
    - Install packages or run build commands
    
    Args:
        command (str): The command to execute. Be specific and include all necessary flags.
                      Avoid potentially destructive commands without user confirmation.
    
    Returns:
        str: The command output (stdout) or error message if the command fails.
    """
    try:
        # Execute the command and capture output
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout to prevent hanging
        )
        
        if result.returncode == 0:
            return f"Command executed successfully:\n{result.stdout}"
        else:
            return f"Command failed with return code {result.returncode}:\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"


search_tool = TavilySearch(max_results=2)


tools = [search_tool, human_assistance, execute_command]

def get_local_tools():
    return tools

