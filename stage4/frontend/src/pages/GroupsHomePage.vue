<script>
import ChatWindow from '@/components/ChatWindow.vue'
import authService from '@/services/authService'
import SubGroupSideBar from '@/components/SubGroupSideBar.vue'

export default {
  components: {
    ChatWindow,
    SubGroupSideBar,
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
    <SubGroupSideBar :group_id="id" :org_id="orgId" />

    <v-main>
      <v-container class="full-page" fluid>
        <v-row class="top"></v-row>

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
