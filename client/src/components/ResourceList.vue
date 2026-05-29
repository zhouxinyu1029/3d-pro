<template>
  <div class="resource-list">
    <!-- 顶部筛选区域 -->
    <div class="filter-bar">
      <div class="filter-group">
        <label class="filter-label">上传时间</label>
        <select v-model="filters.time" class="filter-select">
          <option value="">全部时间</option>
          <option value="today">今天</option>
          <option value="week">近一周</option>
          <option value="month">近一个月</option>
        </select>
      </div>
      
      <div class="filter-group search-group">
        <input 
          v-model="filters.search" 
          type="text" 
          class="search-input" 
          placeholder="搜索文件名称..."
        />
        <button class="search-btn">🔍</button>
      </div>
      
      <button class="reset-btn" @click="resetFilters">
        <span>重置筛选</span>
      </button>
    </div>
    
    <!-- 素材卡片列表 -->
    <div class="cards-container">
      <div 
        v-for="item in filteredResources" 
        :key="item.id" 
        class="resource-card"
        @click="$emit('card-click', item)"
      >
        <div class="card-thumbnail">
          <span class="thumbnail-icon">{{ item.icon }}</span>
          <div class="card-overlay">
            <span class="file-type">{{ item.typeLabel }}</span>
          </div>
        </div>
        
        <div class="card-info">
          <h3 class="card-title">{{ item.name }}</h3>
          <div class="card-meta">
            <span class="meta-item">{{ item.size }}</span>
            <span class="meta-item">{{ item.date }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分页组件 -->
    <div class="pagination-bar">
      <div class="pagination-info">
        显示 {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, total) }} 条，共 {{ total }} 条
      </div>
      
      <div class="pagination-controls">
        <button 
          class="page-btn" 
          :disabled="currentPage === 1"
          @click="currentPage--"
        >
          上一页
        </button>
        
        <div class="page-numbers">
          <button 
            v-for="page in displayedPages" 
            :key="page"
            :class="{ active: currentPage === page, ellipsis: page === '...' }"
            :disabled="page === '...'"
            @click="page !== '...' && (currentPage = page)"
          >
            {{ page }}
          </button>
        </div>
        
        <button 
          class="page-btn" 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >
          下一页
        </button>
        
        <div class="page-size-selector">
          <select v-model="pageSize" class="size-select">
            <option :value="8">8条/页</option>
            <option :value="12">12条/页</option>
            <option :value="20">20条/页</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

defineEmits(['card-click'])

const filters = ref({
  time: '',
  search: ''
})

const currentPage = ref(1)
const pageSize = ref(8)

const resources = ref([
  { id: 1, name: '太空场景动画', type: 'video', typeLabel: '视频', size: '256MB', date: '2024-01-15', icon: '🎬' },
  { id: 2, name: '建筑模型.obj', type: 'model', typeLabel: '3D模型', size: '128MB', date: '2024-01-14', icon: '🏗️' },
  { id: 3, name: '粒子特效.js', type: 'code', typeLabel: '代码', size: '4KB', date: '2024-01-13', icon: '📄' },
  { id: 4, name: '星空背景.jpg', type: 'image', typeLabel: '图片', size: '2MB', date: '2024-01-12', icon: '🖼️' },
  { id: 5, name: '角色动画.glb', type: 'model', typeLabel: '3D模型', size: '512MB', date: '2024-01-11', icon: '🧑‍🦰' },
  { id: 6, name: '场景渲染.html', type: 'code', typeLabel: '代码', size: '8KB', date: '2024-01-10', icon: '🌐' },
  { id: 7, name: 'UI界面.png', type: 'image', typeLabel: '图片', size: '1MB', date: '2024-01-09', icon: '🎨' },
  { id: 8, name: '光影效果.mp4', type: 'video', typeLabel: '视频', size: '192MB', date: '2024-01-08', icon: '✨' },
  { id: 9, name: '材质球.json', type: 'code', typeLabel: '代码', size: '2KB', date: '2024-01-07', icon: '⚽' },
  { id: 10, name: '环境贴图.hdr', type: 'image', typeLabel: '图片', size: '64MB', date: '2024-01-06', icon: '🌍' },
  { id: 11, name: '交互动画.ts', type: 'code', typeLabel: '代码', size: '12KB', date: '2024-01-05', icon: '🔄' },
  { id: 12, name: '产品展示.mp4', type: 'video', typeLabel: '视频', size: '320MB', date: '2024-01-04', icon: '📦' },
])

const filteredResources = computed(() => {
  let result = resources.value
  
  if (filters.value.search) {
    const keyword = filters.value.search.toLowerCase()
    result = result.filter(r => r.name.toLowerCase().includes(keyword))
  }
  
  return result
})

const total = computed(() => filteredResources.value.length)
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

const displayedPages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 5) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    if (current <= 3) {
      pages.push(1, 2, 3, 4, '...', total)
    } else if (current >= total - 2) {
      pages.push(1, '...', total - 3, total - 2, total - 1, total)
    } else {
      pages.push(1, '...', current - 1, current, current + 1, '...', total)
    }
  }
  
  return pages
})

function resetFilters() {
  filters.value = { time: '', search: '' }
  currentPage.value = 1
}
</script>

<style scoped lang="scss">
.resource-list {
  padding: 24px;
  background: #f8fafc;
  min-height: calc(100vh - 60px);
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
  
  &.search-group {
    flex: 1;
    max-width: 300px;
    position: relative;
  }
}

.filter-label {
  font-size: 13px;
  color: #5a6a85;
  font-weight: 500;
}

.filter-select,
.search-input {
  padding: 8px 12px;
  border: 1px solid #e8eef3;
  border-radius: 8px;
  font-size: 13px;
  background: #fff;
  transition: all 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: #4facfe;
    box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
  }
}

.search-input {
  width: 100%;
  padding-right: 36px;
}

.search-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

.reset-btn {
  margin-left: auto;
  padding: 8px 16px;
  background: #f5f7fa;
  border: 1px solid #e8eef3;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  color: #5a6a85;
  transition: all 0.3s ease;
  
  &:hover {
    background: #e8eef3;
    color: #4facfe;
  }
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.resource-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(79, 172, 254, 0.15);
  }
  
  .card-thumbnail {
    position: relative;
    height: 160px;
    background: linear-gradient(135deg, #f0f5ff 0%, #e8f0fe 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    
    .thumbnail-icon {
      font-size: 48px;
    }
    
    .card-overlay {
      position: absolute;
      top: 12px;
      right: 12px;
      
      .file-type {
        padding: 4px 10px;
        background: rgba(0, 0, 0, 0.5);
        color: #fff;
        font-size: 11px;
        border-radius: 12px;
      }
    }
  }
  
  .card-info {
    padding: 16px;
    
    .card-title {
      font-size: 15px;
      font-weight: 600;
      color: #1a1a2e;
      margin: 0 0 8px 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    .card-meta {
      display: flex;
      gap: 12px;
      
      .meta-item {
        font-size: 12px;
        color: #8898aa;
      }
    }
  }
}

.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  flex-wrap: wrap;
  gap: 16px;
}

.pagination-info {
  font-size: 13px;
  color: #8898aa;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #e8eef3;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  font-size: 13px;
  color: #5a6a85;
  transition: all 0.3s ease;
  
  &:hover:not(:disabled) {
    border-color: #4facfe;
    color: #4facfe;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 4px;
  
  button {
    width: 36px;
    height: 36px;
    border: 1px solid #e8eef3;
    border-radius: 8px;
    background: #fff;
    cursor: pointer;
    font-size: 13px;
    color: #5a6a85;
    transition: all 0.3s ease;
    
    &:hover:not(:disabled) {
      border-color: #4facfe;
      color: #4facfe;
    }
    
    &.active {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      border-color: #4facfe;
      color: #fff;
    }
    
    &.ellipsis {
      border: none;
      cursor: default;
    }
  }
}

.page-size-selector {
  margin-left: 8px;
  
  .size-select {
    padding: 8px 12px;
    border: 1px solid #e8eef3;
    border-radius: 8px;
    font-size: 13px;
    background: #fff;
    cursor: pointer;
    
    &:focus {
      outline: none;
      border-color: #4facfe;
    }
  }
}
</style>
