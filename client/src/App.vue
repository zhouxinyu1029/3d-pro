<template>
  <div class="app-container">
    <!-- 侧边导航 -->
    <Sidebar 
      :currentMenu="currentMenu" 
      @menu-change="handleMenuChange" 
    />
    
    <!-- 主内容区域 -->
    <main class="main-content">
      <!-- 顶部标题栏 -->
      <Header 
        :pageTitle="pageTitle" 
      />
      
      <!-- 页面内容 -->
      <div class="page-content">
        <!-- 资源管理列表页 -->
        <ResourceList 
          v-if="currentPage === 'list'" 
          @card-click="handleCardClick"
        />
        
        <!-- 详情编辑页 -->
        <DetailEditor 
          v-else-if="currentPage === 'detail'"
          :resource="selectedResource"
        />
      </div>
    </main>
    
    <!-- 返回按钮（详情页显示） -->
    <button 
      v-if="currentPage === 'detail'"
      class="back-btn"
      @click="goBack"
    >
      <span>←</span>
      <span>返回列表</span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import ResourceList from './components/ResourceList.vue'
import DetailEditor from './components/DetailEditor.vue'

const currentMenu = ref('resources')
const currentPage = ref('list')
const selectedResource = ref(null)

const pageTitle = computed(() => {
  if (currentPage.value === 'list') {
    return '资源管理'
  } else if (currentPage.value === 'detail') {
    return selectedResource.value ? selectedResource.value.name : '素材详情'
  }
  return '资源管理'
})

function handleMenuChange(menu) {
  currentMenu.value = menu
  currentPage.value = 'list'
}

function handleCardClick(resource) {
  selectedResource.value = resource
  currentPage.value = 'detail'
}

function goBack() {
  currentPage.value = 'list'
  selectedResource.value = null
}


</script>

<style scoped lang="scss">
.app-container {
  display: flex;
  min-height: 100vh;
  background: #f8fafc;
}

.main-content {
  flex: 1;
  margin-left: 220px;
  min-height: 100vh;
}

.page-content {
  padding-top: 60px;
}

.back-btn {
  position: fixed;
  top: 75px;
  left: 240px;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: #fff;
  border: 1px solid #e8eef3;
  border-radius: 25px;
  cursor: pointer;
  font-size: 13px;
  color: #5a6a85;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  
  &:hover {
    border-color: #4facfe;
    color: #4facfe;
    box-shadow: 0 4px 12px rgba(79, 172, 254, 0.15);
  }
  
  span:first-child {
    font-size: 16px;
  }
}
</style>
