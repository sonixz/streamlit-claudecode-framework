# 🚀 Streamlit Claude Code Framework

A standardized framework for building Streamlit MVPs with best practices baked in.

## 📋 What This Framework Provides

- **Standard Project Structure** - Organized src/, docs/, tests/ layout
- **Claude Code Directives** - AI-powered development standards in `.claude/`
- **Complete Documentation** - Code docs, session tracking, architecture decisions
- **Configuration Management** - Pydantic-based settings with validation
- **Example Code** - Fully documented Python modules following best practices

## 🎯 Philosophy

This framework enforces:

1. **Well-Documented Code** - All functions have docstrings with type hints
2. **Session Tracking** - Document changes with SESSION_SUMMARY.md
3. **Functional Code** - Organized in functions, no code in global scope
4. **Environment Management** - Consistent .env handling across projects
5. **Standardization** - All Streamlit projects follow the same patterns

## 🏗️ Project Structure

```
streamlit-mvp/
├── .claude/                    # Claude Code directives
│   └── instructions.md         # AI development standards
│
├── docs/                       # Documentation
│   ├── SESSION_SUMMARY.template.md
│   ├── CHANGELOG.md
│   └── ARCHITECTURE.md
│
├── src/                        # Source code
│   ├── app.py                  # Main Streamlit entry point
│   ├── config/
│   │   └── settings.py         # Pydantic settings
│   ├── components/
│   │   └── sidebar.py          # UI components
│   └── utils/
│       └── helpers.py          # Utility functions
│
├── tests/                      # Unit tests
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### 1. Clone the Framework

```bash
git clone <this-repo> my-new-project
cd my-new-project
rm -rf .git
git init
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your values
```

### 3. Run the Application

```bash
streamlit run src/app.py
```

Application will be available at `http://localhost:8501`

## 📝 Development Workflow

### Starting a New Session

1. **Update SESSION_SUMMARY.md** - Document what you're working on
2. **Follow Claude Code Directives** - See `.claude/instructions.md`
3. **Write Documented Code** - All functions need docstrings
4. **Update CHANGELOG.md** - Document changes before committing

### Code Standards

**Every function must have:**
- Google-style docstring
- Type hints for all parameters
- Example usage in docstring

```python
def my_function(param: str, count: int = 1) -> list[str]:
    """
    Brief description of what the function does.

    Detailed explanation if needed.

    Args:
        param: Description of param
        count: Description of count (default: 1)

    Returns:
        Description of return value

    Example:
        >>> my_function("test", 2)
        ['test', 'test']
    """
    return [param] * count
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

- `APP_NAME` - Your application name
- `APP_ENV` - Environment (development/staging/production)
- `DEBUG` - Enable debug mode (True/False)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)

See `.env.example` for full list of available variables.

### Settings Management

Configuration is managed via Pydantic Settings:

```python
from src.config.settings import get_settings

settings = get_settings()
print(settings.APP_NAME)  # Access any setting
```

## 📚 Documentation

- **`.claude/instructions.md`** - Complete development standards and directives
- **`docs/ARCHITECTURE.md`** - Architecture decisions and patterns
- **`docs/CHANGELOG.md`** - Version history and changes
- **`docs/SESSION_SUMMARY.template.md`** - Template for session notes

## ✅ Pre-Commit Checklist

Before every commit, ensure:

- [ ] All functions have docstrings
- [ ] Type hints are present
- [ ] SESSION_SUMMARY.md is updated
- [ ] .env.example is current
- [ ] No secrets in code
- [ ] Tests pass (if applicable)

## 🤖 Claude Code Integration

This framework includes AI-powered development standards in `.claude/instructions.md`.

Claude Code will automatically:
- Enforce documentation standards
- Follow code organization patterns
- Maintain session summaries
- Apply best practices

## 📖 Learn More

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 📄 License

MIT License - Use freely for your Streamlit MVPs!

---

**Built with ❤️ by The Streamlit Guy**
