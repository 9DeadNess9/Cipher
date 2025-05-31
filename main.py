from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from alg import encrypt_text, decrypt_text
from database import init_db, get_operation_history, save_encryption_operation, save_decryption_operation, clear_history
import uvicorn
from typing import List, Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация базы данных
init_db()

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    history = get_operation_history()
    return templates.TemplateResponse("rsa_form.html", {"request": request, "history": history})

@app.post("/encrypt")
async def encrypt_message(
    request: Request, 
    message: str = Form(...),
    n: str = Form(...),
    e: str = Form(...)
):
    try:
        # Преобразуем строки в числа
        n_int = int(n)
        e_int = int(e)
        
        # Создаем публичный ключ
        public_key = {"n": n_int, "e": e_int}
        
        # Шифруем сообщение
        encrypted = encrypt_text(message, public_key)
        
        # Сохраняем операцию в базе данных
        save_encryption_operation(message, str(encrypted), n, e)
        
        return templates.TemplateResponse("encryption_result.html", {
            "request": request,
            "original_message": message,
            "encrypted": encrypted,
            "public_key": public_key
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.post("/decrypt")
async def decrypt_message(
    request: Request,
    encrypted_data: str = Form(...),
    n: str = Form(...),
    d: str = Form(...)
):
    try:
        # Преобразуем строку с зашифрованными данными в список чисел
        try:
            encrypted = [int(x.strip()) for x in encrypted_data.replace('[', '').replace(']', '').split(',')]
        except:
            raise ValueError("Неверный формат зашифрованных данных. Должен быть список чисел, разделенных запятыми.")
        
        # Преобразуем строки в числа
        n_int = int(n)
        d_int = int(d)
        
        # Создаем приватный ключ
        private_key = {"n": n_int, "d": d_int}
        
        # Дешифруем сообщение
        decrypted = decrypt_text(encrypted, private_key)
        
        # Сохраняем операцию в базе данных
        save_decryption_operation(encrypted_data, decrypted, n, d)
        
        return templates.TemplateResponse("decryption_result.html", {
            "request": request,
            "encrypted": encrypted,
            "decrypted": decrypted,
            "private_key": private_key
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.post("/clear-history")
async def clear_history_route():
    try:
        clear_history()
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при очистке истории: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)