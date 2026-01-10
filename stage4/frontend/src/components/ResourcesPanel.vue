<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

interface Resource {
  id: string
  name: string
  description?: string
  type?: string
  url?: string
  group_id: string
  organization_id: string
  created_at?: string
  updated_at?: string
}

interface ResourcesResponse {
  organization_id: string
  group_id: string
  resources: Resource[]
}

const route = useRoute()
const orgId = ref<string>(route.params.orgId as string)
const groupId = ref<string>(route.params.groupId as string)
const resources = ref<Resource[]>([])
const loading = ref<boolean>(true)
const error = ref<string | null>(null)

const fetchResources = async () => {
  try {
    loading.value = true
    error.value = null

    const response = await fetch(
      `/api/organizations/${orgId.value}/groups/${groupId.value}/resources`
    )

    if (!response.ok) {
      throw new Error(`Failed to fetch resources: ${response.statusText}`)
    }

    const data: ResourcesResponse = await response.json()
    resources.value = data.resources
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'An error occurred while fetching resources'
    console.error('Error fetching resources:', err)
  } finally {
    loading.value = false
  }
}

const getResourceIcon = (type?: string) => {
  if (!type) return 'mdi-file'
  switch (type.toLowerCase()) {
    case 'file':
      return 'mdi-file'
    case 'link':
      return 'mdi-link'
    case 'document':
      return 'mdi-file-document'
    default:
      return 'mdi-file'
  }
}

const openResource = (resource: Resource) => {
  if (resource.url) {
    window.open(resource.url, '_blank')
  }
}

onMounted(() => {
  fetchResources()
})
</script>

<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-4">Resources</h1>
        <p class="text-body-2 text-grey mb-4">
          Group ID: {{ groupId }} | Organization ID: {{ orgId }}
        </p>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p class="mt-4">Loading resources...</p>
      </v-col>
    </v-row>

    <v-row v-else-if="error">
      <v-col cols="12">
        <v-alert type="error" variant="tonal">
          {{ error }}
          <template #append>
            <v-btn variant="text" @click="fetchResources">Retry</v-btn>
          </template>
        </v-alert>
      </v-col>
    </v-row>

    <v-row v-else-if="resources.length === 0">
      <v-col cols="12">
        <v-alert type="info" variant="tonal">No resources found in this group.</v-alert>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col v-for="resource in resources" :key="resource.id" cols="12" md="6" lg="4">
        <v-card
          :hover="!!resource.url"
          :class="{ 'cursor-pointer': !!resource.url }"
          @click="openResource(resource)"
        >
          <v-card-item>
            <v-card-title class="d-flex align-center">
              <v-icon :icon="getResourceIcon(resource.type)" class="mr-2"></v-icon>
              {{ resource.name }}
            </v-card-title>
            <v-card-subtitle v-if="resource.description">
              {{ resource.description }}
            </v-card-subtitle>
          </v-card-item>

          <v-card-text v-if="resource.type" class="pt-0">
            <v-chip size="small" color="primary" variant="flat">
              {{ resource.type }}
            </v-chip>
          </v-card-text>

          <v-card-actions v-if="resource.url">
            <v-btn variant="text" prepend-icon="mdi-open-in-new">
              Open Resource
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

