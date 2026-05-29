# 3D编程平台 Agent 开发约束文档

## 文档信息

- **项目名称**：3D编程平台 (3d-code-platform)
- **技术栈**：Vue 3 + Vite + JavaScript + Sass + FastAPI + MySQL
- **文档版本**：v1.0.0
- **最后更新**：2026-05-29

---

## 1. 项目架构规范

### 1.1 技术栈概览

```
┌─────────────────────────────────────────────────────────────┐
│                        前端 (Client)                         │
│  Vue 3 + Vite + JavaScript + Sass + Element Plus          │
│  - 3D渲染: @tresjs/core, @tresjs/cientos                   │
│  - 代码编辑: monaco-editor                                  │
│  - 手势识别: @mediapipe/hands, @mediapipe/camera_utils      │
│  - 文件导出: html2canvas, jspdf                             │
│  - UI组件: element-plus                                     │
│  - HTTP请求: axios                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        后端 (Server)                         │
│  Python 3.14 + FastAPI + MySQL                             │
│  - 框架: FastAPI 0.136.3                                   │
│  - 数据库: MySQL (pymysql)                                  │
│  - 跨域: CORSMiddleware                                    │
│  - 服务器: uvicorn                                          │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 目录结构规范

```
3d-code-platform/
├── client/                    # 前端项目 (Vue 3 + Vite)
│   ├── src/
│   │   ├── assets/           # 静态资源
│   │   ├── components/       # 公共组件
│   │   ├── composables/      # 组合式函数
│   │   ├── layouts/          # 布局组件
│   │   ├── router/           # 路由配置
│   │   ├── stores/           # 状态管理
│   │   ├── styles/           # 全局样式
│   │   ├── utils/            # 工具函数
│   │   ├── views/            # 页面组件
│   │   ├── App.vue           # 根组件
│   │   ├── main.js           # 入口文件
│   │   └── style.scss        # 全局样式文件
│   ├── public/               # 公共静态资源
│   ├── vite.config.js        # Vite 配置
│   └── package.json          # 前端依赖
│
├── server/                    # 后端项目 (Python FastAPI)
│   ├── routers/              # 路由模块
│   ├── models/               # 数据模型
│   ├── schemas/              # Pydantic 模型
│   ├── services/            # 业务逻辑层
│   ├── utils/                # 工具函数
│   ├── config.py             # 配置文件
│   ├── db.py                 # 数据库连接
│   └── main.py               # 应用入口
│
├── docs/                     # 项目文档
└── README.md                 # 项目说明
```

---

## 2. 前端开发约束

### 2.1 Vue 3 开发规范

#### 2.1.1 组件规范

```vue
<!-- ✅ 正确的组件模板结构 -->
<template>
  <div class="component-name">
    <!-- 组件内容 -->
  </div>
</template>

<script setup>
// 引入
import { ref, computed, onMounted } from 'vue'

// Props 定义
const props = defineProps({
  title: {
    type: String,
    default: '默认标题'
  },
  data: {
    type: Array,
    default: () => []
  },
  onChange: {
    type: Function,
    default: null
  }
})

// Emits
const emit = defineEmits(['update', 'delete'])

// Composables 使用
const { loading, fetchData } = useDataLoader()

// 响应式数据
const state = ref('')

// 计算属性
const computedValue = computed(() => {
  return props.data.filter(item => item.active)
})

// 方法
function handleClick() {
  emit('update', state.value)
}

// 生命周期
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.component-name {
  // 样式
}
</style>
```

#### 2.1.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserProfile.vue`, `DatePicker.vue` |
| 组件名 | PascalCase | `UserProfile`, `DatePicker` |
| 组合式函数 | camelCase, use前缀 | `useUserData`, `useFormValidation` |
| 道具 | camelCase | `userName`, `isActive` |
| 事件 | kebab-case | `update:value`, `delete-item` |
| CSS类 | kebab-case | `.user-profile`, `.date-picker` |
| 常量 | UPPER_SNAKE_CASE | `MAX_COUNT`, `API_BASE_URL` |

#### 2.1.3 Script Setup 规范

```javascript
// ✅ 使用 defineProps 和 defineEmits
const props = defineProps({
  modelValue: String,
  options: Array
})

const emit = defineEmits(['update:modelValue', 'submit'])

// ✅ 使用 withDefaults 设置默认值（通过 defineProps 的 default）
defineProps({
  count: {
    type: Number,
    default: 0
  },
  label: {
    type: String,
    default: ''
  }
})

// ✅ 使用 defineExpose 暴露方法
defineExpose({
  focus: () => inputRef.value?.focus(),
  reset: () => {
    state.value = ''
  }
})
```

### 2.2 样式规范 (SCSS)

#### 2.2.1 SCSS 变量定义

```scss
// ✅ 颜色变量
$colors: (
  primary: #007bff,
  secondary: #6c757d,
  success: #28a745,
  danger: #dc3545,
  warning: #ffc107,
  info: #17a2b8
);

// ✅ 使用 map-get 获取颜色
.button--primary {
  color: map-get($colors, primary);
}

// ✅ 响应式断点
$breakpoints: (
  xs: 576px,
  sm: 768px,
  md: 992px,
  lg: 1200px
);

// ✅ 混合器
@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

// ✅ 媒体查询混入
@mixin respond-to($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (min-width: map-get($breakpoints, $breakpoint)) {
      @content;
    }
  }
}
```

#### 2.2.2 样式顺序

```scss
.component {
  // 1. 定位
  position: absolute;
  top: 0;
  left: 0;

  // 2. 盒模型
  display: flex;
  width: 100%;
  height: 100%;
  padding: 16px;
  margin: 0 auto;

  // 3. 排版
  font-size: 16px;
  font-weight: 500;
  line-height: 1.5;
  color: #333;
  text-align: center;

  // 4. 视觉
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  // 5. 过渡
  transition: all 0.3s ease;

  // 6. 其他
  overflow: hidden;
  z-index: 1;
}
```

### 2.3 Vite 配置规范

#### 2.3.1 依赖预构建

```javascript
// ✅ vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  optimizeDeps: {
    // ⚠️ 必须包含以下依赖以避免 ESM 导入错误
    include: [
      'monaco-editor',
      '@mediapipe/hands',
      '@mediapipe/camera_utils',
      'element-plus'
    ]
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/styles/variables.scss" as *;`
      }
    }
  }
})
```

#### 2.3.2 常见问题处理

| 问题 | 解决方案 |
|------|----------|
| `does not provide export named 'default'` | 将包加入 `optimizeDeps.include` |
| CommonJS 模块导入错误 | 使用动态 `import()` |
| 缓存导致构建异常 | 删除 `node_modules/.vite` 目录 |
| Sass `@import` 废弃警告 | 使用 `@use` 和 `@forward` 替代 |

### 2.4 API 请求规范

#### 2.4.1 Axios 封装

```javascript
// ✅ 请求封装
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    if (response.data.code !== 200) {
      return Promise.reject(new Error(response.data.message))
    }
    return response.data
  },
  (error) => {
    console.error(error.message || '网络请求失败')
    return Promise.reject(error)
  }
)

export default apiClient
```

#### 2.4.2 API 调用示例

```javascript
// ✅ 在 composable 中使用
import { ref } from 'vue'
import apiClient from '@/utils/api'

export function useProjects() {
  const projects = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchProjects() {
    loading.value = true
    error.value = null
    try {
      const response = await apiClient.get('/projects')
      projects.value = response.data.data
    } catch (e) {
      error.value = e.message || '获取项目列表失败'
    } finally {
      loading.value = false
    }
  }

  async function saveProject(name, code) {
    await apiClient.post('/save-project', {
      name,
      code
    })
  }

  return {
    projects,
    loading,
    error,
    fetchProjects,
    saveProject
  }
}
```

---

## 3. 后端开发约束

### 3.1 FastAPI 开发规范

#### 3.1.1 项目结构

```python
# ✅ 正确的 FastAPI 项目结构
# server/
# ├── routers/
# │   ├── __init__.py
# │   ├── projects.py      # 项目相关路由
# │   ├── files.py         # 文件操作路由
# │   └── users.py         # 用户相关路由
# ├── models/
# │   ├── __init__.py
# │   ├── project.py
# │   └── user.py
# ├── schemas/
# │   ├── __init__.py
# │   ├── project.py       # Pydantic 模型
# │   └── user.py
# ├── services/
# │   ├── __init__.py
# │   ├── project_service.py
# │   └── file_service.py
# ├── utils/
# │   ├── __init__.py
# │   ├── db.py
# │   └── config.py
# ├── config.py
# ├── db.py
# └── main.py
```

#### 3.1.2 路由定义

```python
# ✅ 正确的路由定义
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional
from schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["项目管理"])


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user)
):
    """获取项目列表"""
    projects = await project_service.get_projects(
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return projects


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user)
):
    """创建新项目"""
    return await project_service.create_project(
        user_id=current_user.id,
        project=project
    )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user)
):
    """获取单个项目"""
    project = await project_service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user)
):
    """更新项目"""
    return await project_service.update_project(
        project_id=project_id,
        user_id=current_user.id,
        project_update=project_update
    )


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user)
):
    """删除项目"""
    await project_service.delete_project(project_id, current_user.id)
    return None
```

#### 3.1.3 请求体定义 (Pydantic)

```python
# ✅ 使用 Pydantic v2 定义模型
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ProjectType(str, Enum):
    THREE_JS = "threejs"
    WEBGL = "webgl"
    CUSTOM = "custom"


class ProjectBase(BaseModel):
    """项目基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="项目名称")
    description: Optional[str] = Field(None, max_length=500, description="项目描述")
    project_type: ProjectType = Field(default=ProjectType.CUSTOM, description="项目类型")


class ProjectCreate(ProjectBase):
    """创建项目请求"""
    code: str = Field(..., description="项目代码")


class ProjectUpdate(BaseModel):
    """更新项目请求"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    code: Optional[str] = None


class ProjectResponse(ProjectBase):
    """项目响应模型"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    code: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class ProjectListResponse(BaseModel):
    """项目列表响应"""
    total: int
    projects: List[ProjectResponse]
```

#### 3.1.4 错误处理

```python
# ✅ 统一错误响应
class APIException(Exception):
    def __init__(
        self,
        status_code: int = 500,
        message: str = "服务器内部错误",
        error_code: Optional[str] = None
    ):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code or f"ERR_{status_code}"


class NotFoundException(APIException):
    def __init__(self, resource: str = "资源"):
        super().__init__(
            status_code=404,
            message=f"{resource}不存在",
            error_code="RESOURCE_NOT_FOUND"
        )


class UnauthorizedException(APIException):
    def __init__(self, message: str = "未授权访问"):
        super().__init__(
            status_code=401,
            message=message,
            error_code="UNAUTHORIZED"
        )


class ValidationException(APIException):
    def __init__(self, message: str = "数据验证失败"):
        super().__init__(
            status_code=422,
            message=message,
            error_code="VALIDATION_ERROR"
        )
```

### 3.2 数据库规范

#### 3.2.1 连接管理

```python
# ✅ 正确的数据库连接管理
import pymysql
from contextlib import contextmanager
from typing import Generator, Optional
import os

# 配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', '3d_platform'),
    'charset': 'utf8mb4'
}


@contextmanager
def get_db_connection() -> Generator:
    """获取数据库连接的上下文管理器"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection
    finally:
        if connection:
            connection.close()


def get_db_cursor(connection):
    """获取数据库游标"""
    return connection.cursor(pymysql.cursors.DictCursor)
```

#### 3.2.2 SQL 查询规范

```python
# ✅ 使用参数化查询避免 SQL 注入
def get_project_by_id(project_id: int) -> Optional[dict]:
    with get_db_connection() as conn:
        cursor = get_db_cursor(conn)
        cursor.execute(
            "SELECT * FROM projects WHERE id = %s AND deleted_at IS NULL",
            (project_id,)
        )
        return cursor.fetchone()


def create_project(name: str, code: str, user_id: int) -> int:
    with get_db_connection() as conn:
        cursor = get_db_cursor(conn)
        cursor.execute(
            "INSERT INTO projects (name, code, user_id) VALUES (%s, %s, %s)",
            (name, code, user_id)
        )
        conn.commit()
        return cursor.lastrowid


# ⚠️ 禁止使用字符串拼接构建 SQL
# 错误示例:
# cursor.execute(f"SELECT * FROM projects WHERE id = {project_id}")  # 危险!


def search_projects(keyword: str, user_id: int) -> List[dict]:
    with get_db_connection() as conn:
        cursor = get_db_cursor(conn)
        cursor.execute(
            "SELECT * FROM projects WHERE user_id = %s AND name LIKE %s",
            (user_id, f"%{keyword}%")
        )
        return cursor.fetchall()
```

### 3.3 CORS 配置规范

```python
# ✅ 后端 CORS 配置 (main.py)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="3D编程平台后端")

# 生产环境应限制来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # 开发环境
        "http://localhost:3000",
        # "https://your-production-domain.com",  # 生产环境
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

---

## 4. 代码质量规范

### 4.1 Git 提交规范

#### 4.1.1 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### 4.1.2 Type 类型

| Type | 说明 |
|------|------|
| feat | 新功能 |
| fix | Bug 修复 |
| docs | 文档更新 |
| style | 代码格式（不影响功能） |
| refactor | 重构 |
| perf | 性能优化 |
| test | 测试相关 |
| chore | 构建/工具相关 |

#### 4.1.3 提交示例

```
feat(project): 添加项目导出功能

- 支持导出 Three.js 项目为独立 HTML 文件
- 支持导出 WebGL 项目为压缩包
- 导出时自动打包依赖资源

Closes #123
```

### 4.2 代码审查清单

#### 4.2.1 前端审查

- [ ] 组件 props 有正确定义和默认值
- [ ] 响应式数据正确使用 `ref` / `reactive`
- [ ] 计算属性正确使用 `computed`
- [ ] 生命周期钩子使用正确
- [ ] 样式使用 scoped，无全局污染
- [ ] SCSS 变量和混入已正确定义
- [ ] 媒体查询和响应式断点正确
- [ ] API 请求有错误处理和加载状态
- [ ] 无硬编码的 API 地址
- [ ] 敏感信息不存储在代码中

#### 4.2.2 后端审查

- [ ] 路由参数有完整的类型注解
- [ ] 请求体有 Pydantic 模型验证
- [ ] SQL 查询使用参数化，防止注入
- [ ] 错误处理返回合适的 HTTP 状态码
- [ ] 敏感信息不硬编码在代码中
- [ ] 数据库连接正确关闭
- [ ] CORS 配置限制来源
- [ ] 有必要的日志记录

---

## 5. 安全规范

### 5.1 前端安全

#### 5.1.1 敏感信息处理

```javascript
// ✅ 敏感信息存储在环境变量
// .env.development
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

// .env.production
VITE_API_BASE_URL=https://api.example.com
VITE_WS_URL=wss://api.example.com

// ⚠️ 禁止在代码中硬编码敏感信息
// 错误示例:
// const API_KEY = "sk-xxx-secret-key"  // 不安全!
```

#### 5.1.2 XSS 防护

```javascript
// ✅ 对用户输入进行转义
function escapeHtml(str) {
  const div = document.createElement('div')
  div.textContent = str
  return div.innerHTML
}

// ✅ 使用 v-html 时确保内容已转义
// <div v-html="sanitizedContent"></div>
```

### 5.2 后端安全

#### 5.2.1 认证授权

```python
# ✅ 使用 JWT 或 Session 进行认证
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """验证 JWT token 并获取当前用户"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据"
        )

    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    return user


@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    """受保护的路由"""
    return {"message": f"欢迎 {current_user.name}"}
```

#### 5.2.2 输入验证

```python
# ✅ 所有用户输入必须验证
from pydantic import BaseModel, Field, validator

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含大写字母')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含小写字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含数字')
        return v
```

---

## 6. 性能优化规范

### 6.1 前端性能

#### 6.1.1 组件加载

```javascript
// ✅ 使用异步组件（代码分割）
const HeavyComponent = defineAsyncComponent({
  loader: () => import('./HeavyComponent.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorBoundary,
  delay: 200,
  timeout: 3000
})

// ✅ 路由懒加载
const routes = [
  {
    path: '/editor/:id',
    component: () => import('./views/CodeEditor.vue')
  }
]
```

#### 6.1.2 依赖优化

```javascript
// ✅ 按需引入 Element Plus
import { ElButton, ElInput, ElSelect } from 'element-plus'

// ✅ 按需引入 Three.js 模块
import * as THREE from 'three/core/THREE.js'
import { OrbitControls } from 'three/controls/OrbitControls'
```

### 6.2 后端性能

#### 6.2.1 数据库优化

```python
# ✅ 使用索引优化查询
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);

# ✅ 分页查询
def get_projects_paginated(user_id: int, page: int = 1, page_size: int = 20):
    offset = (page - 1) * page_size
    with get_db_connection() as conn:
        cursor = get_db_cursor(conn)
        cursor.execute(
            """
            SELECT * FROM projects
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (user_id, page_size, offset)
        )
        return cursor.fetchall()
```

---

## 7. 测试规范

### 7.1 后端测试

#### 7.1.1 API 测试

```python
# ✅ 使用 pytest 进行 API 测试
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_project():
    response = client.post(
        "/save-project",
        data={
            "name": "Test Project",
            "code": "print('hello')"
        }
    )
    assert response.status_code == 200
    assert response.json()["code"] == 200


def test_get_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)
```

---

## 8. 开发流程规范

### 8.1 环境设置

#### 8.1.1 前端环境

```bash
# 安装依赖
cd client
npm install

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

#### 8.1.2 后端环境

```bash
cd server

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行开发服务器
python main.py
```

### 8.2 环境变量

#### 8.2.1 前端环境变量

```bash
# .env.development - 开发环境
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# .env.production - 生产环境
VITE_API_BASE_URL=https://api.example.com
VITE_WS_URL=wss://api.example.com
```

#### 8.2.2 后端环境变量

```bash
# .env - 环境变量文件
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=3d_platform

SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 9. 附录

### 9.1 常用命令

#### 前端

| 命令 | 说明 |
|------|------|
| `npm install` | 安装依赖 |
| `npm run dev` | 启动开发服务器 |
| `npm run build` | 构建生产版本 |
| `npm run preview` | 预览生产版本 |

#### 后端

| 命令 | 说明 |
|------|------|
| `pip install -r requirements.txt` | 安装依赖 |
| `python main.py` | 启动开发服务器 |
| `pytest` | 运行测试 |

### 9.2 技术文档链接

- [Vue 3 文档](https://vuejs.org/)
- [Vite 文档](https://vitejs.dev/)
- [Element Plus 文档](https://element-plus.org/)
- [Three.js 文档](https://threejs.org/)
- [TresJS 文档](https://tresjs.org/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [SCSS 文档](https://sass-lang.com/)

### 9.3 版本历史

| 版本 | 日期 | 修改内容 |
|------|------|----------|
| v1.0.0 | 2026-05-29 | 初始版本 |

---

*本文档由 Agent 自动生成，最后更新于 2026-05-29*
