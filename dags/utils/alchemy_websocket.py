from websocket import WebSocketApp
import json
from influxdb_client import Point


class AlchemySocket(WebSocketApp):

    def __init__(self,
                 socket_url,
                 initiate_msg,
                 logger,
                 influx_api,
                 bucket,
                 org
                ):
        self.logger = logger

        def on_message(ws, message):
            event = json.loads(message)
            self.logger.info(f"Received message: {event}")
            if 'params' in event:
                result_data = event['params']['result']
                p = Point("gasUsed").field("gasUsed", int(result_data['gasUsed'], 16))
                influx_api.write(bucket=bucket, org=org, record=p)
                self.logger.info("Successfully written to InfluxDB")

        def on_error(ws, error):
            self.logger.error(error)

        def on_close(ws, close_status_code, close_msg):
            self.logger.error(f"Closed connection with status code: {close_status_code}, message: {close_msg}")

        def on_open(ws):
            self.logger.info("Connection established")
            ws.send(initiate_msg)
            self.logger.info(f"Sent initiate message: {initiate_msg}")

        super().__init__(url=socket_url,
                         on_open=on_open,
                         on_message=on_message,
                         on_error=on_error,
                         on_close=on_close)
