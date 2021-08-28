import json
from typing import Callable

import pika
from pika.adapters.blocking_connection import BlockingChannel

from logger.log import logger
from .structures import ClientConfig


class RabbitConnectionError(Exception):
    pass


class RabbitClient:
    def __init__(
            self,
            raw_rabbit_config: dict,
            process_task_function: Callable[[str], dict],
            consuming_queue_exchange: str,
            consuming_queue_title: str,
    ):
        """Initialises variables and channels to work with RabbitMQ server."""
        self._rabbit_config = ClientConfig(**raw_rabbit_config)

        self.__consuming_queue_title = consuming_queue_title
        self.__consuming_queue_exchange = consuming_queue_exchange

        self.__process_task = process_task_function

        # fields initialised after __connect()
        self.__connection: pika.BlockingConnection
        self.__channel: BlockingChannel

        self.__connect()

    def begin_consumption(self) -> None:
        """Starts to get incoming messages from a channel."""
        msg_info = "Ready to obtain tasks from a queue."
        logger.info(msg_info)

        while True:
            try:
                self.__channel.start_consuming()
            except RabbitConnectionError:
                self.__connect()
                msg_info = "Success. Reconnected to RabbitMQ. New connection and channels were created."
                logger.info(msg_info)

    def _on_request(
            self,
            ch: pika.adapters.blocking_connection.BlockingChannel,
            method: pika.spec.Basic.Deliver,
            props: pika.spec.BasicProperties,
            body: bytes,
    ) -> None:
        """Callback to work on incoming tasks.
        All exception will be delivered to begin_consumption call."""
        task_in = body.decode()

        msg_info = f'Got task: "{task_in}"'
        logger.info(msg_info)

        task_out = self.__process_task(task_in)

        msg_info = f'Task: "{task_in}" is processed. Result: {task_out}'
        logger.info(msg_info)
        self.__publish_result(result=task_out, method=method)

    def __connect(self) -> None:
        """Initialises connection to RabbitMQ.
        Creates channels to publish and consume messages."""
        creds = pika.PlainCredentials(
            self._rabbit_config.user, self._rabbit_config.password
        )
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self._rabbit_config.ip,
                port=self._rabbit_config.port,
                credentials=creds,
            )
        )
        self.__channel = self.__connection.channel()
        self.__init_publishing_exchange()
        self.__init_consuming_exchange()

    def __init_publishing_exchange(self) -> None:
        """Inits publishing exchange with defined settings."""
        self.__channel.exchange_declare(
            exchange=self._rabbit_config.exchangeAnswers,
            exchange_type="direct",
            durable=True,
        )

    def __init_consuming_exchange(self) -> None:
        self.__channel.queue_declare(queue=self.__consuming_queue_title, durable=True)

        self.__channel.queue_bind(
            exchange=self.__consuming_queue_exchange,
            queue=self.__consuming_queue_title
        )

        self.__channel.basic_consume(
            queue=self.__consuming_queue_title, on_message_callback=self._on_request
        )

    def __publish_result(
            self,
            result: dict,
            method: pika.spec.Basic.Deliver,
    ) -> None:
        """Makes manipulations to publish the result of the task."""
        try:
            self.__channel.basic_publish(
                exchange='task',
                routing_key='',
                body=json.dumps(result).encode(),
            )
            # indicate that task is completed
            self.__channel.basic_ack(delivery_tag=method.delivery_tag)
        except pika.exceptions.AMQPConnectionError:
            msg_err = "RabbitMQ error. AMQP Connection error. Need to reconnect."
            logger.error(msg_err)
            raise RabbitConnectionError

        msg_info = "Result is published."
        logger.info(msg_info)
