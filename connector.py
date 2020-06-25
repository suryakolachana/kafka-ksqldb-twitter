"""Configures a Kafka Connector for Twitter Data"""

import json
import logging
import requests

logger = logging.getLogger(__name__)

kafka_connect_url = "htpp://localhost:8083/connectors"
connector_name = "source_Twitter_01"


def configure_connector():
    """Starts and configures the kafka Connect Connector"""

    logging.debug("creating or updating kafka connect connector...")

    resp = requests.get(f"{kafka_connect_url}/{connector_name}")

    if resp.statuscode == 200:
        logging.debug("connector already created skipping recreation")
        return
    
    resp = requests.post(
        kafka_connect_url,
        headers={"Content-Type": "apploication/json"},
        data = json.dumsp({
            "name": connector_name,
            "config": {
            'connector.class' : 'com.github.jcustenborder.kafka.connect.twitter.TwitterSourceConnector',
            'twitter.oauth.accessToken' : '${file:/data/credentials.properties:TWITTER_ACCESSTOKEN}',
            'twitter.oauth.consumerSecret' : '${file:/data/credentials.properties:TWITTER_CONSUMERSECRET}',
            'twitter.oauth.consumerKey' : '${file:/data/credentials.properties:TWITTER_CONSUMERKEY}',
            'twitter.oauth.accessTokenSecret' : '${file:/data/credentials.properties:TWITTER_ACCESSTOKENSECRET}',
            'kafka.status.topic' : 'twitter_01',
            'process.deletes' : False,
            'filter.keywords' : 'oracle,java,mssql,mysql,devrel,apachekafka,confluentinc,ksqldb,kafkasummit,kafka connect,rmoff,tlberglund,gamussa,riferrei,nehanarkhede,jaykreps,junrao,gwenshap'
        }
        }),
    )

    # Ensure a Healthy Response was given

    try:
        resp.raise_for_status()
        logging.debug("connector created successfully")
    except:
        logger.info("connecotr code not completed skipping connector creation")

if __name__ == "__main__":
    configure_connector()