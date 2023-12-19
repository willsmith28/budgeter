import fastapi


def app_factory():
    app = fastapi.FastAPI()
    return app


app = app_factory()


@app.get("/")
def hello_world():
    return "hello world"
