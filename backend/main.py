import sys
import os
import io
import random
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv()

os.environ["PYTHONIOENCODING"] = "utf-8"
# if sys.stdout is not None:
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
# if sys.stderr is not None:
#     sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import threading


# from fastapi.middleware.cors import CORSMiddleware
import webview
# from pydantic import SecretStr
# from pydantic.v1 import SecretStr  # For v2 compatibility

from database import Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from models import Task  # Import Task model to ensure it's registered
from task_db_handle import TaskDBHandler
from settings_db_handle import SettingsDBHandler 

webview.debug = True

from log import LogHistory
log = LogHistory('log.json')


from langchain_openai import ChatOpenAI
from browser_use import Agent, AgentHistoryList, Browser, BrowserConfig
from browser_use.browser.browser import ProxySettings
# from playwright._impl._api_structures import ProxySettings

from browser_use.browser.context import BrowserContext, BrowserContextConfig
from pathlib import Path
from langchain.prompts import load_prompt
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

async def get_chromium():
    async with async_playwright() as p:
        return await p.chromium.executable_path
        return {
            "chromium": p.chromium.executable_path,
            "firefox": p.firefox.executable_path,
            "webkit": p.webkit.executable_path
        }

__chromium = get_chromium()

import asyncio
import json

def sanitize_unicode(obj):
    """Recursively sanitize Unicode characters in dictionaries, lists, and strings"""
    if isinstance(obj, dict):
        return {k: sanitize_unicode(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_unicode(item) for item in obj]
    elif isinstance(obj, str):
        return obj.encode('ascii', 'replace').decode('ascii')
    else:
        return obj

if getattr(sys, 'frozen', False):
    # Running as bundled executable
    load_dotenv(os.path.join(sys._MEIPASS, '.env'))  # PyInstaller's temp dir
else:
    # Normal development mode
    load_dotenv()

# Set Playwright path for PyInstaller bundles
# os.environ['PLAYWRIGHT_BROWSERS_PATH'] = os.path.join(os.getcwd(), 'playwright_browsers')

# Get correct base path for templates
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent

SYSTEM_PROMPT_PATH = BASE_DIR / 'templates/system_prompt.json'

# Explicitly set the template path for LangChain
os.environ["LANGFUSE_PROMPT_PATH"] = str(SYSTEM_PROMPT_PATH)

# Hardcode Chromium executable path for PyInstaller
CHROMIUM_PATH = (
    BASE_DIR / "playwright_browsers" / "chromium-1148" / "chrome-mac" / "Chromium.app" / "Contents" / "MacOS" / "Chromium"
)


# Initialize FastAPI app
app = FastAPI()

# Initialize database
# @app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def init_database():
    """Initialize database tables"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(startup())
        loop.close()
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

# Initialize database on startup
init_database()


llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.getenv('OPENAI_API_KEY')
    )

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

def parse_proxy_data(proxy_data):
    """Parse proxy data from string format to structured data"""
    # Parse proxy data from string format to structured data
    proxy_list = []
    if proxy_data:
        # Split by newlines to get individual proxy entries
        proxy_entries = proxy_data.strip().split('\n')
        for entry in proxy_entries:
            parts = entry.strip().split()
            if len(parts) >= 1:
                proxy_info = {
                    'server': parts[0]
                }
                # If username and password are provided
                if len(parts) >= 3:
                    proxy_info['username'] = parts[1]
                    proxy_info['password'] = parts[2]
                proxy_list.append(proxy_info)
    return proxy_list

def extract_ip_and_address(html: str):
    """Extract IP address and full address from embedded JSON in <pre> tag inside HTML."""
    soup = BeautifulSoup(html, "html.parser")
    pre_tag = soup.find("pre")
    if not pre_tag:
        return None, "No <pre> tag found"

    try:
        data = json.loads(pre_tag.text)
    except json.JSONDecodeError:
        return None, "Invalid JSON in <pre>"

    ip = data.get("ip", "Unknown IP")
    providers = data.get("providers", {})

    def build_address(provider_data):
        parts = [provider_data.get("city"), provider_data.get("zip_code"), provider_data.get("country")]
        return ", ".join(part for part in parts if part)

    # Choose best provider in order of preference
    for name in ["ip2location", "maxmind", "dbip", "ipinfo"]:
        if name in providers:
            full_address = build_address(providers[name])
            if full_address:
                break
    else:
        full_address = "Unknown Address"

    return ip, full_address

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
        search_keyword = task.get('search_keyword')
        loop_count = task.get('loop', 1)

        # Create the task message
        message = f"""
1. At current tab, go to https://google.com (important) 
2. In the Google search bar, type "{search_keyword}" and press Enter.
3. Locate the Specific Domain in Results:
    * Check the search results for links under the domain {target_website} (very important), prioritize results that are "Sponsored".
    * If not found on the current page: Scroll to end page click the "Next" button (or next page numbers) at the bottom of Google to check subsequent pages.
4. Visit the Target Website:
    * Once you find a result matching the domain, click the link to navigate to {target_website}.
""" 
        
        # Test prompt
        # message = f"""
        # 1. go to "https://webhook-test.com/2b1b57612d6e50c21bbd928a51815657"
        # 2. task complete, return.
        # """

        print(f"_____MESSAGE: {message}")

        # get settings from database
        global app_settings 

        # openaiKey
        openai_api_key = app_settings.get('openaiKey')

        # proxy data
        proxy_data = app_settings.get('proxyData')
        proxy_list = parse_proxy_data(proxy_data)

        # processDelay
        process_delay = app_settings.get('processDelay')
        

        # return;
        
        llm2 = ChatOpenAI(
            model="gpt-4o-mini",
            # openai_api_key=os.getenv('OPENAI_API_KEY')
            openai_api_key=openai_api_key
            )

        print(f"_____LLM2: 1")
        cdp_url = f"http://localhost:9222" 
        async with async_playwright() as p:
            __browser = await p.chromium.connect_over_cdp(cdp_url)

            context = __browser.contexts[0] if __browser.contexts else await __browser.new_context()

            # Open a new page (tab)
            page = await context.new_page()

            # Navigate to the target URL
            await page.goto("https://ip.oxylabs.io/location")

            # Wait for content to load
            await page.wait_for_load_state("load")

            # Get full HTML content of the page
            content = await page.content()
            ip, address = extract_ip_and_address(content)

            print(f"_____IP: {ip}")
            print(f"_____ADDRESS: {address}")

            # Close all tabs in all contexts
            for context in __browser.contexts:
                for page in context.pages:
                    await page.close()
        

        browser_use_browser2 = Browser( 
            config=BrowserConfig(
                headless=False,
                cdp_url=cdp_url,
            )
        )

        print(f"_____BROWSER_USE_BROWSER2: 1")
        __message_context = f"You play as a normal user, following the given tasks exactly to complete the task."
        try:

            initial_actions = [
                {'open_tab': {'url': 'https://www.google.com'}},
            ]
            agent = Agent(
                task=message,
                message_context=__message_context,
                initial_actions=initial_actions,
                llm=llm2,
                browser=browser_use_browser2, 
                use_vision=False,
                max_failures=2,
                max_actions_per_step=1,
            )

            print(f"_____AGENT: 1")
                
            # Execute the agent
            history: AgentHistoryList = await agent.run()
            result = history.final_result()

            # Log the result - handle Unicode characters by replacing them with ASCII equivalents
            log.add_entry(
                action='run_browser_agent',
                details={
                    'message': message.encode('ascii', 'replace').decode('ascii') if isinstance(message, str) else message,
                    'result': json.dumps(result, ensure_ascii=True) if isinstance(result, dict) else str(result).encode('ascii', 'replace').decode('ascii')
                }
            )
            
            # Ensure result is properly encoded for Windows console output
            result = sanitize_unicode(result)
            
            # await main_browser.close()
            # await cdp_browser.close()
            # return result and id & address format string
            return f"result: {result} <p>IP: {ip} - Address: {address}</p>"
        finally:
            print(f"done")
      
    except Exception as e:
        # Handle Unicode encoding errors by replacing problematic characters
        error_message = str(e).encode('ascii', 'replace').decode('ascii')
        log.add_entry(
            action='run_browser_agent',
            details={
                'message': message.encode('ascii', 'replace').decode('ascii') if isinstance(message, str) else message,
                'error': error_message  
            }
        )
        # nsure all string values in the response are properly encoded
        response = sanitize_unicode({
            "status": "error",
            "error": error_message
        })
        # Print debug information
        print(f"Error in browser agent: {error_message}")
        return response

# Define API class to handle all API functions
class Api:
    def __init__(self):
        # Store window reference
        self.window_instance = None
    
    def health_check(self):
        return {"status": "healthy"}
    
    def get_message(self):
        return "Hello from Python backend!"
    
    def init(self):
        self.app_settings = get_app_settings()

        # set app_settings to global variable
        global app_settings
        app_settings = self.app_settings.get('settings')
        print(f"_____APP_SETTINGS: {app_settings}")

        # get settings from database
        return True
    
    def set_window(self, window):
        self.window_instance = window
    
    def get_tasks(self, status=None, ordering=None):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        async_session = AsyncSession(engine)
        try:
            handler = TaskDBHandler(async_session)
            if status:
                tasks = loop.run_until_complete(handler.get_tasks_by_status(status))
            else:
                tasks = loop.run_until_complete(handler.get_all_tasks())
            if ordering is not None:
                tasks = [task for task in tasks if task.ordering == ordering]
            return {"status": "success","tasks": [{"id": task.id,"target_website": task.target_website,"search_keyword": task.search_keyword,"loop": task.loop,"status": task.status,"ordering": task.ordering,"date_add": task.date_add.isoformat()} for task in tasks]}
        except Exception as e:
            error_message = str(e)
            log.add_entry(
                action='get_tasks',
                details={'error': error_message, 'status': status, 'ordering': ordering}
            )
            return {"status": "error", "error": error_message}
        finally:
            if async_session:
                loop.run_until_complete(async_session.close())
    
    def add_task(self, task):
        print(f"_____TASK: {task}")
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        async_session = AsyncSession(engine)
        try:
            handler = TaskDBHandler(async_session)
            task = loop.run_until_complete(handler.create_task(target_website=task.get('target_website'),search_keyword=task.get('search_keyword'),loop=task.get('loop')))
            return {"status": "success","task": {"id": task.id,"target_website": task.target_website,"search_keyword": task.search_keyword,"loop": task.loop,"status": task.status,"ordering": task.ordering,"date_add": task.date_add.isoformat()}}
        except Exception as e:
            error_message = str(e)
            log.add_entry(action='add_task',details={'error': error_message,'task': task})
            return {"status": "error","error": error_message}
        finally:
            if async_session:
                loop.run_until_complete(async_session.close())
    
    def delete_task(self, task_id):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        async_session = AsyncSession(engine)
        try:
            handler = TaskDBHandler(async_session)
            loop.run_until_complete(handler.delete_task(task_id))
            return {"status": "success"}
        except Exception as e:
            error_message = str(e)
            log.add_entry(action='delete_task',details={'error': error_message,'task_id': task_id})
            return {"status": "error","error": error_message}
        finally:
            if async_session:
                loop.run_until_complete(async_session.close())
    
    def update_task(self, task):
        """Update a task in the database"""
        try:
            print(f"_____update_task: {task}")

            # Create event loop if not exists
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Create database session
            async_session = AsyncSession(engine)
            handler = TaskDBHandler(async_session)

            # Update task in the database
            task_id = task.get('id')
            # Remove id from the task dict to avoid passing it as a kwarg
            task_data = {k: v for k, v in task.items() if k != 'id'}
            task = loop.run_until_complete(handler.update_task(task_id, **task_data))

            return {
                "status": "success",
                "task": {
                    "id": task.id,
                    "target_website": task.target_website,
                    "search_keyword": task.search_keyword,
                    "loop": task.loop,
                    "status": task.status,
                    "ordering": task.ordering,
                }
            }
        except Exception as e:
            error_message = str(e)
            log.add_entry(
                action='update_task',
                details={
                    'error': error_message,
                    'task': task
                }
            )
            return {
                "status": "error",
                "error": error_message
            }
        finally:
            if async_session:
                loop.run_until_complete(async_session.close())
    
    def task_reception(self, task):
        """Task reception - synchronous wrapper for async function"""
        try:
            # Check if there is already an event loop
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        try:
            # Pass the task to the async function
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
            
            # Handle Unicode characters in the result
            result = sanitize_unicode(result)
                
            log.add_entry(
                action='run_browser_agent',
                details={
                    'message': message.encode('ascii', 'replace').decode('ascii') if isinstance(message, str) else message,
                    'result': json.dumps(result, ensure_ascii=True) if isinstance(result, dict) else str(result).encode('ascii', 'replace').decode('ascii')
                }
            )
            return result
        finally:
            loop.close()

    # get settings from database
    def get_settings(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            async_session = AsyncSession(engine)
            handler = SettingsDBHandler(async_session)
            settings = loop.run_until_complete(handler.get_settings())
            return {
                "status": "success",
                "settings": settings
            }
        finally:
            if async_session:
                loop.run_until_complete(async_session.close())
    
    # update settings
    def update_settings(self, settings):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            async_session = AsyncSession(engine)
            handler = SettingsDBHandler(async_session)
            settings = loop.run_until_complete(handler.update_settings(settings))

            global app_settings
            app_settings = settings

            return {
                "status": "success",
                "settings": settings
            }
        finally:
            if async_session:
                loop.run_until_complete(async_session.close())


app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/", StaticFiles(directory=BASE_DIR / "static"), name="root")

# Optional: Serve index.html for any unknown routes
@app.get("/{catch_all:path}", include_in_schema=False)
async def catch_all(request: Request):
    # get path index file from 'static/index.html'
    return {"html": open(f"{BASE_DIR}/static/index.html").read()} 

def run_fastapi_server(): 
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Run FastAPI server in a separate thread
server_thread = threading.Thread(target=run_fastapi_server)
server_thread.daemon = True  # Allow the program to exit even if the thread is still running
server_thread.start()

def is_dev_mode():
    """Check if running in development mode"""
    return os.getenv('DEV_MODE') == '1' or not getattr(sys, 'frozen', False)

def get_frontend_url():
    """Get appropriate frontend URL based on mode"""
    # return 'http://localhost:5173'
    return 'http://localhost:5173' if is_dev_mode() else 'http://localhost:8000/index.html'


def get_app_settings():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_session = AsyncSession(engine)
        handler = SettingsDBHandler(async_session)
        settings = loop.run_until_complete(handler.get_settings())
        return {
            "status": "success",
            "settings": settings
        }
    finally:
        if async_session:
            loop.run_until_complete(async_session.close()) 

def create_window():
    # Create a window with exposed JavaScript API
    import time
    time.sleep(1)  # Wait for 1 second

    # Create API instance with all the methods
    api = Api()

    print(f"_____API_INSTANCE: {api}") 
    
    window = webview.create_window(
        'Amebae SEO',
        get_frontend_url(),
        js_api=api,
        width=960,          # Initial width
        height=600,         # Initial height
        min_size=(800, 600),
        text_select=True
    )
    
    
    # Start the application with debug enabled
    webview.start(debug=True)

if __name__ == "__main__":
    create_window()