<template>
  <div class="detail-editor">
    <!-- 左侧：缩略图列表栏 -->
    <div class="left-panel">
      <div class="panel-header">
        <h3>素材列表</h3>
        <span class="count">{{ thumbnails.length }} 页</span>
      </div>
      
      <div class="thumbnail-list">
        <div 
          v-for="(thumb, index) in thumbnails" 
          :key="index"
          :class="{ active: activeIndex === index }"
          class="thumbnail-item"
          @click="activeIndex = index"
        >
          <div class="thumbnail-preview">
            <span>{{ thumb.icon }}</span>
          </div>
          <span class="thumbnail-name">{{ thumb.name }}</span>
          
          <!-- 操作按钮 -->
          <div class="thumbnail-actions">
            <button class="action-btn upload-btn" title="上传新素材" @click.stop="handleUpload(index)">
              <span>📤</span>
            </button>
            <button class="action-btn replace-btn" title="替换此素材" @click.stop="handleReplace(index)">
              <span>🔄</span>
            </button>
            <button class="action-btn delete-btn" title="删除此素材" @click.stop="handleDelete(index)">
              <span>🗑️</span>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 中间：编辑预览区域 -->
    <div class="center-panel">
      <!-- 预览画布区域（左侧） -->
      <div class="preview-container">
        <!-- 预览工具栏 -->
        <div class="preview-toolbar">
          <button 
            v-for="mode in interactModes" 
            :key="mode.id"
            :class="{ active: currentMode === mode.id }"
            class="mode-btn"
            @click="currentMode = mode.id"
          >
            <span>{{ mode.icon }}</span>
            <span>{{ mode.label }}</span>
          </button>
        </div>
        
        <!-- 画布区域 -->
        <div class="canvas-wrapper">
          <!-- 摄像头窗口 -->
          <div class="camera-window" v-if="currentMode === 'gesture'">
            <div class="camera-header">
              <span class="camera-icon">📷</span>
              <span>手势识别中</span>
            </div>
            <div class="camera-feed">
              <div class="camera-placeholder">
                <span class="camera-emoji">🎥</span>
                <span>摄像头预览</span>
              </div>
            </div>
          </div>
          
          <!-- 3D预览画布 -->
          <div class="preview-canvas" ref="canvasRef">
            <div class="canvas-content">
              <div class="scene-3d">
                <div class="cube">
                  <div class="cube-face front">🎲</div>
                  <div class="cube-face back">🎲</div>
                  <div class="cube-face right">🎲</div>
                  <div class="cube-face left">🎲</div>
                  <div class="cube-face top">🎲</div>
                  <div class="cube-face bottom">🎲</div>
                </div>
              </div>
              <div class="canvas-info">
                <span>OrbitControls 已启用</span>
                <span>拖动旋转 | 滚轮缩放 | 右键平移</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 代码编辑器区域（右侧） -->
      <div class="editor-container">
        <!-- 代码编辑器工具栏 -->
        <div class="editor-toolbar">
          <button class="tool-btn" @click="formatCode">
            <span>📋</span>
            <span>格式化</span>
          </button>
          <button class="tool-btn" @click="clearCode">
            <span>🗑️</span>
            <span>清空</span>
          </button>
          <button class="tool-btn run-btn" @click="runCode">
            <span>▶️</span>
            <span>运行</span>
          </button>
          <div class="language-selector">
            <select v-model="currentLanguage" class="lang-select">
              <option value="html">HTML</option>
              <option value="css">CSS</option>
              <option value="javascript">JavaScript</option>
            </select>
          </div>
        </div>
        
        <!-- 代码编辑区域 -->
        <div class="code-editor">
          <pre class="line-numbers"><span v-for="n in lineCount" :key="n">{{ n }}</span></pre>
          <textarea 
            v-model="codeContent" 
            class="code-textarea"
            :class="currentLanguage"
            spellcheck="false"
          ></textarea>
        </div>
      </div>
    </div>
    
    <!-- 右侧：导出功能栏 -->
    <div class="right-panel">
      <div class="panel-header">
        <h3>一键导出</h3>
      </div>
      
      <div class="export-section">
        <div class="section-title">
          <span class="title-icon">📤</span>
          <span>导出格式</span>
        </div>
        
        <div class="format-options">
          <label 
            v-for="format in exportFormats" 
            :key="format.id"
            class="format-label"
          >
            <input 
              type="radio" 
              v-model="selectedFormat" 
              :value="format.id"
            />
            <span class="format-icon">{{ format.icon }}</span>
            <span class="format-name">{{ format.name }}</span>
          </label>
        </div>
        
        <button class="export-btn" @click="handleExport">
          <span class="export-icon">🚀</span>
          <span>开始导出</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { uploadMaterial, replaceMaterial, deleteMaterial } from '../utils/api.js'

const props = defineProps({
  projectId: {
    type: Number,
    default: 1
  }
})

const activeIndex = ref(0)
const currentMode = ref('orbit')
const currentLanguage = ref('javascript')
const selectedFormat = ref('html')

// 文件输入元素引用
const uploadInput = ref(null)
const replaceInput = ref(null)

const codeContent = ref(`// Three.js 3D场景示例
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

// 创建场景
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x1a1a2e);

// 创建相机
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.z = 5;

// 创建渲染器
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 创建几何体
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshPhongMaterial({
  color: 0x4facfe,
  shininess: 100
});
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// 添加光源
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xffffff, 1);
pointLight.position.set(5, 5, 5);
scene.add(pointLight);

// 轨道控制器
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// 动画循环
function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  controls.update();
  renderer.render(scene, camera);
}
animate();

// 窗口resize处理
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});`)

const thumbnails = ref([
  { name: '场景1', icon: '🎬' },
  { name: '场景2', icon: '🌍' },
  { name: '场景3', icon: '✨' },
  { name: '场景4', icon: '🏗️' },
  { name: '场景5', icon: '🎨' },
  { name: '场景6', icon: '🖼️' },
])

const interactModes = [
  { id: 'orbit', label: '轨道控制', icon: '🖱️' },
  { id: 'gesture', label: '手势控制', icon: '🤚' }
]

const exportFormats = [
  { id: 'html', name: 'HTML', icon: '🌐' },
  { id: 'pdf', name: 'PDF', icon: '📄' },
]

const lineCount = computed(() => {
  return codeContent.value.split('\n').length
})

function formatCode() {
  alert('代码格式化功能已触发')
}

function clearCode() {
  if (confirm('确定要清空代码吗？')) {
    codeContent.value = ''
  }
}

function runCode() {
  alert('代码运行中...')
}

function handleExport() {
  alert(`正在导出 ${selectedFormat.value.toUpperCase()} 格式...`)
}

// 上传新素材
function handleUpload(index) {
  // 创建临时文件输入
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*,video/*,model/*,text/*'
  input.style.display = 'none'
  
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    
    try {
      const result = await uploadMaterial(props.projectId, file, null, index + 1)
      if (result.code === 200) {
        // 在当前位置后插入新素材
        thumbnails.value.splice(index + 1, 0, result.data)
        activeIndex.value = index + 1
        alert('上传成功！')
      } else {
        alert(`上传失败: ${result.msg}`)
      }
    } catch (error) {
      console.error('上传失败:', error)
      alert('上传失败，请检查后端服务是否运行')
    }
  }
  
  document.body.appendChild(input)
  input.click()
  document.body.removeChild(input)
}

// 替换素材
function handleReplace(index) {
  const material = thumbnails.value[index]
  if (!material) return
  
  // 创建临时文件输入
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*,video/*,model/*,text/*'
  input.style.display = 'none'
  
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    
    try {
      const result = await replaceMaterial(material.id, file)
      if (result.code === 200) {
        // 更新素材信息
        thumbnails.value[index] = { ...material, ...result.data }
        alert('替换成功！')
      } else {
        alert(`替换失败: ${result.msg}`)
      }
    } catch (error) {
      console.error('替换失败:', error)
      alert('替换失败，请检查后端服务是否运行')
    }
  }
  
  document.body.appendChild(input)
  input.click()
  document.body.removeChild(input)
}

// 删除素材
async function handleDelete(index) {
  const material = thumbnails.value[index]
  if (!material) return
  
  if (!confirm(`确定要删除 "${material.name}" 吗？`)) {
    return
  }
  
  try {
    const result = await deleteMaterial(material.id)
    if (result.code === 200) {
      thumbnails.value.splice(index, 1)
      if (activeIndex.value >= thumbnails.value.length) {
        activeIndex.value = Math.max(0, thumbnails.value.length - 1)
      }
      alert('删除成功！')
    } else {
      alert(`删除失败: ${result.msg}`)
    }
  } catch (error) {
    console.error('删除失败:', error)
    // 如果API调用失败，仍然从界面移除
    thumbnails.value.splice(index, 1)
    if (activeIndex.value >= thumbnails.value.length) {
      activeIndex.value = Math.max(0, thumbnails.value.length - 1)
    }
    alert('已从界面移除（后端服务未运行）')
  }
}

onMounted(() => {
  // 初始化代码编辑器
})
</script>

<style scoped lang="scss">
.detail-editor {
  display: flex;
  height: calc(100vh - 60px);
  padding-top: 60px;
}

/* 左侧缩略图栏 */
.left-panel {
  width: 180px;
  background: #0d1f3c;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  
  .panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    h3 {
      color: #fff;
      font-size: 14px;
      margin: 0;
    }
    
    .count {
      font-size: 12px;
      color: rgba(255, 255, 255, 0.5);
      background: rgba(255, 255, 255, 0.1);
      padding: 4px 10px;
      border-radius: 10px;
    }
  }
  
  .thumbnail-list {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
  }
  
  .thumbnail-item {
    margin-bottom: 12px;
    cursor: pointer;
    border-radius: 8px;
    overflow: hidden;
    border: 2px solid transparent;
    transition: all 0.3s ease;
    
    &:hover {
      border-color: rgba(79, 172, 254, 0.5);
    }
    
    &.active {
      border-color: #4facfe;
      background: rgba(79, 172, 254, 0.1);
    }
    
    .thumbnail-preview {
      height: 80px;
      background: linear-gradient(135deg, #1a3a5c 0%, #0d1f3c 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32px;
    }
    
    .thumbnail-name {
      display: block;
      padding: 8px;
      text-align: center;
      font-size: 12px;
      color: rgba(255, 255, 255, 0.8);
      background: rgba(0, 0, 0, 0.2);
    }
    
    .thumbnail-actions {
      display: flex;
      justify-content: center;
      gap: 8px;
      padding: 8px;
      background: rgba(0, 0, 0, 0.3);
      
      .action-btn {
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
        
        &.upload-btn {
          background: rgba(79, 172, 254, 0.2);
          color: #4facfe;
          
          &:hover {
            background: rgba(79, 172, 254, 0.4);
            transform: scale(1.1);
          }
        }
        
        &.replace-btn {
          background: rgba(255, 193, 7, 0.2);
          color: #ffc107;
          
          &:hover {
            background: rgba(255, 193, 7, 0.4);
            transform: scale(1.1);
          }
        }
        
        &.delete-btn {
          background: rgba(255, 77, 79, 0.2);
          color: #ff4d4f;
          
          &:hover {
            background: rgba(255, 77, 79, 0.4);
            transform: scale(1.1);
          }
        }
      }
    }
  }
}

/* 中间编辑预览区域 */
.center-panel {
  flex: 1;
  display: flex;
  flex-direction: row;
  background: #1e1e1e;
}

/* 代码编辑器 */
.editor-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-left: 1px solid #3c3c3c;
}

.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #252526;
  border-bottom: 1px solid #3c3c3c;
  
  .tool-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 6px 12px;
    background: #3c3c3c;
    border: none;
    border-radius: 4px;
    color: #ccc;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      background: #4c4c4c;
      color: #fff;
    }
    
    &.run-btn {
      background: #007acc;
      color: #fff;
      
      &:hover {
        background: #0088e6;
      }
    }
  }
  
  .language-selector {
    margin-left: auto;
    
    .lang-select {
      padding: 6px 12px;
      background: #3c3c3c;
      border: none;
      border-radius: 4px;
      color: #ccc;
      font-size: 12px;
      cursor: pointer;
      
      &:focus {
        outline: none;
      }
    }
  }
}

.code-editor {
  flex: 1;
  display: flex;
  overflow: hidden;
  font-family: 'Fira Code', 'Consolas', monospace;
}

.line-numbers {
  width: 50px;
  padding: 12px 0;
  background: #252526;
  border-right: 1px solid #3c3c3c;
  text-align: right;
  
  span {
    display: block;
    line-height: 20px;
    font-size: 13px;
    color: #858585;
    padding-right: 8px;
  }
}

.code-textarea {
  flex: 1;
  padding: 12px;
  background: #1e1e1e;
  border: none;
  color: #d4d4d4;
  font-size: 13px;
  line-height: 20px;
  resize: none;
  outline: none;
  font-family: inherit;
  
  &::placeholder {
    color: #4a4a4a;
  }
  
  &.javascript {
    &::-webkit-scrollbar {
      width: 8px;
    }
    &::-webkit-scrollbar-track {
      background: #252526;
    }
    &::-webkit-scrollbar-thumb {
      background: #4c4c4c;
      border-radius: 4px;
    }
  }
}

/* 预览画布 */
.preview-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.preview-toolbar {
  display: flex;
  gap: 8px;
  padding: 8px 12px;
  background: #252526;
  border-bottom: 1px solid #3c3c3c;
  
  .mode-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    background: #3c3c3c;
    border: none;
    border-radius: 6px;
    color: #ccc;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      background: #4c4c4c;
    }
    
    &.active {
      background: #4facfe;
      color: #fff;
    }
  }
}

.canvas-wrapper {
  flex: 1;
  position: relative;
  background: #0a0a0a;
  overflow: hidden;
}

.camera-window {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 200px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 12px;
  overflow: hidden;
  z-index: 10;
  border: 2px solid #4facfe;
  
  .camera-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: #1a1a2e;
    font-size: 12px;
    color: #4facfe;
    
    .camera-icon {
      font-size: 14px;
    }
  }
  
  .camera-feed {
    height: 150px;
    background: #0a0a0a;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .camera-placeholder {
    text-align: center;
    color: #666;
    
    .camera-emoji {
      display: block;
      font-size: 32px;
      margin-bottom: 8px;
    }
  }
}

.preview-canvas {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.canvas-content {
  position: relative;
}

.scene-3d {
  width: 300px;
  height: 300px;
  perspective: 800px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cube {
  width: 100px;
  height: 100px;
  position: relative;
  transform-style: preserve-3d;
  animation: rotate 8s infinite linear;
}

.cube-face {
  position: absolute;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  border: 2px solid rgba(79, 172, 254, 0.5);
  background: rgba(79, 172, 254, 0.1);
  backdrop-filter: blur(2px);
  
  &.front { transform: translateZ(50px); }
  &.back { transform: rotateY(180deg) translateZ(50px); }
  &.right { transform: rotateY(90deg) translateZ(50px); }
  &.left { transform: rotateY(-90deg) translateZ(50px); }
  &.top { transform: rotateX(90deg) translateZ(50px); }
  &.bottom { transform: rotateX(-90deg) translateZ(50px); }
}

@keyframes rotate {
  0% { transform: rotateX(0deg) rotateY(0deg); }
  100% { transform: rotateX(360deg) rotateY(360deg); }
}

.canvas-info {
  position: absolute;
  bottom: -40px;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 12px;
  
  span {
    display: block;
    margin-bottom: 4px;
  }
}

/* 右侧导出栏 */
.right-panel {
  width: 280px;
  background: #fff;
  border-left: 1px solid #e8eef3;
  display: flex;
  flex-direction: column;
  
  .panel-header {
    padding: 16px;
    border-bottom: 1px solid #e8eef3;
    
    h3 {
      margin: 0;
      font-size: 15px;
      color: #1a1a2e;
    }
  }
  
  .export-section {
    flex: 1;
    padding: 16px;
    overflow-y: auto;
  }
  
  .section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #5a6a85;
    margin-bottom: 12px;
    
    .title-icon {
      font-size: 16px;
    }
  }
  
  .format-options {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
  }
  
  .format-label {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
    border: 2px solid #e8eef3;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      border-color: #4facfe;
    }
    
    input[type="radio"] {
      display: none;
      
      &:checked + .format-icon {
        transform: scale(1.2);
      }
      
      &:checked + .format-icon + .format-name {
        color: #4facfe;
        font-weight: 600;
      }
    }
    
    &:has(input:checked) {
      border-color: #4facfe;
      background: rgba(79, 172, 254, 0.05);
    }
    
    .format-icon {
      font-size: 32px;
      margin-bottom: 8px;
      transition: transform 0.3s ease;
    }
    
    .format-name {
      font-size: 13px;
      color: #5a6a85;
    }
  }
  
  .export-btn {
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    border: none;
    border-radius: 10px;
    color: #fff;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.3s ease;
    margin-bottom: 20px;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(79, 172, 254, 0.4);
    }
    
    .export-icon {
      font-size: 18px;
    }
  }
}
</style>
