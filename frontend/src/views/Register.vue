<template>
  <div class="container" style="max-width: 400px; margin: 100px auto;">
    <h2 style="margin-bottom: 30px; text-align: center; color: #111827;">注册</h2>
    <form @submit.prevent="handleRegister">
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
        <label>邮箱</label>
        <input
          v-model="form.email"
          type="email"
          required
          placeholder="请输入邮箱"
        />
      </div>
      <div class="form-group">
        <label>密码</label>
        <input
          v-model="form.password"
          type="password"
          required
          placeholder="请输入密码"
          minlength="6"
        />
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>
      <button type="submit" class="btn btn-primary" style="width: 100%;" :disabled="loading">
        {{ loading ? '注册中...' : '注册' }}
      </button>
      <div style="text-align: center; margin-top: 20px;">
        <span style="color: #6b7280;">已有账号？</span>
        <router-link to="/login" style="color: #667eea; text-decoration: none; margin-left: 5px;">
          立即登录
        </router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const form = ref({
  username: '',
  email: '',
  password: ''
})
const loading = ref(false)
const error = ref('')
const success = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    await api.post('/auth/register', form.value)
    success.value = '注册成功！正在跳转到登录页面...'
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (err) {
    error.value = err.response?.data?.detail || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>
