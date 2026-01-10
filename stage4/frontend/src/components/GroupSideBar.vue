<script>
export default {
  name: 'CollegeSidebar',
  data() {
    return {
      searchQuery: '', // 1. Added search variable
      colleges: [
        {
          name: 'كلية علوم الحاسب والمعلومات',
          students: 3200,
          active: 245,
          icon: 'mdi-laptop',
          bgColor: 'orange-lighten-5',
          iconColor: 'orange-darken-2',
        },
        {
          name: 'كلية الهندسة',
          students: 5100,
          active: 412,
          icon: 'mdi-cog-outline',
          bgColor: 'light-green-lighten-5',
          iconColor: 'light-green-darken-2',
        },
        {
          name: 'كلية الطب',
          students: 2800,
          active: 189,
          icon: 'mdi-hospital-building',
          bgColor: 'green-lighten-5',
          iconColor: 'green-darken-2',
        },
        {
          name: 'كلية إدارة الأعمال',
          students: 4200,
          active: 356,
          icon: 'mdi-briefcase-outline',
          bgColor: 'lime-lighten-5',
          iconColor: 'lime-darken-3',
        },
        {
          name: 'كلية العلوم',
          students: 3600,
          active: 298,
          icon: 'mdi-microscope',
          bgColor: 'cyan-lighten-5',
          iconColor: 'cyan-darken-2',
        },
        {
          name: 'كلية الآداب',
          students: 4800,
          active: 401,
          icon: 'mdi-book-open-variant',
          bgColor: 'amber-lighten-5',
          iconColor: 'amber-darken-2',
        },
      ],
    }
  },
  computed: {
    // 2. Added filtering logic
    filteredColleges() {
      if (!this.searchQuery) return this.colleges

      const query = this.searchQuery.toLowerCase()
      return this.colleges.filter((college) => college.name.toLowerCase().includes(query))
    },
  },
}
</script>

<template>
  <v-navigation-drawer
    width="400"
    permanent
    location="right"
    border="left"
    class="pa-4 bg-grey-lighten-5"
  >
    <h2 class="text-h6 mb-4 text-right font-weight-bold" style="color: #333">الكليات</h2>

    <v-text-field
      v-model="searchQuery"
      variant="outlined"
      placeholder="ابحث عن كلية..."
      prepend-inner-icon="mdi-magnify"
      rounded="lg"
      bg-color="white"
      density="compact"
      class="mb-4"
      hide-details
      clearable
    ></v-text-field>

    <v-list bg-color="transparent" class="pa-0">
      <v-card
        v-for="(college, index) in filteredColleges"
        :key="index"
        variant="flat"
        class="mb-4 college-card"
        rounded="xl"
      >
        <v-list-item class="pa-4">
          <div class="d-flex flex-column w-100">
            <div class="d-flex align-center w-100 mb-4">
              <v-avatar :color="college.bgColor" size="48" rounded="lg" class="elevation-1 ms-3">
                <v-icon :color="college.iconColor" size="28">{{ college.icon }}</v-icon>
              </v-avatar>

              <div class="flex-grow-1 text-center">
                <span class="text-subtitle-1 font-weight-bold">
                  {{ college.name }}
                </span>
              </div>

              <span class="text-body-2 text-grey-darken-1"> {{ college.students }} طالب </span>
            </div>

            <v-divider class="mb-3"></v-divider>

            <div class="d-flex justify-space-between align-center">
              <div class="d-flex align-center">
                <v-badge dot color="success" inline class="ms-2"></v-badge>
                <span class="text-caption text-grey-darken-1">نشط {{ college.active }}</span>
              </div>

              <v-icon color="grey-lighten-1" size="small">mdi-chevron-left</v-icon>
            </div>
          </div>
        </v-list-item>
      </v-card>

      <div v-if="filteredColleges.length === 0" class="text-center pa-4 text-grey">
        لا توجد نتائج بحث
      </div>
    </v-list>
  </v-navigation-drawer>
</template>

<style scoped>
.college-card {
  border: 1px solid #ececec !important;
  transition: all 0.3s ease;
  cursor: pointer;
}

.college-card:hover {
  border-color: #d1d1d1 !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
  transform: translateY(-2px);
}
</style>
