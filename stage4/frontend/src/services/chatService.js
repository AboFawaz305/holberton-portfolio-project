const chatService = {
  socket: null,

  init({ host, token, roomId, isOrg = true, onMessage, onStatusUpdate }) {
    const wsUrl = `ws://${host}/api/ws/chat`
    this.socket = new WebSocket(wsUrl)

    this.socket.onopen = () => {
      const authData = {
        token,
        room_id: roomId,
        isOrg,
      }

      this.socket.send(JSON.stringify(authData))
    }

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)

        if (data.type === 'connected' && data.status === 'ok') {
          onStatusUpdate('connected')
          return
        }

        if (data.type === 'error') {
          console.error('WebSocket error:', data.message)
          onStatusUpdate('error')
          return
        }

        if (data.type === 'history') {
          onMessage({ type: 'history', data: data.data })
          return
        }

        onMessage({ type: 'new_message', data })
      } catch (e) {
        console.error('Error parsing WebSocket message:', e)
      }
    }

    this.socket.onerror = (error) => {
      console.error('error=', error)
      onStatusUpdate('error')
    }

    this.socket.onclose = (event) => {
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
      this.socket = null
    }
  },
}

export default chatService
