from typing import Callable
from flask import Flask
from functools import wraps
import pika


class PikaRabbitMQ:
    def __init__(self, app: Flask = None):
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app
        self.config = app.config

    def push(self, key, message):
        self.params = pika.URLParameters(self.config.get("RABBITMQ_URL", ""))
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=key)
        self.channel.basic_publish(
            exchange="",
            routing_key=key,
            body=message,
        )

        self.channel.close()

    def consumes(self, key):
        self.params = pika.URLParameters(self.config.get("RABBITMQ_URL", ""))
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(key)

        def callback(ch, method, properties, body):
            print("Receive new messages")
            print(ch)
            print(method)
            print(properties)
            print(body)

        self.channel.basic_consume(key, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
        self.channel.close()

    def listen(self, key) -> Callable:
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.params = pika.URLParameters(self.config.get("RABBITMQ_URL", ""))
                self.connection = pika.BlockingConnection(self.params)
                self.channel = self.connection.channel()
                self.channel.queue_declare(key)

                def callback(ch, method, properties, body):
                    return func(key, body, *args, **kwargs)

                self.channel.basic_consume(
                    key, on_message_callback=callback, auto_ack=True
                )
                self.channel.start_consuming()
                self.channel.close()

                return func(self.body, *args, **kwargs)

            wrapper()

            return wrapper

        return decorator
