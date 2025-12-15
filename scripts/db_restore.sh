#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "usage: ./db_restore.sh backups/file.sql"
  exit 1
fi

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/../" && pwd)

APP_ENV=${APP_ENV:-docker}
if [ "$APP_ENV" = "docker" ]; then
  ENV_FILE="$PROJECT_ROOT/.env.docker"
  CONTAINER_NAME="db"
else
  ENV_FILE="$PROJECT_ROOT/.env.local"
  CONTAINER_NAME="db"
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)

TMP_FILE=$(mktemp)

# Добавляем ON CONFLICT (headline) DO NOTHING для наложения
sed -E 's/INSERT INTO news \(([^)]+)\) VALUES \(([^)]+)\);/INSERT INTO news (\1) VALUES (\2) ON CONFLICT (headline) DO NOTHING;/' "$1" > "$TMP_FILE"

docker exec -i "$CONTAINER_NAME" \
  psql -U "$POSTGRES_USER" "$POSTGRES_DB" < "$TMP_FILE"

rm "$TMP_FILE"

echo "Database restored from $1 with ON CONFLICT (headline) DO NOTHING"