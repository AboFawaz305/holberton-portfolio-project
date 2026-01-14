<template>
  <div class="d-inline-flex">
    <v-btn color="primary" :loading="loading" :disabled="disabled" @click="onJoinClick">
      {{ !joined ? 'إنضم إلى المنظمة التعليمية' : 'منضم' }}
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
      joined: this.initiallyJoined,
      snackbar: { open: false, message: '', color: 'success' },
    }
  },
  computed: {
    disabled() {
      return this.loading || this.joined
    },
  },
  mounted() {
    this.refreshJoinStatus()
  },
  methods: {
    showMsg(message, color = 'success') {
      this.snackbar = { open: true, message, color }
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
          'فشل الان ضمام'
        this.showMsg(detail, 'error')
      } finally {
        this.loading = false
      }
    },
    async refreshJoinStatus() {
      this.joined = await usersService.isUserJoinedToGroup(this.id, this.isOrg)
    },
  },
}
</script>
