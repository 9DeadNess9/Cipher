from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from alg import generate_key_pair, encrypt_text, decrypt_text, text_to_numbers, numbers_to_text
from database import init_db, get_all_keys, get_last_key_pair, delete_key
import uvicorn
from typing import List, Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация базы данных
init_db()

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    keys = get_all_keys()
    return templates.TemplateResponse("rsa_form.html", {"request": request, "keys": keys})

@app.post("/generate-keys")
async def generate_keys(request: Request, bit_size: int = Form(512)):
    try:
        if bit_size < 256:
            raise ValueError("Размер ключа должен быть не менее 256 бит для безопасности")
        if bit_size > 2048:
            raise ValueError("Размер ключа не должен превышать 2048 бит из-за ограничений производительности")
        
        key_pair = generate_key_pair(bit_size)
        
        return templates.TemplateResponse("key_generation_result.html", {
            "request": request,
            "public_key": key_pair["public_key"],
            "private_key": key_pair["private_key"],
            "bit_size": bit_size
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.post("/encrypt")
async def encrypt_message(
    request: Request, 
    message: str = Form(...), 
    use_stored_key: Optional[bool] = Form(False),
    n: Optional[str] = Form(None),
    e: Optional[str] = Form(None)
):
    try:
        if use_stored_key:
            # Используем последний сохраненный ключ из базы данных
            key_pair = get_last_key_pair()
            if key_pair is None:
                raise ValueError("В базе данных нет сохраненных ключей. Сначала сгенерируйте ключи.")
            public_key = key_pair["public_key"]
        else:
            if not n or not e:
                raise ValueError("Для шифрования необходимы параметры n и e публичного ключа")
            
            # Используем предоставленный ключ
            public_key = {"n": int(n), "e": int(e)}
        
        encrypted = encrypt_text(message, public_key)
        
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
    use_stored_key: Optional[bool] = Form(False),
    n: Optional[str] = Form(None),
    d: Optional[str] = Form(None)
):
    try:
        # Преобразуем строку с зашифрованными данными в список чисел
        try:
            encrypted = [int(x.strip()) for x in encrypted_data.replace('[', '').replace(']', '').split(',')]
        except:
            raise ValueError("Неверный формат зашифрованных данных. Должен быть список чисел, разделенных запятыми.")
        
        if use_stored_key:
            # Используем последний сохраненный ключ из базы данных
            key_pair = get_last_key_pair()
            if key_pair is None:
                raise ValueError("В базе данных нет сохраненных ключей. Сначала сгенерируйте ключи.")
            private_key = key_pair["private_key"]
        else:
            if not n or not d:
                raise ValueError("Для дешифрования необходимы параметры n и d закрытого ключа")
            
            # Используем предоставленный ключ
            private_key = {"n": int(n), "d": int(d)}
        
        decrypted = decrypt_text(encrypted, private_key)
        
        return templates.TemplateResponse("decryption_result.html", {
            "request": request,
            "encrypted": encrypted,
            "decrypted": decrypted,
            "private_key": private_key
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

@app.post("/delete-key/{key_id}")
async def delete_key_route(key_id: int):
    try:
        delete_key(key_id)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении ключа: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)