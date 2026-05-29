<template>
  <header class="header">
    <div class="header-left">
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>
    

  </header>
</template>

<script setup>
defineProps({
  pageTitle: {
    type: String,
    default: '资源管理'
  }
})


</script>

<style scoped lang="scss">
.header {
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e8eef3;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: fixed;
  top: 0;
  left: 220px;
  right: 0;
  z-index: 99;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-left {
  .page-title {
    font-size: 18px;
    font-weight: 600;
    color: #1a1a2e;
    margin: 0;
  }
}
</style>
