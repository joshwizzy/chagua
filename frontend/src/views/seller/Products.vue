<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">My Products</h1>
          <p class="mt-2 text-sm text-gray-600">Manage your product listings</p>
        </div>
        <router-link to="/seller/products/create" class="btn btn-primary">
          + Add New Product
        </router-link>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <!-- Empty State -->
      <div v-else-if="products.length === 0" class="text-center py-12">
        <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
        </svg>
        <h3 class="mt-4 text-lg font-medium text-gray-900">No products yet</h3>
        <p class="mt-2 text-gray-600">Get started by adding your first product</p>
        <router-link to="/seller/products/create" class="btn btn-primary mt-6 inline-block">
          Add Your First Product
        </router-link>
      </div>

      <!-- Products Table -->
      <div v-else class="card">
        <div class="overflow-x-auto">
          <table class="table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Category</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Status</th>
                <th>Views</th>
                <th>Sales</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in products" :key="product.id">
                <td>
                  <div class="flex items-center space-x-3">
                    <img
                      v-if="product.primary_image"
                      :src="product.primary_image"
                      :alt="product.name"
                      class="w-12 h-12 rounded-lg object-cover"
                    />
                    <div v-else class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center">
                      <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                      </svg>
                    </div>
                    <span class="font-medium text-gray-900">{{ product.name }}</span>
                  </div>
                </td>
                <td class="text-gray-600">{{ product.category_name || 'Uncategorized' }}</td>
                <td class="font-semibold text-gray-900">{{ formatPrice(product.price) }}</td>
                <td>
                  <span :class="[
                    'px-2 py-1 rounded text-sm font-medium',
                    product.stock_quantity > 10 ? 'bg-green-100 text-green-800' :
                    product.stock_quantity > 0 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  ]">
                    {{ product.stock_quantity }}
                  </span>
                </td>
                <td>
                  <span :class="[
                    'status-badge',
                    product.availability === 'IN_STOCK' ? 'badge-success' :
                    product.availability === 'LOW_STOCK' ? 'badge-warning' :
                    'badge-danger'
                  ]">
                    {{ product.availability.replace('_', ' ') }}
                  </span>
                </td>
                <td class="text-gray-600">{{ product.views_count }}</td>
                <td class="text-gray-600">{{ product.sales_count }}</td>
                <td>
                  <div class="flex gap-2">
                    <router-link
                      :to="`/seller/products/edit/${product.id}`"
                      class="btn btn-primary btn-sm"
                    >
                      Edit
                    </router-link>
                    <button
                      @click="handleDelete(product.id)"
                      class="btn btn-danger btn-sm"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const products = ref([])
const loading = ref(true)

onMounted(async () => {
  await fetchProducts()
})

async function fetchProducts() {
  loading.value = true
  try {
    const response = await api.get('/products/seller/products/')
    products.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch products:', error)
  } finally {
    loading.value = false
  }
}

async function handleDelete(productId) {
  if (!confirm('Are you sure you want to delete this product?')) {
    return
  }

  try {
    await api.delete(`/products/seller/products/${productId}/`)
    await fetchProducts()
  } catch (error) {
    console.error('Failed to delete product:', error)
    alert('Failed to delete product')
  }
}

function formatPrice(price) {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}
</script>
