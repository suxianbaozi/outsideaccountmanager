<template>
  <div>
    <div class="header">
      <h1>账号管理系统</h1>
      <button @click="handleLogout" class="btn logout-btn">退出登录</button>
    </div>

    <div class="container">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2 style="color: #111827;">我的账号</h2>
        <button @click="showAddModal = true" class="btn btn-primary">+ 添加账号</button>
      </div>

      <div v-if="accountsStore.loading" style="text-align: center; padding: 40px;">
        加载中...
      </div>

      <div v-else-if="accountsStore.accounts.length === 0" class="empty-state">
        <h3>还没有账号</h3>
        <p>点击上方按钮添加您的第一个账号</p>
      </div>

      <table v-else class="table">
        <thead>
          <tr>
            <th>平台</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>手机号</th>
            <th>备注</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="account in accountsStore.accounts" :key="account.id">
            <td>{{ account.platform }}</td>
            <td>{{ account.username }}</td>
            <td>{{ account.email || '-' }}</td>
            <td>{{ account.phone || '-' }}</td>
            <td>{{ account.notes || '-' }}</td>
            <td>
              <div class="actions">
                <button @click="editAccount(account)" class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px;">
                  编辑
                </button>
                <button @click="deleteAccount(account.id)" class="btn btn-danger" style="padding: 6px 12px; font-size: 12px;">
                  删除
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加/编辑账号模态框 -->
    <div v-if="showAddModal || showEditModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ showEditModal ? '编辑账号' : '添加账号' }}</h2>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>平台名称 *</label>
            <input v-model="form.platform" type="text" required placeholder="例如：GitHub" />
          </div>
          <div class="form-group">
            <label>用户名 *</label>
            <input v-model="form.username" type="text" required placeholder="请输入用户名" />
          </div>
          <div class="form-group">
            <label>密码 *</label>
            <input v-model="form.password" type="password" required placeholder="请输入密码" />
          </div>
          <div class="form-group">
            <label>邮箱</label>
            <input v-model="form.email" type="email" placeholder="请输入邮箱（可选）" />
          </div>
          <div class="form-group">
            <label>手机号</label>
            <input v-model="form.phone" type="tel" placeholder="请输入手机号（可选）" />
          </div>
          <div class="form-group">
            <label>备注</label>
            <textarea v-model="form.notes" placeholder="请输入备注信息（可选）"></textarea>
          </div>
          <div v-if="error" class="error-message">{{ error }}</div>
          <div style="display: flex; gap: 10px; justify-content: flex-end;">
            <button type="button" @click="closeModal" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAccountsStore } from '../stores/accounts'

const router = useRouter()
const authStore = useAuthStore()
const accountsStore = useAccountsStore()

const showAddModal = ref(false)
const showEditModal = ref(false)
const editingId = ref(null)
const loading = ref(false)
const error = ref('')

const form = ref({
  platform: '',
  username: '',
  password: '',
  email: '',
  phone: '',
  notes: ''
})

onMounted(async () => {
  try {
    await accountsStore.fetchAccounts()
  } catch (err) {
    error.value = '加载账号列表失败'
  }
})

function resetForm() {
  form.value = {
    platform: '',
    username: '',
    password: '',
    email: '',
    phone: '',
    notes: ''
  }
  editingId.value = null
  error.value = ''
}

function closeModal() {
  showAddModal.value = false
  showEditModal.value = false
  resetForm()
}

function editAccount(account) {
  editingId.value = account.id
  form.value = {
    platform: account.platform,
    username: account.username,
    password: account.password,
    email: account.email || '',
    phone: account.phone || '',
    notes: account.notes || ''
  }
  showEditModal.value = true
}

async function handleSubmit() {
  loading.value = true
  error.value = ''
  
  try {
    const accountData = {
      platform: form.value.platform,
      username: form.value.username,
      password: form.value.password,
      email: form.value.email || null,
      phone: form.value.phone || null,
      notes: form.value.notes || null
    }
    
    if (editingId.value) {
      await accountsStore.updateAccount(editingId.value, accountData)
    } else {
      await accountsStore.createAccount(accountData)
    }
    
    closeModal()
  } catch (err) {
    error.value = err.response?.data?.detail || '操作失败，请重试'
  } finally {
    loading.value = false
  }
}

async function deleteAccount(id) {
  if (!confirm('确定要删除这个账号吗？')) {
    return
  }
  
  try {
    await accountsStore.deleteAccount(id)
  } catch (err) {
    error.value = err.response?.data?.detail || '删除失败，请重试'
  }
}

function handleLogout() {
  authStore.clearAuth()
  router.push('/login')
}
</script>
