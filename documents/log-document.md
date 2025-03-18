# LogHistory Documentation

## Overview
The `LogHistory` class is a robust logging solution designed to manage and store project history logs with structured data in JSON format. It provides an easy-to-use interface for tracking actions, events, and system changes with detailed timestamps and categorization.

## Features
- JSON-based persistent storage
- Structured log entries with timestamps
- Category-based logging
- Flexible querying and filtering
- Date range filtering
- Keyword search capabilities
- Thread-safe operations

## Installation
The required packages are already included in `requirements.txt`:
```bash
pip install -r backend/requirements.txt
```

## Basic Usage

### Initializing the Logger
```python
from backend.log import LogHistory

# Create a new logger instance
logger = LogHistory("history.json")
```

### Adding Log Entries
```python
# Basic log entry
logger.add_entry(
    action="user_login",
    details={
        "user_id": "12345",
        "ip_address": "192.168.1.1"
    },
    category="authentication"
)

# System event log
logger.add_entry(
    action="system_startup",
    details={
        "version": "1.0.0",
        "environment": "production"
    },
    category="system"
)
```

### Retrieving Logs
```python
# Get all logs
all_logs = logger.get_history()

# Get last 5 logs
recent_logs = logger.get_history(limit=5)

# Get logs by category
auth_logs = logger.get_history(category="authentication")

# Get latest entry
latest = logger.get_latest_entry()
```

### Searching Logs
```python
from datetime import datetime, timedelta

# Search with date range
start_date = datetime.now() - timedelta(days=7)
search_results = logger.search_history(
    keyword="login",
    start_date=start_date
)
```

## API Reference

### Class: LogHistory

#### Constructor
```python
LogHistory(log_file: str = "history.json")
```
- `log_file`: Path to the JSON file where history will be stored

#### Methods

##### add_entry
```python
add_entry(action: str, details: Dict[str, Any], category: str = "general") -> None
```
Adds a new entry to the history log.
- `action`: The type of action performed
- `details`: Additional details about the action
- `category`: Category of the action (e.g., "user", "system", "error")

##### get_history
```python
get_history(
    limit: Optional[int] = None,
    category: Optional[str] = None,
    action: Optional[str] = None
) -> List[Dict[str, Any]]
```
Retrieves history entries with optional filtering.
- `limit`: Maximum number of entries to return
- `category`: Filter by category
- `action`: Filter by action type
- Returns: List of matching history entries

##### get_latest_entry
```python
get_latest_entry() -> Optional[Dict[str, Any]]
```
Gets the most recent history entry.
- Returns: The latest history entry or None if history is empty

##### search_history
```python
search_history(
    keyword: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[Dict[str, Any]]
```
Searches history entries containing a keyword and optional date range.
- `keyword`: Keyword to search for in action or details
- `start_date`: Start date for filtering
- `end_date`: End date for filtering
- Returns: List of matching history entries

##### clear_history
```python
clear_history() -> None
```
Clears all history entries.

## Log Entry Structure
Each log entry is stored in the following JSON format:
```json
{
    "timestamp": "2024-03-14T10:30:45.123456",
    "action": "user_action",
    "category": "authentication",
    "details": {
        "user_id": "123",
        "action_type": "login",
        "ip_address": "192.168.1.1"
    }
}
```

## Best Practices
1. **Consistent Categories**: Use consistent category names across your application
2. **Detailed Actions**: Make action names descriptive and specific
3. **Structured Details**: Keep the details dictionary well-organized and consistent
4. **Regular Maintenance**: Implement log rotation or cleanup for large log files
5. **Error Handling**: Always handle potential I/O errors when working with log files

## Error Handling
The class handles common errors gracefully:
- File I/O errors
- JSON parsing errors
- Invalid date formats
- Missing or corrupt log files

## Thread Safety
The class implements basic thread safety for file operations, making it suitable for multi-threaded applications.

## Examples

### Error Logging
```python
try:
    # Some operation
    raise Exception("Database connection failed")
except Exception as e:
    logger.add_entry(
        action="error",
        details={
            "error_type": type(e).__name__,
            "message": str(e),
            "stack_trace": traceback.format_exc()
        },
        category="error"
    )
```

### API Request Logging
```python
logger.add_entry(
    action="api_request",
    details={
        "endpoint": "/api/users",
        "method": "POST",
        "status_code": 201,
        "response_time": "120ms"
    },
    category="api"
)
```

### System Monitoring
```python
logger.add_entry(
    action="system_metrics",
    details={
        "cpu_usage": "45%",
        "memory_usage": "1.2GB",
        "disk_space": "80%"
    },
    category="monitoring"
)
```
