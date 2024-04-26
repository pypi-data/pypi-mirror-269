from finalsa.common.lambdas.http import HttpHandler, HttpHeaders
from logging import getLogger
from pydantic import BaseModel
from json import dumps


def test_fixed_path():
    test_path = ["arg1"]
    assert HttpHandler.get_regex_path(
        test_path, ["arg1"]) == r"/(?P<arg1>[^/]+)/"

    test_path = ["path", "arg1", "path", "arg2"]
    assert HttpHandler.get_regex_path(
        test_path, ["arg1", "arg2"]) == r"/path/(?P<arg1>[^/]+)/path/(?P<arg2>[^/]+)/"

    test_path = ["path"]
    assert HttpHandler.get_regex_path(test_path, []) == r"/path/"


def test_match_key():
    match_list = {
        r"/path/": "value1",
        r"/path/(?P<arg1>[^/]+)/": "value2",
        r"/path/(?P<arg1>[^/]+)/path/(?P<arg2>[^/]+)/": "value3",
        r"/path/(?P<arg1>[^/]+)/path/(?P<arg2>[^/]+)/path/(?P<arg3>[^/]+)/": "value4",
    }

    assert HttpHandler.match_key(match_list, "/path/")[0] == "value1"
    assert HttpHandler.match_key(match_list, "/path/")[1] == ()
    assert HttpHandler.match_key(match_list, "/path/1/")[0] == "value2"
    assert HttpHandler.match_key(match_list, "/path/1/")[1] == ("1",)
    assert HttpHandler.match_key(match_list, "/path/1/path/2/")[0] == "value3"
    assert HttpHandler.match_key(
        match_list, "/path/1/path/2/")[1] == ("1", "2")
    assert HttpHandler.match_key(
        match_list, "/path/1/path/2/path/3/")[0] == "value4"
    assert HttpHandler.match_key(
        match_list, "/path/1/path/2/path/3/")[1] == ("1", "2", "3")


def test_get_fixed_path():
    test_path = ["arg1"]
    assert HttpHandler.get_fixed_path(test_path) == "/arg1/"

    test_path = ["path", "arg1", "path", "arg2"]
    assert HttpHandler.get_fixed_path(
        test_path) == "/path/arg1/path/arg2/"


def test_http_handler():

    app = HttpHandler(getLogger("test"))

    @app.post("/path/")
    def test_handler():
        return "test"

    assert app.handlers["POST"]["/path/"]["handler"] == test_handler
    assert app.handlers["POST"]["/path/"]["path"] == "/path/"
    assert app.handlers["POST"]["/path/"]["fixed_args"] == []

    @app.delete("/path/{arg1}/")
    def test_handler():
        return "test"

    assert app.handlers["DELETE"]["/path/arg1/"]["handler"] == test_handler
    assert app.handlers["DELETE"]["/path/arg1/"]["path"] == "/path/arg1/"
    assert app.handlers["DELETE"]["/path/arg1/"]["fixed_args"] == ["arg1"]

    @app.get("/path/{arg1}/path/{arg2}/")
    def test_handler():
        return "test"

    assert app.handlers["GET"]["/path/arg1/path/arg2/"]["handler"] == test_handler
    assert app.handlers["GET"]["/path/arg1/path/arg2/"]["path"] == "/path/arg1/path/arg2/"
    assert app.handlers["GET"]["/path/arg1/path/arg2/"]["fixed_args"] == ["arg1", "arg2"]


def test_http_process():
    app = HttpHandler(getLogger("test"))

    @app.get("/path/")
    def test_handler():
        return "test"

    assert app.process({
        "httpMethod": "GET",
        "path": "/path/",
        "headers": {},
        "body": "",
    }, {}) == {"body": "test", "statusCode": 200, "headers": {
        "Content-Type": "text/plain"
    }}

    @app.delete("/path/{arg1}/")
    def test_handler(arg1: str):
        return arg1

    assert app.process({
        "httpMethod": "DELETE",
        "path": "/path/arg1/",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": "arg1", "statusCode": 200, "headers": {
            "Content-Type": "text/plain"
        }
    }

    @app.get("/path/{arg1}/path/{arg2}/")
    def test_handler(arg1: str, arg2: str):
        return arg1 + arg2

    assert app.process({
        "httpMethod": "GET",
        "path": "/path/arg1/path/arg2/",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": "arg1arg2", "statusCode": 200, "headers": {
            "Content-Type": "text/plain"
        }
    }

    assert app.process({
        "httpMethod": "GET",
        "path": "/path/arg2/path/arg2/",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": "arg2arg2", "statusCode": 200, "headers": {
            "Content-Type": "text/plain"
        }
    }

    assert app.process({
        "httpMethod": "GET",
        "path": "/path/arg1/path//",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": dumps({
            "message": "Not Found"

        }), "statusCode": 404, "headers": {
            "Content-Type": "application/json"
        }
    }

    @app.post("/path/")
    def handler_post(body: dict):
        return body

    assert app.process({
        "httpMethod": "POST",
        "path": "/path/",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "{}",
    }, {}) == {
        "body": "{}", "statusCode": 200, "headers": {
            "Content-Type": "application/json"
        }
    }

    @app.post("/path/{arg1}/")
    def handler_post(arg1: str, body: dict):
        print(arg1)
        return body

    assert app.process({
        "httpMethod": "POST",
        "path": "/path/a/",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "{}",
    }, {}) == {
        "body": "{}", "statusCode": 200, "headers": {
            "Content-Type": "application/json"
        }
    }


def test_http_process_headers():
    app = HttpHandler(getLogger("test"))

    @app.post("/test_correlation/")
    def handler_post(headers: HttpHeaders):
        if headers.get("correlation_id"):
            return headers.get("correlation_id")
        else:
            return "No correlation id"

    assert app.process({
        "httpMethod": "POST",
        "path": "/test_correlation/",
        "headers": {
            "correlation_id": "test"
        },
        "body": "",
    }, {}) == {
        "body": "test", "statusCode": 200, "headers": {
            "Content-Type": "text/plain"
        }
    }

    assert app.process({
        "httpMethod": "POST",
        "path": "/test_correlation/",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": "No correlation id", "statusCode": 200, "headers": {
            "Content-Type": "text/plain"
        }
    }


def test_http_process_body():
    app = HttpHandler(getLogger("test"))

    @app.post("/test_body/")
    def handler_post(body: dict):
        return body

    assert app.process({
        "httpMethod": "POST",
        "path": "/test_body/",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "{}",
    }, {}) == {
        "body": "{}", "statusCode": 200, "headers": {
            "Content-Type": "application/json"
        }
    }


def test_http_process_error():
    app = HttpHandler(getLogger("test"))

    @app.post("/test_error/")
    def handler_post():
        raise Exception("test error")

    assert app.process({
        "httpMethod": "POST",
        "path": "/test_error/",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": dumps({
            "message": "Internal Server Error"
        }), "statusCode": 500, "headers": {
            "Content-Type": "application/json"
        }
    }


def test_http_handler_merge():
    app1 = HttpHandler(getLogger("test"))
    app2 = HttpHandler(getLogger("test"))

    @app1.post("/test/")
    def handler_post():
        return "test"

    @app2.get("/test/")
    def handler_get():
        return "test"

    app1.merge(app2)


def test_http_handler_default():
    app = HttpHandler(getLogger("test"))

    @app.default()
    def default_handler():
        return "default"

    assert app.handlers["POST"]["/default/"]["handler"] == default_handler
    assert app.handlers["POST"]["/default/"]["path"] == "/default/"
    assert app.handlers["POST"]["/default/"]["fixed_args"] == []

    assert app.process({
        "httpMethod": "POST",
        "path": "/default/",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": "default", "statusCode": 200, "headers": {
            "Content-Type": "text/plain"
        }
    }


def test_http_handler_default_error():
    app = HttpHandler(getLogger("test"))

    @app.default()
    def default_handler():
        raise Exception("test error")

    assert app.handlers["POST"]["/default/"]["handler"] == default_handler
    assert app.handlers["POST"]["/default/"]["path"] == "/default/"
    assert app.handlers["POST"]["/default/"]["fixed_args"] == []

    assert app.process({
        "httpMethod": "POST",
        "path": "/default/",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": dumps({
            "message": "Internal Server Error"
        }), "statusCode": 500, "headers": {
            "Content-Type": "application/json"
        }
    }


def test_http_handler_not_found_error():
    app = HttpHandler(getLogger("test"))

    assert app.process({
        "httpMethod": "POST",
        "path": "/adfsadpoaskdosak/",
        "headers": {},
        "body": "",
    }, {}) == {
        "body": dumps({
            "message": "Not Found"
        }), "statusCode": 404, "headers": {
            "Content-Type": "application/json"
        }
    }


def test_http_put_test():

    app = HttpHandler(getLogger("test"))

    @app.put("/path/")
    def test_handler():
        return "test"

    assert app.handlers["PUT"]["/path/"]["handler"] == test_handler
    assert app.handlers["PUT"]["/path/"]["path"] == "/path/"
    assert app.handlers["PUT"]["/path/"]["fixed_args"] == []


def test_http_delete_test():

    app = HttpHandler(getLogger("test"))

    @app.delete("/path/")
    def test_handler():
        return "test"

    assert app.handlers["DELETE"]["/path/"]["handler"] == test_handler
    assert app.handlers["DELETE"]["/path/"]["path"] == "/path/"
    assert app.handlers["DELETE"]["/path/"]["fixed_args"] == []


def test_http_patch_test():

    app = HttpHandler(getLogger("test"))

    @app.patch("/path/")
    def test_handler():
        return "test"

    assert app.handlers["PATCH"]["/path/"]["handler"] == test_handler
    assert app.handlers["PATCH"]["/path/"]["path"] == "/path/"
    assert app.handlers["PATCH"]["/path/"]["fixed_args"] == []


def test_http_options_test():

    app = HttpHandler(getLogger("test"))

    @app.options("/path/")
    def test_handler():
        return "test"

    assert app.handlers["OPTIONS"]["/path/"]["handler"] == test_handler
    assert app.handlers["OPTIONS"]["/path/"]["path"] == "/path/"
    assert app.handlers["OPTIONS"]["/path/"]["fixed_args"] == []


def test_http_options_with_post_test():

    app = HttpHandler(getLogger("test"))

    @app.post("/path/")
    def test_handler():
        return "test"

    assert app.handlers["POST"]["/path/"]["handler"] == test_handler
    assert app.handlers["POST"]["/path/"]["path"] == "/path/"
    assert app.handlers["POST"]["/path/"]["fixed_args"] == []

    assert app.handlers["OPTIONS"]["/path/"]["handler"] == test_handler
    assert app.handlers["OPTIONS"]["/path/"]["path"] == "/path/"

    assert app.handlers["OPTIONS"]["/path/"]["fixed_args"] == []


def test_http_headers_in_handler():

    app = HttpHandler(getLogger("test"))

    @app.post("/path/", headers={"test": "test"})
    def test_handler():
        return "test"

    assert app.handlers["POST"]["/path/"]["handler"] == test_handler
    assert app.handlers["POST"]["/path/"]["path"] == "/path/"
    assert app.handlers["POST"]["/path/"]["fixed_args"] == []
    assert app.handlers["POST"]["/path/"]["headers"] == {"test": "test"}

    assert app.process({
        "httpMethod": "POST",
        "path": "/path/",
        "headers": {
            "test": "test"
        },
        "body": "",
    }, {}) == {
        "body": "test", "statusCode": 200, "headers": {
            "Content-Type": "text/plain",
            "test": "test"
        }
    }

    assert app.process({
        "httpMethod": "OPTIONS",
        "path": "/path/",
        "headers": {
            "test": "test"
        },
        "body": "",
    }, {}) == {
        "body": "test", "statusCode": 200, "headers": {
            "Content-Type": "text/plain",
            "test": "test"
        }
    }


def test_body_as_a_model():
    app = HttpHandler(getLogger("test"))

    class TestModel(BaseModel):
        test: str

    @app.post("/path/")
    def test_handler(body: TestModel):
        return body.test

    assert app.handlers["POST"]["/path/"]["handler"] == test_handler

    assert app.process({
        "httpMethod": "POST",
        "path": "/path/",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": dumps({"test": "a"}),
    }, {}) == {
        "body": "a", "statusCode": 200, "headers": {
            "Content-Type": "text/plain"
        }
    }


def test_malformed_body():

    app = HttpHandler(getLogger("test"))

    class TestModel(BaseModel):
        test: str

    @app.post("/path/")
    def test_handler(body: TestModel):
        return body.test

    assert app.handlers["POST"]["/path/"]["handler"] == test_handler

    assert app.process({
        "httpMethod": "POST",
        "path": "/path/",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": dumps({"a": "a"}),
    }, {}) == {
        "body": '{"message": "Bad request"}', "statusCode": 400, "headers": {
            "Content-Type": "application/json"
        }
    }
