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
        chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        extra_chromium_args=['--profile-directory=Default'],
    )
)

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
        min_size=(800, 600),
        text_select=True
    )
    api.set_window(window)
    
    # Start the application with debug enabled
    pywebview.start(debug=True)

if __name__ == "__main__":
    create_window()  