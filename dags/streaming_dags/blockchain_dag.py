import os
from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from utils.alchemy_websocket import AlchemySocket
from dotenv import load_dotenv
import logging
import rel
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


load_dotenv(f"{os.getcwd()}/.env")
dag_logger = logging.getLogger(__name__)

def establish_socket_client(socket_url,
                            initiate_msg,
                            logger,
                            influx_token,
                            bucket,
                            org,
                            url):
    logger.info("Establishing InfluxDB sink client")
    influx_client = influxdb_client.InfluxDBClient(
        url=url,
        token=influx_token,
        org=org
    )
    api = influx_client.write_api(write_options=SYNCHRONOUS)

    logger.info("Creating Alchemy socket")
    ws = AlchemySocket(socket_url=socket_url,
                       initiate_msg=initiate_msg,
                       logger=logger,
                       influx_api=api,
                       bucket=bucket,
                       org=org)
    dag_logger.info("Running Alchemy socket client")
    ws.run_forever(dispatcher=rel, reconnect=1)
    rel.signal(2, rel.abort)
    rel.dispatch()

default_args = {
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
    "max_threads": 1,
    "max_active_runs": 1,
    "concurrency": 1
}

dag_description = "Blockchain data real-time processing pipeline"
tags = ["alchemy", "real-time"]

with DAG("alchemy_block_dag",
         default_args=default_args,
         description=dag_description,
         tags=tags) as dag:

    establish_socket = PythonOperator(
        task_id="establish_socket",
        python_callable=establish_socket_client,
        op_kwargs={
            "socket_url": os.getenv("ALCHEMY_SOCKET_URL"),
            "initiate_msg": '{"jsonrpc":"2.0","id": 1, "method": "eth_subscribe", "params": ["newHeads"]}',
            "logger": dag_logger,
            "influx_token": os.getenv("INFLUX_TOKEN"),
            "bucket": os.getenv("INFLUX_BUCKET"),
            "org": os.getenv("INFLUX_ORG"),
            "url": os.getenv("INFLUX_URL")
        }
    )

    establish_socket
