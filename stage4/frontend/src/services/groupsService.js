// services/groupsService. js

const API_URL = '/api/groups'

const groupsService = {
  /**
   * Get all groups in an organization
   */
  async getGroupsByOrg(orgId) {
    const response = await fetch(`${API_URL}/org/${orgId}`)
    if (!response.ok) throw new Error('Failed to fetch groups')
    return response.json()
  },

  /**
   * Get a specific group by ID
   */
  async getGroupById(groupId) {
    const response = await fetch(`${API_URL}/${groupId}`)
    if (!response.ok) throw new Error('Failed to fetch group')
    return response.json()
  },

  /**
   * Get all subgroups of a group
   */
  async getSubgroups(groupId) {
    const response = await fetch(`${API_URL}/${groupId}/subgroups`)
    if (!response.ok) throw new Error('Failed to fetch subgroups')
    return response.json()
  },
}

export default groupsService
