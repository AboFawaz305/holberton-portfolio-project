<script>
import groupsService from '@/services/groupsService'

export default {
  name: 'SubGroupSideBar',
  props: {
    group_id: String,
    org_id: String,
    parent_group_id: String,
  },
  emits: ['access-denied'],
  data() {
    return {
      searchQuery: '',
      subGroups: [],
      loading: false,
    }
  },
  computed: {
    filteredGroups() {
      if (!this.searchQuery) return this.subGroups
      const query = this.searchQuery.toLowerCase()
      return this.subGroups.filter((group) => group.title.toLowerCase().includes(query))
    },
  },
  watch: {
    group_id: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchSubGroups()
        }
      },
    },
  },
  methods: {
    async fetchSubGroups() {
      console.log('Fetching subgroups for Group ID:', this.group_id)
      this.loading = true
      try {
        this.subGroups = await groupsService.getSubgroups(this.group_id)
      } catch (error) {
        console.error('Fetch error:', error)
      } finally {
        this.loading = false
      }
    },
    async onGroupClick(event, subGroupId) {
      event.preventDefault()

      try {
        await groupsService.getGroupById(subGroupId)

        this.$router.push(`/groups/${subGroupId}`)
      } catch (error) {
        console.error('Access check failed:', error.message)
        this.$emit('access-denied', error.message)
      }
    },
    handleBack() {
      if (this.parent_group_id) {
        // If we are in a subgroup, go to the Parent Group
        this.$router.push(`/groups/${this.parent_group_id}`)
      } else if (this.org_id) {
        // If we are in a Main Group (no parent), go to the Organization Home
        this.$router.push(`/organizations/${this.org_id}`)
      } else {
        // Fallback if everything fails
        this.$router.back()
      }
    },
    goToOrg() {
      if (this.org_id) {
        this.$router.push(`/organizations/${this.org_id}`)
      }
    },
  },
}
</script>

<template>
    <h2 class="text-h6 mb-4 text-right font-weight-bold" style="color: #333">المجموعات</h2>

    <!-- Navigation buttons -->
    <div class="d-flex mb-4 gap-2">
      <v-btn size="small" variant="outlined" @click="handleBack" prepend-icon="mdi-arrow-right">
        رجوع
      </v-btn>
      <v-btn size="small" variant="text" @click="goToOrg" prepend-icon="mdi-domain">
        المنظمة
      </v-btn>
    </div>

    <v-text-field
      v-model="searchQuery"
      variant="outlined"
      placeholder="ابحث عن مجموعة..."
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
        v-for="group in filteredGroups"
        :key="group.group_id"
        variant="flat"
        class="mb-4 college-card"
        rounded="xl"
        @click.stop.prevent="onGroupClick($event, group.group_id)"
      >
        <v-list-item class="pa-4">
          <div class="d-flex flex-column w-100">
            <div class="d-flex align-center w-100 mb-4">
              <v-avatar color="indigo-lighten-5" size="48" rounded="lg" class="elevation-1 ms-3">
                <v-icon color="indigo-darken-2" size="28">mdi-folder-outline</v-icon>
              </v-avatar>

              <div class="flex-grow-1 text-center">
                <span class="text-subtitle-1 font-weight-bold">
                  {{ group.title }}
                </span>
              </div>

              <span class="text-body-2 text-grey-darken-1"> {{ group.members_count }} عضو </span>
            </div>

            <v-divider class="mb-3"></v-divider>

            <div class="d-flex justify-space-between align-center">
              <div class="d-flex align-center"></div>
              <v-icon color="grey-lighten-1" size="small">mdi-chevron-left</v-icon>
            </div>
          </div>
        </v-list-item>
      </v-card>

      <div v-if="filteredGroups.length === 0" class="text-center pa-4 text-grey">
        لا توجد مجموعات فرعية
      </div>
    </v-list>
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

.gap-2 {
  gap: 8px;
}
</style>
