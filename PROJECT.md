# Browser Agent Project Setup Guide

## Prerequisites

Before starting, ensure you have the following installed:
- Python 3.11
- Node.js (Latest LTS version)
- Git
- nv (Python version manager)

## Project Structure

```
browser-agent/
├── backend/         # Python backend (v3.11)
│   └── .venv/      # Python virtual environment
└── frontend/       # Vite React frontend
    ├── src/        # React source code
    ├── public/     # Static assets
    └── node_modules/# Node.js dependencies
```

## Step-by-Step Setup Guide

### 1. Clone the Repository

```bash
git clone [repository-url]
cd browser-agent
```

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Set up Python environment:
   ```bash
   # Use Python 3.11 with nv
   nv use 3.11
   
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   # .venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Running the Application

### Start Backend Server

1. Make sure you're in the backend directory with activated virtual environment
2. Run the server:
   ```bash
   python main.py
   ```

### Start Frontend Development Server

1. In a new terminal, navigate to the frontend directory
2. Start the development server:
   ```bash
   npm run dev
   ```

## Development Guidelines

### Frontend Development

- Use JavaScript for all new components and features
- Follow the existing project structure
- Implement styling using TailwindCSS utility classes
- Use Zustand with Immer for state management
- Utilize React hooks for component logic
- Use PropTypes for prop validation

### Backend Development

- Follow PEP 8 style guide for Python code
- Document all API endpoints
- Implement proper error handling
- Use type hints in Python functions

## Available Scripts

### Frontend

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run test` - Run tests (if configured)

### Backend

- `python main.py` - Start the backend server
- `pytest` - Run tests (if configured)

## Technology Stack Details

### Frontend
- Vite + React for fast development and building
- TailwindCSS for utility-first styling
- Zustand + Immer for state management
- JavaScript (ES6+)
- Hot Module Replacement (HMR) enabled

### Backend
- Python 3.11
- Virtual environment management with nv
- RESTful API architecture

## Troubleshooting

### Common Issues

1. Virtual Environment Issues
   - Ensure Python 3.11 is properly installed
   - Check if nv is correctly configured
   - Verify virtual environment activation

2. Node.js Dependencies
   - Clear node_modules and package-lock.json if facing dependency issues
   - Run `npm install` again

3. Port Conflicts
   - Check if ports are already in use
   - Default ports can be configured in respective configuration files

## Contributing

1. Create a new branch for your feature
2. Follow the coding standards
3. Write tests for new features
4. Submit pull requests with detailed descriptions

## Additional Resources

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
