// services/chatService.js

const chatService = {
  socket: null,

  init({ host, token, orgId, onMessage, onStatusUpdate }) {
    const wsUrl = `ws://${host}/api/ws/chat`
    this.socket = new WebSocket(wsUrl)

    // Handle WebSocket events
    this.socket.onopen = () => {
      const authData = { token, org_id: orgId }
      this.socket.send(JSON.stringify(authData))
    }

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        if (data.type === 'connected' && data.status === 'ok') {
          onStatusUpdate('connected')
          return
        }

        if (data.type === 'history') {
          onMessage({ type: 'history', data: data.data })
          return
        }

        // Push new message
        onMessage({ type: 'new_message', data })
      } catch (e) {
        console.error('Error parsing WebSocket message:', e)
      }
    }

    this.socket.onerror = () => {
      onStatusUpdate('error')
    }

    this.socket.onclose = () => {
      onStatusUpdate('disconnected')
    }
  },

  sendMessage(message) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message)
    }
  },

  close() {
    if (this.socket) {
      this.socket.close()
    }
  },
}

export default chatService
