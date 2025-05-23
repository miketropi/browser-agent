from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models import Settings
from typing import List, Optional

class SettingsDBHandler:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Get all settings from the database
    # Usage:
    # async_session = AsyncSession(engine)
    # handler = SettingsDBHandler(async_session)
    # settings = await handler.get_settings()
    async def get_settings(self):
        """
        Get all settings from the database
        
        Returns:
            Dictionary with setting names and values
            Example: {processDelay: "600", openaiKey: "123", proxyDataUrl: "https://url..."}
        """
        query = select(Settings)
        result = await self.db.execute(query)
        settings = result.scalars().all()
        
        # Convert to dictionary
        settings_dict = {}
        for setting in settings:
            settings_dict[setting.name] = setting.value
            
        return settings_dict

    # Update settings in the database
    # Usage:
    # async_session = AsyncSession(engine)
    # handler = SettingsDBHandler(async_session)
    # settings_data = {"processDelay": "600", "openaiKey": "sk-123456", "proxyDataUrl": "https://example.com/data.json"}
    # updated_settings = await handler.update_settings(settings_data)
    async def update_settings(self, settings_data: dict):
        """
        Update multiple settings in the database 
        
        Args:
            settings_data: Dictionary with setting names and values
                Example: {processDelay: "600", openaiKey: "123", proxyDataUrl: "https://url..."}
        """
        for name, value in settings_data.items():
            # Check if setting exists
            query = select(Settings).where(Settings.name == name)
            result = await self.db.execute(query)
            setting = result.scalar_one_or_none()
            
            if setting:
                # Update existing setting
                query = update(Settings).where(Settings.name == name).values(value=value)
                await self.db.execute(query)
            else:
                # Create new setting
                new_setting = Settings(name=name, value=value)
                self.db.add(new_setting)
                
        await self.db.commit()
        return await self.get_settings()
