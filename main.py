from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from alg import encrypt_text, decrypt_text
from database import init_db
import uvicorn
from typing import List, Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация базы данных
init_db()

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("rsa_form.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def process_form(
    request: Request,
    action: str = Form(...),
    message: Optional[str] = Form(None),
    encrypted_data: Optional[str] = Form(None),
    n: str = Form(...),
    e: Optional[str] = Form(None),
    d: Optional[str] = Form(None)
):
    context = {"request": request}

    try:
        # Преобразуем строки в числа
        n_int = int(n)
        
        if action == "encrypt":
            if not message:
                raise ValueError("Сообщение для шифрования обязательно")
            if not e:
                raise ValueError("Открытая экспонента (e) обязательна")
            
            e_int = int(e)
            
            # Создаем публичный ключ
            public_key = {"n": n_int, "e": e_int}
            
            # Шифруем сообщение
            encrypted = encrypt_text(message, public_key)
            
            # Добавляем результат и исходные данные в контекст
            context.update({
                "encrypt_result": encrypted,
                "encrypt_input": message,
                "encrypt_n": n,
                "encrypt_e": e
            })
            
        elif action == "decrypt":
            if not encrypted_data:
                raise ValueError("Зашифрованные данные обязательны")
            if not d:
                raise ValueError("Закрытая экспонента (d) обязательна")
            
            # Преобразуем строку с зашифрованными данными в список чисел
            try:
                encrypted = [int(x.strip()) for x in encrypted_data.replace('[', '').replace(']', '').split(',')]
            except:
                raise ValueError("Неверный формат зашифрованных данных. Должен быть список чисел, разделенных запятыми.")
            
            d_int = int(d)
            
            # Создаем приватный ключ
            private_key = {"n": n_int, "d": d_int}
            
            # Дешифруем сообщение
            decrypted = decrypt_text(encrypted, private_key)
            
            # Добавляем результат и исходные данные в контекст
            context.update({
                "decrypt_result": decrypted,
                "decrypt_input": encrypted_data,
                "decrypt_n": n,
                "decrypt_d": d
            })
        
        else:
            raise ValueError("Неизвестное действие")
            
        return templates.TemplateResponse("rsa_form.html", context)
        
    except Exception as e:
        context["error"] = str(e)
        return templates.TemplateResponse("rsa_form.html", context)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)