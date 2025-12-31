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

      <div v-if="loading" class="loading">Loading groups...</div>

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
