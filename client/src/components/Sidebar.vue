<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="logo">
        <span class="logo-icon">🎨</span>
        <span class="logo-text">3D内容管理</span>
      </div>
    </div>
    
    <nav class="sidebar-menu">
      <ul>
        <li 
          v-for="item in menuItems" 
          :key="item.id"
          :class="{ active: currentMenu === item.id }"
          @click="$emit('menu-change', item.id)"
        >
          <span class="menu-icon">{{ item.icon }}</span>
          <span class="menu-text">{{ item.label }}</span>
        </li>
      </ul>
    </nav>
    
    <div class="sidebar-footer">
      <div class="user-info">
        <div class="avatar">👤</div>
        <span class="username">管理员</span>
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  currentMenu: {
    type: String,
    default: 'resources'
  }
})

defineEmits(['menu-change'])

const menuItems = [
  { id: 'resources', label: '资源管理', icon: '📁' }
]
</script>

<style scoped lang="scss">
.sidebar {
  width: 220px;
  height: 100vh;
  background: linear-gradient(180deg, #0a1628 0%, #0d1f3c 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  box-shadow: 2px 0 20px rgba(0, 0, 0, 0.3);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  
  .logo-icon {
    font-size: 28px;
  }
  
  .logo-text {
    font-size: 18px;
    font-weight: 600;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

.sidebar-menu {
  flex: 1;
  padding: 16px 0;
  
  ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  li {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    border-left: 3px solid transparent;
    
    &:hover {
      background: rgba(79, 172, 254, 0.15);
      border-left-color: rgba(79, 172, 254, 0.5);
    }
    
    &.active {
      background: linear-gradient(135deg, rgba(79, 172, 254, 0.2) 0%, rgba(0, 242, 254, 0.1) 100%);
      border-left-color: #4facfe;
    }
    
    .menu-icon {
      font-size: 18px;
    }
    
    .menu-text {
      font-size: 14px;
      font-weight: 500;
    }
  }
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  
  .avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
  }
  
  .username {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.8);
  }
}
</style>
