# python -m pip install pip polars sqlalchemy psycopg2 daves_utilities --upgrade
# python
from urllib.parse import quote

from sqlalchemy.engine import create_engine

from daves_utilities.david_secrets import get_credentials

def connect_to_postgres_kubernetes_home():
    # Get the credentials
    crd = get_credentials("postgres")

    # URL encode the username and password
    hostname = crd["hostname"]
    username = crd["usr"]
    password = quote(crd["pwd"])
    connection_string = f"postgresql://{username}:{password}@{hostname}:5432/postgres"

    # Create the engine
    engine = create_engine(connection_string)

    return engine
