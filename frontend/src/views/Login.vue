<template>
  <div class="container" style="max-width: 400px; margin: 100px auto;">
    <h2 style="margin-bottom: 30px; text-align: center; color: #111827;">登录</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>用户名</label>
        <input
          v-model="form.username"
          type="text"
          required
          placeholder="请输入用户名"
        />
      </div>
      <div class="form-group">
        <label>密码</label>
        <input
          v-model="form.password"
          type="password"
          required
          placeholder="请输入密码"
        />
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
      <button type="submit" class="btn btn-primary" style="width: 100%;" :disabled="loading">
        {{ loading ? '登录中...' : '登录' }}
      </button>
      <div style="text-align: center; margin-top: 20px;">
        <span style="color: #6b7280;">还没有账号？</span>
        <router-link to="/register" style="color: #667eea; text-decoration: none; margin-left: 5px;">
          立即注册
        </router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  try {
    const formData = new FormData()
    formData.append('username', form.value.username)
    formData.append('password', form.value.password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    const token = response.data.access_token
    
    // 获取用户信息
    const userResponse = await api.get('/auth/me', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    authStore.setAuth(token, userResponse.data)
    router.push('/accounts')
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>
