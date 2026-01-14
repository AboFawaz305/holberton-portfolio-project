// services/groupsService. js

import authService from './authService'

const API_URL = '/api/groups'

const groupsService = {
  /**
   * Get all groups in an organization
   */
  async getGroupsByOrg(orgId) {
    const response = await fetch(`${API_URL}/org/${orgId}`)
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to fetch organization groups')
    }
    return response.json()
  },

  /**
   * Get a specific group by ID
   */
  async getGroupById(groupId) {
    const response = await fetch(`${API_URL}/${groupId}`, {
      method: 'GET',
      headers: authService.addAuthHeader({
        'Content-Type': 'application/json',
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      // We throw error.detail so the UI gets "EMAIL_NOT_VERIFIED"
      throw new Error(error.detail || 'Failed to fetch group info')
    }
    return response.json()
  },

  /**
   * Get all subgroups of a group
   */
  async getSubgroups(groupId) {
    const response = await fetch(`${API_URL}/${groupId}/subgroups`, {
      method: 'GET',
      headers: authService.addAuthHeader({
        'Content-Type': 'application/json',
      }),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to fetch subgroups')
    }
    return response.json()
  },
}

export default groupsService
