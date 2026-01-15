// services/authService.js
export default {
  // Perform a login API call
  async login({ username, password }) {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Login failed')
    }

    const data = await response.json()
    // Store the token in localStorage
    localStorage.setItem('token', data.access_token)
    return data
  },

  // Perform a registration API call
  async register({ firstname, lastname, username, email, password }) {
    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        first_name: firstname,
        last_name: lastname,
        username: username,
        email: email,
        password: password,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Registration failed')
    }

    return await response.json() // Return user data if registration is successful
  },

  async verifyEmail(token) {
    const response = await fetch(`/api/auth/verify-email/${token}`)
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Verification failed')
    }
    return await response.json()
  },

  // Check if the user is logged in
  async isLoggedIn() {
    const token = localStorage.getItem('token')
    if (!token) return false
    try {
      await this.getCurrentUser()
    } catch {
      localStorage.removeItem('token')
      return false
    }
    return true
  },

  // Retrieve the authentication token
  getToken() {
    return localStorage.getItem('token')
  },

  // Log the user out
  logout() {
    localStorage.removeItem('token') // Clears the token from localStorage
  },

  // Add Authorization header to existing headers
  addAuthHeader(headers = {}) {
    const token = this.getToken()
    if (!token) throw new Error('User is not authenticated')

    return {
      ...headers,
      Authorization: `Bearer ${token}`, // Attach the token in the Authorization header
    }
  },

  // Get the current authenticated user's information
  async getCurrentUser() {
    const response = await fetch('/api/auth/me', {
      headers: this.addAuthHeader(),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to fetch current user information')
    }

    return await response.json() // Return user data
  },
}
