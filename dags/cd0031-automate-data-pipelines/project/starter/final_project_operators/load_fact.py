from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """
    Custom Airflow operator to load data into a fact table in Amazon Redshift.

    This operator takes a SQL query and executes an INSERT statement to load data
    into the specified fact table in Redshift.

    Attributes:
        ui_color (str): The color code for the Airflow UI.

    Args:
        redshift_conn_id (str): The connection ID for Redshift in Airflow.
        table (str): The name of the target fact table in Redshift.
        sql_query (str): The SQL query used to extract data for loading into the fact table.
        *args: Additional arguments for the BaseOperator.
        **kwargs: Additional keyword arguments for the BaseOperator.
    """
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        """
        Executes the SQL query to load data into the fact table.

        This method connects to Redshift, constructs an INSERT INTO statement
        using the provided SQL query, and runs it to load data into the table.

        Args:
            context (dict): The execution context provided by Airflow.
        
        Raises:
            Exception: If the SQL command fails to execute.
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        formatted_sql = f"INSERT INTO {self.table} {self.sql_query}"
        self.log.info(f"Loading data into {self.table} fact table")
        redshift.run(formatted_sql)
