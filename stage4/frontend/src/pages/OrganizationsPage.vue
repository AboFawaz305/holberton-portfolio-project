<script>
import authService from '@/services/authService' // Import authService for authentication checks
import organizationService from '@/services/organizationService' // Import organizationService for API calls

export default {
  data() {
    return {
      organizations: [],
      isLoading: true, // Controls the loading indicator
      error: null, // Stores any error messages
      searchQuery: '', // Binds to the search field for filtering
      showLoginModal: false, // Controls the login modal visibility
    }
  },

  computed: {
    // Filters organizations based on the search query
    filteredOrganizations() {
      if (!this.searchQuery) {
        return this.organizations
      }
      const query = this.searchQuery.toLowerCase()
      return this.organizations.filter((org) => {
        return (
          org.organization_name.toLowerCase().includes(query) ||
          org.location.toLowerCase().includes(query)
        )
      })
      // return [
      //   {
      //     organization_id: 1,
      //     organization_name: 'dasfsad',
      //     user_count: 123,
      //     location: 'fsdfa',
      //   },
      //   {
      //     organization_id: 1,
      //     organization_name: 'dasfsad',
      //     user_count: 123,
      //     location: 'fsdfa',
      //   },
      //   {
      //     organization_id: 1,
      //     organization_name: 'dasfsad',
      //     user_count: 123,
      //     location: 'fsdfa',
      //   },
      //   {
      //     organization_id: 1,
      //     organization_name: 'dasfsad',
      //     user_count: 123,
      //     location: 'fsdfa',
      //   },
      //   {
      //     organization_id: 1,
      //     organization_name: 'dasfsad',
      //     user_count: 123,
      //     location: 'fsdfa',
      //   },
      // ]
    },
  },

  methods: {
    // Fetch organizations from the API using the organizationService
    async fetchOrganizations() {
      this.isLoading = true // Start loading
      this.error = null

      try {
        this.organizations = await organizationService.getAll() // Fetch data from the service
      } catch (err) {
        // Handle errors gracefully
        this.error = err.message
      } finally {
        this.isLoading = false // Stop loading
      }
    },

    // Handle organization entry and require login if the user is not authenticated
    async handleEntry(org) {
      if (!(await authService.isLoggedIn())) {
        this.showLoginModal = true // Show modal if not logged in
      } else {
        // Redirect to the organization's route
        this.$router.push({
          path: `/organizations/${org.organization_id}`,
          state: {
            name: org.organization_name,
          },
        })
      }
    },

    // Close the login modal and redirect to the login page
    goToLogin() {
      this.showLoginModal = false
      this.$router.push('/login')
    },
  },

  // Fetch organizations when the component is mounted
  mounted() {
    this.fetchOrganizations()
  },
}
</script>

<template>
  <!-- Top Section -->
  <v-card flat class="pa-12 text-center gradient-bg">
    <v-avatar size="64" class="mx-auto mb-4" color="primary">
      <v-icon color="white">mdi-school-outline</v-icon>
    </v-avatar>
    <v-card-title class="text-h4 font-weight-bold">اختر مؤسستك التعليمية</v-card-title>
    <v-card-subtitle>ابدأ بتحديد جامعتك للوصول الى مجتمعك</v-card-subtitle>
    <!-- Search Field -->
    <v-text-field
      v-model="searchQuery"
      label="ابحث عن مؤسستك التعليمية"
      outlined
      bg-color="white"
      rounded
      class="mt-6 mr-16 ml-16"
    />
  </v-card>
  <v-container class="full_page">
    <!-- Bottom Section -->
    <v-row class="bottm mt-8">
      <!-- Loading State -->
      <v-col v-if="isLoading" cols="12" class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p>جاري تحميل البيانات ...</p>
      </v-col>

      <!-- Error State -->
      <v-col v-else-if="error" cols="12" class="text-center text-danger">
        Error: {{ error }}
      </v-col>

      <!-- No Data State -->
      <v-col v-else-if="organizations.length === 0" cols="12" class="text-center">
        <p>لا توجد مؤسسات</p>
      </v-col>

      <!-- Organizations Grid -->
      <v-col
        v-for="org in filteredOrganizations"
        :key="org.organization_id"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card outlined class="card" @click="handleEntry(org)">
          <v-img :src="org.photo_url" height="250px" class="stretched-img" alt="logo"></v-img>
          <v-card-title>{{ org.organization_name }}</v-card-title>
          <v-card-subtitle>
            <v-chip color="teal lighten-5" class="ma-2">{{ org.location }}</v-chip>
            <v-chip color="orange lighten-5" class="ma-2">{{ org.user_count }} طالب</v-chip>
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>

    <!-- Login Modal -->
    <v-dialog v-model="showLoginModal" max-width="400px">
      <v-card>
        <v-card-title>
          <v-icon color="error" large>mdi-lock</v-icon>
          <span class="ml-4">تسجيل الدخول مطلوب</span>
        </v-card-title>
        <v-card-text>
          يجب عليك تسجيل الدخول أولاً لتتمكن من الانضمام إلى مجتمع هذه المؤسسة.
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="goToLogin">تسجيل الدخول</v-btn>
          <v-btn text @click="showLoginModal = false">إغلاق</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.stretched-img :deep(img) {
  object-fit: fill !important;
}
.card {
  transition: 0.2s ease;
  cursor: pointer;
}

.card:hover {
  transform: scale(1.05);
}
</style>
