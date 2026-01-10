<script>
import chatService from '@/services/chatService' // Import the chat service

export default {
  props: { id: String, token: String },
  data() {
    return {
      messages: [],
      messageText: '',
      connectionStatus: 'connecting', // Connection status for UI display
      errorMessage: '',
      host: window.location.host,
    }
  },

  computed: {
    statusLabel() {
      const labels = {
        connected: 'متصل',
        connecting: 'جاري الاتصال...',
        disconnected: 'غير متصل',
        error: 'خطأ في الاتصال',
      }
      return labels[this.connectionStatus] || this.connectionStatus
    },
  },

  methods: {
    // Format timestamp into a readable time
    formatTime(ts) {
      return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },

    // Initialize the chat service
    initChat() {
      chatService.init({
        host: this.host,
        token: this.token,
        orgId: this.id,

        // Handle incoming messages
        onMessage: (event) => {
          if (event.type === 'history') {
            this.messages = event.data
            this.scrollToBottom()
          } else if (event.type === 'new_message') {
            this.messages.push(event.data)
            this.scrollToBottom()
          }
        },

        // Handle connection status updates
        onStatusUpdate: (status) => {
          this.connectionStatus = status
          this.$emit('status-update', status) // Notify parent component of the status
        },
      })
    },

    // Scroll to the bottom of the messages container
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messageBox
        if (container) container.scrollTop = container.scrollHeight
      })
    },

    // Send a message through the WebSocket
    sendMessage() {
      if (!this.messageText.trim()) return // Prevent empty messages
      chatService.sendMessage(this.messageText) // Use the service to send the message
      this.messageText = '' // Clear the input field
    },
  },

  // Cleanup the WebSocket when the component is destroyed
  beforeUnmount() {
    chatService.close() // Close the WebSocket connection
  },

  mounted() {
    this.initChat() // Initialize WebSocket chat on component mount
  },
}
</script>

<template>
  <v-card class="chat-window pa-3">
    <v-card-title>
      <v-icon color="primary">mdi-message</v-icon>
      <span class="ml-3">المحادثة العامة</span>
      <v-chip class="ml-auto" color="primary" label outlined>
        {{ statusLabel }}
      </v-chip>
    </v-card-title>

    <!-- Divider -->
    <v-divider></v-divider>

    <!-- Messages Container -->
    <div class="messages-container" ref="messageBox">
      <div v-for="(msg, index) in messages" :key="index" class="d-flex message-row pa-2">
        <v-avatar size="40" rounded="lg">
          <img
            :src="'https://ui-avatars.com/api/?name=' + (msg.user?.username || msg.username || 'U')"
            alt="avatar"
          />
        </v-avatar>

        <div class="message-body ml-3">
          <div class="d-flex align-center">
            <span class="font-weight-bold">{{
              msg.user?.username || msg.username || 'مستخدم'
            }}</span>
            <span class="ml-2 text-caption">{{ formatTime(msg.timestamp) }}</span>
          </div>
          <div>{{ msg.content }}</div>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <v-row class="mt-3">
      <v-col cols="10">
        <v-text-field
          v-model="messageText"
          placeholder="اكتب رسالتك"
          outlined
          dense
          :disabled="connectionStatus !== 'connected'"
          @keyup.enter="sendMessage"
        />
      </v-col>
      <v-col cols="2">
        <v-btn
          color="primary"
          icon
          :disabled="connectionStatus !== 'connected'"
          @click="sendMessage"
        >
          <v-icon>mdi-send</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>

<style scoped>
.messages-container {
  height: 400px;
  overflow-y: auto;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #dadada;
  padding: 8px;
}
.message-row {
  display: flex;
}
</style>
