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
  <div class="d-flex align-center justify-space-between mb-4">
    <h2 class="text-h6 font-weight-bold" style="color: #333">المجموعات</h2>

    <v-btn
      v-if="current_group_data?.admin === currentUserId"
      icon="mdi-cog"
      variant="tonal"
      size="small"
      color="primary"
      @click="openCurrentGroupSettings"
      title="إعدادات المجموعة الحالية"
    ></v-btn>
  </div>

  <!-- Navigation buttons -->
  <div class="d-flex mb-4 gap-2">
    <v-btn size="small" variant="outlined" @click="handleBack" prepend-icon="mdi-arrow-right">
      رجوع
    </v-btn>
    <v-btn size="small" variant="text" @click="goToOrg" prepend-icon="mdi-domain"> المنظمة </v-btn>
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
              <v-icon color="indigo-darken-2" size="28">mdi-forum</v-icon>
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
            <div class="d-flex align-center">
              <v-btn
                v-if="group.admin === currentUserId"
                icon="mdi-shield-edit-outline"
                variant="plain"
                color="primary"
                size="x-small"
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

    <CreateGroupButton
      :org-id="org_id"
      :parent-group-id="group_id"
      button-label="إضافة مجموعة فرعية"
      @created="fetchSubGroups"
    />

    <div v-if="filteredGroups.length === 0 && !loading" class="text-center pa-4 text-grey">
      <v-icon size="40" class="mb-2">mdi-folder-open-outline</v-icon>
      <p>لا توجد مجموعات متاحة</p>
    </div>
  </v-list>

  <GroupManageDialog
    v-model="dialog.open"
    :group-id="dialog.groupId"
    :org-id="org_id"
    :initial-domains="dialog.domains"
    @saved="onSaved"
  />
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
