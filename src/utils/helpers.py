"""
Fonctions utilitaires partagées.

Ce module contient les fonctions helper réutilisables à travers l'application.
Toutes les fonctions ici doivent être pures (pas d'effets de bord) autant que possible.

Author: The Streamlit Guy
Date: 2026-01-03
"""

import logging
from typing import Any, Optional
from datetime import datetime


def setup_logging(level: str = "INFO") -> None:
    """
    Configure le système de logging de l'application.

    Configure le format des logs et le niveau de logging pour toute
    l'application. Cette fonction doit être appelée une seule fois
    au démarrage de l'application.

    Args:
        level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            Default: "INFO"

    Example:
        >>> setup_logging("DEBUG")
        >>> logging.info("Application started")  # doctest: +SKIP
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Log the configuration
    logging.info(f"Logging configuré au niveau: {level}")


def safe_get(
    data: dict[str, Any],
    key: str,
    default: Any = None
) -> Any:
    """
    Récupère une valeur d'un dictionnaire de manière sécurisée.

    Cette fonction wrapper permet d'éviter les KeyError et de fournir
    une valeur par défaut si la clé n'existe pas.

    Args:
        data: Dictionnaire source
        key: Clé à récupérer
        default: Valeur par défaut si la clé n'existe pas

    Returns:
        La valeur associée à la clé ou la valeur par défaut

    Example:
        >>> data = {"name": "John", "age": 30}
        >>> safe_get(data, "name")
        'John'
        >>> safe_get(data, "email", "no-email@example.com")
        'no-email@example.com'
        >>> safe_get(data, "missing")
        None
    """
    return data.get(key, default)


def format_timestamp(
    dt: datetime,
    format_str: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Formate un datetime en string selon le format spécifié.

    Args:
        dt: Objet datetime à formater
        format_str: Format de sortie (strftime format)
            Default: "%Y-%m-%d %H:%M:%S"

    Returns:
        String formatée représentant la date/heure

    Example:
        >>> from datetime import datetime
        >>> dt = datetime(2026, 1, 3, 14, 30, 0)
        >>> format_timestamp(dt)
        '2026-01-03 14:30:00'
        >>> format_timestamp(dt, "%d/%m/%Y")
        '03/01/2026'
    """
    return dt.strftime(format_str)


def truncate_string(
    text: str,
    max_length: int,
    suffix: str = "..."
) -> str:
    """
    Tronque une string à la longueur maximale spécifiée.

    Si la string est plus longue que max_length, elle est tronquée
    et un suffixe est ajouté (par défaut "...").

    Args:
        text: Texte à tronquer
        max_length: Longueur maximale (incluant le suffixe)
        suffix: Suffixe à ajouter si tronqué
            Default: "..."

    Returns:
        Texte tronqué avec suffixe si nécessaire

    Raises:
        ValueError: Si max_length est inférieur à la longueur du suffixe

    Example:
        >>> truncate_string("Hello World!", 8)
        'Hello...'
        >>> truncate_string("Short", 10)
        'Short'
        >>> truncate_string("Long text here", 10, "~")
        'Long text~'
    """
    if max_length < len(suffix):
        raise ValueError(
            f"max_length ({max_length}) doit être >= longueur du suffixe ({len(suffix)})"
        )

    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def validate_email(email: str) -> bool:
    """
    Valide basiquement un format d'email.

    Cette fonction fait une validation simple du format email.
    Pour une validation complète, utiliser une librairie dédiée.

    Args:
        email: Adresse email à valider

    Returns:
        True si le format est valide, False sinon

    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
        >>> validate_email("user@")
        False
    """
    # Validation simple: contient @ et un point après @
    if "@" not in email:
        return False

    local, domain = email.rsplit("@", 1)

    if not local or not domain:
        return False

    if "." not in domain:
        return False

    return True


def chunk_list(
    items: list[Any],
    chunk_size: int
) -> list[list[Any]]:
    """
    Divise une liste en chunks de taille spécifiée.

    Utile pour traiter de grandes listes en lots ou pour la pagination.

    Args:
        items: Liste à diviser
        chunk_size: Taille de chaque chunk

    Returns:
        Liste de listes (chunks)

    Raises:
        ValueError: Si chunk_size est <= 0

    Example:
        >>> items = [1, 2, 3, 4, 5, 6, 7]
        >>> chunk_list(items, 3)
        [[1, 2, 3], [4, 5, 6], [7]]
        >>> chunk_list(items, 2)
        [[1, 2], [3, 4], [5, 6], [7]]
    """
    if chunk_size <= 0:
        raise ValueError(f"chunk_size doit être > 0, reçu: {chunk_size}")

    return [
        items[i:i + chunk_size]
        for i in range(0, len(items), chunk_size)
    ]


def merge_dicts(
    dict1: dict[str, Any],
    dict2: dict[str, Any],
    prefer_second: bool = True
) -> dict[str, Any]:
    """
    Fusionne deux dictionnaires.

    Args:
        dict1: Premier dictionnaire
        dict2: Deuxième dictionnaire
        prefer_second: Si True, les valeurs de dict2 écrasent celles de dict1
            en cas de conflit. Si False, les valeurs de dict1 sont préservées.
            Default: True

    Returns:
        Nouveau dictionnaire fusionné

    Example:
        >>> d1 = {"a": 1, "b": 2}
        >>> d2 = {"b": 3, "c": 4}
        >>> merge_dicts(d1, d2)
        {'a': 1, 'b': 3, 'c': 4}
        >>> merge_dicts(d1, d2, prefer_second=False)
        {'a': 1, 'b': 2, 'c': 4}
    """
    if prefer_second:
        return {**dict1, **dict2}
    else:
        return {**dict2, **dict1}


def calculate_percentage(
    part: float,
    total: float,
    decimals: int = 2
) -> float:
    """
    Calcule un pourcentage avec gestion du division par zéro.

    Args:
        part: Partie (numérateur)
        total: Total (dénominateur)
        decimals: Nombre de décimales à arrondir
            Default: 2

    Returns:
        Pourcentage calculé (0.0 si total est zéro)

    Example:
        >>> calculate_percentage(25, 100)
        25.0
        >>> calculate_percentage(1, 3)
        33.33
        >>> calculate_percentage(10, 0)
        0.0
    """
    if total == 0:
        return 0.0

    percentage = (part / total) * 100
    return round(percentage, decimals)


def format_file_size(size_bytes: int) -> str:
    """
    Formate une taille de fichier en bytes vers une unité lisible.

    Args:
        size_bytes: Taille en bytes

    Returns:
        String formatée (ex: "1.5 MB", "256 KB")

    Example:
        >>> format_file_size(1024)
        '1.0 KB'
        >>> format_file_size(1536)
        '1.5 KB'
        >>> format_file_size(1048576)
        '1.0 MB'
        >>> format_file_size(500)
        '500 B'
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.1f} PB"
