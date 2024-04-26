from typing import Optional, Union, Dict, Any, List
from finalsa.common.lambdas.sqs.SqsHandler import SqsHandler
from finalsa.common.lambdas.http.HttpHandler import HttpHandler
from finalsa.sqs.client import SqsServiceTest
from logging import Logger, getLogger
from warnings import warn


class AppEntry():

    def __init__(self, logger: Optional[Logger] = None) -> None:
        if logger is None:
            logger = getLogger("root")
        self.__is_test__ = False
        self.sqs = SqsHandler(logger)
        self.http = HttpHandler(logger)

    def sqs_excecution(self, event: Dict, context: Any) -> List[Optional[Dict]]:
        return self.sqs.process(event, context)

    def http_excecution(self, event: Dict, context: Any) -> Dict:
        return self.http.process(event, context)

    def default_excutor(self, event: Dict, context: Optional[Any] = None) -> Union[List[Optional[Dict]], Dict]:
        warn("Use execute instead", DeprecationWarning)
        return self.execute(event, context)

    def execute(self, event: Dict, context: Optional[Any] = None) -> Union[List[Optional[Dict]], Dict]:
        if context is None:
            context = {}
        is_sqs = event.get("Records", None)
        if is_sqs:
            return self.sqs_excecution(event, context)
        return self.http_excecution(event, context)

    def set_test_mode(self) -> None:
        self.__is_test__ = True
        self.sqs.get_sqs_client(default=SqsServiceTest)
