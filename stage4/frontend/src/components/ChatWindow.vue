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
      snackbar: false,
      msg: '',
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
    showMessage(text) {
      this.msg = text
      this.snackbar = true
    },

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
          } else if (event.data && event.data.error === 'MESSAGE_IS_SPAM') {
            this.showMessage('لم يتم الإرسال بنجاح الرسالة مزعجة')
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
  <v-card class="chat-window-card d-flex flex-column h-100 pa-0" flat>
    <v-card-title class="flex-shrink-0 px-4 py-3">
      <v-icon color="primary" start>mdi-message</v-icon>
      <span class="ml-3 font-weight-bold">المحادثة العامة</span>
      <v-chip class="ml-auto" color="primary" label size="small" variant="tonal">
        {{ statusLabel }}
      </v-chip>
    </v-card-title>

    <v-divider></v-divider>

    <div class="messages-container flex-grow-1" ref="messageBox">
      <div v-for="(msg, index) in messages" :key="index" class="d-flex message-row pa-2">
        <v-avatar size="42" rounded="lg" class="me-3">
          <img
            :src="'https://ui-avatars.com/api/?name=' + (msg.user?.username || msg.username || 'U')"
            alt="avatar"
          />
        </v-avatar>

        <div class="message-body">
          <div class="d-flex align-center mb-1">
            <span class="font-weight-bold text-subtitle-2">{{
              msg.user?.username || msg.username || 'مستخدم'
            }}</span>
            <span class="ms-2 text-caption opacity-60">{{ formatTime(msg.timestamp) }}</span>
          </div>
          <div class="text-body-2">{{ msg.content }}</div>
        </div>
      </div>
    </div>

    <v-divider></v-divider>
    <div class="chat-footer pa-4 flex-shrink-0 bg-white">
      <v-row no-gutters align="center">
        <v-col class="flex-grow-1">
          <v-text-field
            v-model="messageText"
            placeholder="اكتب رسالتك..."
            variant="solo-filled"
            flat
            hide-details
            density="compact"
            rounded="pill"
            :disabled="connectionStatus !== 'connected'"
            @keyup.enter="sendMessage"
          />
        </v-col>
        <v-col cols="auto" class="ps-2">
          <v-btn
            color="primary"
            icon="mdi-send"
            variant="text"
            :disabled="connectionStatus !== 'connected'"
            @click="sendMessage"
          />
        </v-col>
      </v-row>
    </div>

    <v-snackbar v-model="snackbar" timeout="5000" closable>
      {{ msg }}
      <template v-slot:actions>
        <v-btn color="pink" variant="text" @click="snackbar = false">إغلاق</v-btn>
      </template>
    </v-snackbar>
  </v-card>
</template>

<style scoped>
.chat-window-card {
  height: 100% !important;
  max-height: 100% !important;
  overflow: hidden;
}

.messages-container {
  /* REMOVED: height: 400px */
  overflow-y: auto;
  background-color: #fcfcfc;
  padding: 16px;
  /* flex-grow handles the height filling */
  min-height: 0;
}

.message-row {
  margin-bottom: 8px;
}

.message-body {
  background: white;
  padding: 8px 14px;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  max-width: 85%;
}

/* Custom scrollbar for a cleaner look */
.messages-container::-webkit-scrollbar {
  width: 5px;
}
.messages-container::-webkit-scrollbar-thumb {
  background: #eee;
  border-radius: 10px;
}
</style>
