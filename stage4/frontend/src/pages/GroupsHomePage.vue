<script>
import ChatWindow from '@/components/ChatWindow.vue'
import authService from '@/services/authService'
import SubGroupSideBar from '@/components/SubGroupSideBar.vue'
import ResourcesPanel from '@/components/ResourcesPanel.vue'
import groupsService from '@/services/groupsService'

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
      tab: 'subgroups',
      parentGroupId: null,
      chatKey: 0,
      snackbar: false,
      snackbarMessage: '',
    }
  },
  watch: {
    id: {
      immediate: true,
      async handler(newId) {
        if (newId) {
          this.groupName = 'Loading...'
          await this.fetchGroupInfo()
          this.chatKey++
        }
      },
    },
  },
  methods: {
    async fetchGroupInfo() {
      try {
        const data = await groupsService.getGroupById(this.id)

        this.groupName = data.title
        this.orgId = data.org_id
        this.parentGroupId = data.parentGroupId
      } catch (error) {
        console.error('Failed to fetch group:', error.message)
        this.groupName = 'Error loading group'

        this.onAccessDenied(error.message)
      }
    },
    updateConnectionStatus(status) {
      this.connectionStatus = status
    },
    onAccessDenied(errorCode) {
      if (errorCode === 'EMAIL_NOT_VERIFIED') {
        this.snackbarMessage = 'يجب تأكيد بريدك الإلكتروني للوصول لهذه المجموعة'
      } else if (errorCode === 'EMAIL_DOMAIN_NOT_ALLOWED') {
        this.snackbarMessage = 'بريدك الإلكتروني غير مسموح له بالوصول لهذه المجموعة'
      } else {
        this.snackbarMessage = 'لا يمكنك الوصول لهذه المجموعة'
      }
      this.snackbar = true
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
          <SubGroupSideBar
      :group_id="id"
      :org_id="orgId"
      :parent_group_id="parentGroupId"
      @access-denied="onAccessDenied"
    />
        </v-window-item>

        <v-window-item class="pa-4" value="resources">
          <ResourcesPanel :group_id="id" />
        </v-window-item>
      </v-window>
    </v-navigation-drawer>

    <!-- Main content -->
    <v-main>
      <v-container class="full-page" fluid>
        <v-row class="top"></v-row>
        
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

  <v-snackbar v-model="snackbar" color="error" timeout="4000">
    {{ snackbarMessage }}
  </v-snackbar>
</template>

<style scoped>
.full-page {
  height: 100vh;
}
</style>
