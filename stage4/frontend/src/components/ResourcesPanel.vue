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
      if (!this.searchQuery) return this.resources
      const query = this.searchQuery.toLowerCase()
      return this.resources.filter((resource) => resource.name.toLowerCase().includes(query))
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
      variant="flat"
      class="mb-4 college-card"
      rounded="xl"
      @click="$emit('select-resource', resource._id)"
    >
      <v-list-item class="pa-4">
        <div class="d-flex flex-column w-100">
          <div class="d-flex align-center w-100 mb-4">
            <v-avatar color="indigo-lighten-5" size="48" rounded="lg" class="elevation-1 ms-3">
              <v-icon color="indigo-darken-2" size="28">mdi-town-hall</v-icon>
            </v-avatar>

            <div class="flex-grow-1 text-center">
              <!-- Download button -->
              <a :href="resource.file_url" target="_blank" rel="noopener">
                <v-btn color="primary" small rounded="lg">
                  <v-icon left>mdi-download</v-icon>
                  تحميل
                </v-btn>
              </a>
              <span class="text-subtitle-1 font-weight-bold">
                {{ resource.name }}
              </span>
              <!-- description -->
              <div class="text-body-2 text-grey-darken-1">
                {{ resource.description }}
              </div>
              <div class="text-body-2 text-grey-darken-1">بواسطة {{ resource.uploaded_by }}</div>
              <!-- Upvote and downvote buttons -->
              <div class="d-flex align-center justify-center mt-2">
                <v-btn icon small>
                  <v-icon @click="upvoteResource(resource._id)" color="green">mdi-thumb-up</v-icon>
                </v-btn>
                <span class="mx-2">{{ resource.upvotes }}</span>
                <v-btn icon small>
                  <v-icon @click="downvoteResource(resource._id)" color="red"
                    >mdi-thumb-down</v-icon
                  >
                </v-btn>
                <span class="mx-2">{{ resource.downvotes }}</span>
              </div>
            </div>
            <v-divider class="mb-3"></v-divider>

            <div class="d-flex justify-space-between align-center">
              <div class="d-flex align-center"></div>
              <v-icon color="grey-lighten-1" size="small">mdi-chevron-left</v-icon>
            </div>
          </div>
        </div>
      </v-list-item>
    </v-card>

    <div v-if="filteredGroups.length === 0" class="text-center pa-4 text-grey">لا توجد مصادر</div>
  </v-list>
  <!-- </v-navigation-drawer> -->
</template>

<style scoped>
.college-card {
  border: 1px solid #ececec !important;
  transition: all 0.3s ease;
  cursor: pointer;
}

.college-card:hover {
  border-color: #d1d1d1 !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
  transform: translateY(-2px);
}
</style>
