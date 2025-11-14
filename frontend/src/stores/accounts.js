import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useAccountsStore = defineStore('accounts', () => {
  const accounts = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchAccounts() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/accounts/')
      accounts.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '获取账号列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createAccount(accountData) {
    loading.value = true
    error.value = null
    try {
      const response = await api.post('/accounts/', accountData)
      accounts.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '创建账号失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateAccount(id, accountData) {
    loading.value = true
    error.value = null
    try {
      const response = await api.put(`/accounts/${id}`, accountData)
      const index = accounts.value.findIndex(acc => acc.id === id)
      if (index !== -1) {
        accounts.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || '更新账号失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteAccount(id) {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/accounts/${id}`)
      accounts.value = accounts.value.filter(acc => acc.id !== id)
    } catch (err) {
      error.value = err.response?.data?.detail || '删除账号失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    accounts,
    loading,
    error,
    fetchAccounts,
    createAccount,
    updateAccount,
    deleteAccount
  }
})
