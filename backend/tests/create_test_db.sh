#!/bin/bash

# Script to create test database for integration tests
# Usage: ./create_test_db.sh

set -e  # Exit on error

# Database configuration
DB_HOST=${POSTGRES_HOST:-localhost}
DB_PORT=${POSTGRES_PORT:-5432}
DB_USER=${POSTGRES_USER:-postgres}
DB_PASSWORD=${POSTGRES_PASSWORD:-postgres}
DB_NAME="ai_image_bot_test"

echo "Creating test database: $DB_NAME"
echo "Host: $DB_HOST:$DB_PORT"
echo "User: $DB_USER"
echo ""

# Check if PostgreSQL is running
if ! command -v psql &> /dev/null; then
    echo "Error: psql command not found. Please install PostgreSQL client."
    exit 1
fi

# Drop database if exists (to start fresh)
echo "Dropping database if exists..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "DROP DATABASE IF EXISTS $DB_NAME;" postgres

# Create database
echo "Creating database..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "CREATE DATABASE $DB_NAME;" postgres

echo ""
echo "✅ Test database created successfully!"
echo ""
echo "To run integration tests:"
echo "  cd backend"
echo "  pytest tests/test_api_integration.py -v"
echo ""
echo "To drop test database:"
echo "  PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c \"DROP DATABASE $DB_NAME;\" postgres"
echo ""
