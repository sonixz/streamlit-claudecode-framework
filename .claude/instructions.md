# Streamlit MVP Framework - Claude Code Instructions

## 🎯 Mission
Maintenir un code Python professionnel, documenté, et déployable sur Azure App Service pour tous les projets Streamlit.

## 📝 Standards de Documentation

### 1. Code Python - Documentation Obligatoire

**Règle d'or:** Tout code dans `src/` doit être documenté avec des docstrings Google-style.

#### Type Hints Obligatoires
- Tous les paramètres de fonction
- Tous les retours de fonction
- Variables complexes

#### Format des Docstrings

```python
def process_user_data(user_id: int, data: dict[str, Any]) -> UserModel:
    """
    Traite les données utilisateur et retourne un modèle validé.

    Cette fonction valide les données brutes, applique les transformations
    nécessaires, et retourne une instance du modèle utilisateur.

    Args:
        user_id: Identifiant unique de l'utilisateur (doit être > 0)
        data: Dictionnaire contenant les données brutes de l'utilisateur
            Format attendu: {"name": str, "email": str, "age": int}

    Returns:
        UserModel: Instance du modèle utilisateur validé avec tous les champs

    Raises:
        ValueError: Si user_id est négatif ou zéro
        ValidationError: Si les données ne passent pas la validation Pydantic

    Example:
        >>> user_data = {"name": "John", "email": "john@example.com", "age": 30}
        >>> user = process_user_data(1, user_data)
        >>> print(user.name)
        'John'
    """
    if user_id <= 0:
        raise ValueError(f"user_id doit être positif, reçu: {user_id}")

    # Validation et traitement...
    return UserModel(**data)
```

#### Commentaires en Français
- Expliquer la logique complexe
- Documenter les décisions techniques
- Clarifier les "pourquoi" pas seulement les "quoi"

```python
# Utilisation de cache pour éviter les appels API répétés
# Performance critique: cette fonction est appelée à chaque render
@st.cache_data(ttl=3600)
def fetch_user_data(user_id: int) -> dict[str, Any]:
    """Récupère les données utilisateur depuis l'API."""
    # ...
```

### 2. Fichiers de Suivi Obligatoires

#### SESSION_SUMMARY.md

**Quand:** Créer/mettre à jour après chaque session de développement significative

**Format Standard:**
```markdown
# Session - [DATE YYYY-MM-DD]

## 🎯 Objectifs de la Session
- Objectif principal
- Objectifs secondaires

## ✅ Changements Réalisés

### Fichiers Modifiés
- `src/app.py` - Description des modifications
- `src/utils/helpers.py` - Nouvelles fonctions ajoutées
- `docs/CHANGELOG.md` - Mise à jour

### Nouvelles Fonctionnalités
1. **Feature Name** - Description détaillée
   - Fichiers touchés
   - Décisions techniques prises

### Corrections de Bugs
- **Bug #1**: Description du problème et de la solution
- **Bug #2**: Description du problème et de la solution

## 🔧 Décisions Techniques

### Architecture
- Décision 1: Pourquoi et comment
- Décision 2: Alternatives considérées et choix final

### Dépendances
- Nouvelles dépendances ajoutées et justification
- Mises à jour de dépendances existantes

## 🐛 Problèmes Rencontrés

### Problème 1
- **Description:** Qu'est-ce qui n'a pas marché
- **Solution:** Comment ça a été résolu
- **Learnings:** Ce qu'on a appris

## 📋 TODO

### Priorité Haute
- [ ] Tâche urgente 1
- [ ] Tâche urgente 2

### Priorité Moyenne
- [ ] Amélioration 1
- [ ] Amélioration 2

### Priorité Basse
- [ ] Nice to have 1

## 📊 Métriques (si applicable)
- Tests passant: X/Y
- Coverage: XX%
- Performance: amélioration/dégradation notée

## 🔗 Références
- Links vers documentation pertinente
- Issues GitHub liées
- PRs associées
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

### 3. Structure du Code Python

#### Organisation en Fonctions

**Règles Strictes:**
1. **Pas de code en vrac** - Tout dans des fonctions
2. **Fonctions courtes** - Maximum 50 lignes (idéal: 20-30)
3. **Single Responsibility** - Une fonction = une responsabilité
4. **Nommage clair** - Le nom doit expliquer ce que fait la fonction

**Structure Standard de app.py:**

```python
"""
Application Streamlit principale.

Ce module orchestre l'interface utilisateur et coordonne
les différents composants de l'application MVP.

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

    Cette fonction configure toutes les variables de session nécessaires
    au bon fonctionnement de l'application. Elle est idempotente et peut
    être appelée plusieurs fois sans effet de bord.

    Session State Variables:
        user (Optional[dict]): Informations de l'utilisateur connecté
        page (str): Page courante de l'application
        data_loaded (bool): Indicateur si les données ont été chargées
    """
    if 'user' not in st.session_state:
        st.session_state.user = None

    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


def configure_page() -> None:
    """
    Configure la page Streamlit avec les paramètres de base.

    Définit le titre, l'icône, le layout et autres configurations
    de la page Streamlit.
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
    Point d'entrée principal de l'application Streamlit.

    Cette fonction orchestre l'initialisation et le rendu de l'application.
    Elle doit rester simple et déléguer la logique complexe à d'autres fonctions.
    """
    # Configuration
    setup_logging()
    configure_page()
    initialize_session_state()

    # Rendu de l'interface
    render_header()
    render_sidebar()

    # Logique principale basée sur la page courante
    page = st.session_state.page

    if page == 'home':
        render_home_page()
    elif page == 'dashboard':
        render_dashboard_page()
    else:
        st.error(f"Page inconnue: {page}")


def render_home_page() -> None:
    """Rend la page d'accueil de l'application."""
    st.title("🏠 Accueil")
    st.write("Bienvenue dans votre application Streamlit MVP!")


def render_dashboard_page() -> None:
    """Rend la page de dashboard avec métriques."""
    st.title("📊 Dashboard")
    # Logic...


if __name__ == "__main__":
    main()
```

#### Modularité

**src/utils/helpers.py:**
```python
"""
Fonctions utilitaires partagées.

Ce module contient les fonctions helper réutilisables à travers l'application.
"""

import logging
from typing import Any


def setup_logging(level: str = "INFO") -> None:
    """
    Configure le système de logging de l'application.

    Args:
        level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def safe_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Récupère une valeur d'un dictionnaire de manière sécurisée.

    Args:
        data: Dictionnaire source
        key: Clé à récupérer
        default: Valeur par défaut si la clé n'existe pas

    Returns:
        La valeur associée à la clé ou la valeur par défaut

    Example:
        >>> data = {"name": "John"}
        >>> safe_get(data, "name")
        'John'
        >>> safe_get(data, "age", 0)
        0
    """
    return data.get(key, default)
```

### 4. Gestion des Variables d'Environnement

#### .env.example - Template Obligatoire

Ce fichier DOIT être présent dans chaque repo et mis à jour quand de nouvelles variables sont ajoutées.

```bash
# =============================================================================
# STREAMLIT MVP - ENVIRONMENT VARIABLES
# =============================================================================
# Copier ce fichier vers .env et remplir avec vos vraies valeurs
# Ne JAMAIS commiter le fichier .env !

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
# Azure App Service (si déployé)
# -----------------------------------------------------------------------------
AZURE_SUBSCRIPTION_ID=your-subscription-id-here
AZURE_RESOURCE_GROUP=your-resource-group
AZURE_APP_SERVICE_NAME=your-app-service-name

# -----------------------------------------------------------------------------
# Database (si applicable)
# -----------------------------------------------------------------------------
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# -----------------------------------------------------------------------------
# API Keys (si applicable)
# -----------------------------------------------------------------------------
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here

# -----------------------------------------------------------------------------
# External Services (si applicable)
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

#### Configuration avec Pydantic (src/config/settings.py)

```python
"""
Configuration de l'application avec validation Pydantic.

Ce module gère toutes les variables d'environnement et
assure leur validation au démarrage de l'application.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration principale de l'application.

    Toutes les variables d'environnement sont chargées et validées
    automatiquement via Pydantic Settings.
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
        """Valide que l'environnement est valide."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"APP_ENV doit être dans {allowed}")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Valide que le niveau de log est valide."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"LOG_LEVEL doit être dans {allowed}")
        return v.upper()


@lru_cache
def get_settings() -> Settings:
    """
    Récupère l'instance singleton des settings.

    Utilise lru_cache pour ne charger les settings qu'une seule fois
    et les réutiliser ensuite.

    Returns:
        Instance de Settings validée

    Example:
        >>> settings = get_settings()
        >>> print(settings.APP_NAME)
        'Streamlit MVP'
    """
    return Settings()
```

### 5. Configuration pour Azure App Service

#### Dockerfile Standard

```dockerfile
# Streamlit MVP - Dockerfile pour Azure App Service
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

#### startup.sh - Script de Démarrage Azure

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

#### .gitignore Standard

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

#### Format des Commits

**Standard Conventional Commits:**

```
<type>: <description courte>

<body optionnel - description détaillée>

<footer optionnel - références et co-auteurs>
```

**Types Standards:**
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation seulement
- `style`: Formatage (pas de changement de code)
- `refactor`: Refactoring (pas de feat ni fix)
- `test`: Ajout ou modification de tests
- `chore`: Maintenance (deps, config, etc.)

**Exemple:**
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

### 7. Tests (Optionnel mais Recommandé)

#### Structure des Tests

```python
"""
Tests pour les fonctions utilitaires.

Ce module teste toutes les fonctions du module utils.helpers.
"""

import pytest
from src.utils.helpers import safe_get, setup_logging


class TestSafeGet:
    """Tests pour la fonction safe_get."""

    def test_safe_get_existing_key(self):
        """Test récupération d'une clé existante."""
        data = {"name": "John", "age": 30}
        assert safe_get(data, "name") == "John"
        assert safe_get(data, "age") == 30

    def test_safe_get_missing_key_with_default(self):
        """Test récupération d'une clé manquante avec valeur par défaut."""
        data = {"name": "John"}
        assert safe_get(data, "age", 0) == 0
        assert safe_get(data, "email", "default@example.com") == "default@example.com"

    def test_safe_get_missing_key_without_default(self):
        """Test récupération d'une clé manquante sans valeur par défaut."""
        data = {"name": "John"}
        assert safe_get(data, "age") is None


class TestSetupLogging:
    """Tests pour la fonction setup_logging."""

    def test_setup_logging_default_level(self):
        """Test configuration logging avec niveau par défaut."""
        setup_logging()
        # Verify logging is configured...

    def test_setup_logging_custom_level(self):
        """Test configuration logging avec niveau custom."""
        setup_logging("DEBUG")
        # Verify logging level is DEBUG...
```

## 🚫 Interdictions Strictes

### 1. Documentation
- ❌ **Jamais de fonction sans docstring** dans src/
- ❌ **Jamais de code complexe sans commentaire**
- ❌ **Jamais de paramètre sans type hint**

### 2. Sécurité
- ❌ **Jamais de secrets hardcodés** dans le code
- ❌ **Jamais de .env commité** dans git
- ❌ **Jamais d'API key en clair** dans les logs

### 3. Code Quality
- ❌ **Jamais de print()** (utiliser logging ou st.write)
- ❌ **Jamais de fonctions > 100 lignes** (refactor obligatoire)
- ❌ **Jamais de code dupliqué** (DRY principle)
- ❌ **Jamais de variables globales mutables**

### 4. Streamlit Specifics
- ❌ **Jamais de st.write() pour les erreurs** (utiliser st.error)
- ❌ **Jamais de calculs lourds sans @st.cache_data**
- ❌ **Jamais de state management anarchique**

## ✅ Checklist Avant Commit

Avant chaque commit, vérifier:

- [ ] **Documentation**
  - [ ] Toutes les nouvelles fonctions ont des docstrings
  - [ ] Type hints présents partout
  - [ ] Commentaires pour la logique complexe

- [ ] **Fichiers de Suivi**
  - [ ] SESSION_SUMMARY.md mis à jour
  - [ ] CHANGELOG.md mis à jour si release
  - [ ] .env.example à jour si nouvelles variables

- [ ] **Code Quality**
  - [ ] Pas de code dupliqué
  - [ ] Fonctions < 50 lignes
  - [ ] Pas de secrets hardcodés
  - [ ] Imports organisés et triés

- [ ] **Tests** (si applicable)
  - [ ] Tests passent tous
  - [ ] Nouveaux tests pour nouvelles features
  - [ ] Coverage maintenu ou amélioré

- [ ] **Git**
  - [ ] Message de commit suit le format
  - [ ] .gitignore à jour si nouveaux fichiers à exclure

## 🎓 Exemples et Templates

Tous les templates et exemples sont disponibles dans le repo `streamlit-claudecode-framework`.

Pour démarrer un nouveau projet:
```bash
git clone https://github.com/yourusername/streamlit-claudecode-framework.git my-new-project
cd my-new-project
rm -rf .git
git init
# Suivre les instructions du README.md
```

## 📚 Ressources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Azure App Service Python](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

**Version:** 1.0.0
**Last Updated:** 2026-01-03
**Maintained by:** The Streamlit Guy
