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
      organizationName: window.history.state?.name || 'Loading...',
      host: window.location.host,
    }
  },
  methods: {
    updateConnectionStatus(status) {
      this.connectionStatus = status
    },
  },
}
</script>

<template>
  <v-card flat class="pa-12 text-center gradient-bg">
    <h1 start>{{ organizationName }} #</h1>
  </v-card>
  <v-layout>
    <GroupSideBar :org_id="id" />

    <v-main>
      <v-container class="full-page" fluid>
        <v-row class="top"> </v-row>

        <v-row>
          <v-col cols="12">
            <ChatWindow :id="id" :token="token" @status-update="updateConnectionStatus" />
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
