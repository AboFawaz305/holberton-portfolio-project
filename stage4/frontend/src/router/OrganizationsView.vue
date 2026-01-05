<script>
export default {
  data() {
    return {
      organizations: [],
      isLoading: true,
      error: null,
      searchQuery: '',
    }
  },

  computed: {
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
    async fetchOrganizations() {
      this.isLoading = true
      this.error = null

      try {
        const response = await fetch('/api/organizations')

        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`)
        }

        const data = await response.json()
        this.organizations = data
      } catch (err) {
        this.error = `خطأ في الشبكة  : ${err}`
      } finally {
        this.isLoading = false
      }
    },
  },

  mounted() {
    this.fetchOrganizations()
  },
}
</script>
<template>
  <div class="full_page">
    <div class="top">
      <div class="icon-box">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="white"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M22 10L12 5L2 10L12 15L22 10Z"></path>
          <path d="M6 12.5V16C6 16 8.5 18 12 18C15.5 18 18 16 18 16V12.5"></path>
        </svg>
      </div>
      <h1>اختر مؤسستك التعليمية</h1>
      <p>ابدأ بتحديد جامعتك للوصول الى مجتمعك</p>
      <div class="search-container">
        <input v-model="searchQuery" type="text" placeholder="ابحث عن مؤسستك التعليمية" />
      </div>
    </div>

    <div class="bottm">
      <div v-if="isLoading">جاري تحميل البيانات ...</div>
      <div v-else-if="error" class="error">Error: {{ error }}</div>
      <div v-else-if="organizations.length === 0">لا توجد مؤسسات</div>
      <div v-else class="grid-container">
        <div v-for="org in filteredOrganizations" :key="org.organization_id" class="card">
          <div class="card-content">
            <img :src="org.photo_url" class="org_photo" alt="logo" />
            <h3 class="org_name">{{ org.organization_name }}</h3>
          </div>
          <div class="card_footer">
            <div class="org_location">{{ org.location }}</div>
            <div class="user_count">{{ org.user_count }} طالب</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.full_page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.top {
  background-image: linear-gradient(to right, #75b9c4, #04809f);
  display: flex;
  flex-direction: column;
  text-align: center;
  align-items: center;
  position: relative;
  height: 400px;
  flex: 0 0 auto;
  overflow: visible;
  color: white;
}
.icon-box {
  margin-top: 75px;
}
.bottm {
  padding: 80px 250px 50px 250px;
}
.error {
  color: red;
}

input {
  color: black;
  background-color: white;
  border-radius: 15px;
  border: 2px solid #5dadbb;
  height: 45px;
  width: 450px;
  padding: 0 20px;
  box-shadow: 0px 4px 9px rgba(93, 173, 187, 0.3);
  outline: none;
  font-size: 1rem;
}

input:focus {
  border-color: #04809f;
  box-shadow: 0px 4px 12px rgba(4, 128, 159, 0.4);
}

.no-results {
  width: 100%;
  text-align: center;
  padding: 40px;
  color: #777;
  font-size: 1.2rem;
}

.icon-box {
  width: 80px;
  height: 80px;
  background-color: #ffffff33;
  border-radius: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: inset 0 0 15px rgba(255, 255, 255, 0.2);
}

svg {
  width: 40px;
  height: 40px;
}
.grid-container {
  /* border: 2px solid red; */
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin: 0 auto;
  max-width: 1170px;
  min-height: 800px;
  align-content: flex-start;
  padding: 15px;
}
.card {
  /* border: 2px solid blue; */
  background-color: white;
  border-radius: 18px;
  overflow: hidden;
  transition: all 0.3s ease;
  height: 270px;
  width: 370px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.card:hover {
  transform: translateY(-8px);
}
.card-content {
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
}

.org_photo {
  padding-top: 0%;
  height: 150px;
  width: 370px;
}

.org_name {
  font-size: 1.25rem;
  font-weight: bold;
  justify-content: flex-start;
  padding: 0px 20px;
  box-sizing: border-box;
}

.card_footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
  padding: 20px 20px 5px 20px;
}

.org_location {
  color: #777;
  font-size: 0.9rem;
}

.user_count {
  background-color: #fff9e6;
  color: #c08d3e;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: bold;
}
</style>
