// services/groupsService. js
import authService from './authService'

export default {
  // Upload a new resource to a group
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
