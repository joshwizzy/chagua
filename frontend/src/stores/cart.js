import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useCartStore = defineStore('cart', () => {
  const cart = ref(null)
  const loading = ref(false)

  const itemsCount = computed(() => cart.value?.items_count || 0)
  const total = computed(() => cart.value?.total || 0)
  const items = computed(() => cart.value?.items || [])

  async function fetchCart() {
    loading.value = true
    try {
      const response = await api.get('/orders/cart/')
      cart.value = response.data
      return { success: true }
    } catch (error) {
      console.error('Failed to fetch cart:', error)
      return { success: false }
    } finally {
      loading.value = false
    }
  }

  async function addToCart(productId, quantity = 1, variantId = null) {
    try {
      const response = await api.post('/orders/cart/add/', {
        product_id: productId,
        quantity,
        variant_id: variantId
      })
      cart.value = response.data
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  async function updateCartItem(itemId, quantity) {
    try {
      const response = await api.put(`/orders/cart/items/${itemId}/`, { quantity })
      await fetchCart()
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  async function removeFromCart(itemId) {
    try {
      await api.delete(`/orders/cart/items/${itemId}/remove/`)
      await fetchCart()
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  async function clearCart() {
    try {
      await api.post('/orders/cart/clear/')
      cart.value = null
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data }
    }
  }

  return {
    cart,
    loading,
    itemsCount,
    total,
    items,
    fetchCart,
    addToCart,
    updateCartItem,
    removeFromCart,
    clearCart
  }
})
