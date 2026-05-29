from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import shutil
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
MATERIAL_DIR = os.path.join(UPLOAD_DIR, "materials")
THUMBNAIL_DIR = os.path.join(UPLOAD_DIR, "thumbnails")
os.makedirs(MATERIAL_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

# 静态文件服务
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 获取文件类型
def get_file_type(filename):
    ext = filename.lower().split('.')[-1]
    if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        return 'image'
    elif ext in ['mp4', 'webm', 'mov', 'avi', 'mkv']:
        return 'video'
    elif ext in ['obj', 'glb', 'gltf', 'fbx']:
        return 'model'
    elif ext in ['js', 'ts', 'html', 'css', 'json']:
        return 'code'
    return 'other'

# 获取文件图标
def get_file_icon(file_type):
    icons = {
        'image': '🖼️',
        'video': '🎬',
        'model': '🏗️',
        'code': '📄',
        'other': '📁'
    }
    return icons.get(file_type, '📁')

# 1. 保存项目
@app.post("/save-project")
def save_project(name: str = Form(...), code: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projects (name, code) VALUES (%s, %s)",
        (name, code)
    )
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"code": 200, "msg": "保存成功", "project_id": project_id}

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
    cursor.execute("SELECT * FROM projects ORDER BY create_time DESC")
    data = cursor.fetchall()
    conn.close()
    return {"code": 200, "data": data}

# ========== 素材管理接口 ==========

# 4. 上传新素材
@app.post("/materials/upload")
async def upload_material(
    project_id: int = Form(...),
    file: UploadFile = File(...),
    name: str = Form(None),
    sort_order: int = Form(0)
):
    try:
        print(f"[DEBUG] upload_material called with project_id={project_id}, file={file.filename}")
        
        # 保存文件
        filename = file.filename
        if not name:
            name = os.path.splitext(filename)[0]
        
        file_type = get_file_type(filename)
        file_size = 0
        
        # 生成唯一文件名
        import uuid
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(MATERIAL_DIR, unique_name)
        
        print(f"[DEBUG] Saving file to: {file_path}")
        
        with open(file_path, "wb") as f:
            content = await file.read()
            file_size = len(content)
            f.write(content)
        
        print(f"[DEBUG] File saved, size: {file_size} bytes")
        
        # 保存到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO materials (project_id, name, type, file_path, thumbnail, size, sort_order)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (project_id, name, file_type, file_path, "", file_size, sort_order)
        )
        material_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"[DEBUG] Material saved to DB with id: {material_id}")
        
        return {
            "code": 200, 
            "msg": "上传成功",
            "data": {
                "id": material_id,
                "name": name,
                "type": file_type,
                "typeLabel": file_type,
                "icon": get_file_icon(file_type),
                "size": f"{file_size/1024:.1f}KB" if file_size < 1024*1024 else f"{file_size/1024/1024:.1f}MB",
                "date": "刚刚",
                "sort_order": sort_order
            }
        }
    except Exception as e:
        print(f"[ERROR] upload_material failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 5. 替换素材
@app.post("/materials/{material_id}/replace")
async def replace_material(
    material_id: int,
    file: UploadFile = File(...),
    name: str = Form(None)
):
    try:
        # 获取原素材信息
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materials WHERE id = %s", (material_id,))
        original = cursor.fetchone()
        
        if not original:
            conn.close()
            raise HTTPException(status_code=404, detail="素材不存在")
        
        # 删除原文件
        if original['file_path'] and os.path.exists(original['file_path']):
            os.remove(original['file_path'])
        
        # 保存新文件
        filename = file.filename
        if not name:
            name = os.path.splitext(filename)[0]
        
        file_type = get_file_type(filename)
        file_size = 0
        
        # 生成唯一文件名
        import uuid
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(MATERIAL_DIR, unique_name)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            file_size = len(content)
            f.write(content)
        
        # 更新数据库
        cursor.execute(
            """UPDATE materials SET name = %s, type = %s, file_path = %s, size = %s
               WHERE id = %s""",
            (name, file_type, file_path, file_size, material_id)
        )
        conn.commit()
        conn.close()
        
        return {
            "code": 200, 
            "msg": "替换成功",
            "data": {
                "id": material_id,
                "name": name,
                "type": file_type,
                "typeLabel": file_type,
                "icon": get_file_icon(file_type),
                "size": f"{file_size/1024:.1f}KB" if file_size < 1024*1024 else f"{file_size/1024/1024:.1f}MB"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. 删除素材
@app.delete("/materials/{material_id}")
def delete_material(material_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取素材信息
        cursor.execute("SELECT * FROM materials WHERE id = %s", (material_id,))
        material = cursor.fetchone()
        
        if not material:
            conn.close()
            raise HTTPException(status_code=404, detail="素材不存在")
        
        # 删除文件
        if material['file_path'] and os.path.exists(material['file_path']):
            os.remove(material['file_path'])
        
        # 删除数据库记录
        cursor.execute("DELETE FROM materials WHERE id = %s", (material_id,))
        conn.commit()
        conn.close()
        
        return {"code": 200, "msg": "删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 7. 获取项目的素材列表
@app.get("/projects/{project_id}/materials")
def get_project_materials(project_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, type, file_path, size, sort_order, create_time
            FROM materials 
            WHERE project_id = %s 
            ORDER BY sort_order ASC, create_time DESC
        """, (project_id,))
        materials = cursor.fetchall()
        conn.close()
        
        result = []
        for m in materials:
            result.append({
                "id": m['id'],
                "name": m['name'],
                "type": m['type'],
                "typeLabel": m['type'],
                "icon": get_file_icon(m['type']),
                "size": f"{m['size']/1024:.1f}KB" if m['size'] < 1024*1024 else f"{m['size']/1024/1024:.1f}MB",
                "date": m['create_time'].strftime("%Y-%m-%d"),
                "sort_order": m['sort_order']
            })
        
        return {"code": 200, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 8. 批量上传素材
@app.post("/materials/batch-upload")
async def batch_upload_materials(
    project_id: int = Form(...),
    files: list[UploadFile] = File(...)
):
    try:
        results = []
        for file in files:
            filename = file.filename
            name = os.path.splitext(filename)[0]
            file_type = get_file_type(filename)
            
            import uuid
            unique_name = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(MATERIAL_DIR, unique_name)
            
            with open(file_path, "wb") as f:
                content = await file.read()
                file_size = len(content)
                f.write(content)
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO materials (project_id, name, type, file_path, thumbnail, size)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (project_id, name, file_type, file_path, "", len(content))
            )
            material_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            results.append({
                "id": material_id,
                "name": name,
                "type": file_type,
                "typeLabel": file_type,
                "icon": get_file_icon(file_type),
                "size": f"{file_size/1024:.1f}KB" if file_size < 1024*1024 else f"{file_size/1024/1024:.1f}MB"
            })
        
        return {"code": 200, "msg": f"成功上传 {len(results)} 个素材", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)