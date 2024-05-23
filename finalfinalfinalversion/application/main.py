
from fastapi import FastAPI, Request

from application.db_app import models
from application.db_app.database import engine
from application.routers import dish_routers, menu_routers, submenu_routers
from fastapi import FastAPI

from application.backgroundtasks.tasks import book_table, result_backend
from dramatiq.results.errors import ResultMissing
from fastapi import Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(menu_routers.router)
app.include_router(submenu_routers.router)
app.include_router(dish_routers.router)


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


@app.get("/book_table", tags=["dramatiq"])
def result_email(email_receiver: str = Query(..., title="Email Receiver", description="Enter the email address to send the booking confirmation")):
    try:
        task = book_table.send(email_receiver)  
        return result_backend.get_result(task)
    except ResultMissing:
        return "Waiting for all requests"
    except Exception as e:
        return f"An error occurred: {str(e)}"



