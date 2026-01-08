<script>
export default {
  props: { id: String },
  data() {
    return {
      token: localStorage.getItem('token'),
      socket: null,
      messages: [],
      messageText: "",
      connectionStatus: "connecting",
      errorMessage: "",
      organizationName: window.history.state?.name || 'Loading...',
      host: window.location.host,
    };
  },
  mounted() {
    if (!this.token) {
      this.connectionStatus = "error";
      this.errorMessage = "No authentication token found";
      return;
    }
    this.initChat();
  },
  computed: {
  statusLabel() {
    const labels = {
      connected: 'Connected',
      connecting: 'Connecting...',
      disconnected: 'Offline',
      error: 'Connection Error'
    };
    return labels[this.connectionStatus] || this.connectionStatus;
  }
},
  methods: {
    formatTime(ts) {
      return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    },
    initChat() {
      this.connectionStatus = "connecting";
      const wsUrl = `ws://${this.host}/api/ws`;
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
        const authData = { token: this.token, org_id: this.id };
        this.socket.send(JSON.stringify(authData));
      };

      this.socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === "connected" && data.status === "ok") {
            this.connectionStatus = "connected";
            return;
          }
          if (data.type === "history") {
            this.messages = data.data;
            this.scrollToBottom();
            return;
          }
          this.messages.push(data);
          this.scrollToBottom();
        } catch (e) {
          console.log("Error parsing message", e);
        }
      };

      this.socket.onerror = () => { this.connectionStatus = "error"; };
      this.socket.onclose = () => { this.connectionStatus = "disconnected"; };
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$el.querySelector('.messages-container');
        if (container) container.scrollTop = container.scrollHeight;
      });
    },
    sendMessage() {
      if (!this.messageText.trim()) return;
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(this.messageText);
        this.messageText = "";
      }
    }
  }
};
</script>

<template>
  <div class="full-page">
    <div class="top">
      <h1> {{ organizationName }} #</h1>
    </div>

    <div class="bottom">
      <div class="group-window">
        </div>

      <div class="chat-window">
        <div class="chat-header">
            <div class="header-icon">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="white">
              <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
            </svg>
          </div>
          <div class="header-info">
            <div class="header-title-row">
                <h3>المحادثة العامة</h3>
                <div :class="['status-badge', connectionStatus]">
                    <span class="status-dot"></span>
                    <span class="status-text">{{ statusLabel }}</span>
                </div>
            </div>
            <p>تواصل مع جميع طلاب الجامعة</p>
          </div>

        </div>

        <hr class="divider">

        <div class="messages-container" ref="messageBox">
          <div v-for="(msg, index) in messages" :key="index" class="message-row">
            <div class="avatar">
               <img :src="'https://ui-avatars.com/api/?name=' + (msg.user?.username ||msg.username|| 'U')" alt="avatar">
            </div>

            <div class="message-body">
              <div class="message-header">
                <span class="username">{{ msg.user?.username || msg.username || 'مستخدم' }}</span>
                <span class="major-badge">ضايع</span>
                <span class="time-ago" v-if="msg.timestamp">
                  {{ formatTime(msg.timestamp) }}
                </span>
              </div>
              
              <div class="message-text">
                {{ msg.content }}
              </div>

              <div class="message-footer">
              </div>
            </div>
          </div>
        </div>

        <div class="input-container">
          <div class="input-bar">
            <input 
              v-model="messageText" 
              @keyup.enter="sendMessage" 
              placeholder="شارك أفكارك مع المجتمع..."
              :disabled="connectionStatus !== 'connected'"
            />
            <button 
              @click="sendMessage" 
              class="send-btn"
              :disabled="connectionStatus !== 'connected'"
            >
              <svg viewBox="0 0 24 24" width="20" height="20" fill="white">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.full-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.top {
  height: 120px;
  background: linear-gradient(to right, #75b9c4, #04809f);
  color: white;
  display: flex;
  align-items: center;
  padding: 0 40px;
  flex-shrink: 0;
}

.bottom {
  display: flex;
  flex: 1;
  overflow: hidden;
  background-color: #f8f9fa;
}

.group-window {
  width: 250px;
  background-color: white;
  border-left: 1px solid #eee;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: white;
  margin: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 20px 30px;
  gap: 15px;
}

.header-info {
  text-align: right;
}

.header-info h3 { margin: 0; font-size: 1.1rem; color: #333; }
.header-info p { margin: 0; font-size: 0.85rem; color: #888; }
.header-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #bdc3c7;
}
.status-badge.connected {
  color: #27ae60;
  background-color: #eafaf1;
}
.status-badge.connected .status-dot {
  background-color: #27ae60;
  box-shadow: 0 0 4px rgba(39, 174, 96, 0.4);
}
.status-badge.connecting {
  color: #f39c12;
  background-color: #fef5e7;
}
.status-badge.connecting .status-dot {
  background-color: #f39c12;
  animation: pulse 1.5s infinite;
}
.status-badge.disconnected, .status-badge.error {
  color: #e74c3c;
  background-color: #fdedec;
}
.status-badge.disconnected .status-dot, .status-badge.error .status-dot {
  background-color: #e74c3c;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.5; }
  100% { transform: scale(1); opacity: 1; }
}
.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 2px 10px;
  border-radius: 20px;
  background-color: #f0f2f5;
  font-size: 0.7rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.header-icon {
  background-color: #5dadbb;
  padding: 10px;
  border-radius: 10px;
  display: flex;
}

.divider {
  border: 0;
  border-top: 1px solid #f0f0f0;
  margin: 0 30px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 30px;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.message-row {
  display: flex;
  gap: 15px;
}

.avatar img {
  width: 45px;
  height: 45px;
  border-radius: 12px;
  background-color: #eee;
}

.message-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username { font-weight: bold; color: #444; }

.major-badge {
  background-color: #fff9e6;
  color: #d4a017;
  padding: 2px 10px;
  border-radius: 15px;
  font-size: 0.75rem;
}

.time-ago { font-size: 0.75rem; color: #bbb; }

.message-text {
  color: #666;
  line-height: 1.5;
  font-size: 0.95rem;
}

.message-footer {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: #aaa;
  margin-top: 5px;
}

.input-container {
  padding: 20px 30px;
}

.input-bar {
  display: flex;
  align-items: center;
  background-color: #f8f9fa;
  border-radius: 30px;
  padding: 5px 15px;
  gap: 10px;
}

.input-bar input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px;
  outline: none;
  font-size: 0.9rem;
}

.icon-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #888;
  cursor: pointer;
}

.send-btn {
  background-color: #4db3c2;
  border: none;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s;
}

.send-btn:hover { transform: scale(1.1); }
</style>