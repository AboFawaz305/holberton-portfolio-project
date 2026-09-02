<script>
import ChatWindow from '@/components/ChatWindow.vue'
import JoinGroupButton from '@/components/JoinGroupButton.vue'
import authService from '@/services/authService'
import SubGroupSideBar from '@/components/SubGroupSideBar.vue'
import ResourcesPanel from '@/components/ResourcesPanel.vue'
import groupsService from '@/services/groupsService'

export default {
  components: {
    ChatWindow,
    SubGroupSideBar,
    ResourcesPanel,
    JoinGroupButton,
  },
  props: { id: String },
  data() {
    return {
      token: authService.getToken(),
      connectionStatus: 'connecting',
      errorMessage: '',
      groupData: null,
      groupName: '',
      orgId: null,
      tab: 'subgroups',
      parentGroupId: null,
      chatKey: 0,
      snackbar: false,
      snackbarMessage: '',
      breadcrumbChain: [],
      loading: true,
    }
  },
  computed: {
    breadcrumbItems() {
      const items = []

      // 1. Root is the specific Organization Name
      if (this.orgId) {
        items.push({
          title: this.orgName,
          disabled: false,
          to: `/organizations/${this.orgId}`,
        })
      }

      // 2. Add each group in the hierarchy path
      this.breadcrumbChain.forEach((group, index) => {
        const isLast = index === this.breadcrumbChain.length - 1
        items.push({
          title: group.title,
          disabled: isLast,
          to: `/groups/${group.group_id}`,
        })
      })

      return items
    },
  },
  watch: {
    id: {
      immediate: true,
      async handler(newId) {
        if (newId) {
          this.groupName = ''
          await this.fetchGroupInfo()
          this.chatKey++
        }
      },
    },
  },
  methods: {
    async fetchGroupInfo() {
      try {
        const [pathResponse, groupData] = await Promise.all([
          groupsService.getGroupPath(this.id),
          groupsService.getGroupById(this.id),
        ])

        this.orgName = pathResponse.org_name
        this.breadcrumbChain = pathResponse.path

        this.groupData = groupData
        this.groupName = groupData.title
        this.orgId = groupData.org_id
        this.parentGroupId = groupData.parentGroupId
      } catch (error) {
        console.error('Failed to fetch group:', error.message)
        this.groupName = 'Error loading group'

        this.onAccessDenied(error.message)
      } finally {
        this.loading = false
      }
    },
    handleBack() {
      if (this.parentGroupId) {
        this.$router.push(`/groups/${this.parentGroupId}`)
      } else if (this.orgId) {
        this.$router.push(`/organizations/${this.orgId}`)
      } else {
        this.$router.back()
      }
    },
    updateConnectionStatus(status) {
      this.connectionStatus = status
    },
    onJoined() {
      this.chatKey++
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
        <template v-if="loading">
          <v-skeleton-loader
            type="text"
            width="180"
            bg-color="transparent"
            class="mb-2 opacity-50"
          ></v-skeleton-loader>
          <v-skeleton-loader type="heading" width="250" bg-color="transparent"></v-skeleton-loader>
        </template>

        <template v-else>
          <v-btn icon variant="text" color="white" @click="handleBack" class="mb-2 me-n2">
            <v-icon size="36">mdi-arrow-right</v-icon>
          </v-btn>

          <v-breadcrumbs :items="breadcrumbItems" class="pa-0 mb-2 text-white opacity-70">
            <template v-slot:divider>
              <v-icon icon="mdi-chevron-left" size="small" color="white"></v-icon>
            </template>
          </v-breadcrumbs>

          <h1 class="text-h3 font-weight-bold text-white">
            <span dir="ltr" class="d-inline-flex align-center">
              {{ groupName }}

              <span class="opacity-50 text-h4 me-2">#</span>
            </span>
          </h1>
        </template>
      </div>

      <div class="d-flex flex-column align-center flex-grow-1 header-action">
        <template v-if="loading">
          <v-skeleton-loader
            type="avatar"
            size="70"
            bg-color="transparent"
            class="mb-4 opacity-30"
          ></v-skeleton-loader>
          <v-skeleton-loader type="button" width="120" bg-color="transparent"></v-skeleton-loader>
        </template>
        <template v-else>
          <v-icon color="white" size="70" class="opacity-70 mb-4">mdi-account-group-outline</v-icon>
          <JoinGroupButton :id="id" :isOrg="false" @joined="onJoined" />
        </template>
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
        style="direction: ltr"
      >
        <div class="d-flex flex-column h-100 overflow-hidden" style="direction: rtl; min-height: 0">
          <v-tabs
            v-model="tab"
            grow
            color="primary"
            class="flex-shrink-0 border-b"
            height="48"
            density="compact"
          >
            <v-tab value="subgroups">القروبات</v-tab>
            <v-tab value="resources">المصادر</v-tab>
          </v-tabs>

          <div class="flex-grow-1 overflow-hidden" style="min-height: 0; position: relative">
            <v-window
              v-model="tab"
              :touch="false"
              :transition="false"
              :reverse-transition="false"
              class="h-100 sidebar-scroll-container overflow-y-auto"
            >
              <v-window-item value="subgroups" class="h-100 pa-6" style="direction: rtl">
                <SubGroupSideBar
                  :group_id="id"
                  :org_id="orgId"
                  :parent_group_id="parentGroupId"
                  :current_group_data="groupData"
                  @access-denied="onAccessDenied"
                  @refresh-parent="fetchGroupInfo"
                />
              </v-window-item>

              <v-window-item value="resources" class="h-100 pa-6" style="direction: rtl">
                <ResourcesPanel :key="id" :group_id="id" />
              </v-window-item>
            </v-window>
          </div>
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
              :isOrg="false"
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

.chat-outer-box {
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
}

.sidebar-scroll-container::-webkit-scrollbar {
  width: 6px;
}
.sidebar-scroll-container::-webkit-scrollbar-thumb {
  background-color: transparent;
  border-radius: 10px;
}
.sidebar-scroll-container:hover::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
}

:deep(.v-skeleton-loader) {
  background: transparent !important;
}

.v-window::-webkit-scrollbar {
  width: 6px;
}
.v-window::-webkit-scrollbar-thumb {
  background-color: transparent;
  border-radius: 10px;
}
.v-window:hover::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
}

:deep(.v-slide-group__container) {
  height: 48px !important;
  min-height: 48px !important;
}

:deep(.v-slide-group__wrapper) {
  height: 48px !important;
}

.v-tabs {
  max-height: 48px !important;
  flex: 0 0 48px !important;
  border-bottom: 1px solid #edf2f7 !important;
}

:deep(.v-window__container) {
  height: 100% !important;
  min-height: 0 !important;
}

.v-window {
  margin: 0 !important;
  padding: 0 !important;
}

.opacity-30 {
  opacity: 0.3;
}
.opacity-50 {
  opacity: 0.5;
}
.opacity-70 {
  opacity: 0.7;
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
    min-height: 320px;
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

  .header-details :deep(.v-breadcrumbs) {
    width: 100%;
    overflow-x: auto;
  }

  .header-details :deep(.v-breadcrumbs__item) {
    white-space: nowrap;
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
    height: 360px !important;
    flex: 0 0 360px;
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

  :deep(.v-window-item) {
    padding: 16px !important;
  }
}
</style>
