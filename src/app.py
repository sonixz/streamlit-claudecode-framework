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
    de la page Streamlit basées sur les settings de l'application.
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

    Flow:
        1. Configuration du logging
        2. Configuration de la page Streamlit
        3. Initialisation du session state
        4. Rendu de l'interface utilisateur
        5. Routing vers la page appropriée
    """
    # Configuration
    setup_logging()
    configure_page()
    initialize_session_state()

    # Rendu de l'interface
    render_header()
    render_sidebar()

    # Routing basé sur la page courante
    page = st.session_state.page

    if page == 'home':
        render_home_page()
    elif page == 'dashboard':
        render_dashboard_page()
    elif page == 'settings':
        render_settings_page()
    else:
        st.error(f"❌ Page inconnue: {page}")


def render_header() -> None:
    """
    Rend le header de l'application.

    Affiche le logo, le titre et la navigation principale.
    """
    settings = get_settings()

    col1, col2 = st.columns([1, 4])

    with col1:
        st.markdown("# 🚀")

    with col2:
        st.title(settings.APP_NAME)
        st.caption("Build Systems, Not Just Apps")


def render_home_page() -> None:
    """
    Rend la page d'accueil de l'application.

    Cette page affiche un message de bienvenue et des liens rapides
    vers les principales fonctionnalités.
    """
    st.markdown("## 🏠 Bienvenue")

    st.write("""
    Bienvenue dans votre application Streamlit MVP!

    Ce template suit le **Streamlit Claude Code Framework** pour garantir:
    - ✅ Code bien documenté
    - ✅ Structure standardisée
    - ✅ Déployable sur Azure App Service
    - ✅ Best practices Python
    """)

    # Quick stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Users", "0", "+0")

    with col2:
        st.metric("Requests", "0", "+0")

    with col3:
        st.metric("Uptime", "100%", "0%")

    # Quick actions
    st.markdown("### 🚀 Actions Rapides")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Voir Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

    with col2:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.page = 'settings'
            st.rerun()


def render_dashboard_page() -> None:
    """
    Rend la page de dashboard avec métriques et visualisations.

    Cette page affiche les métriques clés de l'application et
    des visualisations interactives.
    """
    st.markdown("## 📊 Dashboard")

    st.info("🚧 Dashboard en construction - Ajoutez vos métriques ici!")

    # Example chart
    import pandas as pd
    import numpy as np

    # Generate sample data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )

    st.line_chart(chart_data)


def render_settings_page() -> None:
    """
    Rend la page de settings de l'application.

    Permet à l'utilisateur de configurer les préférences de l'application.
    """
    st.markdown("## ⚙️ Settings")

    settings = get_settings()

    st.write(f"**App Name:** {settings.APP_NAME}")
    st.write(f"**Environment:** {settings.APP_ENV}")
    st.write(f"**Debug Mode:** {'✅ Enabled' if settings.DEBUG else '❌ Disabled'}")

    st.divider()

    st.markdown("### Préférences Utilisateur")

    theme = st.selectbox(
        "Theme",
        ["Light", "Dark", "Auto"],
        index=1
    )

    language = st.selectbox(
        "Language",
        ["Français", "English"],
        index=0
    )

    if st.button("💾 Sauvegarder", type="primary"):
        st.success("✅ Préférences sauvegardées!")


if __name__ == "__main__":
    main()
