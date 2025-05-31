from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from alg import cash_withdrawal
from database import init_db, get_banknotes, reset_banknotes
import uvicorn
from itertools import groupby

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация базы данных
init_db()

# Фильтр для группировки купюр
templates.env.filters["groupby"] = lambda x: [(k, list(g)) for k, g in groupby(sorted(x))]

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    banknotes = get_banknotes()
    return templates.TemplateResponse("coin_change_form.html", {"request": request, "banknotes": banknotes})

@app.post("/withdraw")
async def withdraw_cash(request: Request, amount: int = Form(...)):
    try:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительным числом.")
        result = cash_withdrawal(amount)
        if isinstance(result, str):
            return templates.TemplateResponse("coin_change_result.html", {
                "request": request,
                "result": result,
            })
        else:
            return templates.TemplateResponse("coin_change_result.html", {
                "request": request,
                "result": result,
            })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.get("/reset")
async def reset_banknotes_route():
    reset_banknotes()
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)