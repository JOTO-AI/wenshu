# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

智能问数 (Wenshu) is an enterprise-grade private conversational data analysis platform built with a unified application architecture using FastAPI + React + Nx Monorepo.

**Key Architecture**: Unified single-page application supporting both client and admin roles with role-based routing and layouts.

## Development Commands

### Essential Commands
```bash
# Install dependencies
pnpm install

# Start frontend development server (http://localhost:3000)
pnpm dev:web

# Start backend API server (http://localhost:8000) 
pnpm dev:api

# Start all services in parallel (Nx managed)
pnpm dev

# Start all services with concurrently
pnpm dev:all

# Safe development startup (handles zombie processes)
pnpm dev:safe

# Build all projects
pnpm build

# Run tests across all projects
pnpm test

# Lint all code
pnpm lint

# Type checking for all TypeScript projects
pnpm typecheck

# Format code
pnpm format
```

### Backend Python Commands
```bash
# Navigate to API directory
cd apps/api

# Install Python dependencies
uv sync

# Run with hot reload
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Type checking
mypy src/

# Format code
black src/
isort src/
```

### Development Process Management
The project includes `scripts/dev-manager.sh` for managing development processes safely:

```bash
# Clean way to start development (handles zombie processes)
./scripts/dev-manager.sh start

# Check for zombie processes
./scripts/dev-manager.sh check

# Clean up all development processes
./scripts/dev-manager.sh stop

# Reset Nx environment
./scripts/dev-manager.sh reset
```

## Architecture

### Monorepo Structure
```
apps/
├── web-app/         # Unified React application (client + admin)
└── api/             # Python FastAPI backend

libs/
├── shared-types/    # TypeScript type definitions shared between frontend/backend
├── api-client/      # Unified API client library
└── ui/              # shadcn-ui component library (packages/ui symlink)
```

### Frontend Architecture - Unified Application
The frontend uses a **unified application architecture** with role-based feature organization:

```
apps/web-app/src/
├── features/              # Feature modules by role
│   ├── client/           # Regular user features
│   │   ├── chat/        # Core chat functionality
│   │   ├── dashboard/   # Personal dashboard
│   │   ├── profile/     # User profile/settings
│   │   └── dev/         # Development tools (UI testing)
│   └── admin/           # Administrator features
│       ├── analytics/   # Analytics & reporting
│       ├── permissions/ # User & permission management
│       ├── datasources/ # Data source management
│       ├── knowledge/   # Knowledge base management
│       ├── datasets/    # Dataset management
│       └── audit-logs/  # Audit logs
├── layouts/             # Layout components
│   ├── client-layout/   # Client-side layout & sidebar
│   ├── admin-layout/    # Admin-side layout & sidebar
│   └── auth-layout/     # Authentication pages layout
├── routes/              # Route configuration
│   ├── client-routes.tsx # Client routes
│   ├── admin-routes.tsx  # Admin routes
│   └── guards/          # Route guards (auth, admin)
├── auth/               # Authentication module
├── components/         # Shared application components
├── stores/            # Global state management
└── middleware/        # Route guards & permissions
```

### Backend Architecture
```
apps/api/src/
├── main.py            # FastAPI app entry point
├── core/              # Core infrastructure
│   ├── config.py     # Configuration management
│   ├── database.py   # Database connection
│   ├── dependencies.py # Dependency injection
│   └── security.py   # Security utilities
├── auth/              # Authentication module
├── chat/              # Chat functionality
└── users/             # User management
```

### Key Architectural Principles

1. **Unified App with Role-Based Features**: Single React app with `/admin/*` and client routes, different layouts and permissions
2. **Code Splitting**: Admin features are lazy-loaded, regular users don't download admin code
3. **Shared Types**: TypeScript interfaces shared between frontend and backend via `@wenshu/shared-types`
4. **Nx Monorepo**: Efficient build caching, dependency management, and parallel execution

## Technology Stack

### Frontend
- **React 18.3.1** + TypeScript (strict mode)
- **Vite** for build tooling
- **Tailwind CSS v3.4.15** + **shadcn-ui** components
- **React Router v6** with future flags enabled
- **Zustand** for state management
- **@assistant-ui/react** for chat interface

### Backend  
- **Python 3.11+** with **FastAPI**
- **uv** for Python package management
- **PostgreSQL** for database (production)
- **JWT** authentication + **RBAC** permissions

### Development Tools
- **Nx** for monorepo management and build orchestration
- **pnpm** for Node.js package management
- **ESLint + Prettier** for code quality
- **Vitest** for testing
- **MyPy** for Python type checking

## Path Resolution & Import Guidelines

### Critical Import Rules (Prevents Circular Dependencies)

**Within UI Library (`libs/ui/`)**: Always use relative paths
```typescript
// ✅ Correct in libs/ui/src/components/ui/
import { Button } from './button';
import { cn } from '../../lib/utils';
```

**In Applications**: Use workspace aliases
```typescript
// ✅ Correct in apps/web-app/src/
import { Button, Card } from '@workspace/ui';
import { UserAPI } from '@wenshu/api-client';
import { User } from '@wenshu/shared-types';
```

**Path Mappings** (tsconfig.base.json):
```json
{
  "@wenshu/api-client": ["libs/api-client/src/index.ts"],
  "@wenshu/shared-types": ["libs/shared-types/src/index.ts"],
  "@workspace/ui": ["packages/ui/src/index.ts"]
}
```

### Common Import Errors to Avoid

❌ **Never use `@/` paths within libs/ui** - causes circular dependencies
❌ **Never mix relative and workspace alias imports** in same file  
❌ **Never use cross-workspace direct path imports**

## Environment Configuration

Create `.env` in workspace root:
```bash
# Frontend port (default: 3000)
WEB_APP_PORT=3000

# Backend port (default: 8000) 
API_PORT=8000

# CORS origins for API
CORS_ORIGINS=http://localhost:3000
```

## Testing Strategy

### Frontend Testing
```bash
# Run tests for specific project
nx test web-app

# Run tests with coverage
nx test web-app --coverage

# Test specific file
nx test web-app --testNamePattern="ComponentName"
```

### Backend Testing  
```bash
cd apps/api
pytest
pytest --cov=src  # With coverage
```

## Code Quality Standards

### TypeScript Standards
- **Strict mode enabled** - all projects use strict TypeScript
- **Path aliases** - use workspace aliases for cross-project imports
- **Proper typing** - avoid `any`, use proper interfaces from `@wenshu/shared-types`

### Python Standards
- **PEP 8** compliance with Black formatting
- **Type hints** required for all function signatures
- **Pydantic models** for data validation
- **FastAPI dependency injection** pattern

### Development Workflow

1. **Before making changes**: Run `pnpm typecheck` and `pnpm lint`
2. **After changes**: Run affected tests with `nx affected:test`  
3. **Before committing**: Ensure `pnpm build` succeeds
4. **Path imports**: Verify no `@/` imports exist in `libs/ui/` components

## Common Issues & Solutions

### Frontend Issues
- **Build failures**: Usually path import issues - check for `@/` in `libs/ui/`
- **Vite errors**: Clear cache with `rm -rf node_modules/.vite`
- **Type errors**: Run `nx reset` to clear Nx cache

### Backend Issues
- **CORS errors**: Check `CORS_ORIGINS` environment variable
- **Import errors**: Ensure proper Python path structure in `src/`

### Nx Issues
- **Zombie processes**: Use `./scripts/dev-manager.sh cleanup`
- **Cache issues**: Run `nx reset` or `pnpm dev:fast` (skip cache)
- **Graph visualization**: Use `nx graph` to debug dependencies

## Development Guidelines

### Adding New Features
1. **Frontend features**: Add to appropriate `features/client/` or `features/admin/` directory
2. **Backend features**: Follow existing module structure (`router.py`, `schemas.py`, `service.py`, `models.py`)
3. **Shared types**: Add to `libs/shared-types/src/` and export from `index.ts`
4. **UI components**: Add to `libs/ui/src/components/ui/` using relative imports

### Code Style
- **No unnecessary comments** unless documenting complex business logic
- **Descriptive variable names** that self-document code intent
- **Single responsibility** - functions/components do one thing well
- **Early returns** to reduce nesting depth

## Security Guidelines

- **Input validation**: All API endpoints use Pydantic schemas
- **Authentication**: JWT tokens with proper expiration
- **CORS**: Properly configured for development and production
- **No secrets in code**: Use environment variables
- **RBAC**: Role-based access control for admin features