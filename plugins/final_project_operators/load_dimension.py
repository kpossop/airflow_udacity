from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """
    Custom Airflow operator to load data into a dimension table in Amazon Redshift.

    This operator allows loading data into a dimension table either by appending
    or using a truncate-insert pattern, based on the specified mode.

    Attributes:
        ui_color (str): The color code for the Airflow UI.

    Args:
        redshift_conn_id (str): The connection ID for Redshift in Airflow.
        table (str): The name of the target dimension table in Redshift.
        sql_query (str): The SQL query used to extract data for loading into the dimension table.
        mode (str): The mode of data loading, either 'append' or 'truncate-insert'.
        *args: Additional arguments for the BaseOperator.
        **kwargs: Additional keyword arguments for the BaseOperator.
    """
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql_query="",
                 mode="append",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.mode = mode

    def execute(self, context):
        """
        Executes the SQL query to load data into the dimension table.

        This method connects to Redshift and runs an INSERT INTO statement to load data
        into the table. If the mode is 'truncate-insert', the table is truncated before loading.

        Args:
            context (dict): The execution context provided by Airflow.
        
        Raises:
            Exception: If the SQL command fails to execute.
        """
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        if self.mode == 'truncate-insert':
            self.log.info(f"Truncating {self.table} table")
            redshift.run(f"TRUNCATE TABLE {self.table}")

        formatted_sql = f"INSERT INTO {self.table} {self.sql_query}"
        self.log.info(f"Loading data into {self.table} dimension table")
        redshift.run(formatted_sql)
