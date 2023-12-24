import os


class DbCredentials:
    """
        A class for handling database credentials.

        This class initializes an instance containing database credentials
        and application settings, which are extracted from environment variables.

        Attributes:
            db_host (str): Host address of the database, fetched from the 'DB_HOST' environment variable.
            db_username (str): Username for the database, fetched from the 'DB_USERNAME' environment variable.
            db_password (str): Password for the database, fetched from the 'DB_PASSWORD' environment variable.
            db_port (str): Port number for the database, fetched from the 'DB_PORT' environment variable.
            application (str): Name or identifier of the application using these credentials,
                               fetched from the 'APPLICATION' environment variable.

        Note:
            If the environment variables are not set, the corresponding attributes are initialized to None.
        """

    def __init__(self):
        self.db_host = os.getenv("DB_HOST", None)
        self.db_username = os.getenv("DB_USERNAME", None)
        self.db_password = os.getenv("DB_PASSWORD", None)
        self.db_port = os.getenv("DB_PORT", None)
        self.application = os.getenv("APPLICATION", None)
