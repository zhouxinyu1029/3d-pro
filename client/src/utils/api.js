// 后端API基础地址（使用Vite代理）
const BASE_URL = '/api';

// 上传新素材
export async function uploadMaterial(projectId, file, name = null, sortOrder = 0) {
  const formData = new FormData();
  formData.append('project_id', projectId);
  formData.append('file', file);
  if (name) {
    formData.append('name', name);
  }
  formData.append('sort_order', sortOrder);

  const response = await fetch(`${BASE_URL}/materials/upload`, {
    method: 'POST',
    body: formData
  });

  return await response.json();
}

// 替换素材
export async function replaceMaterial(materialId, file, name = null) {
  const formData = new FormData();
  formData.append('file', file);
  if (name) {
    formData.append('name', name);
  }

  const response = await fetch(`${BASE_URL}/materials/${materialId}/replace`, {
    method: 'POST',
    body: formData
  });

  return await response.json();
}

// 删除素材
export async function deleteMaterial(materialId) {
  const response = await fetch(`${BASE_URL}/materials/${materialId}`, {
    method: 'DELETE'
  });

  return await response.json();
}

// 获取项目的素材列表
export async function getProjectMaterials(projectId) {
  const response = await fetch(`${BASE_URL}/projects/${projectId}/materials`);
  return await response.json();
}

// 批量上传素材
export async function batchUploadMaterials(projectId, files) {
  const formData = new FormData();
  formData.append('project_id', projectId);
  files.forEach(file => {
    formData.append('files', file);
  });

  const response = await fetch(`${BASE_URL}/materials/batch-upload`, {
    method: 'POST',
    body: formData
  });

  return await response.json();
}

// 保存项目
export async function saveProject(name, code) {
  const formData = new FormData();
  formData.append('name', name);
  formData.append('code', code);

  const response = await fetch(`${BASE_URL}/save-project`, {
    method: 'POST',
    body: formData
  });

  return await response.json();
}

// 获取项目列表
export async function getProjects() {
  const response = await fetch(`${BASE_URL}/projects`);
  return await response.json();
}