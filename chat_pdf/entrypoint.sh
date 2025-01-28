#!/bin/sh

echo "Starting entrypoint script..."

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."
    echo "Database host: $DATABASE_HOST"
    echo "Database port: $DATABASE_PORT"
    
    while ! nc -z "$DATABASE_HOST" "$DATABASE_PORT"; do
        sleep 0.1
    done
    
    echo "PostgreSQL started"
fi

echo "Running database migrations..."
alembic upgrade head

if [ "$LCNC_ENV" = "development" ]; then
    echo "Running database seeders..."
    python seed.py
fi

echo "Starting server..."
# Run the application
python /app/chat_pdf.py
