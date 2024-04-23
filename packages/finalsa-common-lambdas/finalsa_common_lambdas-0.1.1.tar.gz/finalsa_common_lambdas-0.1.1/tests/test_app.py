from finalsa.common.lambdas.app import App, AppEntry
from json import dumps


def test_app_entry_sqs():
    app_entry = AppEntry()

    @app_entry.sqs.default()
    def sqs_lambda_handler(message: dict):
        print(message)

    app_entry_two = AppEntry()

    @app_entry_two.sqs.handler("one-time-actions")
    def one_time_actions_sqs_lambda_handler(message: dict):
        print(message)

    # assert app_entry.sqs.default() == sqs_lambda_handler
    # assert app_entry_two.sqs.handler("one-time-actions") == one_time_actions_sqs_lambda_handler
    assert app_entry.sqs.handlers["default"] == sqs_lambda_handler
    assert app_entry_two.sqs.handlers["one-time-actions"] == one_time_actions_sqs_lambda_handler

    app = App()
    app.set_test_mode()
    app.register(app_entry)
    app.register(app_entry_two)

    assert app.sqs.handlers["default"] == sqs_lambda_handler
    assert app.sqs.handlers["one-time-actions"] == one_time_actions_sqs_lambda_handler


def test_app_entry_http():
    app_entry = AppEntry()

    @app_entry.http.post("/one-time-actions")
    def create_one_time_action(body: dict):
        pass

    app_entry_two = AppEntry()

    @app_entry_two.http.get("/one-time-actions")
    def get_one_time_action():
        pass

    assert app_entry.http.handlers["POST"]["/one-time-actions/"]["handler"] == create_one_time_action
    assert app_entry_two.http.handlers["GET"]["/one-time-actions/"]["handler"] == get_one_time_action

    app = App()
    app.register(app_entry)
    app.register(app_entry_two)

    assert app.http.handlers["POST"]["/one-time-actions/"]["handler"] == create_one_time_action
    assert app.http.handlers["GET"]["/one-time-actions/"]["handler"] == get_one_time_action


def test_app_entry_sqs_and_http():

    app_container = AppEntry()

    @app_container.sqs.default()
    def sqs_lambda_handler(message: dict):
        print(message)
        return message

    @app_container.http.post("/one-time-actions")
    def create_one_time_action(body: dict):
        return body

    app = App()
    app.set_test_mode()
    app.register(app_container)

    assert app.sqs.handlers["default"] == sqs_lambda_handler
    assert app.http.handlers["POST"]["/one-time-actions/"]["handler"] == create_one_time_action
    real_message_body = {
        "test": "test"
    }
    body = dumps({
        'Type': 'Notification',
        'TopicArn': 'mytopic',
        'Message': dumps(real_message_body),
        'MessageAttributes': {'correlation_id': {
            'Type': 'String', 'Value': '123e4567-e89b-12d3-a456-426614174000'
        }}
    })
    response = app.execute({
        "eventSource": "aws:sqs",
        "Records": [
            {
                "messageId": "c80e8021-a70a-42c7-a470-796e1186f753",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": body,
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                }

            }
        ]
    }, {})
    assert response == [real_message_body]

    response = app.execute({
        "httpMethod": "POST",
        "path": "/one-time-actions/",
        "body": dumps(real_message_body)
    }, {})
    assert response["statusCode"] == 200
    assert response["body"] == dumps(real_message_body)
