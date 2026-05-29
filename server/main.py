from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from db import init_db, get_db_connection

app = FastAPI(title="3D编程平台后端")

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
init_db()

# 文件存储目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 1. 保存项目
@app.post("/save-project")
def save_project(name: str = Form(...), code: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projects (name, code) VALUES (%s, %s)",
        (name, code)
    )
    conn.commit()
    return {"code": 200, "msg": "保存成功"}

# 2. 上传文件
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    return {"code": 200, "path": path}

# 3. 获取项目列表
@app.get("/projects")
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    data = cursor.fetchall()
    return {"code": 200, "data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)