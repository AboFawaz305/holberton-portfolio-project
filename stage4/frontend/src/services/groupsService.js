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

  /**
   * Create group (or subgroup) in an organization
   * Backend endpoint: POST /api/organizations/{org_id}/groups
   *
   * groupData examples:
   * - { title: "AI Group" }
   * - { title: "Week 1", parent_group_id: "65f..." }
   */
  async createGroup(orgId, groupData, token) {
    const response = await fetch(`/api/organizations/${orgId}/groups`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(groupData),
    })

    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'Failed to create group')
    return data
  },
}

export default groupsService