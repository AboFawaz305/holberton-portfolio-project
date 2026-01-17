<script>
import ChatWindow from '@/components/ChatWindow.vue' // The child component for chat functionality
import JoinGroupButton from '@/components/JoinGroupButton.vue' // The child component for chat functionality
import authService from '@/services/authService'
import GroupSideBar from '@/components/GroupSideBar.vue'

export default {
  components: {
    GroupSideBar,
    ChatWindow, // Make sure the component is registered
    JoinGroupButton,
  },
  props: { id: String },
  data() {
    return {
      token: authService.getToken(),
      connectionStatus: 'connecting',
      errorMessage: '',
      organizationName: 'Loading...',
      host: window.location.host,
      isOrg: true,
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
  <div class="main-dashboard-wrapper">
    <v-card
      flat
      class="px-8 py-10 gradient-bg d-flex align-center justify-space-between header-section"
      rounded="0"
    >
      <div class="d-flex flex-column align-start" style="min-width: 320px">
        <v-btn
          icon
          variant="text"
          color="white"
          @click="$router.push('/organizations')"
          class="mb-2 me-n2"
        >
          <v-icon size="36">mdi-arrow-right</v-icon>
        </v-btn>
        <h1 class="text-h3 font-weight-bold text-white">
          <span class="opacity-50 text-h4 ms-2">#</span>{{ organizationName }}
        </h1>
      </div>

      <div class="d-flex flex-column align-center flex-grow-1">
        <v-icon color="white" size="70" class="opacity-70 mb-4">mdi-school-outline</v-icon>
        <JoinGroupButton :isOrg="isOrg" :id="id" />
      </div>

      <div style="min-width: 320px"></div>
    </v-card>

    <v-layout class="flex-grow-1 page-background overflow-hidden" style="min-height: 0">
      <v-navigation-drawer
        width="400"
        permanent
        elevation="0"
        class="sidebar-border"
        color="#f8fafd"
      >
        <div class="pa-0 h-100 overflow-y-auto">
          <GroupSideBar class="pa-2" :org_id="id" @access-denied="onAccessDenied" />
        </div>
      </v-navigation-drawer>

      <v-main class="flex-grow-1 d-flex flex-column overflow-hidden" style="min-height: 0">
        <v-container fluid class="pa-6 pb-12 d-flex flex-column flex-grow-1" style="min-height: 0">
          <div
            class="chat-outer-box bg-white rounded-xl layered-shadow overflow-hidden flex-grow-1 d-flex flex-column"
          >
            <ChatWindow
              class="h-100"
              :key="chatKey"
              :id="id"
              :token="token"
              :isOrg="true"
              @status-update="updateConnectionStatus"
            />
          </div>
        </v-container>
      </v-main>
    </v-layout>
  </div>

  <v-snackbar v-model="snackbar" color="error" timeout="4000" rounded="pill">
    <v-icon start>mdi-alert-circle-outline</v-icon>
    {{ snackbarMessage }}
  </v-snackbar>
</template>

<style scoped>
.main-dashboard-wrapper {
  /* Set total height to what's left under your top navbar */
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header-section {
  /* Use flex-basis to lock the header height */
  flex: 0 0 250px;
  z-index: 10;
}

.page-background {
  background-color: #f4f7fa;
}

.sidebar-border {
  border-inline-end: 1px solid #edf2f7 !important;
}

.layered-shadow {
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
}

.opacity-50 {
  opacity: 0.5;
}
.opacity-70 {
  opacity: 0.7;
}
</style>
