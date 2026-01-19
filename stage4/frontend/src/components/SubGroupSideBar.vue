<script>
import groupsService from '@/services/groupsService'
import authService from '@/services/authService'
import GroupManageDialog from '@/components/GroupManageDialog.vue'
import CreateGroupButton from '@/components/CreateGroupButton.vue'

export default {
  name: 'SubGroupSideBar',
  components: {
    GroupManageDialog,
    CreateGroupButton,
  },
  props: {
    group_id: String,
    org_id: String,
    parent_group_id: String,
    current_group_data: Object,
  },
  emits: ['access-denied', 'refresh-parent'],
  data() {
    return {
      searchQuery: '',
      subGroups: [],
      loading: false,
      currentUser: null,
      dialog: {
        open: false,
        groupId: null,
        domains: [],
      },
    }
  },
  computed: {
    filteredGroups() {
      if (!this.searchQuery) return this.subGroups
      const query = this.searchQuery.toLowerCase()
      return this.subGroups.filter((group) => group.title.toLowerCase().includes(query))
    },
    currentUserId() {
      return this.currentUser ? String(this.currentUser.user_id) : null
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
  async created() {
    try {
      this.currentUser = await authService.getCurrentUser()
    } catch (error) {
      console.error('Auth error:', error)
    }
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
    openSubGroupSettings(subgroup) {
      this.dialog.groupId = subgroup.group_id
      this.dialog.domains = subgroup.AllowedEmailDomains || []
      this.dialog.open = true
    },
    openCurrentGroupSettings() {
      if (!this.current_group_data) return
      this.dialog.groupId = this.current_group_data.group_id
      this.dialog.domains = this.current_group_data.AllowedEmailDomains || []
      this.dialog.open = true
    },
    onSaved() {
      this.fetchSubGroups()
      this.$emit('refresh-parent')
    },
    async onGroupClick(event, subGroupId) {
      event.preventDefault()
      try {
        await groupsService.getGroupById(subGroupId)
        this.$router.push(`/groups/${subGroupId}`)
      } catch (error) {
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
  <div class="sidebar-main-wrapper">
    <div class="d-flex align-center justify-space-between mb-4">
      <h2 class="text-h6 font-weight-bold" style="color: #333">المجموعات</h2>

      <v-btn
        v-if="current_group_data?.admin === currentUserId"
        icon="mdi-cog"
        variant="tonal"
        size="small"
        color="primary"
        class="rounded-lg"
        @click="openCurrentGroupSettings"
        title="إعدادات المجموعة الحالية"
      ></v-btn>
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

    <div v-if="loading" class="list-wrapper pt-4">
      <v-card
        v-for="n in 3"
        :key="'shimmer-' + n"
        variant="flat"
        class="mb-4 college-shimmer-card"
        rounded="xl"
      >
        <v-list-item class="pa-4">
          <div class="d-flex align-center w-100 mb-4">
            <v-skeleton-loader type="avatar" size="48" class="ms-3"></v-skeleton-loader>
            <div class="flex-grow-1">
              <v-skeleton-loader type="text" width="60%" class="mx-auto"></v-skeleton-loader>
            </div>
            <v-skeleton-loader type="text" width="40px"></v-skeleton-loader>
          </div>
          <v-divider class="mb-3"></v-divider>
          <v-skeleton-loader type="text" width="30%"></v-skeleton-loader>
        </v-list-item>
      </v-card>
    </div>

    <v-list v-else bg-color="transparent" class="pa-0 list-wrapper pt-4">
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
                <v-icon color="indigo-darken-2" size="28">mdi-forum</v-icon>
              </v-avatar>

              <div class="flex-grow-1 text-center">
                <span class="text-subtitle-1 font-weight-bold">
                  {{ group.title }}
                </span>
              </div>

              <span class="text-body-2 text-grey-darken-1"> {{ group.members_count }} عضو </span>
            </div>

            <v-divider class="mb-3 opacity-20"></v-divider>

            <div class="d-flex justify-space-between align-center">
              <div class="d-flex align-center">
                <v-btn
                  v-if="group.admin === currentUserId"
                  icon="mdi-cog-outline"
                  variant="tonal"
                  color="primary"
                  size="x-small"
                  class="rounded-lg"
                  @click.stop="openSubGroupSettings(group)"
                ></v-btn>

                <v-icon
                  v-if="group.AllowedEmailDomains?.length"
                  color="orange-darken-2"
                  size="small"
                  class="ms-2"
                  >mdi-lock-outline</v-icon
                >
              </div>
              <v-icon color="grey-lighten-1" size="small">mdi-chevron-left</v-icon>
            </div>
          </div>
        </v-list-item>
      </v-card>

      <div class="mt-2">
        <CreateGroupButton
          :org-id="org_id"
          :parent-group-id="group_id"
          button-label="إضافة مجموعة "
          @created="fetchSubGroups"
        />
      </div>

      <div
        v-if="filteredGroups.length === 0 && !loading"
        class="text-center pa-8 text-grey-lighten-1"
      >
        <v-icon size="48" class="mb-2">mdi-folder-open-outline</v-icon>
        <p>لا توجد مجموعات متاحة</p>
      </div>
    </v-list>
  </div>

  <GroupManageDialog
    v-model="dialog.open"
    :group-id="dialog.groupId"
    :org-id="org_id"
    :initial-domains="dialog.domains"
    @saved="onSaved"
  />
</template>

<style scoped>
.sidebar-main-wrapper {
  padding-left: 8px;
  padding-right: 16px;
}

.list-wrapper {
  padding-top: 12px;
}

.college-card {
  border: 1px solid #ececec !important;
  transition:
    transform 0.25s cubic-bezier(0.4, 0, 0.2, 1),
    box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1),
    border-color 0.2s ease;
  cursor: pointer;
  position: relative;
  z-index: 1;
}

.college-card:hover {
  border-color: #d1d1d1 !important;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08) !important;
  transform: translateY(-6px);
  z-index: 2;
}

.college-shimmer-card {
  border: 1px solid #f5f5f5 !important;
  background-color: white !important;
}

.opacity-20 {
  opacity: 0.2;
}

:deep(.v-skeleton-loader) {
  background: transparent !important;
}
</style>
