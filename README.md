## Final Solution
![image](https://github.com/Dev317/block_gas_pipeline/assets/70529335/1411a554-513c-4cca-bb3c-2d5934827981)

## Techstack
1. Airflow to orchestrate pipeline
2. Alchemy socket to get data about latest block
3. InfluxDB to store gas used value for each newly mined block
4. Docker (docker-compose) to run different components locally

## How to run
1. Create an `.env` file as follow
  ```
  # Airflow variables
  AIRFLOW_VERSION=2.8.3
  AIRFLOW_UID=50000
  AIRFLOW_PROJ_DIR=.
  _AIRFLOW_WWW_USER_USERNAME={YOUR_AIRFLOW_USERNAME}
  _AIRFLOW_WWW_USER_PASSWORD={YOUR_AIRFLOW_PASSWORD}
  
  # Alchemy variables
  ALCHEMY_SOCKET_URL={YOUR_ALCHEMY_SOCKET}
  
  # InfluxDB variables
  INFLUX_TOKEN={YOUR_INFLUX_DB_TOKEN}
  INFLUX_BUCKET={YOUR_INFLUX_DB_BUCKET}
  INFLUX_ORG={YOUR_INFLUX_DB_ORG}
  INFLUX_URL="http://influxdb:8086"
  ```
2. Initiate the whole stack with
  ```
  docker compose up --build
  ```
3. Login to InfluxDB UI at `http://localhost:8086` and generate the InfluxDB token. Paste the token into `.env` file
4. Login to Airflow at `http://localhost:8080` with the username and password indicated in `.env` file
5. Trigger the `alchemy_block_dag` pipeline to start collecting the data! 
 
