<script>
import ChatWindow from '@/components/ChatWindow.vue'
import authService from '@/services/authService'
import SubGroupSideBar from '@/components/SubGroupSideBar.vue'
import ResourcesPanel from '@/components/ResourcesPanel.vue'

export default {
  components: {
    ChatWindow,
    SubGroupSideBar,
    ResourcesPanel,
  },
  props: { id: String },
  data() {
    return {
      token: authService.getToken(),
      connectionStatus: 'connecting',
      errorMessage: '',
      groupName: 'Loading...',
      orgId: null,
      chatKey: 0,
      tab: 'subgroups',
    }
  },
  watch: {
    id: {
      immediate: true,
      async handler(newId) {
        if (newId) {
          await this.fetchGroupInfo()
          this.chatKey++
        }
      },
    },
  },
  methods: {
    async fetchGroupInfo() {
      try {
        const response = await fetch(`/api/groups/${this.id}`)
        if (response.ok) {
          const data = await response.json()
          this.groupName = data.title
          this.orgId = data.org_id
        }
      } catch (error) {
        console.error('Failed to fetch group:', error)
      }
    },
    updateConnectionStatus(status) {
      this.connectionStatus = status
    },
  },
}
</script>

<template>
  <v-card flat class="pa-12 text-center gradient-bg">
    <h1>{{ groupName }} #</h1>
  </v-card>

  <v-layout>
    <!-- Sidebar -->
    <v-navigation-drawer width="360" permanent>
      <v-tabs v-model="tab" grow>
        <v-tab value="subgroups">القروبات</v-tab>
        <v-tab value="resources">المصادر</v-tab>
      </v-tabs>

      <v-window v-model="tab" class="mt-4">
        <v-window-item class="pa-4" value="subgroups">
          <SubGroupSideBar :group_id="id" :org_id="orgId" />
        </v-window-item>

        <v-window-item class="pa-4" value="resources">
          <ResourcesPanel :group_id="id" />
        </v-window-item>
      </v-window>
    </v-navigation-drawer>

    <!-- Main content -->
    <v-main>
      <v-container class="full-page" fluid>
        <v-row>
          <v-col cols="12">
            <ChatWindow
              :key="chatKey"
              :id="id"
              :token="token"
              :isOrg="false"
              @status-update="updateConnectionStatus"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-layout>
</template>

<style scoped>
.full-page {
  height: 100vh;
}
</style>
