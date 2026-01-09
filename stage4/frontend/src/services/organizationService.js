// services/organizationService.js

export default {
  // Fetch all organizations
  async getAll() {
    try {
      const response = await fetch('/api/organizations')

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      return await response.json() // Return the organizations data
    } catch (err) {
      throw new Error(`خطأ في الشبكة: ${err.message}`)
    }
  },
}
