<script>
import groupsService from '@/services/groupsService'
import AddResourceButton from '@/components/AddResourceButton.vue'

export default {
  components: {
    AddResourceButton,
  },
  props: { group_id: String },
  data() {
    return {
      searchQuery: '',
      resources: [],
      loading: false,
    }
  },
  computed: {
    filteredGroups() {
      let filtered = this.resources
      
      // Filter by search query if present
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter((resource) => resource.name.toLowerCase().includes(query))
      }
      
      // Sort by net votes (upvotes - downvotes) in descending order
      return filtered.slice().sort((a, b) => {
        const netVotesA = (a.upvotes || 0) - (a.downvotes || 0)
        const netVotesB = (b.upvotes || 0) - (b.downvotes || 0)
        return netVotesB - netVotesA
      })
    },
  },
  async mounted() {
    await this.fetchResources()
  },
  methods: {
    async fetchResources() {
      this.resources = await groupsService.getAllResources(this.group_id)
      console.log(this.resources)
    },
    async upvoteResource(resourceId) {
      await groupsService.upvoteResource(this.group_id, resourceId)
      await this.fetchResources()
    },
    async downvoteResource(resourceId) {
      await groupsService.downvoteResource(this.group_id, resourceId)
      await this.fetchResources()
    },
  },
  // watch: {
  //   group_id: {
  //     immediate: true,
  //     handler(newVal) {
  //       if (newVal) {
  //         groupsService.getAllResources(this.group_id)
  //       }
  //     },
  //   },
  // },
}
</script>

<template>
  <!-- <v-navigation-drawer -->
  <!--   width="350" -->
  <!--   permanent -->
  <!--   location="right" -->
  <!--   border="left" -->
  <!--   class="pa-4 bg-grey-lighten-5" -->
  <!-- > -->
  <h2 class="text-h6 mb-4 text-right font-weight-bold" style="color: #333">المصادر</h2>

  <v-text-field
    v-model="searchQuery"
    variant="outlined"
    placeholder="أبحث عن مصدر..."
    prepend-inner-icon="mdi-magnify"
    rounded="lg"
    bg-color="white"
    density="compact"
    class="mb-4"
    hide-details
    clearable
  ></v-text-field>
  <AddResourceButton @uploaded="fetchResources" :groupId="group_id" />

  <div v-if="loading" class="text-center pa-10">
    <v-progress-circular indeterminate color="primary"></v-progress-circular>
  </div>

  <v-list v-else bg-color="transparent" class="pa-0 pt-2">
    <v-card
      v-for="resource in filteredGroups"
      :key="resource._id"
      variant="outlined"
      class="mb-4 resource-card"
      rounded="lg"
    >
      <v-card-text class="pa-4">
        <!-- Header Section -->
        <div class="d-flex align-start mb-3">
          <v-avatar 
            color="primary" 
            size="56" 
            rounded="lg" 
            class="elevation-2"
          >
            <v-icon color="white" size="32">mdi-file-document</v-icon>
          </v-avatar>
          
          <div class="flex-grow-1 mr-4">
            <h3 class="text-h6 font-weight-bold mb-1 text-right">
              {{ resource.name }}
            </h3>
            <p class="text-body-2 text-grey-darken-1 text-right mb-2" v-if="resource.description">
              {{ resource.description }}
            </p>
            <div class="d-flex align-center justify-end text-caption text-grey">
              <v-icon size="14" class="ml-1">mdi-account</v-icon>
              <span>{{ resource.uploaded_by }}</span>
            </div>
          </div>
        </div>

        <v-divider class="my-3"></v-divider>

        <!-- Actions Section -->
        <div class="d-flex align-center justify-space-between">
          <!-- Vote Section -->
          <div class="d-flex align-center gap-2">
            <v-btn
              size="small"
              variant="tonal"
              color="success"
              @click.stop="upvoteResource(resource._id)"
              class="vote-btn"
            >
              <v-icon size="18" class="ml-1">mdi-thumb-up</v-icon>
              {{ resource.upvotes }}
            </v-btn>
            
            <v-btn
              size="small"
              variant="tonal"
              color="error"
              @click.stop="downvoteResource(resource._id)"
              class="vote-btn"
            >
              <v-icon size="18" class="ml-1">mdi-thumb-down</v-icon>
              {{ resource.downvotes }}
            </v-btn>
          </div>

          <!-- Download Button -->
          <a :href="resource.file_url" :download="resource.name" rel="noopener" @click.stop>
            <v-btn 
              color="primary" 
              variant="flat"
              size="default"
              rounded="lg"
              class="download-btn"
            >
              <v-icon class="ml-2">mdi-download</v-icon>
              تحميل
            </v-btn>
          </a>
        </div>
      </v-card-text>
    </v-card>

    <div v-if="filteredGroups.length === 0" class="text-center pa-4 text-grey">لا توجد مصادر</div>
  </v-list>
  <!-- </v-navigation-drawer> -->
</template>

<style scoped>
.resource-card {
  border: 1px solid #e0e0e0 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
}

.resource-card:hover {
  border-color: #1976d2 !important;
  box-shadow: 0 4px 20px rgba(25, 118, 210, 0.12) !important;
  transform: translateY(-2px);
}

.vote-btn {
  min-width: 70px;
  font-weight: 600;
}

.download-btn {
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.2);
}

.download-btn:hover {
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
}

.gap-2 {
  gap: 0.5rem;
}
</style>
