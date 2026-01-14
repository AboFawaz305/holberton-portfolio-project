<script>
import groupsService from '@components/services/groupsService'
export default {
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
  watch: {
    group_id: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          groupsService.getAllResources(this.group_id)
        }
      },
    },
  },
}
</script>

<template>
  <v-navigation-drawer
    width="350"
    permanent
    location="right"
    border="left"
    class="pa-4 bg-grey-lighten-5"
  >
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

    <div v-if="loading" class="text-center pa-10">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <v-list v-else bg-color="transparent" class="pa-0">
      <v-card
        v-for="resource in filteredGroups"
        :key="resource.group_id"
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
                <span class="text-subtitle-1 font-weight-bold">
                  {{ resource.name }}
                </span>
              </div>

              <a target="_blank" :href="resource.file_url">تحميل</a>
            </div>

            <v-divider class="mb-3"></v-divider>

            <div class="d-flex justify-space-between align-center">
              <div class="d-flex align-center"></div>
              <v-icon color="grey-lighten-1" size="small">mdi-chevron-left</v-icon>
            </div>
          </div>
        </v-list-item>
      </v-card>

      <div v-if="filteredGroups.length === 0" class="text-center pa-4 text-grey">لا توجد مصادر</div>
    </v-list>
  </v-navigation-drawer>
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
