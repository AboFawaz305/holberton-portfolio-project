<script>
import groupsService from '@/services/groupsService'
import CreateGroupButton from '@/components/CreateGroupButton.vue'
import authService from '@/services/authService'
import ManageDomainsDialog from '@/components/GroupManageDialog.vue'


export default {
  name: 'GroupSideBar',
  components: { 
    ManageDomainsDialog ,
    CreateGroupButton ,
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
  async created() {
    try {
      this.currentUser = await authService.getCurrentUser()
    } catch (error) {
      console.error('Could not fetch user info:', error)
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
  <h2 class="text-h6 mb-4 text-right font-weight-bold" style="color: #333">الكليات</h2>

  <CreateGroupButton :org-id="org_id" class="mb-4" @created="fetchGroups" />
  <v-text-field
    v-model="searchQuery"
    variant="outlined"
    placeholder="ابحث عن كلية..."
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
                icon="mdi-shield-edit-outline"
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
            <div class="d-flex align-center"></div>
            <v-icon color="grey-lighten-1" size="small">mdi-chevron-left</v-icon>
          </div>
        </div>
      </v-list-item>
    </v-card>

    <div v-if="filteredGroups.length === 0" class="text-center pa-4 text-grey">
      لا توجد مجموعات متاحة
    </div>
  </v-list>

  <ManageDomainsDialog
    v-model="domainDialog.open"
    :group-id="domainDialog.groupId"
    :org-id="org_id"
    :initial-domains="domainDialog.domains"
    @saved="onDomainsSaved"
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
</style>
