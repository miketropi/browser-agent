# TaskDBHandler Documentation

## Overview
The `TaskDBHandler` class provides a comprehensive interface for managing browser automation tasks in the database. It implements CRUD (Create, Read, Update, Delete) operations and additional utility methods for task management.

## Class Structure

### Initialization
```python
class TaskDBHandler:
    def __init__(self, db: AsyncSession):
        self.db = db
```
- Takes an SQLAlchemy async session as a parameter
- Used for all database operations

## Methods

### Create Operations

#### create_task
```python
async def create_task(self, target_website: str, search_keyword: str, loop: int = 1) -> Task
```
Creates a new task in the database.
- **Parameters**:
  - `target_website`: Target website URL (required)
  - `search_keyword`: Search keyword for Google (required)
  - `loop`: Number of iterations (default: 1)
- **Returns**: Created Task object
- **Example**:
```python
task = await handler.create_task(
    target_website="example.com",
    search_keyword="test keyword",
    loop=2
)
```

### Read Operations

#### get_task
```python
async def get_task(self, task_id: int) -> Optional[Task]
```
Retrieves a single task by ID.
- **Parameters**:
  - `task_id`: ID of the task to retrieve
- **Returns**: Task object or None if not found
- **Example**:
```python
task = await handler.get_task(task_id=1)
```

#### get_all_tasks
```python
async def get_all_tasks(self) -> List[Task]
```
Retrieves all tasks ordered by priority and creation date.
- **Returns**: List of all tasks
- **Example**:
```python
all_tasks = await handler.get_all_tasks()
```

#### get_tasks_by_status
```python
async def get_tasks_by_status(self, status: str) -> List[Task]
```
Retrieves tasks filtered by status.
- **Parameters**:
  - `status`: Status to filter by (pending, running, completed, failed)
- **Returns**: List of tasks with specified status
- **Example**:
```python
pending_tasks = await handler.get_tasks_by_status("pending")
```

#### get_next_pending_task
```python
async def get_next_pending_task(self) -> Optional[Task]
```
Retrieves the next pending task based on ordering and creation date.
- **Returns**: Next pending task or None if no pending tasks exist
- **Example**:
```python
next_task = await handler.get_next_pending_task()
```

### Update Operations

#### update_task_status
```python
async def update_task_status(self, task_id: int, status: str) -> Optional[Task]
```
Updates the status of a task.
- **Parameters**:
  - `task_id`: ID of the task to update
  - `status`: New status value
- **Returns**: Updated Task object or None if not found
- **Example**:
```python
updated_task = await handler.update_task_status(task_id=1, status="running")
```

#### update_task
```python
async def update_task(self, task_id: int, **kwargs) -> Optional[Task]
```
Updates any fields of a task.
- **Parameters**:
  - `task_id`: ID of the task to update
  - `**kwargs`: Fields to update and their values
- **Returns**: Updated Task object or None if not found
- **Example**:
```python
updated_task = await handler.update_task(
    task_id=1,
    target_website="new-example.com",
    loop=3
)
```

#### update_ordering
```python
async def update_ordering(self, task_id: int, new_ordering: int) -> Optional[Task]
```
Updates the ordering priority of a task.
- **Parameters**:
  - `task_id`: ID of the task to update
  - `new_ordering`: New ordering value
- **Returns**: Updated Task object or None if not found
- **Example**:
```python
updated_task = await handler.update_ordering(task_id=1, new_ordering=5)
```

### Delete Operations

#### delete_task
```python
async def delete_task(self, task_id: int) -> bool
```
Deletes a task from the database.
- **Parameters**:
  - `task_id`: ID of the task to delete
- **Returns**: True if deleted, False if not found
- **Example**:
```python
success = await handler.delete_task(task_id=1)
```

## Usage Examples

### FastAPI Integration
```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from task_db_handle import TaskDBHandler

app = FastAPI()

@app.post("/tasks")
async def create_task(
    target_website: str,
    search_keyword: str,
    loop: int = 1,
    db: AsyncSession = Depends(get_db)
):
    handler = TaskDBHandler(db)
    return await handler.create_task(target_website, search_keyword, loop)

@app.get("/tasks/pending")
async def get_pending_tasks(db: AsyncSession = Depends(get_db)):
    handler = TaskDBHandler(db)
    return await handler.get_tasks_by_status("pending")
```

## Best Practices
1. Always use async/await when calling methods
2. Handle potential None returns appropriately
3. Use appropriate status values (pending, running, completed, failed)
4. Implement proper error handling
5. Use transactions for data consistency
6. Keep database sessions properly managed

## Dependencies
- SQLAlchemy
- aiosqlite
- Python 3.7+ (for async/await support)
