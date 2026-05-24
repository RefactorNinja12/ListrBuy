from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers.auth import router as auth_router
from app.routers.shoppinglist import router as shoppinglist_router
from app.routers.item import router as item_router




app = FastAPI()
app.include_router(auth_router)
app.include_router(shoppinglist_router)
app.include_router(item_router)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title="API", version="1.0.0", routes=app.routes)
    schema["components"]["securitySchemes"] = {
        "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in schema["paths"].values():
        for op in path.values():
            op["security"] = [{"bearerAuth": []}]
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
