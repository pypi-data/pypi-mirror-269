from typing import Optional
from finalsa.common.lambdas.app.AppEntry import AppEntry
from logging import Logger


class App(AppEntry):

    def __init__(
        self,
        logger: Optional[Logger] = None
    ) -> None:
        if logger is None:
            logger = Logger("root")
        super().__init__(logger)

    def register(self, app_entry: AppEntry) -> None:
        if self.__is_test__:
            app_entry.set_test_mode()
        self.sqs.merge(app_entry.sqs)
        self.http.merge(app_entry.http)
