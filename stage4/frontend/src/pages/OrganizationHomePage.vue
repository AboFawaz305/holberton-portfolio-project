<script>
import ChatWindow from '@/components/ChatWindow.vue'
import JoinGroupButton from '@/components/JoinGroupButton.vue'
import authService from '@/services/authService'
import GroupSideBar from '@/components/GroupSideBar.vue'

export default {
  components: {
    GroupSideBar,
    ChatWindow,
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
      <div class="d-flex flex-column align-start header-details" style="min-width: 320px">
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

      <div class="d-flex flex-column align-center flex-grow-1 header-action">
        <v-icon color="white" size="70" class="opacity-90 mb-4">mdi-school-outline</v-icon>
        <JoinGroupButton :isOrg="isOrg" :id="id" />
      </div>

      <div class="header-spacer" style="min-width: 320px"></div>
    </v-card>

    <v-layout class="flex-grow-1 page-background overflow-hidden" style="min-height: 0">
      <v-navigation-drawer
        width="400"
        permanent
        elevation="0"
        class="sidebar-border"
        color="#f8fafd"
      >
        <div class="pa-6 h-100 overflow-y-auto sidebar-scroll-container">
          <GroupSideBar :org_id="id" @access-denied="onAccessDenied" />
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
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header-section {
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

.opacity-90 {
  opacity: 0.9;
}

.sidebar-scroll-container {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
  transition: scrollbar-color 0.3s ease;
}

.sidebar-scroll-container::-webkit-scrollbar {
  width: 6px;
}

.sidebar-scroll-container::-webkit-scrollbar-thumb {
  background-color: transparent;
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.sidebar-scroll-container:hover::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
}

.sidebar-scroll-container:hover {
  scrollbar-color: #cbd5e1 transparent;
}

@media (max-width: 959px) {
  .main-dashboard-wrapper {
    height: auto;
    min-height: calc(100svh - 72px);
    overflow: visible;
  }

  .header-section {
    flex: 0 0 auto;
    flex-direction: column !important;
    min-height: 280px;
    gap: 16px;
    padding: 24px 16px !important;
  }

  .header-details {
    width: 100%;
    min-width: 0 !important;
    align-items: center !important;
    text-align: center;
  }

  .header-details h1 {
    max-width: 100%;
    overflow-wrap: anywhere;
    font-size: 2rem !important;
    line-height: 1.3;
  }

  .header-action {
    width: 100%;
  }

  .header-action > .v-icon {
    font-size: 56px !important;
  }

  .header-spacer {
    display: none;
  }

  .page-background {
    flex-direction: column;
    overflow: visible !important;
  }

  .sidebar-border {
    position: relative !important;
    top: auto !important;
    right: auto !important;
    bottom: auto !important;
    left: auto !important;
    width: 100% !important;
    height: 320px !important;
    flex: 0 0 320px;
    transform: none !important;
    border-inline-end: 0 !important;
    border-bottom: 1px solid #edf2f7 !important;
  }

  .page-background :deep(.v-main) {
    width: 100%;
    padding: 0 !important;
  }

  .page-background :deep(.v-navigation-drawer__content) {
    height: 100%;
    overflow-y: auto;
  }

  .page-background :deep(.v-main > .v-container) {
    min-height: 560px !important;
    padding: 12px !important;
  }

  .chat-outer-box {
    min-height: 536px;
  }
}
</style>
