# Architecture Documentation

## 📋 Table des Matières

1. [Vue d'Ensemble](#vue-densemble)
2. [Principes de Design](#principes-de-design)
3. [Structure du Projet](#structure-du-projet)
4. [Composants Principaux](#composants-principaux)
5. [Flux de Données](#flux-de-données)
6. [Décisions d'Architecture](#décisions-darchitecture)
7. [Sécurité](#sécurité)
8. [Performance](#performance)
9. [Déploiement](#déploiement)

---

## Vue d'Ensemble

### Description
[Décrire brièvement ce que fait l'application]

### Technologies Utilisées
- **Frontend/UI:** Streamlit
- **Backend:** Python 3.11+
- **Database:** [PostgreSQL / SQLite / MongoDB / etc.]
- **Caching:** [Redis / Streamlit Cache / etc.]
- **Hosting:** Azure App Service
- **CI/CD:** [GitHub Actions / Azure DevOps / etc.]

### Objectifs Architecturaux
1. **Simplicité:** Code clair et maintenable
2. **Modularité:** Composants indépendants et réutilisables
3. **Scalabilité:** Capable de gérer la croissance
4. **Sécurité:** Protection des données et des accès
5. **Performance:** Temps de réponse optimal

---

## Principes de Design

### 1. Separation of Concerns
Chaque module a une responsabilité unique et bien définie.

### 2. DRY (Don't Repeat Yourself)
Réutilisation du code via des fonctions et composants partagés.

### 3. KISS (Keep It Simple, Stupid)
Solutions simples privilégiées sur la complexité inutile.

### 4. YAGNI (You Aren't Gonna Need It)
Implémenter uniquement ce qui est nécessaire maintenant.

### 5. Fail Fast
Détecter et signaler les erreurs le plus tôt possible.

---

## Structure du Projet

```
streamlit-mvp/
├── .claude/                    # Directives Claude Code
│   └── instructions.md
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md         # Ce fichier
│   ├── CHANGELOG.md            # Historique des versions
│   └── SESSION_SUMMARY.md      # Résumés de sessions
│
├── src/                        # Code source
│   ├── app.py                  # Point d'entrée Streamlit
│   │
│   ├── components/             # Composants UI réutilisables
│   │   ├── __init__.py
│   │   ├── header.py           # Header de l'application
│   │   ├── sidebar.py          # Sidebar navigation
│   │   └── footer.py           # Footer
│   │
│   ├── config/                 # Configuration
│   │   ├── __init__.py
│   │   └── settings.py         # Pydantic Settings
│   │
│   ├── utils/                  # Utilitaires
│   │   ├── __init__.py
│   │   ├── helpers.py          # Fonctions helper générales
│   │   ├── validators.py       # Validations custom
│   │   └── formatters.py       # Formatage de données
│   │
│   ├── services/               # Logique métier
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
├── .env.example                # Template variables d'environnement
├── .gitignore                  # Git ignore rules
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── startup.sh                  # Azure startup script
└── README.md                   # Documentation principale
```

---

## Composants Principaux

### 1. Application Entry Point (`src/app.py`)

**Responsabilité:** Orchestration de l'application Streamlit

**Fonctions clés:**
- `initialize_session_state()`: Configuration du state
- `configure_page()`: Configuration Streamlit
- `main()`: Point d'entrée principal

**Dépendances:**
- `src.config.settings`
- `src.components.*`
- `src.services.*`

### 2. Configuration (`src/config/settings.py`)

**Responsabilité:** Gestion centralisée de la configuration

**Pattern:** Singleton avec Pydantic Settings

**Variables gérées:**
- Application settings (APP_NAME, DEBUG, etc.)
- Database credentials
- API keys
- External services configuration

**Validation:** Automatique via Pydantic au démarrage

### 3. Components (`src/components/`)

**Responsabilité:** Composants UI réutilisables

**Composants standards:**
- `header.py`: Header avec logo et navigation
- `sidebar.py`: Sidebar avec menu
- `footer.py`: Footer avec informations

**Pattern:** Fonctions render_* qui retournent void et utilisent st.* directement

### 4. Services (`src/services/`)

**Responsabilité:** Logique métier et orchestration

**Pattern:** Classes ou modules fonctionnels selon la complexité

**Exemples:**
- `auth_service.py`: Authentification et autorisation
- `data_service.py`: Opérations sur les données
- `api_service.py`: Intégration APIs externes

### 5. Utils (`src/utils/`)

**Responsabilité:** Fonctions utilitaires partagées

**Caractéristiques:**
- Pure functions (pas d'effets de bord)
- Bien testées
- Documentation complète

---

## Flux de Données

### Flux Principal

```
User Input → Streamlit Widget → Session State → Service Layer → Data Layer → Response
                                       ↓
                                   UI Update
```

### Exemple: Chargement de Données

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
    """Cache pendant 1 heure."""
    return requests.get(api_url).json()

# Cache resources (DB connections, etc.)
@st.cache_resource
def get_database_connection():
    """Singleton connection."""
    return create_engine(DATABASE_URL)
```

---

## Décisions d'Architecture

### ADR-001: Pydantic pour la Configuration

**Date:** 2026-01-03

**Status:** Accepted

**Context:**
Besoin de gérer les variables d'environnement avec validation.

**Decision:**
Utiliser Pydantic Settings pour:
- Validation automatique des types
- Documentation auto-générée
- Defaults et valeurs optionnelles
- IDE autocomplete

**Consequences:**
- ✅ Type safety au démarrage
- ✅ Erreurs claires si config invalide
- ❌ Dépendance supplémentaire

**Alternatives considérées:**
1. python-decouple: Moins de validation
2. dynaconf: Plus complexe pour nos besoins

---

### ADR-002: Pas d'ORM pour le Moment

**Date:** 2026-01-03

**Status:** Accepted

**Context:**
Application simple sans relations complexes.

**Decision:**
Utiliser SQL direct ou pandas pour data access.

**Consequences:**
- ✅ Moins de dépendances
- ✅ Queries SQL explicites
- ❌ Pas de migrations automatiques
- ❌ Plus de code boilerplate

**When to reconsider:**
Si > 5 tables avec relations complexes → SQLAlchemy

---

### ADR-003: [Votre Décision]

**Date:** [DATE]

**Status:** [Proposed | Accepted | Deprecated | Superseded]

**Context:**
[Décrivez le contexte et le problème]

**Decision:**
[Quelle décision a été prise et pourquoi]

**Consequences:**
[Conséquences positives et négatives]

**Alternatives considérées:**
[Autres options envisagées]

---

## Sécurité

### Authentification
- [ ] [Décrire le système d'auth si applicable]
- [ ] [JWT / Session / OAuth / etc.]

### Autorisation
- [ ] [Gestion des rôles et permissions]
- [ ] [RBAC / ABAC / etc.]

### Protection des Données
- [ ] Variables sensibles dans .env (jamais hardcodées)
- [ ] .env dans .gitignore
- [ ] Secrets Azure Key Vault en production
- [ ] HTTPS obligatoire en production

### Validation des Inputs
- [ ] Pydantic models pour validation
- [ ] Sanitization des inputs utilisateur
- [ ] Protection CSRF (si applicable)

### Logging Sécurisé
- [ ] Pas de secrets dans les logs
- [ ] Masking des données sensibles
- [ ] Logs centralisés (Azure Monitor)

---

## Performance

### Optimisations Streamlit

#### Caching
```python
# Cache données (invalidé après TTL)
@st.cache_data(ttl=600)
def expensive_computation(param):
    # ...

# Cache resources (jamais invalidé automatiquement)
@st.cache_resource
def get_db_connection():
    # ...
```

#### Session State
```python
# Éviter les recomputes
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = process_data()

# Réutiliser
data = st.session_state.processed_data
```

### Database
- [ ] Indexes sur colonnes fréquemment queryées
- [ ] Connection pooling
- [ ] Query optimization
- [ ] Pagination pour grandes datasets

### Frontend
- [ ] Lazy loading des composants lourds
- [ ] Compression des images
- [ ] Minimisation des re-renders

### Monitoring
- [ ] Azure Application Insights
- [ ] Temps de réponse des endpoints
- [ ] Utilisation mémoire
- [ ] Erreurs et exceptions

---

## Déploiement

### Environnements

#### Development
- Local machine
- .env avec variables de dev
- DEBUG=True
- Hot reload activé

#### Staging
- Azure App Service (Staging slot)
- Variables d'environnement via Azure
- DEBUG=False
- Tests d'intégration automatiques

#### Production
- Azure App Service (Production slot)
- Secrets via Azure Key Vault
- DEBUG=False
- Monitoring actif
- Backup automatique

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml (exemple)
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
- Azure Deployment Slots pour swap instant
- Keep last 3 versions déployées
- Plan de rollback documenté

---

## Maintenance

### Logs
- **Location:** Azure App Service Logs
- **Retention:** 30 jours
- **Analysis:** Azure Monitor / Log Analytics

### Backups
- **Database:** Backup quotidien automatique
- **Config:** Versionné dans git
- **Retention:** 7 jours (rolling)

### Monitoring Alerts
- [ ] Temps de réponse > 2s
- [ ] Error rate > 1%
- [ ] Memory usage > 80%
- [ ] Disk usage > 85%

---

## Évolution Future

### Roadmap Technique

#### Court Terme (1-3 mois)
- [ ] Ajout de tests d'intégration
- [ ] Amélioration monitoring
- [ ] Documentation API

#### Moyen Terme (3-6 mois)
- [ ] Migration vers microservices (si nécessaire)
- [ ] Cache distribué (Redis)
- [ ] CDN pour assets statiques

#### Long Terme (6-12 mois)
- [ ] Multi-region deployment
- [ ] Auto-scaling avancé
- [ ] Machine Learning pipeline

---

**Version:** 1.0
**Last Updated:** 2026-01-03
**Next Review:** [DATE]
