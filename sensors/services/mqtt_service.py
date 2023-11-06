import logging
import time

from sensors.services.base_service import BaseService
from paho.mqtt import client as mqtt_client
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 


class MQTTService(BaseService):
    def __init__(self, broker: str, port: int, topic: str, client_id: str, user_name: str, password: str):
        self.__logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        self.__client = mqtt_client.Client(client_id=client_id, protocol=mqtt_client.MQTTv5)
        self.__client.username_pw_set(username=user_name, password=password)
        self.__client.enable_logger(logger=self.__logger)

        self.__broker = broker
        self.__port = port
        self.__topic = topic

        self.__first_reconnect_delay = 1
        self.__delay_before_stop = 10
        self.__reconnect_rate = 2
        self.__max_reconnect_count = 12
        self.__max_reconnect_delay = 60

        self.__expiry_interval = 30
        self.__session_expiry_interval = 30 * 60

        self.__mqtt_keepalive = 60
        self.__mqtt_qos = 0

    def __on_connect(self, client: mqtt_client.Client, userdata, flags, rc, properties=None) -> None:
        if rc == 0 and client.is_connected():
            self.__logger.info("Connected to MQTT Broker!")
            subscribe_properties = Properties(PacketTypes.SUBSCRIBE)
            client.subscribe(topic=self.__topic, qos=self.__mqtt_qos, options=None, properties=subscribe_properties)
        else:
            self.__logger.info(f"Failed to connect to MQTT Broker, return code {rc}")

    def __on_disconnect(self, client, userdata, rc, properties=None) -> None:
        self.__logger.info(f"Disconnected with result code: {rc}")
        reconnect_count, reconnect_delay = 0, self.__first_reconnect_delay
        while reconnect_count < self.__max_reconnect_count:
            self.__logger.info(f"Reconnecting in {reconnect_delay} seconds ...")
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                self.__logger.info("Reconnected successfully!")
                return
            except Exception as ex:
                self.__logger.error(msg="Reconnect failed. Retrying ...", exc_info=ex, stack_info=True)

            reconnect_delay *= self.__reconnect_rate
            reconnect_delay = min(reconnect_delay, self.__max_reconnect_delay)
            reconnect_count += 1
        self.__logger.info(f"Reconnect failed after {reconnect_count} attempts. Exiting ...")

    def __on_message(self, client: mqtt_client.Client, userdata, msg: mqtt_client.MQTTMessage) -> None:
        log_info: str = f"Received message {msg.payload.decode()} on topic '{msg.topic}'"
        log_info += f" with QoS {msg.qos}"
        self.__logger.info(log_info)

    def run(self) -> None:
        if self.__client is not None:
            try:
                self.__client.on_connect = self.__on_connect
                self.__client.on_disconnect = self.__on_disconnect
                self.__client.on_message = self.__on_message
                connect_properties = Properties(PacketTypes.CONNECT)
                connect_properties.SessionExpiryInterval = self.__session_expiry_interval
                self.__client.connect(
                    host=self.__broker, 
                    port=self.__port, 
                    clean_start=mqtt_client.MQTT_CLEAN_START_FIRST_ONLY, 
                    keepalive=self.__mqtt_keepalive,
                    properties=connect_properties
                )
                self.__client.loop_start()
                self.__logger.info("A MQTT Service is started ...")
                time.sleep(self.__first_reconnect_delay)
            except Exception as ex:
                self.__logger.error(msg="Failed to start MQTT Service ...", exc_info=ex, stack_info=True)

    def stop(self):
        if self.__client is not None:
            try:
                time.sleep(self.__delay_before_stop)
                if self.__client.is_connected():
                    disconect_properties = Properties(PacketTypes.DISCONNECT)
                    self.__client.disconnect(properties=disconect_properties)
                self.__client.loop_stop()
            except Exception as ex:
                self.__logger.error(msg="Failed to stop MQTT Service ...", exc_info=ex, stack_info=True)

    
    def send_message(self, message: str) -> None:
        if self.__client is not None:
            try:
                if self.__client.is_connected():
                    publish_properties = Properties(PacketTypes.PUBLISH)
                    publish_properties.MessageExpiryInterval = self.__expiry_interval
                    result = self.__client.publish(topic=self.__topic, payload=message, qos=self.__mqtt_qos, properties=publish_properties)
                    result.wait_for_publish()
                    status = result[0]
                    if status == 0:
                        self.__logger.info(f"Send message: '{message}' to topic: '{self.__topic}'")
                    else:
                        self.__logger.info(f"Failed to send message '{message}' to topic '{self.__topic}'")
            except Exception as ex:
                self.__logger.error(msg="Failed to send message in MQTT Service ...", exc_info=ex, stack_info=True)
            