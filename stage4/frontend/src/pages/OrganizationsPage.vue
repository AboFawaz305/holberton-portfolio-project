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
            isOrg: true,
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
  <v-card flat class="pa-10 text-center gradient-bg" rounded="0">
    <div class="mx-auto mb-4">
      <v-icon color="white" size="64" class="opacity-90">mdi-school-outline</v-icon>
    </div>

    <v-card-title class="text-h4 font-weight-bold mb-1 text-white"
      >اختر مؤسستك التعليمية</v-card-title
    >
    <v-card-subtitle class="text-body-2 text-white opacity-80"
      >ابدأ بتحديد جامعتك للوصول الى مجتمعك وزملائك</v-card-subtitle
    >

    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="5">
        <v-text-field
          v-model="searchQuery"
          label="ابحث عن اسم الجامعة أو الموقع..."
          variant="solo"
          bg-color="white"
          rounded="lg"
          prepend-inner-icon="mdi-magnify"
          color="primary"
          class="mt-8 shadow-lg"
          hide-details
          flat
        />
      </v-col>
    </v-row>
  </v-card>

  <div class="page-background py-10">
    <v-container class="content-width">
      <v-row>
        <template v-if="isLoading">
          <v-col v-for="n in 6" :key="n" cols="12" md="6" lg="4">
            <v-skeleton-loader
              type="image, article"
              rounded="xl"
              class="bg-white layered-shadow"
            ></v-skeleton-loader>
          </v-col>
        </template>

        <v-col v-else-if="filteredOrganizations.length === 0" cols="12" class="text-center py-12">
          <v-avatar size="100" color="white" class="mb-4 layered-shadow">
            <v-icon size="48" color="grey-lighten-1">mdi-magnify-close</v-icon>
          </v-avatar>
          <h3 class="text-h6 font-weight-bold text-grey-darken-2">لم يتم العثور على نتائج</h3>
        </v-col>

        <v-col
          v-for="org in filteredOrganizations"
          :key="org.organization_id"
          cols="12"
          md="6"
          lg="4"
        >
          <v-card
            link
            variant="flat"
            class="org-card h-100 layered-shadow"
            rounded="xl"
            @click="handleEntry(org)"
          >
            <v-img :src="org.photo_url" height="160px" cover class="bg-white">
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="grey-lighten-4"></v-progress-circular>
                </v-row>
              </template>
            </v-img>

            <v-card-title class="pt-4 px-5 font-weight-bold text-h6 text-truncate">
              {{ org.organization_name }}
            </v-card-title>

            <v-divider class="mx-5 my-1"></v-divider>

            <v-card-subtitle class="pa-5 d-flex justify-space-between align-center">
              <v-chip
                color="orange-lighten-3"
                text-color="orange-darken-4"
                class="font-weight-bold"
                size="small"
                label
              >
                <v-icon start size="16">mdi-account-group</v-icon>
                {{ org.members_count }} طالب
              </v-chip>

              <div class="text-grey-darken-2 d-flex align-center text-caption">
                <v-icon size="18" class="me-1">mdi-map-marker-outline</v-icon>
                <span class="text-truncate" style="max-width: 140px">{{ org.location }}</span>
              </div>
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-dialog v-model="showLoginModal" max-width="450px" persistent>
      <v-card rounded="xl" class="pa-6 text-center">
        <v-avatar color="error-lighten-5" size="70" class="mb-4">
          <v-icon color="error" size="36">mdi-lock-outline</v-icon>
        </v-avatar>
        <v-card-title class="text-h5 font-weight-bold justify-center"
          >تسجيل الدخول مطلوب</v-card-title
        >
        <v-card-text class="text-body-1"
          >يجب عليك تسجيل الدخول أولاً للوصول لهذه المؤسسة.</v-card-text
        >
        <v-card-actions class="flex-column mt-4" style="gap: 8px">
          <v-btn class="gradient-bg text-white" block size="large" rounded="lg" @click="goToLogin"
            >تسجيل الدخول</v-btn
          >
          <v-btn variant="text" block @click="showLoginModal = false">إلغاء</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.page-background {
  background-color: #f4f7fa;
  min-height: 100vh;
}

.content-width {
  max-width: 1200px !important;
}

.layered-shadow {
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
}

.shadow-lg {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

.org-card {
  background-color: white !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid #edf2f7 !important;
}

.org-card:hover {
  transform: translateY(-4px);
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
}

.opacity-90 {
  opacity: 0.9;
}
.opacity-80 {
  opacity: 0.8;
}
</style>
