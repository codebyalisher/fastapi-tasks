# Disable Browsable API in Production:In FastAPI, the default interactive API documentation (Swagger UI) can be disabled in production by disabling the docs_url parameter.
from fastapi import FastAPI
from routes.__init__ import item_router,jwt_login_logout_router
from routes.item_routes import ItemView
item_view = ItemView()
app=FastAPI()

def all_routes():    
    # Include the authentication routes    
    app.include_router(item_router, prefix="/items", tags=["items"])
    app.include_router(jwt_login_logout_router, prefix="/users", tags=["users"])      
    app.include_router(item_view.router,prefix="/items",tags=["items"])
# Disable Browsable API in Production:In FastAPI, the default interactive API documentation (Swagger UI) can be disabled in production by disabling the docs_url parameter.
#app = FastAPI(docs_url=None, redoc_url=None)


all_routes()