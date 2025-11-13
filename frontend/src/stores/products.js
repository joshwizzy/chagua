import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useProductsStore = defineStore('products', () => {
  const products = ref([])
  const currentProduct = ref(null)
  const categories = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchProducts(params = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/products/', { params })
      products.value = response.data.results || response.data
      return { success: true }
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch products'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchProductBySlug(slug) {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/products/${slug}/`)
      currentProduct.value = response.data
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data || 'Failed to fetch product'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    try {
      const response = await api.get('/products/categories/')
      categories.value = response.data
    } catch (err) {
      console.error('Failed to fetch categories:', err)
    }
  }

  async function fetchFeaturedProducts() {
    try {
      const response = await api.get('/products/featured/')
      return response.data
    } catch (err) {
      console.error('Failed to fetch featured products:', err)
      return []
    }
  }

  async function fetchPopularProducts() {
    try {
      const response = await api.get('/products/popular/')
      return response.data
    } catch (err) {
      console.error('Failed to fetch popular products:', err)
      return []
    }
  }

  async function toggleSaveProduct(productId) {
    try {
      const response = await api.post(`/products/${productId}/toggle-save/`)
      return { success: true, data: response.data }
    } catch (err) {
      return { success: false, error: err.response?.data }
    }
  }

  return {
    products,
    currentProduct,
    categories,
    loading,
    error,
    fetchProducts,
    fetchProductBySlug,
    fetchCategories,
    fetchFeaturedProducts,
    fetchPopularProducts,
    toggleSaveProduct
  }
})
