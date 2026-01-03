# Streamlit MVP Framework - Claude Code Instructions

## 🎯 Mission
Maintain professional, documented Python code that's deployable to Azure App Service for all Streamlit projects.

## 📝 Documentation Standards

### 1. Python Code - Mandatory Documentation

**Golden Rule:** All code in `src/` must be documented with Google-style docstrings.

#### Mandatory Type Hints
- All function parameters
- All function returns
- Complex variables

#### Docstring Format

```python
def process_user_data(user_id: int, data: dict[str, Any]) -> UserModel:
    """
    Process user data and return a validated model.

    This function validates raw data, applies necessary transformations,
    and returns a user model instance.

    Args:
        user_id: Unique user identifier (must be > 0)
        data: Dictionary containing raw user data
            Expected format: {"name": str, "email": str, "age": int}

    Returns:
        UserModel: Validated user model instance with all fields

    Raises:
        ValueError: If user_id is negative or zero
        ValidationError: If data fails Pydantic validation

    Example:
        >>> user_data = {"name": "John", "email": "john@example.com", "age": 30}
        >>> user = process_user_data(1, user_data)
        >>> print(user.name)
        'John'
    """
    if user_id <= 0:
        raise ValueError(f"user_id must be positive, received: {user_id}")

    # Validation and processing...
    return UserModel(**data)
```

#### Comments in English
- Explain complex logic
- Document technical decisions
- Clarify the "why" not just the "what"

```python
# Use cache to avoid repeated API calls
# Performance critical: this function is called on every render
@st.cache_data(ttl=3600)
def fetch_user_data(user_id: int) -> dict[str, Any]:
    """Fetch user data from the API."""
    # ...
```

### 2. Mandatory Tracking Files

#### SESSION_SUMMARY.md

**When:** Create/update after each significant development session

**Standard Format:**
```markdown
# Session - [DATE YYYY-MM-DD]

## 🎯 Session Goals
- Primary objective
- Secondary objectives

## ✅ Changes Made

### Modified Files
- `src/app.py` - Description of modifications
- `src/utils/helpers.py` - New functions added
- `docs/CHANGELOG.md` - Updated

### New Features
1. **Feature Name** - Detailed description
   - Files affected
   - Technical decisions made

### Bug Fixes
- **Bug #1**: Problem description and solution
- **Bug #2**: Problem description and solution

## 🔧 Technical Decisions

### Architecture
- Decision 1: Why and how
- Decision 2: Alternatives considered and final choice

### Dependencies
- New dependencies added and justification
- Updates to existing dependencies

## 🐛 Problems Encountered

### Problem 1
- **Description:** What didn't work
- **Solution:** How it was resolved
- **Learnings:** What we learned

## 📋 TODO

### High Priority
- [ ] Urgent task 1
- [ ] Urgent task 2

### Medium Priority
- [ ] Improvement 1
- [ ] Improvement 2

### Low Priority
- [ ] Nice to have 1

## 📊 Metrics (if applicable)
- Tests passing: X/Y
- Coverage: XX%
- Performance: improvement/degradation noted

## 🔗 References
- Links to relevant documentation
- Related GitHub issues
- Associated PRs
```

#### CHANGELOG.md

**Format:** [Keep a Changelog](https://keepachangelog.com/)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features that have been added

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes

## [1.0.0] - 2026-01-03

### Added
- Initial release
- Core feature X
- Core feature Y

### Changed
- Improved performance of Z

### Fixed
- Bug in authentication flow
```

### 3. Python Code Structure

#### Function Organization

**Strict Rules:**
1. **No loose code** - Everything in functions
2. **Short functions** - Maximum 50 lines (ideal: 20-30)
3. **Single Responsibility** - One function = one responsibility
4. **Clear naming** - Name should explain what the function does

**Standard app.py Structure:**

```python
"""
Main Streamlit application.

This module orchestrates the user interface and coordinates
the different components of the MVP application.

Author: The Streamlit Guy
Date: 2026-01-03
"""

import streamlit as st
from typing import Optional

from src.config.settings import get_settings
from src.utils.helpers import setup_logging
from src.components.sidebar import render_sidebar
from src.components.header import render_header


def initialize_session_state() -> None:
    """
    Initialize Streamlit session state variables.

    This function configures all necessary session variables
    for the application to function properly. It's idempotent and can
    be called multiple times without side effects.

    Session State Variables:
        user (Optional[dict]): Logged-in user information
        page (str): Current application page
        data_loaded (bool): Indicator if data has been loaded
    """
    if 'user' not in st.session_state:
        st.session_state.user = None

    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


def configure_page() -> None:
    """
    Configure Streamlit page with basic settings.

    Sets the title, icon, layout and other Streamlit page configurations.
    """
    settings = get_settings()

    st.set_page_config(
        page_title=settings.APP_NAME,
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def main() -> None:
    """
    Main entry point for the Streamlit application.

    This function orchestrates the initialization and rendering of the application.
    It should remain simple and delegate complex logic to other functions.
    """
    # Configuration
    setup_logging()
    configure_page()
    initialize_session_state()

    # Render interface
    render_header()
    render_sidebar()

    # Main logic based on current page
    page = st.session_state.page

    if page == 'home':
        render_home_page()
    elif page == 'dashboard':
        render_dashboard_page()
    else:
        st.error(f"Unknown page: {page}")


def render_home_page() -> None:
    """Render the home page of the application."""
    st.title("🏠 Home")
    st.write("Welcome to your Streamlit MVP application!")


def render_dashboard_page() -> None:
    """Render the dashboard page with metrics."""
    st.title("📊 Dashboard")
    # Logic...


if __name__ == "__main__":
    main()
```

#### Modularity

**src/utils/helpers.py:**
```python
"""
Shared utility functions.

This module contains reusable helper functions across the application.
"""

import logging
from typing import Any


def setup_logging(level: str = "INFO") -> None:
    """
    Configure the application logging system.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def safe_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely retrieve a value from a dictionary.

    Args:
        data: Source dictionary
        key: Key to retrieve
        default: Default value if key doesn't exist

    Returns:
        The value associated with the key or the default value

    Example:
        >>> data = {"name": "John"}
        >>> safe_get(data, "name")
        'John'
        >>> safe_get(data, "age", 0)
        0
    """
    return data.get(key, default)
```

### 4. Environment Variable Management

#### .env.example - Mandatory Template

This file MUST be present in each repo and updated when new variables are added.

```bash
# =============================================================================
# STREAMLIT MVP - ENVIRONMENT VARIABLES
# =============================================================================
# Copy this file to .env and fill in your actual values
# NEVER commit the .env file!

# -----------------------------------------------------------------------------
# Application Settings
# -----------------------------------------------------------------------------
APP_NAME="Streamlit MVP"
APP_ENV=development  # development, staging, production
DEBUG=True
LOG_LEVEL=INFO

# -----------------------------------------------------------------------------
# Streamlit Configuration
# -----------------------------------------------------------------------------
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=True

# -----------------------------------------------------------------------------
# Azure App Service (if deployed)
# -----------------------------------------------------------------------------
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_APP_SERVICE_NAME=your-app-service-name

# -----------------------------------------------------------------------------
# Database (if applicable)
# -----------------------------------------------------------------------------
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# -----------------------------------------------------------------------------
# API Keys (if applicable)
# -----------------------------------------------------------------------------
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here

# -----------------------------------------------------------------------------
# External Services (if applicable)
# -----------------------------------------------------------------------------
REDIS_URL=redis://localhost:6379/0
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------
SECRET_KEY=your-secret-key-here-min-32-chars
JWT_SECRET=your-jwt-secret-here
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

#### Configuration with Pydantic (src/config/settings.py)

```python
"""
Application configuration with Pydantic validation.

This module manages all environment variables and
ensures their validation at application startup.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Main application configuration.

    All environment variables are automatically loaded and validated
    via Pydantic Settings.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    APP_NAME: str = Field(default="Streamlit MVP")
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")

    # Streamlit
    STREAMLIT_SERVER_PORT: int = Field(default=8501)
    STREAMLIT_SERVER_ADDRESS: str = Field(default="0.0.0.0")

    # Database (optional)
    DATABASE_URL: Optional[str] = Field(default=None)

    # API Keys (optional)
    OPENAI_API_KEY: Optional[str] = Field(default=None)

    @field_validator("APP_ENV")
    @classmethod
    def validate_env(cls, v: str) -> str:
        """Validate that the environment is valid."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"APP_ENV must be one of {allowed}")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate that the log level is valid."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v.upper()


@lru_cache
def get_settings() -> Settings:
    """
    Get the singleton settings instance.

    Uses lru_cache to load settings only once
    and reuse them afterward.

    Returns:
        Validated Settings instance

    Example:
        >>> settings = get_settings()
        >>> print(settings.APP_NAME)
        'Streamlit MVP'
    """
    return Settings()
```

### 5. Azure App Service Configuration

#### Standard Dockerfile

```dockerfile
# Streamlit MVP - Dockerfile for Azure App Service
FROM python:3.11-slim

# Metadata
LABEL maintainer="The Streamlit Guy"
LABEL description="Streamlit MVP Application"

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "src/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
```

#### startup.sh - Azure Startup Script

```bash
#!/bin/bash
# Streamlit MVP - Azure App Service Startup Script

echo "🚀 Starting Streamlit MVP Application..."

# Set default port if not provided by Azure
export PORT=${PORT:-8501}

echo "📦 Environment: ${APP_ENV:-development}"
echo "🔌 Port: ${PORT}"

# Run database migrations if needed
# python -m alembic upgrade head

# Start Streamlit
streamlit run src/app.py \
    --server.port=${PORT} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --logger.level=${LOG_LEVEL:-info}
```

### 6. Git Standards

#### Standard .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Streamlit
.streamlit/secrets.toml
.streamlit/config.toml

# Environment Variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Database
*.db
*.sqlite3

# Temporary files
tmp/
temp/
*.tmp
```

#### Commit Format

**Conventional Commits Standard:**

```
<type>: <short description>

<optional body - detailed description>

<optional footer - references and co-authors>
```

**Standard Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no code change)
- `refactor`: Refactoring (no feat or fix)
- `test`: Adding or modifying tests
- `chore`: Maintenance (deps, config, etc.)

**Example:**
```bash
git commit -m "$(cat <<'EOF'
feat: add user authentication with JWT

Implement JWT-based authentication system with:
- Login/logout endpoints
- Token refresh mechanism
- Password hashing with bcrypt
- Session management in Streamlit

Files changed:
- src/auth/jwt_handler.py (new)
- src/components/login.py (new)
- src/app.py (modified)

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 7. Tests (Optional but Recommended)

#### Test Structure

```python
"""
Tests for utility functions.

This module tests all functions in the utils.helpers module.
"""

import pytest
from src.utils.helpers import safe_get, setup_logging


class TestSafeGet:
    """Tests for the safe_get function."""

    def test_safe_get_existing_key(self):
        """Test retrieving an existing key."""
        data = {"name": "John", "age": 30}
        assert safe_get(data, "name") == "John"
        assert safe_get(data, "age") == 30

    def test_safe_get_missing_key_with_default(self):
        """Test retrieving a missing key with default value."""
        data = {"name": "John"}
        assert safe_get(data, "age", 0) == 0
        assert safe_get(data, "email", "default@example.com") == "default@example.com"

    def test_safe_get_missing_key_without_default(self):
        """Test retrieving a missing key without default value."""
        data = {"name": "John"}
        assert safe_get(data, "age") is None


class TestSetupLogging:
    """Tests for the setup_logging function."""

    def test_setup_logging_default_level(self):
        """Test logging configuration with default level."""
        setup_logging()
        # Verify logging is configured...

    def test_setup_logging_custom_level(self):
        """Test logging configuration with custom level."""
        setup_logging("DEBUG")
        # Verify logging level is DEBUG...
```

## 🚫 Strict Prohibitions

### 1. Documentation
- ❌ **Never a function without docstring** in src/
- ❌ **Never complex code without comments**
- ❌ **Never a parameter without type hint**

### 2. Security
- ❌ **Never hardcoded secrets** in code
- ❌ **Never commit .env** to git
- ❌ **Never API keys in clear text** in logs

### 3. Code Quality
- ❌ **Never use print()** (use logging or st.write)
- ❌ **Never functions > 100 lines** (mandatory refactor)
- ❌ **Never duplicate code** (DRY principle)
- ❌ **Never mutable global variables**

### 4. Streamlit Specifics
- ❌ **Never st.write() for errors** (use st.error)
- ❌ **Never heavy computation without @st.cache_data**
- ❌ **Never chaotic state management**

## ✅ Pre-Commit Checklist

Before each commit, verify:

- [ ] **Documentation**
  - [ ] All new functions have docstrings
  - [ ] Type hints present everywhere
  - [ ] Comments for complex logic

- [ ] **Tracking Files**
  - [ ] SESSION_SUMMARY.md updated
  - [ ] CHANGELOG.md updated if release
  - [ ] .env.example updated if new variables

- [ ] **Code Quality**
  - [ ] No duplicate code
  - [ ] Functions < 50 lines
  - [ ] No hardcoded secrets
  - [ ] Imports organized and sorted

- [ ] **Tests** (if applicable)
  - [ ] All tests pass
  - [ ] New tests for new features
  - [ ] Coverage maintained or improved

- [ ] **Git**
  - [ ] Commit message follows format
  - [ ] .gitignore updated if new files to exclude

## 🎓 Examples and Templates

All templates and examples are available in the `streamlit-claudecode-framework` repo.

To start a new project:
```bash
git clone https://github.com/sonixz/streamlit-claudecode-framework.git my-new-project
cd my-new-project
rm -rf .git
git init
# Follow instructions in README.md
```

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Azure App Service Python](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

**Version:** 1.0.0
**Last Updated:** 2026-01-03
**Maintained by:** The Streamlit Guy
