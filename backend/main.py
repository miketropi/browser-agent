from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import webview as pywebview
import os
from pydantic import SecretStr
from database import Base, engine
from sqlalchemy.ext.asyncio import AsyncSession
from models import Task  # Import Task model to ensure it's registered
from task_db_handle import TaskDBHandler

pywebview.debug = True

from log import LogHistory
log = LogHistory('../log.json')

from langchain_openai import ChatOpenAI
from browser_use import Agent, AgentHistoryList, Browser, BrowserConfig
from dotenv import load_dotenv
import asyncio
import json
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Initialize database
@app.on_event("startup")
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
    * Check the search results for links under the domain {target_website} (very important).
    * If not found on the current page: Scroll to end page click the "Next" button (or next page numbers) at the bottom of Google to check subsequent pages.
4. Visit the Target Website:
    * Once you find a result matching the domain, click the link to navigate to {target_website}.
"""
        
        llm2 = ChatOpenAI(model="gpt-4o-mini")
        browser_use_browser2 = Browser(
            config=BrowserConfig(
                headless=False,
                # chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
                # extra_chromium_args=['--profile-directory=Default'],
            )
        )

        agent = Agent(
            task=message,
            llm=llm2,
            browser=browser_use_browser2,
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
        self.db = None

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
    
    def get_tasks(self, status=None, ordering=None):
        """Get tasks from the database
        
        Args:
            status (str, optional): Filter tasks by status (pending, running, completed, failed)
            ordering (int, optional): Filter tasks by ordering value
            
        Returns:
            dict: Response containing tasks information or error
        """
        try:
            # Create event loop if not exists
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Create database session
            async_session = AsyncSession(engine)
            handler = TaskDBHandler(async_session)
            
            # Get tasks based on parameters
            if status:
                tasks = loop.run_until_complete(handler.get_tasks_by_status(status))
            else:
                tasks = loop.run_until_complete(handler.get_all_tasks())
            
            # Filter by ordering if specified
            if ordering is not None:
                tasks = [task for task in tasks if task.ordering == ordering]
            
            # Format response
            return {
                "status": "success",
                "tasks": [{
                    "id": task.id,
                    "target_website": task.target_website,
                    "search_keyword": task.search_keyword,
                    "loop": task.loop,
                    "status": task.status,
                    "ordering": task.ordering,
                    "date_add": task.date_add.isoformat()
                } for task in tasks]
            }
            
        except Exception as e:
            error_message = str(e)
            log.add_entry(
                action='get_tasks',
                details={
                    'error': error_message,
                    'status': status,
                    'ordering': ordering
                }
            )
            return {
                "status": "error",
                "error": error_message
            }
        finally:
            if async_session:
                loop.run_until_complete(async_session.close())

    def add_task(self, task):
        """Add a task to the database"""
        try:
            print(f"_____TASK: {task}")

            # Create event loop if not exists
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        
            # Create database session
            async_session = AsyncSession(engine)
            handler = TaskDBHandler(async_session)

            # Add task to the database
            # loop.run_until_complete(handler.create_task(task))
            # create task to db
            task = loop.run_until_complete(handler.create_task(
                target_website=task.get('target_website'),
                search_keyword=task.get('search_keyword'),
                loop=task.get('loop')
            ))

            return {
                "status": "success",
                "task": {
                    "id": task.id,
                    "target_website": task.target_website,
                    "search_keyword": task.search_keyword,
                    "loop": task.loop,
                    "status": task.status,
                    "ordering": task.ordering,
                    "date_add": task.date_add.isoformat()
                }
            }
        except Exception as e:
            error_message = str(e)
            log.add_entry(
                action='add_task',
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

    def delete_task(self, task_id):
        """Delete a task from the database"""
        try:
            # Create event loop if not exists
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Create database session
            async_session = AsyncSession(engine)
            handler = TaskDBHandler(async_session)  

            # Delete task from the database
            loop.run_until_complete(handler.delete_task(task_id))

            return {
                "status": "success"
            }
        except Exception as e:
            error_message = str(e)
            log.add_entry(
                action='delete_task',
                details={
                    'error': error_message,
                    'task_id': task_id
                }
            )
            return {
                "status": "error",
                "error": error_message
            }
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
        'Amebae SEO',
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