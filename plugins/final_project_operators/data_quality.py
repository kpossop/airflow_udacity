from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    Custom Airflow operator to perform data quality checks on tables in Amazon Redshift.

    This operator runs one or more SQL queries and compares their results to expected values.
    If any of the checks fail, an exception is raised to alert of data quality issues.

    Attributes:
        ui_color (str): The color code for the Airflow UI.

    Args:
        redshift_conn_id (str): The connection ID for Redshift in Airflow.
        test_cases (list): A list of dictionaries, each containing a 'test_sql' query and an 'expected_result'.
        *args: Additional arguments for the BaseOperator.
        **kwargs: Additional keyword arguments for the BaseOperator.
    """
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 test_cases=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.test_cases = test_cases

    def execute(self, context):
        """
        Executes the data quality checks defined in the test_cases attribute.

        Each test case consists of an SQL query and the expected result. If the result of any
        test does not match the expected result, an exception is raised.

        Args:
            context (dict): The execution context provided by Airflow.

        Raises:
            ValueError: If any data quality check fails.
        """
        self.log.info("Running data quality checks")
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        for test_case in self.test_cases:
            sql = test_case['test_sql']
            expected_result = test_case['expected_result']
            
            records = redshift_hook.get_records(sql)
            if records[0][0] != expected_result:
                raise ValueError(f"Data quality check failed. SQL: {sql}, Expected: {expected_result}, Got: {records[0][0]}")
            
            self.log.info(f"Data quality check passed. SQL: {sql}, Expected: {expected_result}, Got: {records[0][0]}")
