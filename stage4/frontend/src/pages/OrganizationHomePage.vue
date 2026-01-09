<script>
import ChatWindow from '@/components/ChatWindow.vue' // The child component for chat functionality
import authService from '@/services/authService'

export default {
  components: {
    ChatWindow, // Make sure the component is registered
  },
  props: { id: String },
  data() {
    return {
      token: authService.getToken(), // Retrieve token using authService
      connectionStatus: 'connecting', // WebSocket connection status
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
  <v-container class="full-page">
    <v-row class="top">
      <v-col cols="12" class="text-center">
        <v-btn icon color="primary">
          <v-icon>mdi-university</v-icon>
        </v-btn>
        <h1>{{ organizationName }} #</h1>
      </v-col>
    </v-row>

    <!-- Chat Window -->
    <v-row>
      <v-col cols="12">
        <ChatWindow :id="id" :token="token" @status-update="updateConnectionStatus" />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.full-page {
  height: 100vh;
}
</style>
