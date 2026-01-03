# Architecture Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [Project Structure](#project-structure)
4. [Main Components](#main-components)
5. [Data Flow](#data-flow)
6. [Architecture Decisions](#architecture-decisions)
7. [Security](#security)
8. [Performance](#performance)
9. [Deployment](#deployment)

---

## Overview

### Description
[Briefly describe what the application does]

### Technologies Used
- **Frontend/UI:** Streamlit
- **Backend:** Python 3.11+
- **Database:** [PostgreSQL / SQLite / MongoDB / etc.]
- **Caching:** [Redis / Streamlit Cache / etc.]
- **Hosting:** Azure App Service
- **CI/CD:** [GitHub Actions / Azure DevOps / etc.]

### Architectural Goals
1. **Simplicity:** Clear and maintainable code
2. **Modularity:** Independent and reusable components
3. **Scalability:** Able to handle growth
4. **Security:** Data and access protection
5. **Performance:** Optimal response time

---

## Design Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility.

### 2. DRY (Don't Repeat Yourself)
Code reuse through shared functions and components.

### 3. KISS (Keep It Simple, Stupid)
Simple solutions favored over unnecessary complexity.

### 4. YAGNI (You Aren't Gonna Need It)
Implement only what is necessary now.

### 5. Fail Fast
Detect and report errors as early as possible.

---

## Project Structure

```
streamlit-mvp/
├── .claude/                    # Claude Code directives
│   └── instructions.md
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md         # This file
│   ├── CHANGELOG.md            # Version history
│   └── SESSION_SUMMARY.md      # Session summaries
│
├── src/                        # Source code
│   ├── app.py                  # Streamlit entry point
│   │
│   ├── components/             # Reusable UI components
│   │   ├── __init__.py
│   │   ├── header.py           # Application header
│   │   ├── sidebar.py          # Sidebar navigation
│   │   └── footer.py           # Footer
│   │
│   ├── config/                 # Configuration
│   │   ├── __init__.py
│   │   └── settings.py         # Pydantic Settings
│   │
│   ├── utils/                  # Utilities
│   │   ├── __init__.py
│   │   ├── helpers.py          # General helper functions
│   │   ├── validators.py       # Custom validations
│   │   └── formatters.py       # Data formatting
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── [service_name].py
│   │
│   └── models/                 # Data models (Pydantic)
│       ├── __init__.py
│       └── [model_name].py
│
├── tests/                      # Tests
│   ├── __init__.py
│   ├── test_utils.py
│   ├── test_services.py
│   └── test_components.py
│
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── startup.sh                  # Azure startup script
└── README.md                   # Main documentation
```

---

## Main Components

### 1. Application Entry Point (`src/app.py`)

**Responsibility:** Streamlit application orchestration

**Key Functions:**
- `initialize_session_state()`: State configuration
- `configure_page()`: Streamlit configuration
- `main()`: Main entry point

**Dependencies:**
- `src.config.settings`
- `src.components.*`
- `src.services.*`

### 2. Configuration (`src/config/settings.py`)

**Responsibility:** Centralized configuration management

**Pattern:** Singleton with Pydantic Settings

**Managed Variables:**
- Application settings (APP_NAME, DEBUG, etc.)
- Database credentials
- API keys
- External services configuration

**Validation:** Automatic via Pydantic at startup

### 3. Components (`src/components/`)

**Responsibility:** Reusable UI components

**Standard Components:**
- `header.py`: Header with logo and navigation
- `sidebar.py`: Sidebar with menu
- `footer.py`: Footer with information

**Pattern:** render_* functions that return void and use st.* directly

### 4. Services (`src/services/`)

**Responsibility:** Business logic and orchestration

**Pattern:** Classes or functional modules depending on complexity

**Examples:**
- `auth_service.py`: Authentication and authorization
- `data_service.py`: Data operations
- `api_service.py`: External API integration

### 5. Utils (`src/utils/`)

**Responsibility:** Shared utility functions

**Characteristics:**
- Pure functions (no side effects)
- Well tested
- Complete documentation

---

## Data Flow

### Main Flow

```
User Input → Streamlit Widget → Session State → Service Layer → Data Layer → Response
                                       ↓
                                   UI Update
```

### Example: Data Loading

```python
# 1. User interacts
if st.button("Load Data"):

    # 2. Service layer call
    data = data_service.fetch_user_data(user_id)

    # 3. Session state update
    st.session_state.data = data

    # 4. UI update
    st.success("Data loaded!")
    st.dataframe(data)
```

### Caching Strategy

```python
# Cache data expensive to compute
@st.cache_data(ttl=3600)
def fetch_external_data(api_url: str) -> pd.DataFrame:
    """Cache for 1 hour."""
    return requests.get(api_url).json()

# Cache resources (DB connections, etc.)
@st.cache_resource
def get_database_connection():
    """Singleton connection."""
    return create_engine(DATABASE_URL)
```

---

## Architecture Decisions

### ADR-001: Pydantic for Configuration

**Date:** 2026-01-03

**Status:** Accepted

**Context:**
Need to manage environment variables with validation.

**Decision:**
Use Pydantic Settings for:
- Automatic type validation
- Auto-generated documentation
- Defaults and optional values
- IDE autocomplete

**Consequences:**
- ✅ Type safety at startup
- ✅ Clear errors if config is invalid
- ❌ Additional dependency

**Alternatives Considered:**
1. python-decouple: Less validation
2. dynaconf: More complex for our needs

---

### ADR-002: No ORM For Now

**Date:** 2026-01-03

**Status:** Accepted

**Context:**
Simple application without complex relationships.

**Decision:**
Use direct SQL or pandas for data access.

**Consequences:**
- ✅ Fewer dependencies
- ✅ Explicit SQL queries
- ❌ No automatic migrations
- ❌ More boilerplate code

**When to Reconsider:**
If > 5 tables with complex relationships → SQLAlchemy

---

### ADR-003: [Your Decision]

**Date:** [DATE]

**Status:** [Proposed | Accepted | Deprecated | Superseded]

**Context:**
[Describe the context and problem]

**Decision:**
[What decision was made and why]

**Consequences:**
[Positive and negative consequences]

**Alternatives Considered:**
[Other options considered]

---

## Security

### Authentication
- [ ] [Describe auth system if applicable]
- [ ] [JWT / Session / OAuth / etc.]

### Authorization
- [ ] [Role and permission management]
- [ ] [RBAC / ABAC / etc.]

### Data Protection
- [ ] Sensitive variables in .env (never hardcoded)
- [ ] .env in .gitignore
- [ ] Azure Key Vault secrets in production
- [ ] HTTPS mandatory in production

### Input Validation
- [ ] Pydantic models for validation
- [ ] User input sanitization
- [ ] CSRF protection (if applicable)

### Secure Logging
- [ ] No secrets in logs
- [ ] Sensitive data masking
- [ ] Centralized logs (Azure Monitor)

---

## Performance

### Streamlit Optimizations

#### Caching
```python
# Cache data (invalidated after TTL)
@st.cache_data(ttl=600)
def expensive_computation(param):
    # ...

# Cache resources (never automatically invalidated)
@st.cache_resource
def get_db_connection():
    # ...
```

#### Session State
```python
# Avoid recomputes
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = process_data()

# Reuse
data = st.session_state.processed_data
```

### Database
- [ ] Indexes on frequently queried columns
- [ ] Connection pooling
- [ ] Query optimization
- [ ] Pagination for large datasets

### Frontend
- [ ] Lazy loading of heavy components
- [ ] Image compression
- [ ] Minimize re-renders

### Monitoring
- [ ] Azure Application Insights
- [ ] Endpoint response times
- [ ] Memory usage
- [ ] Errors and exceptions

---

## Deployment

### Environments

#### Development
- Local machine
- .env with dev variables
- DEBUG=True
- Hot reload enabled

#### Staging
- Azure App Service (Staging slot)
- Environment variables via Azure
- DEBUG=False
- Automatic integration tests

#### Production
- Azure App Service (Production slot)
- Secrets via Azure Key Vault
- DEBUG=False
- Active monitoring
- Automatic backup

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml (example)
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run tests
        run: pytest

      - name: Build Docker image
        run: docker build -t myapp .

      - name: Push to Azure
        # ... deployment steps
```

### Rollback Strategy
- Azure Deployment Slots for instant swap
- Keep last 3 deployed versions
- Documented rollback plan

---

## Maintenance

### Logs
- **Location:** Azure App Service Logs
- **Retention:** 30 days
- **Analysis:** Azure Monitor / Log Analytics

### Backups
- **Database:** Automatic daily backup
- **Config:** Versioned in git
- **Retention:** 7 days (rolling)

### Monitoring Alerts
- [ ] Response time > 2s
- [ ] Error rate > 1%
- [ ] Memory usage > 80%
- [ ] Disk usage > 85%

---

## Future Evolution

### Technical Roadmap

#### Short Term (1-3 months)
- [ ] Add integration tests
- [ ] Improve monitoring
- [ ] API documentation

#### Medium Term (3-6 months)
- [ ] Migrate to microservices (if necessary)
- [ ] Distributed cache (Redis)
- [ ] CDN for static assets

#### Long Term (6-12 months)
- [ ] Multi-region deployment
- [ ] Advanced auto-scaling
- [ ] Machine Learning pipeline

---

**Version:** 1.0
**Last Updated:** 2026-01-03
**Next Review:** [DATE]
