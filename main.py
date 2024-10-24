from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import timedelta
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
import security
from models import User, SessionLocal, init_db

app = FastAPI()
templates = Jinja2Templates(directory="./templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
init_db()
print('server started')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str




@app.post("/signup")
async def signup(username: str = Form(...), email: str = Form(...), password: str = Form(...),
                 db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="there is already such a penis")

    hashed_password = security.hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse("/success", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/success")
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    response = RedirectResponse(url=f"/profile?username={user.username}", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token)
    return response


@app.get("/")
async def main():
    return FileResponse("templates/index.html")


@app.get("/login")
async def login():
    return FileResponse("templates/login.html")


@app.get("/profile")
async def profile(request: Request, username: str, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return templates.TemplateResponse("profile.html",
                                      {"request": request, "username": user.username, "email": user.email})

# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
#     if exc.status_code == 404:
#         return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
#     return await request.app.default_exception_handler(request, exc)