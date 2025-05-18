from fastapi import FastAPI

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
