import functools
import pika
import time
import json

from varys.process import Process


class Producer(Process):
    def __init__(
        self,
        message_queue,
        exchange,
        configuration,
        log_file,
        log_level,
        queue_suffix,
        exchange_type,
        routing_key="arbitrary_string",
        reconnect_wait=10,
    ):
        super().__init__(
            message_queue,
            exchange,
            configuration,
            log_file,
            log_level,
            queue_suffix,
            exchange_type,
            routing_key=routing_key,
            reconnect_wait=reconnect_wait,
        )

        self._message_number = 0

        self._message_properties = pika.BasicProperties(
            content_type="json", delivery_mode=pika.DeliveryMode.Persistent,
        )

    def publish_message(self, message, max_attempts=1):
        try:
            message_str = json.dumps(message, ensure_ascii=False)
        except TypeError:
            self._log.error(f"Unable to serialise message into json: {str(message)}")

        attempt = 0
        while attempt < max_attempts:
            try:
                attempt += 1
                self._log.info(f"Sending message (attempt {attempt}): {json.dumps(message)}")
                self._connection.add_callback_threadsafe(
                    functools.partial(
                        self._channel.basic_publish,
                        self._exchange,
                        self._routing_key,
                        message_str,
                        self._message_properties,
                        mandatory=True,
                    )
                )
            except pika.exceptions.ConnectionWrongStateError:
                self._log.exception(f"Exception while trying to publish message on attempt {attempt}!")

                if attempt < max_attempts and self._reconnect_wait >= 0:
                    time.sleep(self._reconnect_wait)
                    continue
                else:
                    raise

            break

        self._message_number += 1
        self._log.info(f"Published message #{self._message_number}")

    def run(self):
        while not self._stopping:
            try:
                self._connection = pika.BlockingConnection(self._parameters)
                self._channel = self._connection.channel()
                self._channel.exchange_declare(
                    exchange=self._exchange,
                    exchange_type=self._exchange_type,
                    durable=True,
                )
                self._channel.queue_declare(queue=self._queue, durable=True)
                self._channel.queue_bind(queue=self._queue, exchange=self._exchange, routing_key=self._routing_key)
                self._channel.confirm_delivery()
                # time_limit=None leads to the connection being dropped for inactivity
                # not sure if this should be while not self._stopping
                while True:
                    self._connection.process_data_events(time_limit=1)
            except:
                self._log.exception("Producer caught exception:")

            if self._stopping or self._reconnect_wait < 0:
                break
            else:
                time.sleep(self._reconnect_wait)
                continue

    def stop(self):
        self._log.info("Stopping producer as instructed...")
        # probably have to say we're closing so run doesn't try to reopen connection
        self._stopping = True

        self._connection.add_callback_threadsafe(
            functools.partial(self._connection.process_data_events, time_limit=1)
        )

        self._connection.add_callback_threadsafe(
            self._channel.close
        )
        self._connection.add_callback_threadsafe(
            self._connection.close
        )

        self._log.debug("Stopping producer logger...")
        self._stop_logger()

        self._log.info("Stopped producer as instructed.")
