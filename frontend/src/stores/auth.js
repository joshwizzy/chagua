import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))

  const isAuthenticated = computed(() => !!accessToken.value)
  const userRole = computed(() => user.value?.role || null)
  const isSeller = computed(() => userRole.value === 'SELLER')
  const isAdmin = computed(() => userRole.value === 'ADMIN')

  async function register(userData) {
    try {
      const response = await api.post('/users/register/', userData)
      setAuthData(response.data)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data || 'Registration failed' }
    }
  }

  async function login(credentials) {
    try {
      const response = await api.post('/users/login/', credentials)
      setAuthData(response.data)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data || 'Login failed' }
    }
  }

  async function logout() {
    try {
      await api.post('/users/logout/', { refresh_token: refreshToken.value })
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      clearAuthData()
    }
  }

  async function fetchProfile() {
    try {
      const response = await api.get('/users/profile/')
      user.value = response.data
    } catch (error) {
      console.error('Failed to fetch profile:', error)
    }
  }

  function setAuthData(data) {
    user.value = data.user
    accessToken.value = data.tokens.access
    refreshToken.value = data.tokens.refresh
    localStorage.setItem('access_token', data.tokens.access)
    localStorage.setItem('refresh_token', data.tokens.refresh)
    localStorage.setItem('user_role', data.user.role)
  }

  function clearAuthData() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_role')
  }

  return {
    user,
    isAuthenticated,
    userRole,
    isSeller,
    isAdmin,
    register,
    login,
    logout,
    fetchProfile
  }
})
