<script>
import ChatWindow from '@/components/ChatWindow.vue'
import authService from '@/services/authService'
import GroupSideBar from '@/components/GroupSideBar.vue'

export default {
  components: {
    ChatWindow,
    GroupSideBar,
  },
  props: { id: String },
  data() {
    return {
      token: authService.getToken(),
      connectionStatus: 'connecting',
      errorMessage: '',
      organizationName: 'Loading...',
      host: window.location.host,
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
          await this.fetchOrgInfo()
          this.chatKey++
        }
      },
    },
  },
  methods: {
    async fetchOrgInfo() {
      try {
        const response = await fetch(`/api/organizations/${this.id}`)
        if (response.ok) {
          const data = await response.json()
          this.organizationName = data.organization_name
        }
      } catch (error) {
        console.error('Failed to fetch organization:', error)
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
    <h1 start>{{ organizationName }} #</h1>
  </v-card>
  <v-layout>
    <GroupSideBar :org_id="id" @access-denied="onAccessDenied" />

    <v-main>
      <v-container class="full-page" fluid>
        <v-row class="top"></v-row>

        <v-row>
          <v-col cols="12">
            <!-- Added :key and :isOrg="true" -->
            <ChatWindow
              :key="chatKey"
              :id="id"
              :token="token"
              :isOrg="true"
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
