import json
from contextlib import suppress
from uuid import uuid4

import pytest
from decouple import UndefinedValueError, config
from fauna import fql
from fauna.client import Client

try:
    from fluctuate.migrations import migrate
except ImportError:
    # Create a mock of the migrate function that will run pytest.skip on any call or
    # attribute access.
    class MigrateMock:
        def __getattr__(self, name):
            pytest.skip(
                "Cannot use fluctuate migrations without installing the `fluctuate`"
                " extra dependencies."
            )

        def __call__(self, *args, **kwargs):
            pytest.skip(
                "Cannot use fluctuate migrations without installing the `fluctuate`"
                " extra dependencies."
            )

    migrate = MigrateMock()


@pytest.fixture(scope="session")
def fauna_admin_key(request):
    """Attempts to return a Fauna DB admin key based on the environment configuration.

    In order to use this fixture, one of `FAUNA_ADMIN_KEY` or
    `FAUNA_ADMIN_KEY_SECRET_ID` must either be set as an environment variable or in a
    .env file. If neither are set, the test requesting this fixture is skipped.

    `FAUNA_ADMIN_KEY` takes precedent over `FAUNA_ADMIN_KEY_SECRET_ID`.

    This fixture is session scoped to reduce potentially hitting SecretsManager multiple
    times to retrieve the same secret value in the same test session.
    """
    with suppress(UndefinedValueError):
        return config("FAUNA_ADMIN_KEY")

    with suppress(UndefinedValueError, pytest.FixtureLookupError):
        secretsmanager_client = request.getfixturevalue("secretsmanager_client")
        secret = secretsmanager_client.get_secret_value(
            SecretId=config("FAUNA_ADMIN_KEY_SECRET_ID")
        )
        secret = json.loads(secret["SecretString"])
        # Return the secret key out of the Key object.
        return secret["secret"]

    pytest.skip(
        "Cannot access FaunaDB without setting `FAUNA_ADMIN_KEY` or"
        " `FAUNA_ADMIN_KEY_SECRET_ID` in an environment variable or .env file. If"
        " FAUNA_ADMIN_KEY_SECRET_ID is set, and you're still seeing this message,"
        " ensure the aws extra dependencies are installed."
    )


@pytest.fixture(scope="session")
def fauna_admin_client(fauna_admin_key):
    """Create an return a FQLv10 admin client for the top level database.

    This fixture is session scoped as the admin key is expected to be set once and not
    changed during the session, so we can save time by not needing to re-instantiate the
    admin client multiple times.
    """
    return Client(secret=fauna_admin_key)


@pytest.fixture
def test_db_scoped_key():
    """This fixture returns a method to use to construct a scoped key for the provided
    child DB.

    See the following documentation link for more info on scoped keys:
    https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
    """

    def _inner(test_db, admin_key):
        """This returns a key scoped to the child DB given the child DB object from
        FaunaDB and the admin key for the parent DB.

        See the following documentation link for more info on scoped keys:
        https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
        """
        return f"{admin_key}:{test_db['name']}:admin"

    return _inner


@pytest.fixture
def test_db(fauna_admin_client):
    """Create a randomly named test child database for use in this test module and
    return its name.

    This will delete the test database after the session completes.
    """
    # Create the test database
    test_db_name = f"test_{uuid4().hex}"
    result = fauna_admin_client.query(
        fql(
            "Database.create({name: ${test_db_name}}) {name}", test_db_name=test_db_name
        )
    )

    # Yield the test database.
    yield result.data

    # Use a top level admin key to delete the child database.
    fauna_admin_client.query(
        fql("Database.byName(${test_db_name}).delete()", test_db_name=test_db_name)
    )


@pytest.fixture
def test_db_with_migrations(test_db, fauna_admin_key, test_db_scoped_key):
    """Create a randomly named test child database for use in this test module, apply
    migrations to it, and return it.

    This will delete the test database after the session completes.
    """
    # Apply migrations.
    migrate(key=test_db_scoped_key(test_db=test_db, admin_key=fauna_admin_key))

    return test_db


@pytest.fixture
def fauna_test_client(test_db, test_db_scoped_key, fauna_admin_key):
    """Returns a FQLv10 test client configured with access to a test fauna database."""
    # Create a fauna client using a scoped key to the child database. See the following
    # documentation link for more info on scoped keys:
    # https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
    return Client(secret=test_db_scoped_key(test_db=test_db, admin_key=fauna_admin_key))


@pytest.fixture
def fauna_test_client_with_migrations(
    test_db_with_migrations, test_db_scoped_key, fauna_admin_key
):
    """Returns a test client configured with access to a test fauna database that has
    had migrations applied to it.
    """
    # Create a fauna client using a scoped key to the child database. See the following
    # documentation link for more info on scoped keys:
    # https://docs.fauna.com/fauna/current/learn/security_model/keys#scoped-keys
    return Client(
        secret=test_db_scoped_key(
            test_db=test_db_with_migrations, admin_key=fauna_admin_key
        )
    )
