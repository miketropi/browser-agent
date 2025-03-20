# SQLite Documentation

## Overview
This document provides information about the SQLite database setup and usage in the browser-agent project.

## Database Configuration
The SQLite database is configured in `backend/database.py` with the following key components:

### Database URL
```python
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
```
- Database file: `sql_app.db` (created in the backend directory)
- Using `aiosqlite` for async support

### Key Components
1. **Async Engine**
   - Created using SQLAlchemy's async engine
   - Configured with SQLite-specific parameters

2. **Session Management**
   - Async session factory for database operations
   - Automatic session cleanup and error handling

3. **Base Model**
   - Declarative base for all database models
   - Used as the parent class for all model definitions

## Usage Guide

### Database Session
To use the database in your endpoints, inject the database session:

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

@app.get("/items")
async def get_items(db: AsyncSession = Depends(get_db)):
    # Use db session here
    pass
```

### Creating Models
Create new models in `models.py`:

```python
from sqlalchemy import Column, Integer, String
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
```

### Common Operations

#### Create
```python
new_item = Item(name="Example", description="Description")
db.add(new_item)
await db.commit()
```

#### Read
```python
# Get all items
items = await db.query(Item).all()

# Get by ID
item = await db.query(Item).filter(Item.id == 1).first()
```

#### Update
```python
item.name = "Updated Name"
await db.commit()
```

#### Delete
```python
await db.delete(item)
await db.commit()
```

## Best Practices
1. Always use async/await with database operations
2. Use the provided `get_db()` dependency for session management
3. Handle exceptions appropriately
4. Commit transactions after successful operations
5. Use rollback for error handling

## Database Initialization
The database is automatically initialized when the application starts:
- Tables are created based on model definitions
- The database file is created if it doesn't exist

## Dependencies
Required packages for SQLite support:
- `sqlalchemy==2.0.27`
- `aiosqlite==0.19.0`

## Error Handling
The database session includes automatic error handling:
- Commits successful transactions
- Rolls back failed transactions
- Ensures proper session cleanup
