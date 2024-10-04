import json
from urllib.parse import parse_qs
from typing import Dict, Any, Callable, Union, List
from lecture_1.hw.maths import get_factorial, get_fibonacci, get_mean
from typing import Any, Awaitable, Callable


async def app(scope, receive, send) -> None:
    if scope["type"] == "http":
        path = scope["path"]
        method = scope["method"]
        query_string = scope["query_string"].decode()
        params = parse_qs(query_string)

        if path == "/factorial" and method == "GET":
            await handle_factorial(params, send)
        elif path.startswith("/fibonacci") and method == "GET":
            await handle_fibonacci(path, send)
        elif path == "/mean" and method == "GET":
            await handle_mean(receive, send)
        else:
            response_body = json.dumps(
                {"error": "Invalid path or parameters"}).encode("utf-8")
            await send_response(send, 404, response_body)
    elif scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return


async def handle_factorial(params: Dict[str, List[str]], send: Callable) -> None:
    n = params.get("n", 0)
    if not n:
        response_body = json.dumps({"error": "Invalid number"}).encode("utf-8")
        await send_response(send, 422, response_body)
        return

    try:
        number = int(n[0])
        if number < 0:
            response_body = json.dumps({"error": "number < 0"}).encode("utf-8")
            await send_response(send, 400, response_body)
            return

        result = get_factorial(number)
        response_body = json.dumps({"result": result}).encode("utf-8")
        await send_response(send, 200, response_body)

    except Exception:
        response_body = json.dumps({"error": "Invalid number"}).encode("utf-8")
        await send_response(send, 422, response_body)


async def handle_fibonacci(path: str, send: Callable) -> None:
    try:
        number = int(path.split("/")[-1])
        if number < 0:
            response_body = json.dumps({"error": "number < 0"}).encode("utf-8")
            await send_response(send, 400, response_body)
            return

        result = get_fibonacci(number)
        response_body = json.dumps({"result": result}).encode("utf-8")
        await send_response(send, 200, response_body)

    except Exception:
        response_body = json.dumps({"error": "Invalid number"}).encode("utf-8")
        await send_response(send, 422, response_body)


async def handle_mean(receive: Callable, send: Callable) -> None:
    body = await receive()
    if body.get("type") == "http.request":
        try:
            request_body: bytes = body.get("body", b"")
            numbers: Union[List[float], None] = json.loads(request_body.decode())

            if not isinstance(numbers, list) or not all(isinstance(x, (int, float)) for x in numbers):
                raise ValueError("Invalid input format")

            if not numbers:
                response_body: bytes = json.dumps({"error": "Array is empty"}).encode("utf-8")
                await send_response(send, 400, response_body)
            else:
                mean_value: float = get_mean(numbers)
                response_body: bytes = json.dumps({"result": mean_value}).encode("utf-8")
                await send_response(send, 200, response_body)
        except (ValueError, json.JSONDecodeError):
            response_body: bytes = json.dumps({"error": "Invalid input format"}).encode("utf-8")
            await send_response(send, 422, response_body)


async def send_response(send: Callable, status_code: int, response_body: bytes) -> None:
    await send(
        {
            "type": "http.response.start",
            "status": status_code,
            "headers": [(b"content-type", b"application/json")],
        }
    )
    await send({"type": "http.response.body", "body": response_body})