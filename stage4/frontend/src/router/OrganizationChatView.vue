<script>
export default {
  props: { id: String },
  
  data() {
    return {
      token: localStorage.getItem('token'),
      uuid: crypto.randomUUID(),
      socket: null,
      messages: [],
      messageText: "",
      connectionStatus: "connecting",
      errorMessage: "",
      // Fix: Use correct assignment syntax here
      host: window.location.host,
      protocol: window.location.protocol === 'https:' ? 'wss:' : 'ws:'
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

  methods: {
    initChat() {
      this.connectionStatus = "connecting";
      
      // Fix: Use 'this.' to access host and protocol from data()
      // Note: No trailing slash to match @app.websocket("/wsss")
      const wsUrl = `${this.protocol}//${this.host}/api/wsss`;
      console.log("Connecting to:", wsUrl);
      
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = () => {
        console.log("WebSocket connected, sending auth...");
        const authData = {
          token: this.token,
          org_id: this.id
        };
        this.socket.send(JSON.stringify(authData));
      };

      this.socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            
            if (data.type === "connected" && data.status === "ok") {
              this.connectionStatus = "connected";
              console.log("Authentication successful");
              return;
            }
            
            this.messages.push(data);
        } catch (e) {
            console.log("Received non-JSON message:", event.data);
        }
      };

      this.socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        this.connectionStatus = "error";
        this.errorMessage = "Connection error occurred";
      };

      this.socket.onclose = (event) => {
        console.log("WebSocket closed:", event.code, event.reason);
        this.connectionStatus = "disconnected";
        
        // Don't reconnect if it's an Auth error (1008) or normal closure
        if (event.code !== 1008 && event.code !== 1000) {
          setTimeout(() => {
            console.log("Attempting to reconnect...");
            this.initChat();
          }, 3000);
        } else if (event.code === 1008) {
          this.errorMessage = "Authentication failed";
        }
      };
    },

    sendMessage() {
      if (!this.messageText.trim()) return;
      
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(this.messageText);
        this.messageText = "";
      } else {
        alert("Not connected to chat server");
      }
    }
  },

  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  }
};
</script>

<template>
  <div>
    <h2>Chat Room</h2>
    
    <div :class="'status-' + connectionStatus" style="padding: 10px; margin-bottom: 10px; border-radius: 4px;">
      <span v-if="connectionStatus === 'connecting'">🔄 Connecting...</span>
      <span v-else-if="connectionStatus === 'connected'">✅ Connected</span>
      <span v-else-if="connectionStatus === 'disconnected'">🔴 Disconnected - Reconnecting...</span>
      <span v-else-if="connectionStatus === 'error'">❌ Error: {{ errorMessage }}</span>
    </div>
    
    <div style="height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; background: white;">
      <div v-for="(msg, index) in messages" :key="index" style="margin-bottom: 8px;">
        <strong>{{ msg.username || 'User' }}:</strong> {{ msg.content || msg }}
        <small v-if="msg.timestamp" style="color: gray; margin-left: 10px;">
          {{ new Date(msg.timestamp).toLocaleTimeString() }}
        </small>
      </div>
    </div>

    <div style="margin-top: 10px; display: flex;">
      <input 
        v-model="messageText" 
        @keyup.enter="sendMessage" 
        placeholder="Say something..."
        :disabled="connectionStatus !== 'connected'"
        style="flex-grow: 1; padding: 8px;"
      >
      <button 
        @click="sendMessage"
        :disabled="connectionStatus !== 'connected'"
        style="width: 80px; padding: 8px; margin-left: 10px;"
      >
        Send
      </button>
    </div>
  </div>
</template>

<style scoped>
.status-connecting { background-color: #fff3cd; color: #856404; }
.status-connected { background-color: #d4edda; color: #155724; }
.status-disconnected { background-color: #f8d7da; color: #721c24; }
.status-error { background-color: #f8d7da; color: #721c24; }
</style>