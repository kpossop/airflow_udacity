from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.secrets.metastore import MetastoreBackend

class StageToRedshiftOperator(BaseOperator):
    """
    Custom Airflow operator to load data from S3 to Amazon Redshift using the COPY command.

    This operator connects to Amazon Redshift and loads data from a specified S3 path into a
    target table using the AWS access and secret keys stored in Airflow connections.

    Attributes:
        ui_color (str): The color code for the Airflow UI.
        template_fields (tuple): Fields that support Airflow's template rendering.

    Args:
        redshift_conn_id (str): The connection ID for Redshift in Airflow.
        aws_credentials_id (str): The connection ID for AWS credentials in Airflow.
        table (str): The name of the target Redshift table.
        s3_bucket (str): The S3 bucket name where the data is stored.
        s3_key (str): The S3 key (path) for the data file.
        json_path (str): The JSON path file or 'auto' for Redshift's default. Defaults to 'auto'.
        region (str): The AWS region where the S3 bucket is located. Defaults to 'us-west-2'.
        *args: Additional arguments for the BaseOperator.
        **kwargs: Additional keyword arguments for the BaseOperator.
    """
    ui_color = '#358140'
    template_fields = ("s3_key", "json_path")  # Incluyendo json_path si es necesario renderizarlo dinámicamente

    @apply_defaults
    def __init__(self,
                 redshift_conn_id: str,
                 aws_credentials_id: str,
                 table: str,
                 s3_bucket: str,
                 s3_key: str,
                 json_path: str = 'auto',
                 region: str = 'us-west-2',
                 *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path
        self.region = region

    def execute(self, context):
        """
        Executes the COPY command to load data from S3 to Redshift.

        This method connects to Redshift, retrieves AWS credentials from Airflow connections,
        constructs the COPY SQL command, and runs it.

        Args:
            context (dict): The execution context provided by Airflow.
        
        Raises:
            Exception: If the COPY command fails to execute.
        """
        metastoreBackend = MetastoreBackend()
        aws_connection = metastoreBackend.get_connection(self.aws_credentials_id)
        access_key = aws_connection.login
        secret_key = aws_connection.password

        self.log.info(f"Starting data copy from S3 to Redshift table {self.table}")

        rendered_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        copy_sql = f"""
        COPY {self.table}
        FROM '{s3_path}'
        ACCESS_KEY_ID '{access_key}'
        SECRET_ACCESS_KEY '{secret_key}'
        REGION '{self.region}'
        FORMAT AS JSON '{self.json_path}';
        """
        
        try:
            redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
            self.log.info(f"Executing COPY command for {self.table}")
            redshift.run(copy_sql)
            self.log.info(f"Data successfully copied to {self.table}")
        except Exception as e:
            self.log.error(f"Failed to copy data to {self.table}: {e}")
            raise

