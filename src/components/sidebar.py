"""
Composant Sidebar pour la navigation.

Ce module gère l'affichage et la logique de la sidebar de navigation
de l'application Streamlit.

Author: The Streamlit Guy
Date: 2026-01-03
"""

import streamlit as st
from typing import Optional


def render_sidebar() -> None:
    """
    Rend la sidebar avec navigation et informations.

    Cette fonction affiche le menu de navigation, les informations utilisateur
    et d'autres éléments utiles dans la sidebar de l'application.

    Side Effects:
        - Modifie st.session_state.page quand l'utilisateur change de page
        - Affiche des éléments dans st.sidebar

    Example:
        >>> render_sidebar()  # doctest: +SKIP
    """
    with st.sidebar:
        # Logo et titre
        st.markdown("# 🚀")
        st.markdown("### Navigation")

        # Menu de navigation
        selected_page = _render_navigation_menu()

        # Mettre à jour la page si changement
        if selected_page and selected_page != st.session_state.page:
            st.session_state.page = selected_page
            st.rerun()

        st.divider()

        # Informations utilisateur
        _render_user_info()

        st.divider()

        # Footer sidebar
        _render_sidebar_footer()


def _render_navigation_menu() -> Optional[str]:
    """
    Rend le menu de navigation principal.

    Returns:
        La page sélectionnée par l'utilisateur, ou None si aucun changement

    Private:
        Cette fonction est privée (prefix _) et ne devrait être appelée
        que depuis render_sidebar()
    """
    st.markdown("#### Menu")

    # Liste des pages disponibles
    pages = {
        "🏠 Accueil": "home",
        "📊 Dashboard": "dashboard",
        "⚙️ Settings": "settings"
    }

    # Afficher les boutons de navigation
    selected = None

    for label, page_id in pages.items():
        # Highlighter la page courante
        is_current = st.session_state.page == page_id

        if st.button(
            label,
            use_container_width=True,
            type="primary" if is_current else "secondary",
            disabled=is_current
        ):
            selected = page_id

    return selected


def _render_user_info() -> None:
    """
    Affiche les informations de l'utilisateur connecté.

    Montre le nom de l'utilisateur, son avatar et un bouton de déconnexion
    si un utilisateur est connecté. Sinon, affiche un bouton de connexion.

    Private:
        Cette fonction est privée et ne devrait être appelée que depuis
        render_sidebar()
    """
    st.markdown("#### Utilisateur")

    user = st.session_state.get('user')

    if user:
        # Utilisateur connecté
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown("👤")

        with col2:
            st.markdown(f"**{user.get('name', 'User')}**")
            st.caption(user.get('email', 'No email'))

        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    else:
        # Utilisateur non connecté
        st.info("Non connecté")

        if st.button("🔐 Se connecter", use_container_width=True, type="primary"):
            # Simulation de connexion (à remplacer par vraie auth)
            st.session_state.user = {
                "name": "Demo User",
                "email": "demo@example.com"
            }
            st.rerun()


def _render_sidebar_footer() -> None:
    """
    Affiche le footer de la sidebar avec informations système.

    Montre la version de l'application, des liens utiles et le statut système.

    Private:
        Cette fonction est privée et ne devrait être appelée que depuis
        render_sidebar()
    """
    from src.config.settings import get_settings

    settings = get_settings()

    st.markdown("#### Informations")

    # Version et environnement
    st.caption(f"**Version:** 1.0.0")
    st.caption(f"**Env:** {settings.APP_ENV}")

    # Statut système
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Status", "✅ OK")

    with col2:
        st.metric("Mode", "🐛" if settings.DEBUG else "🚀")

    # Liens utiles
    st.markdown("---")
    st.markdown("""
    **Liens:**
    - [Documentation](#)
    - [Support](#)
    - [GitHub](#)
    """)


def render_sidebar_compact() -> None:
    """
    Version compacte de la sidebar pour les pages nécessitant plus d'espace.

    Cette version alternative de la sidebar affiche uniquement les éléments
    essentiels pour maximiser l'espace disponible pour le contenu principal.

    Example:
        >>> # Utiliser dans une page spécifique
        >>> render_sidebar_compact()  # doctest: +SKIP
        >>> # Au lieu de render_sidebar()
    """
    with st.sidebar:
        # Logo seulement
        st.markdown("# 🚀")

        # Navigation minimale
        if st.button("🏠", help="Accueil"):
            st.session_state.page = "home"
            st.rerun()

        if st.button("📊", help="Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

        if st.button("⚙️", help="Settings"):
            st.session_state.page = "settings"
            st.rerun()
