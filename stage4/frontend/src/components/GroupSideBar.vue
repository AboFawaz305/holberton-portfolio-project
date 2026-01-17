<script>
import groupsService from '@/services/groupsService'
import CreateGroupButton from '@/components/CreateGroupButton.vue'
import authService from '@/services/authService'
import ManageDomainsDialog from '@/components/GroupManageDialog.vue'

export default {
  name: 'GroupSideBar',
  components: {
    ManageDomainsDialog,
    CreateGroupButton,
  },
  props: { org_id: String },
  emits: ['access-denied'],
  data() {
    return {
      searchQuery: '',
      groups: [],
      loading: false,
      currentUser: null,
      domainDialog: {
        open: false,
        groupId: null,
        domains: [],
      },
    }
  },
  computed: {
    filteredGroups() {
      if (!this.searchQuery) return this.groups
      const query = this.searchQuery.toLowerCase()
      return this.groups.filter((group) => group.title.toLowerCase().includes(query))
    },
    currentUserId() {
      return this.currentUser ? String(this.currentUser.user_id) : null
    },
  },
  watch: {
    org_id: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.fetchGroups()
        }
      },
    },
  },
  async created() {
    try {
      this.currentUser = await authService.getCurrentUser()
    } catch (error) {
      console.error('Could not fetch user info:', error)
    }
  },
  methods: {
    async fetchGroups() {
      console.log('Fetching for Org ID:', this.org_id)
      this.loading = true
      try {
        this.groups = await groupsService.getGroupsByOrg(this.org_id)
      } catch (error) {
        console.error('Fetch error:', error)
      } finally {
        this.loading = false
      }
    },
    openSettings(group) {
      this.domainDialog.groupId = group.group_id
      this.domainDialog.domains = group.AllowedEmailDomains || []
      this.domainDialog.open = true
    },
    onDomainsSaved() {
      this.fetchGroups()
    },
    async onGroupClick(event, groupId) {
      event.preventDefault() // Stop navigation

      try {
        await groupsService.getGroupById(groupId)

        this.$router.push(`/groups/${groupId}`)
      } catch (error) {
        this.$emit('access-denied', error.message)
      }
    },
  },
}
</script>

<template>
  <div class="sidebar-main-wrapper">
    <h2 class="text-h6 mb-4 text-right font-weight-bold" style="color: #333">الاقسام</h2>

    <v-text-field
      v-model="searchQuery"
      variant="outlined"
      placeholder="ابحث عن قسم..."
      prepend-inner-icon="mdi-magnify"
      rounded="lg"
      bg-color="white"
      density="compact"
      class="mb-4"
      hide-details
      clearable
    ></v-text-field>

    <div v-if="loading" class="shimmer-container pt-4">
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

    <div v-else class="groups-list-wrapper pt-4">
      <v-list bg-color="transparent" class="pa-0 overflow-visible">
        <v-card
          v-for="group in filteredGroups"
          :key="group.group_id"
          variant="flat"
          class="mb-4 college-card"
          rounded="xl"
          @click="onGroupClick($event, group.group_id)"
        >
          <v-list-item class="pa-4">
            <div class="d-flex flex-column w-100">
              <div class="d-flex align-center w-100 mb-4">
                <v-avatar color="indigo-lighten-5" size="48" rounded="lg" class="elevation-1 ms-3">
                  <v-icon color="indigo-darken-2" size="28">mdi-town-hall</v-icon>
                </v-avatar>

                <div class="flex-grow-1 text-center">
                  <span class="text-subtitle-1 font-weight-bold">
                    {{ group.title }}
                  </span>
                </div>

                <span class="text-body-2 text-grey-darken-1"> {{ group.members_count }} طالب </span>
              </div>

              <v-divider class="mb-3"></v-divider>

              <div class="d-flex justify-space-between align-center">
                <div class="d-flex align-center">
                  <v-btn
                    v-if="group.admin === currentUserId"
                    icon="mdi-cog"
                    variant="tonal"
                    color="primary"
                    size="x-small"
                    @click.stop="openSettings(group)"
                  ></v-btn>

                  <v-icon
                    v-if="group.AllowedEmailDomains?.length"
                    color="orange-darken-2"
                    size="small"
                    class="ms-2"
                    title="دخول مقيد"
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
            button-label="إضافة قسم جديد"
            @created="fetchGroups"
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
  </div>

  <ManageDomainsDialog
    v-model="domainDialog.open"
    :group-id="domainDialog.groupId"
    :org-id="org_id"
    :initial-domains="domainDialog.domains"
    @saved="onDomainsSaved"
  />
</template>

<style scoped>
.sidebar-main-wrapper {
  padding: 0 8px;
}

.groups-list-wrapper {
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

/* Shimmer Styles */
:deep(.v-skeleton-loader) {
  background: transparent !important;
}
</style>
