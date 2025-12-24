<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

interface Group {
  id: string
  name: string
  description?: string
  organization_id: string
}

interface GroupsResponse {
  organization_id: string
  groups: Group[]
}

const route = useRoute()
const orgId = ref<string>(route.params.orgId as string)
const groups = ref<Group[]>([])
const loading = ref<boolean>(true)
const error = ref<string | null>(null)

const fetchGroups = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await fetch(`/api/organizations/${orgId.value}/groups`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch groups: ${response.statusText}`)
    }
    
    const data: GroupsResponse = await response.json()
    groups.value = data.groups
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An error occurred while fetching groups'
    console.error('Error fetching groups:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchGroups()
})
</script>

<template>
  <div class="organization-view">
    <div class="container">
      <h1>Organization Groups</h1>
      <p class="org-id">Organization ID: {{ orgId }}</p>
      
      <div v-if="loading" class="loading">
        Loading groups...
      </div>
      
      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <button @click="fetchGroups" class="retry-btn">Retry</button>
      </div>
      
      <div v-else>
        <div v-if="groups.length === 0" class="no-groups">
          <p>No groups found in this organization.</p>
        </div>
        
        <div v-else class="groups-list">
          <div v-for="group in groups" :key="group.id" class="group-card">
            <h2>{{ group.name }}</h2>
            <p v-if="group.description">{{ group.description }}</p>
            <span class="group-id">ID: {{ group.id }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.organization-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.org-id {
  color: #666;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.loading, .error, .no-groups {
  text-align: center;
  padding: 3rem;
  color: #666;
}

.error {
  color: #d32f2f;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.retry-btn:hover {
  background: #5568d3;
}

.groups-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.group-card {
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.group-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.group-card h2 {
  color: #333;
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
}

.group-card p {
  color: #666;
  margin: 0.5rem 0;
  line-height: 1.5;
}

.group-id {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.25rem 0.5rem;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 4px;
  font-size: 0.85rem;
  font-family: monospace;
}
</style>

