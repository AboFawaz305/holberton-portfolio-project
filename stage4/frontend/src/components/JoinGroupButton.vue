<template>
  <div class="d-inline-flex">
    <v-btn color="primary" :loading="loading" :disabled="disabled" @click="onJoinClick">
      {{buttonText}}
    </v-btn>

    <v-snackbar v-model="snackbar.open" :timeout="4000" :color="snackbar.color" location="bottom">
      {{ snackbar.message }}
      <template #actions>
        <v-btn variant="text" @click="snackbar.open = false">إغلاق</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import authService from '@/services/authService'
import usersService from '@/services/usersService'

export default {
  props: {
    id: { type: String, required: true },
    isOrg: { type: Boolean, required: true },
    disable: { type: Boolean, default: false },
  },
  data() {
    return {
      loading: false,
      joined: false,
      snackbar: { open: false, message: '', color: 'success' },
    }
  },
  computed: {
    disabled() {
      return this.joined || this.disable
    },
    buttonText() {
      if (this.joined) return 'منضم'
      return this.isOrg ? 'إنضم إلى المنظمة' : 'إنضم إلى المجموعة'
    }
  },
  watch: {
    id: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.refreshJoinStatus()
        }
      },
    },
  },
  mounted() {
    this.refreshJoinStatus()
  },
  methods: {
    showMsg(message, color = 'success') {
      this.snackbar = { open: true, message, color }
    },
    async refreshJoinStatus() {
      // If not logged in, we assume not joined
      if (!authService.isLoggedIn()) {
        this.joined = false
        return
      }

      try {
        // Fetch fresh status from backend
        this.joined = await usersService.isUserJoinedToGroup(this.id, this.isOrg)
      } catch (err) {
        console.error('Failed to refresh join status:', err)
        this.joined = false
      }
    },

    async onJoinClick() {
      if (!authService.isLoggedIn()) {
        this.showMsg('يرجى تسجيل تادخول', 'warning')
        setTimeout(() => {
          this.$router.push('/login')
        }, 1000)
        return
      }

      this.loading = true
      try {
        await usersService.joinGroup(this.id, this.isOrg)
        this.joined = true
        this.$emit('joined', { id: this.id, isOrg: this.isOrg })
        this.showMsg('تم اانضمام بنجاح', 'success')
        await this.refreshJoinStatus()
      } catch (err) {
        const detail =
          (err && err.response && err.response.data && err.response.data.detail) ||
          err.message ||
          'فشل الانضمام'
        this.showMsg(detail, 'error')
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
<style scoped>

.v-btn {
  min-width: 150px;
}
</style>