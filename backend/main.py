from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import webview as pywebview
import os
from pydantic import SecretStr

pywebview.debug = True

from log import LogHistory
log = LogHistory('../log.json')

from langchain_openai import ChatOpenAI
from browser_use import Agent, AgentHistoryList, Browser, BrowserConfig
from dotenv import load_dotenv
import asyncio
import json
load_dotenv()

# api_key = os.getenv('DEEPSEEK_API_KEY', '')
# if not api_key:
# 	raise ValueError('DEEPSEEK_API_KEY is not set')

llm = ChatOpenAI(model="gpt-4o")
# llm = ChatOpenAI(
#     base_url='https://api.deepseek.com/v3',
#     model='deepseek-reasoner',
#     api_key=SecretStr(api_key),
# )

browser_use_browser = Browser(
    config=BrowserConfig(
        headless=False,
        # chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        # extra_chromium_args=['--profile-directory=Default'],
    )
)

async def run_browser_agent_v2(task):
    """
    Run the browser agent to execute the task
    
    Args:
        task (dict): Task information containing target_website, google_search_keyword, etc.
        
    Returns:
        dict: Result of the browser agent execution
    """
    try:
        target_website = task.get('target_website')
        google_search_keyword = task.get('google_search_keyword')
        loop_count = task.get('loop', 1)

        # Create the task message
        message = f"""
1. Access Google:
    * Open your browser and navigate to https://google.com.
2. Search for the Keyword:
    * In the Google search bar, type "{google_search_keyword}" and press Enter.
3. Locate the Specific Domain in Results:
    * Check the search results for links under the domain {target_website}.
    * If not found on the current page: Click the "Next" button (or page numbers) at the bottom of Google to check subsequent pages.
4. Visit the Target Website:
    * Once you find a result matching the domain, click the link to navigate to {target_website}.
"""
        
        agent = Agent(
            task=message,
            llm=llm,
            browser=browser_use_browser,
            use_vision=False,
            max_failures=2,
            max_actions_per_step=1
        )
            
        # Execute the agent
        history: AgentHistoryList = await agent.run()
        result = history.final_result()

        # Log the result
        log.add_entry(
            action='run_browser_agent',
            details={
                'message': message,
                'result': result 
            }
        )

        return result  
      
    except Exception as e:
        error_message = str(e)
        log.add_entry(
            action='run_browser_agent',
            details={
                'message': message,
                'error': error_message  
            }
        )
        return {
            "status": "error",
            "error": error_message
        }


class Api:
    def __init__(self):
        self.window = None

    def set_window(self, window):
        self.window = window

    def health_check(self):
        """Health check endpoint"""
        return {"status": "healthy"}

    def get_message(self):
        """Get a message from the backend"""
        return "Hello from Python backend!"

    def init(self):
        """Initialize the API"""
        return True
    def task_reception(self, task):
        """Task reception - synchronous wrapper for async function"""
        try:
            # Check if there is already an event loop
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            return loop.run_until_complete(run_browser_agent_v2(task))
        finally:
            if loop.is_running():
                loop.close()
    
    def run_browser_agent(self, message):
        """Run the browser agent"""
        print(f"_____MESSAGE: {message}")
        
        # Create an event loop and run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            agent = Agent(
                task=message,
                llm=llm,
                browser=browser_use_browser,
                use_vision=False,
                max_failures=2,
                max_actions_per_step=1
            )
                
            history: AgentHistoryList = loop.run_until_complete(agent.run())
            result = history.final_result()
            log.add_entry(
                action='run_browser_agent',
                details={
                    'message': message,
                    'result': result 
                }
            )
            return result
        finally:
            loop.close()

api = Api()

def create_window():
    # Create a window with exposed JavaScript API
    window = pywebview.create_window(
        'Browser Agent',
        'http://localhost:5173',
        js_api=api,
        width=960,          # Initial width
        height=600,         # Initial height
        min_size=(800, 600),
        text_select=True
    )
    api.set_window(window)
    
    # Start the application with debug enabled
    pywebview.start(debug=True)

if __name__ == "__main__":
    create_window()  