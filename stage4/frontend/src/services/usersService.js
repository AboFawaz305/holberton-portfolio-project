// services/usersService.js
import authService from './authService'

export default {
  // Update user information
  async updateUser(valuesToUpdate) {
    const response = await fetch('/api/users', {
      method: 'PATCH',
      headers: authService.addAuthHeader({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify(valuesToUpdate),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to update user information')
    }

    return await response.json() // Return updated user data
  },

  // Add a new email to the user's account
  async addEmail(email) {
    const response = await fetch('/api/users/emails', {
      method: 'POST',
      headers: authService.addAuthHeader({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({ email }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to add email')
    }

    return await response.json() // Return success response
  },

  // Delete an eamil from the user account
  async deleteEmail(email_id) {
    const response = await fetch(`/api/users/emails/${email_id}`, {
      method: 'DELETE',
      headers: authService.addAuthHeader({}),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to delete email')
    }

    return await response.json() // Return success response
  },
}
