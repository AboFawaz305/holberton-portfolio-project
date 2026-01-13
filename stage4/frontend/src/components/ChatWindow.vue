<script>
import chatService from '@/services/chatService'

export default {
  props: {
    id: String,
    token: String,
    isOrg: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      messages: [],
      messageText: '',
      connectionStatus: 'connecting',
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

  watch: {
    // Reinitialize chat when id or isOrg changes
    id: {
      handler() {
        this.reconnectChat()
      },
    },
    isOrg: {
      handler() {
        this.reconnectChat()
      },
    },
  },

  methods: {
    formatTime(ts) {
      const date = new Date(ts)
      return date.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
      })
    },

    reconnectChat() {
      // Close existing connection and reinitialize
      chatService.close()
      this.messages = []
      this.connectionStatus = 'connecting'
      this.initChat()
    },

    initChat() {
      if (!this.id || !this.token) {
        console.error('Missing id or token for chat')
        return
      }

      chatService.init({
        host: this.host,
        token: this.token,
        roomId: this.id,
        isOrg: this.isOrg,

        onMessage: (event) => {
          if (event.type === 'history') {
            this.messages = event.data
            this.scrollToBottom()
          } else if (event.type === 'new_message') {
            this.messages.push(event.data)
            this.scrollToBottom()
          }
        },

        onStatusUpdate: (status) => {
          this.connectionStatus = status
          this.$emit('status-update', status)
        },
      })
    },

    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messageBox
        if (container) container.scrollTop = container.scrollHeight
      })
    },

    sendMessage() {
      if (!this.messageText.trim()) return
      chatService.sendMessage(this.messageText)
      this.messageText = ''
    },
  },

  beforeUnmount() {
    chatService.close()
  },

  mounted() {
    this.initChat()
  },
}
</script>

<template>
  <v-card class="chat-window pa-3">
    <v-card-title>
      <v-icon color="primary" start>mdi-message</v-icon>
      <span class="ml-3">المحادثة العامة</span>
      <v-chip class="ml-auto" color="primary" label outlined>
        {{ statusLabel }}
      </v-chip>
    </v-card-title>

    <v-divider></v-divider>

    <div class="messages-container" ref="messageBox">
      <div v-for="(msg, index) in messages" :key="index" class="d-flex message-row pa-2">
        <v-avatar size="large" rounded="lg">
          <img
            :src="
              'https://ui-avatars.com/api/? name=' + (msg.user?.username || msg.username || 'U')
            "
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
