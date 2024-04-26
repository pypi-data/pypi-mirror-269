from logging import Logger
from finalsa.sqs.client import SqsService, SqsServiceImpl
from typing import Callable, Optional, Union, Dict, Any, List, Tuple
from finalsa.common.lambdas.sqs.SqsEvent import SqsEvent
from finalsa.common.models import SqsMessage
from pydantic import BaseModel


def get_handler_filled_args(attrrs: Dict[str, Any], payload: Union[Dict, str], parsed_event: SqsEvent) -> Dict:
    filled_args = {}
    for key, value in attrrs.items():
        if key == 'return':
            continue
        if isinstance(value, type):
            if issubclass(value, SqsEvent):
                filled_args[key] = parsed_event
                continue
            elif issubclass(value, BaseModel):
                filled_args[key] = value(**payload)
                continue
        if key == "message":
            filled_args[key] = payload
        elif key in payload:
            filled_args[key] = payload[key]
    return filled_args


class SqsHandler():

    def __init__(self, logger: Logger) -> None:
        self.handlers = {}
        self.handlers_args = {}
        self.retries = {}
        self.sqs_client = None
        self.logger = logger
        self.sqs_urls_cache = {}

    def get_sqs_client(self, default=SqsServiceImpl) -> SqsService:
        if self.sqs_client is None:
            self.sqs_client = default()
        return self.sqs_client

    def get_handler(self, topic: str) -> Optional[Callable[[Union[Dict, SqsEvent]], Union[Dict, str]]]:
        if topic not in self.handlers:
            return self.handlers.get("default")
        return self.handlers.get(topic)

    def get_retries(self, topic: str) -> int:
        if topic not in self.retries:
            return self.retries.get("default", 0)
        return self.retries.get(topic)

    def try_excecution_str(
        self,
        message: SqsEvent,
    ) -> Tuple[Optional[Union[Dict, str]], bool]:
        try:
            handler = self.get_handler("default")
            handler_attrs = self.handlers_args["default"]
            filled_args = get_handler_filled_args(
                handler_attrs, {}, message)
            response = handler(**filled_args)
            return response, True
        except Exception as e:
            self.logger.error("Error processing sqs event", extra={
                "error": e,
            })
            return None, False

    def try_excecution_dict(
            self,
            payload: Dict,
            message: SqsEvent,
            handler: Optional[Callable] = None,
            retries: Optional[int] = None
    ) -> Tuple[Optional[Union[Dict, str]], bool]:
        topic = message.topic
        if topic not in self.handlers:
            topic = "default"
        if retries is None:
            retries = self.get_retries(topic)
        if handler is None:
            handler = self.get_handler(topic)
        try:
            get_handler = self.get_handler(topic)
            handler_attrs = self.handlers_args[topic]
            filled_args = get_handler_filled_args(
                handler_attrs, payload, message)
            response = get_handler(**filled_args)
            return response, True
        except Exception as e:
            if retries > 0:
                self.logger.error("Error processing sqs event", extra={
                    "error": e,
                    "retries": retries
                })
                return self.try_excecution_dict(payload, message, handler, retries - 1)
            else:
                self.logger.error("Error processing sqs event", extra={
                    "error": e,
                    "retries": retries
                })
                return None, False

    @staticmethod
    def try_parse_payload(payload: Dict) -> Union[Dict, SqsMessage]:
        try:
            message = SqsMessage(**payload)
            return message
        except Exception:
            return payload

    def try_excution(
        self,
        message: SqsEvent
    ) -> Tuple[Optional[Union[Dict, str]], bool]:
        parsed_payload = message.try_parse()
        if isinstance(parsed_payload, str):
            return self.try_excecution_str(message)
        # TODO: Add correlation id
        real_payload = self.try_parse_payload(parsed_payload)
        if isinstance(real_payload, SqsMessage):
            message.topic = real_payload.topic
            return self.try_excecution_dict(real_payload.get_payload(), message)
        return self.try_excecution_dict(real_payload, message)

    def get_sqs_url(self, sqs_name: str) -> str:
        if sqs_name in self.sqs_urls_cache:
            return self.sqs_urls_cache[sqs_name]
        sqs_url = self.get_sqs_client().get_queue_url(sqs_name)
        self.sqs_urls_cache[sqs_name] = sqs_url
        return sqs_url

    def delete_message(self, message: SqsEvent) -> None:
        sqs_arn = message.event_source_arn
        receipt_handle = message.receipt_handle
        sqs_name = sqs_arn.split(":")[-1]
        sqs_url = self.get_sqs_url(sqs_name)
        self.get_sqs_client().delete_message(sqs_url, receipt_handle)

    def process(self, event: Dict, context: Any) -> List[Dict]:
        self.logger.info("Processing sqs event", extra={
            "context": context,
        })
        records = event['Records']
        responses = []
        for record in records:
            message = SqsEvent.from_sqs_lambda_event(record)
            response, is_sucess = self.try_excution(message)
            if is_sucess:
                self.delete_message(message)
            responses.append(response)
        return responses

    def handler(self, topic: str, retries: Optional[int] = 1) -> Callable:
        if retries < 0:
            raise ValueError("Retries must be greater than 0")
        if topic in self.handlers:
            raise ValueError("Topic already has a handler")
        self.retries[topic] = retries

        def decorator(handler: Callable) -> Callable:
            def wrapper(*args, **kwargs) -> Optional[Union[Dict, str]]:
                self.logger.info("Processing sqs event", extra={
                    "topic": topic,
                    "retries": retries
                })
                result = handler(*args, **kwargs)
                self.logger.info("Processed sqs event", extra={
                    "result": result,
                })
                return result
            self.handlers_args[topic] = handler.__annotations__
            self.handlers[topic] = wrapper
            return wrapper
        return decorator

    def default(self, retries: Optional[int] = 1) -> Callable:
        return self.handler("default", retries)

    def merge(self, other: 'SqsHandler') -> None:
        for topic, handler in other.handlers.items():
            if topic in self.handlers:
                raise ValueError("Topic already has a handler")
            self.handlers[topic] = handler
            self.handlers_args[topic] = other.handlers_args[topic]
        for topic, retries in other.retries.items():
            if topic in self.retries:
                raise ValueError("Topic already has a handler")
            self.retries[topic] = retries
