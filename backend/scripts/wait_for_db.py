import time

import psycopg2
from sqlalchemy.engine.url import make_url

from app.config import settings


def main() -> None:
    url = make_url(settings.database_url)
    host = url.host or 'postgres'
    port = int(url.port or 5432)
    user = url.username
    password = url.password
    database = url.database

    deadline = time.time() + 90
    last_error = None

    while time.time() < deadline:
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=database,
                connect_timeout=3,
            )
            conn.close()
            print('Database is ready')
            return
        except Exception as exc:
            last_error = exc
            print(f'Waiting for database at {host}:{port}...')
            time.sleep(2)

    raise SystemExit(f'Database is not ready after timeout: {last_error}')


if __name__ == '__main__':
    main()
