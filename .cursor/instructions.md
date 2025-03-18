# Browser Agent Project

A desktop application that combines Python 3.11 backend with Vite React frontend, featuring real-time updates and modern development practices.

## Project Overview

### Purpose
Browser Agent is a desktop application designed to [Add specific project purpose here].

### Key Features
- Real-time code updates during development
- Modern React UI with TailwindCSS
- Efficient state management with Zustand
- Hot Module Replacement (HMR)
- Python 3.11 backend with modern features

## Project Structure

```
browser-agent/
├── backend/                 # Python backend (v3.11)
│   ├── src/                # Source code
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core business logic
│   │   ├── models/        # Data models
│   │   ├── services/      # Business services
│   │   └── utils/         # Utility functions
│   ├── tests/             # Test files
│   │   ├── unit/         # Unit tests
│   │   └── integration/  # Integration tests
│   ├── .env              # Environment variables
│   ├── .env.example      # Example environment config
│   ├── requirements.txt  # Production dependencies
│   └── requirements-dev.txt # Development dependencies
│
└── frontend/              # Vite React frontend
    ├── src/              # React source code
    │   ├── components/   # Reusable UI components
    │   ├── pages/       # Page components
    │   ├── hooks/       # Custom React hooks
    │   ├── store/       # Zustand state management
    │   ├── utils/       # Utility functions
    │   └── App.jsx      # Root component
    ├── public/          # Static assets
    ├── index.html       # Entry HTML file
    ├── package.json     # Node.js dependencies
    └── vite.config.js   # Vite configuration
```

## Technology Stack

### Backend (Python 3.11)
- **Framework**: [Add backend framework]
- **Virtual Environment**: nv + venv
- **API**: [Add API framework]
- **Database**: [Add database if applicable]
- **Testing**: pytest
- **Code Quality**: black, flake8, mypy

### Frontend (Vite + React)
- **Framework**: React 18+
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: Zustand + Immer
- **Package Manager**: npm/yarn
- **Code Quality**: ESLint, Prettier

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 16+
- npm or yarn
- Git

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Set up Python environment:
   ```bash
   # Create and activate virtual environment
   nv use 3.11
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # On Windows use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   # Install production dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

4. Configure environment:
   ```bash
   # Copy example environment file
   cp .env.example .env
   # Edit .env with your configurations
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or using yarn
   yarn install
   ```

3. Configure environment:
   ```bash
   # Copy example environment file
   cp .env.example .env
   ```

## Development Workflow

### Running the Application

1. Start the backend server:
   ```bash
   # In backend directory with activated virtual environment
   python main.py
   ```

2. Start the frontend development server:
   ```bash
   # In frontend directory
   npm run dev
   # or using yarn
   yarn dev
   ```

3. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:[port]

### Development Guidelines

#### Backend Development
- Follow PEP 8 style guide
- Use type hints for all functions and classes
- Write unit tests for new features
- Document functions and modules using docstrings
- Run linting and type checking before commits:
  ```bash
  # In backend directory
  black .
  flake8
  mypy .
  ```

#### Frontend Development
- Follow React best practices
- Use PropTypes for prop validation
- Implement component-based architecture
- Write unit tests for components
- Run linting before commits:
  ```bash
  # In frontend directory
  npm run lint
  # or
  yarn lint
  ```

### Testing

#### Backend Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_specific.py
```

#### Frontend Testing
```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage
```

## Build and Deployment

### Building for Production

1. Backend:
   ```bash
   # Additional backend build steps if needed
   ```

2. Frontend:
   ```bash
   # Build frontend assets
   npm run build
   # or
   yarn build
   ```

### Deployment
[Add deployment instructions specific to your setup]

## Configuration

### Backend Configuration
- Environment variables in `.env`
- Logging configuration
- Database settings (if applicable)

### Frontend Configuration
- Vite configuration in `vite.config.js`
- Environment variables in `.env`
- TailwindCSS configuration

## Troubleshooting

### Common Issues
1. **Virtual Environment Issues**
   - Ensure Python 3.11 is installed
   - Verify virtual environment activation

2. **Node.js Dependencies**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility

3. **Development Server Issues**
   - Check port conflicts
   - Verify environment configurations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes following conventional commits
4. Push to the branch
5. Create a Pull Request

## License
[Add license information]

## Support
[Add support contact information]

## Changelog
[Add changelog or link to changelog file]
