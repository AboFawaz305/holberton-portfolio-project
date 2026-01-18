<script>
import chatService from '@/services/chatService'
import EmojiPicker from 'vue3-emoji-picker'
import 'vue3-emoji-picker/css'

export default {
  components: { EmojiPicker },
  props: {
    id: String,
    token: String,
    isOrg: { type: Boolean, default: true },
  },
  data() {
    return {
      messages: [],
      loadingHistory: true,
      messageText: '',
      connectionStatus: 'connecting',
      colors: [
        '#1976D2',
        '#388E3C',
        '#D32F2F',
        '#7B1FA2',
        '#FFA000',
        '#00796B',
        '#C2185B',
        '#5D4037',
        '#455A64',
        '#0097A7',
        '#689F38',
        '#E64A19',
      ],
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
    statusColor() {
      return this.connectionStatus === 'connected' ? 'success' : 'warning'
    },
  },

  methods: {
    onSelectEmoji(emoji) {
      if (emoji && emoji.i) {
        this.messageText += emoji.i
      }
    },
    getUserColor(username) {
      if (!username) return '#9e9e9e'
      let hash = 0
      for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash)
      }
      const index = Math.abs(hash % this.colors.length)
      return this.colors[index]
    },
    getInitials(username) {
      if (!username) return 'U'
      return username.slice(0, 2).toUpperCase()
    },
    formatTime(ts) {
      const date = new Date(ts)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })
    },
    showMessage(text) {
      this.msg = text
      this.snackbar = true
    },
    shouldShowAvatar(index) {
      if (index === 0) return true
      const currentMsg = this.messages[index]
      const prevMsg = this.messages[index - 1]
      return (
        (currentMsg.user?.username || currentMsg.username) !==
        (prevMsg.user?.username || prevMsg.username)
      )
    },
    reconnectChat() {
      chatService.close()
      this.messages = []
      this.connectionStatus = 'connecting'
      this.initChat()
    },
    initChat() {
      if (!this.id || !this.token) return
      this.loadingHistory = true
      chatService.init({
        host: this.host,
        token: this.token,
        roomId: this.id,
        isOrg: this.isOrg,
        onMessage: (event) => {
          if (event.type === 'history') {
            this.messages = event.data
            this.loadingHistory = false
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
  mounted() {
    this.initChat()
  },
  beforeUnmount() {
    chatService.close()
  },
}
</script>

<template>
  <v-card class="chat-window-card d-flex flex-column h-100 pa-0" flat>
    <v-card-title class="flex-shrink-0 px-4 py-3 border-b">
      <v-icon color="primary" start>mdi-message-text-outline</v-icon>
      <span class="ml-3 font-weight-bold">المحادثة العامة</span>
      <v-chip class="ml-auto" :color="statusColor" label size="small" variant="tonal">
        {{ statusLabel }}
      </v-chip>
    </v-card-title>

    <div class="messages-container flex-grow-1" ref="messageBox">
      <template v-if="loadingHistory">
        <div v-for="n in 6" :key="'shimmer-' + n" class="d-flex px-4 mb-6">
          <div style="width: 50px" class="flex-shrink-0 d-flex justify-center">
            <v-skeleton-loader type="avatar" size="40" bg-color="transparent"></v-skeleton-loader>
          </div>
          <div class="flex-grow-1">
            <v-skeleton-loader
              type="text"
              width="80"
              class="mb-2"
              bg-color="transparent"
            ></v-skeleton-loader>
            <v-skeleton-loader
              type="paragraph"
              class="shimmer-bubble"
              bg-color="white"
            ></v-skeleton-loader>
          </div>
        </div>
      </template>

      <template v-else>
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="d-flex message-row px-4"
          :class="shouldShowAvatar(index) ? 'mt-4' : 'mt-1'"
        >
          <div style="width: 50px" class="flex-shrink-0 d-flex justify-center">
            <v-avatar
              v-if="shouldShowAvatar(index)"
              size="40"
              rounded="lg"
              :style="{ backgroundColor: getUserColor(msg.user?.username || msg.username) }"
            >
              <span class="text-white font-weight-bold two-letter-initials">{{
                getInitials(msg.user?.username || msg.username)
              }}</span>
            </v-avatar>
          </div>

          <div class="flex-grow-1 min-width-0">
            <div v-if="shouldShowAvatar(index)" class="d-flex align-center mb-1">
              <span
                class="font-weight-bold text-subtitle-2"
                :style="{ color: getUserColor(msg.user?.username || msg.username) }"
              >
                {{ msg.user?.username || msg.username || 'مستخدم' }}
              </span>
              <span class="ms-2 text-caption opacity-40">{{ formatTime(msg.timestamp) }}</span>
            </div>

            <div class="d-flex align-center bubble-container">
              <div class="message-bubble">
                <div class="text-body-2 text-grey-darken-3 message-text" dir="auto">
                  {{ msg.content }}
                </div>
              </div>
              <span v-if="!shouldShowAvatar(index)" class="ms-2 text-caption time-on-hover">
                {{ formatTime(msg.timestamp) }}
              </span>
            </div>
          </div>
        </div>
      </template>
    </div>

    <v-divider></v-divider>
    <div class="chat-footer pa-4 flex-shrink-0 bg-white">
      <div class="d-flex align-center bg-grey-lighten-4 rounded-pill px-4">
        <v-menu
          :close-on-content-click="false"
          location="top"
          transition="slide-y-reverse-transition"
        >
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              icon="mdi-emoticon-outline"
              variant="text"
              color="grey-darken-1"
              density="comfortable"
              class="me-1"
            />
          </template>
          <v-sheet rounded="lg" elevation="12" width="300">
            <EmojiPicker
              :native="true"
              :hide-group-names="true"
              theme="light"
              @select="onSelectEmoji"
            />
          </v-sheet>
        </v-menu>

        <v-text-field
          v-model="messageText"
          placeholder="اكتب رسالتك..."
          variant="plain"
          hide-details
          density="compact"
          class="flex-grow-1 chat-input-field"
          dir="auto"
          :disabled="connectionStatus !== 'connected'"
          @keyup.enter="sendMessage"
        />
        <v-btn
          color="primary"
          icon="mdi-send-variant"
          variant="text"
          :disabled="connectionStatus !== 'connected'"
          @click="sendMessage"
        />
      </div>
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
:deep(.chat-input-field input) {
  text-align: right !important;
  unicode-bidi: plaintext;
}

:deep(.chat-input-field input::placeholder) {
  text-align: right !important;
}

:deep(.v-skeleton-loader) {
  background: transparent !important;
}
.chat-window-card {
  height: 100% !important;
  max-height: 100% !important;
  overflow: hidden;
}

.message-text {
  text-align: right;
  unicode-bidi: plaintext;
  direction: ltr;
  display: block;
  width: 100%;
}

.messages-container {
  direction: rtl;
  text-align: right;
  unicode-bidi: isolate;
  overflow-y: auto;
  background-color: #fcfcfc;
  padding: 16px;
  min-height: 0;
}
.message-bubble {
  background: white;
  padding: 8px 14px;
  border-radius: 12px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  display: inline-block;
  max-width: 85%;
  border: 1px solid #f1f5f9;
}
.mt-1 .message-bubble {
  border-top-right-radius: 4px;
}
.time-on-hover {
  opacity: 0;
  transition: opacity 0.2s;
  color: #94a3b8;
}
.message-row:hover .time-on-hover {
  opacity: 1;
}
.two-letter-initials {
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.messages-container::-webkit-scrollbar {
  width: 5px;
}
.messages-container::-webkit-scrollbar-thumb {
  background: #eee;
  border-radius: 10px;
}
</style>
