#!/bin/bash
set -e  # Остановка на ошибке

# Экспорт пароля для psql
export PGPASSWORD="${POSTGRES_PASSWORD:-Iseedeadpeople222!}"

# Ждём PostgreSQL
echo "⏳ Waiting for PostgreSQL to start..."
until pg_isready -h db -p 5432 -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-secundadb}"; do
  echo "PostgreSQL is not ready yet - sleeping..."
  sleep 2
done
echo "✅ PostgreSQL is ready!"

# 📦 Создаём расширения (postgis уже от образа, но ltree нужно; IF NOT EXISTS безопасно)
echo "📦 Creating/ensuring PostgreSQL extensions..."
psql -h db -p 5432 -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-secundadb}" -q -c "
  -- Создаём расширения
  CREATE EXTENSION IF NOT EXISTS postgis;
  CREATE EXTENSION IF NOT EXISTS ltree;

  -- Проверяем расширения (SQL вместо \dx)
  SELECT 'Extensions list:' AS info;
  SELECT extname, extversion FROM pg_extension WHERE extname IN ('postgis', 'ltree') ORDER BY extname;

  -- Тест LTREE типа
  SELECT 'LTREE ready: ' || COALESCE(typname, 'NOT FOUND') AS ltree_status
  FROM pg_type WHERE typname = 'ltree' LIMIT 1;

  -- Тест PostGIS
  SELECT 'PostGIS ready: ' || postgis_full_version() AS postgis_status;
"
if [ $? -ne 0 ]; then
  echo "❌ Failed to create/ensure extensions!"
  exit 1
fi
echo "✅ Extensions ready!"

# 🔄 Миграции Alembic
echo "🔄 Running Alembic migrations..."
cd /src
alembic upgrade head
if [ $? -ne 0 ]; then
  echo "❌ Alembic migrations failed!"
  exit 1
fi
echo "✅ Migrations completed!"

# 🌱 Сидирование (твои данные; ::ltree для типов)
echo "🌱 Seeding database with test data..."
psql -h db -p 5432 -U "${POSTGRES_USER:-postgres}" -d "${POSTGRES_DB:-secundadb}" -q <<-EOSQL
-- Activities (path LTREE; таблица 'activities' — если 'activitys', измени)
INSERT INTO activitys (name, path, level) VALUES
('Еда', 'еда'::ltree, 0),
('Мясная продукция', 'еда.мясная'::ltree, 1),
('Молочная продукция', 'еда.молочная'::ltree, 1),
('Автомобили', 'автомобили'::ltree, 0),
('Грузовые', 'автомобили.грузовые'::ltree, 1),
('Легковые', 'автомобили.легковые'::ltree, 1),
('Запчасти', 'автомобили.легковые.запчасти'::ltree, 2),
('Аксессуары', 'автомобили.легковые.аксессуары'::ltree, 2)
ON CONFLICT (id) DO NOTHING;

-- Buildings (PostGIS geometry)
INSERT INTO buildings (address, coords) VALUES
('г. Москва, Красная площадь, 1', ST_GeomFromText('POINT(37.6173 55.7539)', 4326)),
('г. Москва, ул. Тверская, 13', ST_GeomFromText('POINT(37.6096 55.7606)', 4326)),
('г. Москва, ул. Арбат, 25', ST_GeomFromText('POINT(37.5916 55.7494)', 4326)),
('г. Москва, ул. Ленина, 42', ST_GeomFromText('POINT(37.6100 55.7500)', 4326))
ON CONFLICT (id) DO NOTHING;

-- Organizations
INSERT INTO organizations (name, building_id) VALUES
('ООО Рога и Копыта', 1),
('Мясной Двор', 2),
('Молочный Комбинат', 3),
('АвтоМир', 4),
('Грузовик Сервис', 1)
ON CONFLICT (id) DO NOTHING;

-- Phone Numbers
INSERT INTO phonenumbers (phone_number, organization_id) VALUES
('+7-495-111-11-11', 1),
('+7-495-222-22-22', 1),
('+7-495-333-33-33', 2),
('+7-495-444-44-44', 3),
('+7-495-555-55-55', 4),
('+7-495-666-66-66', 5)
ON CONFLICT (id) DO NOTHING;

-- Organization-Activity relationships
INSERT INTO organization_activities (organization_id, activity_id) VALUES
(1, 1), (1, 2), (1, 3),
(2, 2),
(3, 3),
(4, 4), (4, 6), (4, 7),
(5, 5)
ON CONFLICT DO NOTHING;

-- Проверка сидирования
SELECT 'Seeding OK: ' || COUNT(*) AS activities_count FROM activities;
EOSQL
if [ $? -ne 0 ]; then
  echo "❌ Seeding failed!"
  exit 1
fi
echo "✅ Test data seeded!"

# 🚀 Uvicorn
echo "🚀 Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000