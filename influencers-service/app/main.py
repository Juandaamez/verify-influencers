from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.v1 import auth, claims, influencers
from app.api.v1.search import router as search_router

app = FastAPI(
    title="Verify Influencers API",
    version="1.0.0",
    description="API for verifying health-related claims from influencers.",
    docs_url="/docs",
)

origins = [
    "http://localhost:4200",
    "https://whimsical-cannoli-98452e.netlify.app",
    "https://fastapi-backend-vqtd.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(claims.router, prefix="/api/v1/claims", tags=["Claims"])
app.include_router(influencers.router, prefix="/api/v1/influencers", tags=["Influencers"])
app.include_router(search_router, prefix="/api/v1/search", tags=["Search"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Verify Influencers API",
        version="1.0.0",
        description="API for verifying health-related claims from influencers.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/api/v1/auth/login",
                    "scopes": {},
                }
            },
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
