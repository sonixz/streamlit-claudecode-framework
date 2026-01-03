"""
Configuration de l'application avec validation Pydantic.

Ce module gère toutes les variables d'environnement et
assure leur validation au démarrage de l'application.

Author: The Streamlit Guy
Date: 2026-01-03
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration principale de l'application.

    Toutes les variables d'environnement sont chargées et validées
    automatiquement via Pydantic Settings. Les valeurs par défaut sont
    définies pour faciliter le développement local.

    Attributes:
        APP_NAME: Nom de l'application affiché dans l'interface
        APP_ENV: Environnement d'exécution (development, staging, production)
        DEBUG: Mode debug activé/désactivé
        LOG_LEVEL: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        STREAMLIT_SERVER_PORT: Port du serveur Streamlit
        STREAMLIT_SERVER_ADDRESS: Adresse d'écoute du serveur
        DATABASE_URL: URL de connexion à la base de données (optionnel)
        OPENAI_API_KEY: Clé API OpenAI (optionnel)

    Example:
        >>> settings = Settings()
        >>> print(settings.APP_NAME)
        'Streamlit MVP'
        >>> settings.DEBUG
        False
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application Settings
    APP_NAME: str = Field(
        default="Streamlit MVP",
        description="Nom de l'application affiché dans l'interface"
    )

    APP_ENV: str = Field(
        default="development",
        description="Environnement d'exécution (development, staging, production)"
    )

    DEBUG: bool = Field(
        default=False,
        description="Active le mode debug avec logs détaillés"
    )

    LOG_LEVEL: str = Field(
        default="INFO",
        description="Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )

    # Streamlit Configuration
    STREAMLIT_SERVER_PORT: int = Field(
        default=8501,
        description="Port du serveur Streamlit",
        ge=1024,
        le=65535
    )

    STREAMLIT_SERVER_ADDRESS: str = Field(
        default="0.0.0.0",
        description="Adresse d'écoute du serveur Streamlit"
    )

    # Database Configuration (Optional)
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description="URL de connexion à la base de données (format: dialect://user:pass@host:port/db)"
    )

    DATABASE_POOL_SIZE: int = Field(
        default=5,
        description="Taille du pool de connexions à la base de données",
        ge=1,
        le=50
    )

    # API Keys (Optional)
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="Clé API OpenAI pour intégrations GPT"
    )

    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None,
        description="Clé API Anthropic pour intégrations Claude"
    )

    # Security
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        min_length=32,
        description="Clé secrète pour encryption (min 32 caractères)"
    )

    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:8501",
        description="Origines autorisées pour CORS (séparées par des virgules)"
    )

    @field_validator("APP_ENV")
    @classmethod
    def validate_env(cls, v: str) -> str:
        """
        Valide que l'environnement est un des environnements autorisés.

        Args:
            v: Valeur de APP_ENV à valider

        Returns:
            La valeur validée en lowercase

        Raises:
            ValueError: Si l'environnement n'est pas valide

        Example:
            >>> Settings.validate_env("Development")
            'development'
            >>> Settings.validate_env("invalid")  # doctest: +SKIP
            ValueError: APP_ENV doit être dans ['development', 'staging', 'production']
        """
        allowed = ["development", "staging", "production"]
        v_lower = v.lower()

        if v_lower not in allowed:
            raise ValueError(
                f"APP_ENV doit être dans {allowed}, reçu: {v}"
            )

        return v_lower

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """
        Valide que le niveau de log est un des niveaux standards.

        Args:
            v: Niveau de log à valider

        Returns:
            Le niveau de log en uppercase

        Raises:
            ValueError: Si le niveau n'est pas valide

        Example:
            >>> Settings.validate_log_level("info")
            'INFO'
            >>> Settings.validate_log_level("invalid")  # doctest: +SKIP
            ValueError: LOG_LEVEL doit être dans ...
        """
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()

        if v_upper not in allowed:
            raise ValueError(
                f"LOG_LEVEL doit être dans {allowed}, reçu: {v}"
            )

        return v_upper

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key_production(cls, v: str, info) -> str:
        """
        Valide que la SECRET_KEY n'est pas la valeur par défaut en production.

        Args:
            v: SECRET_KEY à valider
            info: Contexte de validation Pydantic

        Returns:
            La SECRET_KEY validée

        Raises:
            ValueError: Si la clé par défaut est utilisée en production

        Example:
            >>> Settings.validate_secret_key_production("my-secure-key-32chars", None)
            'my-secure-key-32chars'
        """
        # Check if we're in production (via APP_ENV in values)
        app_env = info.data.get("APP_ENV", "development")

        if app_env == "production" and v == "dev-secret-key-change-in-production":
            raise ValueError(
                "SECRET_KEY par défaut ne peut pas être utilisée en production! "
                "Définissez une vraie clé secrète dans .env"
            )

        return v

    def get_allowed_origins_list(self) -> list[str]:
        """
        Retourne la liste des origines autorisées pour CORS.

        Returns:
            Liste des URLs autorisées

        Example:
            >>> settings = Settings()
            >>> settings.get_allowed_origins_list()
            ['http://localhost:3000', 'http://localhost:8501']
        """
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        """
        Indique si l'application tourne en production.

        Returns:
            True si APP_ENV est 'production', False sinon

        Example:
            >>> settings = Settings(APP_ENV="production")
            >>> settings.is_production
            True
        """
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        """
        Indique si l'application tourne en développement.

        Returns:
            True si APP_ENV est 'development', False sinon

        Example:
            >>> settings = Settings()
            >>> settings.is_development
            True
        """
        return self.APP_ENV == "development"


@lru_cache
def get_settings() -> Settings:
    """
    Récupère l'instance singleton des settings.

    Utilise lru_cache pour ne charger les settings qu'une seule fois
    et les réutiliser ensuite à travers toute l'application. Cette approche
    garantit la cohérence et améliore les performances.

    Returns:
        Instance de Settings validée et prête à l'emploi

    Example:
        >>> settings = get_settings()
        >>> print(settings.APP_NAME)
        'Streamlit MVP'
        >>> # Appel suivant retourne la même instance (cached)
        >>> settings2 = get_settings()
        >>> settings is settings2
        True
    """
    return Settings()
