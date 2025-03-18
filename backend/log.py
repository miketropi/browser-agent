import logging
import json
from datetime import datetime
from typing import Optional, Dict, List, Any
from pathlib import Path


class LogHistory:
    """
    A class to manage and store project history logs with structured data.
    Supports JSON storage and retrieval of log entries with timestamps.
    """

    def __init__(self, log_file: str = "history.json"):
        """
        Initialize the LogHistory instance.
        
        Args:
            log_file (str): Path to the JSON file where history will be stored
        """
        self.log_file = Path(log_file)
        self.history: List[Dict[str, Any]] = []
        self._load_history()

    def _load_history(self) -> None:
        """Load existing history from the JSON file if it exists."""
        try:
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading history file: {e}")
            self.history = []

    def _save_history(self) -> None:
        """Save the current history to the JSON file."""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, default=str)
        except IOError as e:
            print(f"Error saving history file: {e}")

    def add_entry(self, action: str, details: Dict[str, Any], category: str = "general") -> None:
        """
        Add a new entry to the history log.
        
        Args:
            action (str): The type of action performed
            details (dict): Additional details about the action
            category (str): Category of the action (e.g., "user", "system", "error")
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "category": category,
            "details": details
        }
        self.history.append(entry)
        self._save_history()

    def get_history(self, 
                   limit: Optional[int] = None, 
                   category: Optional[str] = None, 
                   action: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve history entries with optional filtering.
        
        Args:
            limit (int, optional): Maximum number of entries to return
            category (str, optional): Filter by category
            action (str, optional): Filter by action type
            
        Returns:
            List of history entries matching the criteria
        """
        filtered_history = self.history

        if category:
            filtered_history = [
                entry for entry in filtered_history 
                if entry["category"] == category
            ]

        if action:
            filtered_history = [
                entry for entry in filtered_history 
                if entry["action"] == action
            ]

        if limit:
            filtered_history = filtered_history[-limit:]

        return filtered_history

    def clear_history(self) -> None:
        """Clear all history entries."""
        self.history = []
        self._save_history()

    def get_latest_entry(self) -> Optional[Dict[str, Any]]:
        """
        Get the most recent history entry.
        
        Returns:
            The latest history entry or None if history is empty
        """
        return self.history[-1] if self.history else None

    def search_history(self, 
                      keyword: str, 
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Search history entries containing a keyword and optional date range.
        
        Args:
            keyword (str): Keyword to search for in action or details
            start_date (datetime, optional): Start date for filtering
            end_date (datetime, optional): End date for filtering
            
        Returns:
            List of matching history entries
        """
        results = []
        
        for entry in self.history:
            entry_time = datetime.fromisoformat(entry["timestamp"])
            
            # Check date range if specified
            if start_date and entry_time < start_date:
                continue
            if end_date and entry_time > end_date:
                continue
                
            # Search in action and details
            if (keyword.lower() in entry["action"].lower() or
                any(keyword.lower() in str(v).lower() 
                    for v in entry["details"].values())):
                results.append(entry)
                
        return results


# Example usage
if __name__ == "__main__":
    # Create a log history instance
    history_logger = LogHistory("project_history.json")
    
    # Add some example entries
    history_logger.add_entry(
        action="file_created",
        details={
            "filename": "example.txt",
            "size": 1024,
            "user": "john_doe"
        },
        category="file_system"
    )
    
    history_logger.add_entry(
        action="user_login",
        details={
            "user_id": "12345",
            "ip_address": "192.168.1.1"
        },
        category="user"
    )
    
    # Retrieve recent history
    recent_entries = history_logger.get_history(limit=5)
    
    # Search for specific entries
    search_results = history_logger.search_history(
        keyword="file",
        start_date=datetime.now().replace(hour=0, minute=0)
    )
