import click
from flask import g, current_app
from werkzeug.local import LocalProxy

from app.database.database_client import DatabaseClient, DatabaseType
from app.database.postgres_client import PostgresClient
from app.database.sqlite_client import SQLiteClient


# from app.database.oracle_client import OracleClient


def create_database_client(db_type: DatabaseType, connection_str: str) -> DatabaseClient:
    """Factory method to get the appropriate database client based on the database type."""
    if db_type == DatabaseType.POSTGRES:
        return PostgresClient(connection_str=connection_str)
    elif db_type == DatabaseType.SQLITE:
        return SQLiteClient(connection_str=connection_str)
    # elif db_type == DatabaseType.ORACLE:
    #     return OracleClient(connection_str=connection_str)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def init_app(app):
    # app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db(db_type: DatabaseType) -> DatabaseClient:
    """Retrieve the database client based on the database type, creating it if necessary."""
    if 'db_clients' not in g:
        g.db_clients = {}

    if db_type.value not in g.db_clients:
        conn_str = current_app.config['DATABASES'][db_type.value]
        db_client = create_database_client(db_type, conn_str)
        g.db_clients[db_type.value] = db_client
        db_client.connect()

    return g.db_clients[db_type.value]


def close_db(error=None):
    """Closes all database connections."""
    db_clients = g.pop('db_clients', {})
    for db_client in db_clients.values():
        db_client.close()


@click.command('init-db')
def init_db_command():
    """Initialize the databases with the schema defined in schema.sql."""
    init_db()
    click.echo('Initialized the databases.')


def init_db():
    """Initialize all databases with the schema defined in schema.sql."""
    for db_type in DatabaseType:
        db = get_db(db_type)
        schema_path = f'{db_type.value}_schema.sql'
        if current_app.open_resource(schema_path, mode='r').read():
            with current_app.open_resource(schema_path, mode='r') as f:
                db.execute(f.read())  # Adjust method based on how schema is applied


# Direct access proxies
pg_db = LocalProxy(lambda: get_db(DatabaseType.POSTGRES))
sqlite_db = LocalProxy(lambda: get_db(DatabaseType.SQLITE))
# ora_db = LocalProxy(lambda: get_db(DatabaseType.ORACLE))  # Uncomment when OracleClient is implemented
