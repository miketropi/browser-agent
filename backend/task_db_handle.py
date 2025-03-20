from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models import Task
from typing import List, Optional

class TaskDBHandler:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, target_website: str, search_keyword: str, loop: int = 1, status: str = "pending") -> Task:
        """Create a new task"""
        task = Task(
            target_website=target_website,
            search_keyword=search_keyword,
            loop=loop,
            status=status
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID""" 
        query = select(Task).where(Task.id == task_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        query = select(Task).order_by(Task.ordering, Task.date_add)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_tasks_by_status(self, status: str) -> List[Task]:
        """Get tasks by status"""
        query = select(Task).where(Task.status == status).order_by(Task.ordering, Task.date_add)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_task_status(self, task_id: int, status: str) -> Optional[Task]:
        """Update task status"""
        task = await self.get_task(task_id)
        if task:
            task.status = status
            await self.db.commit()
            await self.db.refresh(task)
        return task

    async def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update task fields"""
        task = await self.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            await self.db.commit()
            await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        task = await self.get_task(task_id)
        if task:
            await self.db.delete(task)
            await self.db.commit()
            return True
        return False

    async def update_ordering(self, task_id: int, new_ordering: int) -> Optional[Task]:
        """Update task ordering"""
        return await self.update_task(task_id, ordering=new_ordering)

    async def get_next_pending_task(self) -> Optional[Task]:
        """Get the next pending task based on ordering and date"""
        query = select(Task).where(
            Task.status == "pending"
        ).order_by(Task.ordering, Task.date_add)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
