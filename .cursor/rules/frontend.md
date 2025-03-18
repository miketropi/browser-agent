# Vite React Development Guidelines

## Project Structure
- Keep a clear and consistent project structure:
```
src/
├── assets/        # Static files (images, fonts, etc.)
├── components/    # Reusable UI components
├── hooks/         # Custom React hooks
├── layouts/       # Layout components
├── pages/         # Page components
├── services/      # API services and external integrations
├── store/         # State management (Zustand)
└── utils/         # Utility functions
```

## Code Organization

### Components
- Use functional components with PropTypes
- Follow single responsibility principle
- Keep components small and focused
- Use proper naming convention: PascalCase for components
- Separate complex logic into custom hooks
- Implement proper prop validation
```javascript
import PropTypes from 'prop-types';

function Button({ onClick, children, variant = 'primary' }) {
  return (
    <button onClick={onClick} className={`btn-${variant}`}>
      {children}
    </button>
  );
}

Button.propTypes = {
  onClick: PropTypes.func.isRequired,
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary'])
};
```

### State Management
- Use React Query for server state
- Choose appropriate state management:
  - Local state: `useState`
  - Complex local state: `useReducer`
  - Global state: Zustand
- Avoid prop drilling by using Context API

## Performance Optimization
- Implement code splitting using `React.lazy` and `Suspense`
- Use proper memoization (`useMemo`, `useCallback`)
- Optimize images and assets
- Implement proper lazy loading
- Use virtual scrolling for long lists

## Development Best Practices

### Vite Configuration
- Configure aliases for clean imports
```javascript
// vite.config.js
export default defineConfig({
  resolve: {
    alias: {
      '@': '/src',
      '@components': '/src/components',
      '@styles': '/src/styles'
    }
  }
})
```

### Environment Variables
- Use `.env` files properly:
  - `.env`: Default values
  - `.env.development`: Development-specific
  - `.env.production`: Production-specific
- Always prefix with `VITE_` for client-side variables

### Debugging
- Configure source maps properly
- Use React Developer Tools
- Implement proper error boundaries
- Use logging effectively in development
```javascript
if (import.meta.env.DEV) {
  console.log('Debug info:', data);
}
```

### Testing
- Write unit tests for components using Vitest
- Implement E2E tests using Cypress/Playwright
- Use React Testing Library for component testing
- Maintain good test coverage

## Code Quality

### ESLint & Prettier
- Configure ESLint for React
- Use Prettier for consistent formatting
- Implement pre-commit hooks using husky
- Configure import sorting

### Error Handling
- Implement proper error boundaries
- Use try-catch blocks appropriately
- Handle async errors properly
- Show user-friendly error messages

## Build & Deployment
- Optimize build configuration
- Implement proper CI/CD pipeline
- Use build-time environment variables
- Configure proper caching strategies

## Documentation
- Document complex logic and algorithms
- Use JSDoc for component props
- Maintain a changelog
- Document environment setup

## Security
- Implement proper CORS policies
- Sanitize user inputs
- Use HTTPS in production
- Keep dependencies updated
- Implement proper authentication/authorization

## Monitoring & Maintenance
- Implement error tracking (e.g., Sentry)
- Monitor performance metrics
- Regular dependency updates
- Code review guidelines

## VSCode Setup
Recommended extensions:
- ESLint
- Prettier
- JavaScript (ES6+)
- Error Lens
- Import Cost
- Path Intellisense

## Git Workflow
- Use meaningful commit messages
- Follow conventional commits
- Create feature branches
- Regular rebasing with main branch

Remember:
- Keep code DRY (Don't Repeat Yourself)
- Follow SOLID principles
- Write self-documenting code
- Regular code reviews
- Continuous learning and improvement
