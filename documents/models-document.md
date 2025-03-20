# Models Documentation

## Overview
This document provides information about the database models used in the browser-agent project.

## Task Model
The Task model is defined in `backend/models.py` and represents a browser automation task.

### Fields

| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | Integer | Primary key | Auto-increment, Indexed |
| target_website | String | Target website URL | Required (non-null) |
| search_keyword | String | Search keyword for Google | Required (non-null) |
| loop | Integer | Number of iterations | Default: 1 |
| status | String | Task status | Default: "pending" |
| ordering | Integer | Sort order | Default: 0 |
| date_add | DateTime | Creation timestamp | Auto-set on creation |

### Status Values
The `status` field can have the following values:
- `pending`: Task is waiting to be processed
- `running`: Task is currently being executed
- `completed`: Task has finished successfully
- `failed`: Task encountered an error

### Usage Examples

#### Creating a New Task
```python
from models import Task
from sqlalchemy.ext.asyncio import AsyncSession

async def create_task(db: AsyncSession, target_website: str, search_keyword: str, loop: int = 1):
    task = Task(
        target_website=target_website,
        search_keyword=search_keyword,
        loop=loop
    )
    db.add(task)
    await db.commit()
    return task
```

#### Querying Tasks
```python
# Get all tasks
tasks = await db.query(Task).all()

# Get pending tasks
pending_tasks = await db.query(Task).filter(Task.status == "pending").all()

# Get task by ID
task = await db.query(Task).filter(Task.id == task_id).first()
```

#### Updating Task Status
```python
async def update_task_status(db: AsyncSession, task_id: int, new_status: str):
    task = await db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = new_status
        await db.commit()
```

#### Deleting a Task
```python
async def delete_task(db: AsyncSession, task_id: int):
    task = await db.query(Task).filter(Task.id == task_id).first()
    if task:
        await db.delete(task)
        await db.commit()
```

### Best Practices
1. Always use async/await when working with the database
2. Handle database sessions properly using the provided `get_db()` dependency
3. Use appropriate status values to track task progress
4. Implement proper error handling for database operations
5. Use transactions for data consistency

### Database Schema
The Task table is automatically created with the following SQL structure:
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_website VARCHAR NOT NULL,
    search_keyword VARCHAR NOT NULL,
    loop INTEGER DEFAULT 1,
    status VARCHAR DEFAULT 'pending',
    ordering INTEGER DEFAULT 0,
    date_add DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Dependencies
The Task model requires:
- SQLAlchemy
- aiosqlite (for async SQLite support)
- Python 3.7+ (for async/await support)
