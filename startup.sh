#!/bin/bash
# Streamlit MVP Framework - Azure App Service Startup Script
# This script is executed when the container starts on Azure App Service

set -e  # Exit on error

echo "========================================="
echo "🚀 Starting Streamlit MVP Application"
echo "========================================="

# Display environment information
echo "📦 Environment: ${APP_ENV:-development}"
echo "🔌 Port: ${PORT:-8501}"
echo "🐛 Debug Mode: ${DEBUG:-false}"
echo "📝 Log Level: ${LOG_LEVEL:-INFO}"

# Set default port if not provided by Azure
export PORT=${PORT:-8501}

# Optional: Run database migrations if using a database
# if [ -f "alembic.ini" ]; then
#     echo "🔄 Running database migrations..."
#     python -m alembic upgrade head
# fi

# Optional: Run health checks before starting
# if [ -f "scripts/healthcheck.py" ]; then
#     echo "🏥 Running health checks..."
#     python scripts/healthcheck.py
# fi

# Start Streamlit application
echo "========================================="
echo "✅ Starting Streamlit server on port ${PORT}"
echo "========================================="

streamlit run src/app.py \
    --server.port=${PORT} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --logger.level=${LOG_LEVEL:-info}
