import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useOrdersStore = defineStore('orders', () => {
  const orders = ref([])
  const currentOrder = ref(null)
  const loading = ref(false)

  async function fetchOrders() {
    loading.value = true
    try {
      const response = await api.get('/orders/')
      orders.value = response.data.results || response.data
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    } finally {
      loading.value = false
    }
  }

  async function fetchOrderByTrackingNumber(trackingNumber) {
    loading.value = true
    try {
      const response = await api.get(`/orders/${trackingNumber}/`)
      currentOrder.value = response.data
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data }
    } finally {
      loading.value = false
    }
  }

  async function createOrder(orderData) {
    try {
      const response = await api.post('/orders/create/', orderData)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  async function trackOrder(trackingNumber) {
    try {
      const response = await api.get(`/orders/track/${trackingNumber}/`)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  async function updateOrderStatus(orderId, statusData) {
    try {
      const response = await api.post(`/orders/${orderId}/status/`, statusData)
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  async function cancelOrder(orderId, reason = '') {
    try {
      await api.post(`/orders/${orderId}/cancel/`, { reason })
      await fetchOrders()
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  return {
    orders,
    currentOrder,
    loading,
    fetchOrders,
    fetchOrderByTrackingNumber,
    createOrder,
    trackOrder,
    updateOrderStatus,
    cancelOrder
  }
})
