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
  async addResource(groupId, { name, description, file }, onProgress) {
    const formData = new FormData()
    formData.append('name', name)
    formData.append('file', file)
    if (description) {
      formData.append('description', description)
    }

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest()

      // Track upload progress
      xhr.upload.addEventListener('progress', (event) => {
        if (event.lengthComputable && onProgress) {
          const percentComplete = Math.round((event.loaded / event.total) * 100)
          onProgress(percentComplete)
        }
      })

      xhr.addEventListener('load', () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          resolve(JSON.parse(xhr.responseText || '{}'))
        } else {
          try {
            const error = JSON.parse(xhr.responseText)
            reject(new Error(error.detail || 'فشل رفع المصدر'))
          } catch {
            reject(new Error('فشل رفع المصدر'))
          }
        }
      })

      xhr.addEventListener('error', () => {
        reject(new Error('خطأ في الشبكة'))
      })

      xhr.open('POST', `/api/groups/${groupId}/resources`)
      xhr.setRequestHeader('Authorization', `Bearer ${authService.getToken()}`)
      xhr.send(formData)
    })
  },
}

export default groupsService
