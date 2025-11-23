<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Product Management</h1>
          <p class="mt-2 text-sm text-gray-600">Moderate and manage all products</p>
        </div>
        <button @click="router.push('/admin/dashboard')" class="btn btn-secondary">
          ← Back to Dashboard
        </button>
      </div>

      <!-- Filters -->
      <div class="flex gap-4 mb-6">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search products..."
          class="form-input flex-1"
          @input="fetchProducts"
        />
        <select v-model="filters.is_active" @change="fetchProducts" class="form-select w-48">
          <option value="">All Status</option>
          <option value="true">Active</option>
          <option value="false">Inactive</option>
        </select>
        <select v-model="filters.is_featured" @change="fetchProducts" class="form-select w-48">
          <option value="">All Products</option>
          <option value="true">Featured</option>
          <option value="false">Not Featured</option>
        </select>
      </div>

      <!-- Products Table -->
      <div class="card">
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        <div v-else-if="products.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-500">No products found</p>
        </div>
        <div v-else>
          <div class="overflow-x-auto">
            <table class="table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Seller</th>
                  <th>Category</th>
                  <th>Price</th>
                  <th>Stock</th>
                  <th>Status</th>
                  <th>Featured</th>
                  <th>Views</th>
                  <th>Sales</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in products" :key="product.id">
                  <td class="font-medium text-gray-900">{{ product.name }}</td>
                  <td class="text-gray-600">{{ product.seller_name }}</td>
                  <td class="text-gray-600">{{ product.category_name || 'N/A' }}</td>
                  <td class="font-semibold">{{ product.price }}</td>
                  <td>{{ product.stock_quantity }}</td>
                  <td>
                    <span :class="[
                      'badge',
                      product.is_active ? 'badge-success' : 'badge-danger'
                    ]">
                      {{ product.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td>
                    <span v-if="product.is_featured" class="text-yellow-500 text-xl">⭐</span>
                    <span v-else class="text-gray-300">-</span>
                  </td>
                  <td class="text-gray-600">{{ product.views_count }}</td>
                  <td class="text-gray-600">{{ product.sales_count }}</td>
                  <td>
                    <button @click="editProduct(product)" class="btn btn-primary btn-sm">
                      Edit
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="totalCount > 0" class="px-6 py-4 border-t border-gray-200 text-sm text-gray-600">
            Showing {{ products.length }} of {{ totalCount }} products
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Product Modal -->
    <div v-if="selectedProduct" class="modal-overlay" @click.self="selectedProduct = null">
      <div class="modal-content w-full max-w-lg">
        <div class="modal-header">
          <h2 class="text-xl font-bold">Moderate Product</h2>
          <button @click="selectedProduct = null" class="text-gray-400 hover:text-gray-600 text-3xl font-light leading-none">&times;</button>
        </div>
        <div class="modal-body space-y-4">
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ selectedProduct.name }}</h3>
            <div class="space-y-2 text-sm">
              <p><span class="font-medium text-gray-600">Seller:</span> {{ selectedProduct.seller_name }}</p>
              <p><span class="font-medium text-gray-600">Price:</span> {{ selectedProduct.price }}</p>
              <p><span class="font-medium text-gray-600">Stock:</span> {{ selectedProduct.stock_quantity }}</p>
              <p><span class="font-medium text-gray-600">Views:</span> {{ selectedProduct.views_count }}</p>
              <p><span class="font-medium text-gray-600">Sales:</span> {{ selectedProduct.sales_count }}</p>
            </div>
          </div>

          <div class="border-t pt-4 space-y-3">
            <label class="flex items-center space-x-2 cursor-pointer">
              <input type="checkbox" v-model="selectedProduct.is_active" class="w-4 h-4 text-primary-600 rounded" />
              <span class="text-sm font-medium text-gray-700">Active (Visible to buyers)</span>
            </label>
            <label class="flex items-center space-x-2 cursor-pointer">
              <input type="checkbox" v-model="selectedProduct.is_featured" class="w-4 h-4 text-primary-600 rounded" />
              <span class="text-sm font-medium text-gray-700">Featured (Show on homepage)</span>
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="deleteProduct" class="btn btn-danger">Delete Product</button>
          <button @click="selectedProduct = null" class="btn btn-secondary">Cancel</button>
          <button @click="updateProduct" class="btn btn-primary">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'

const router = useRouter()
const loading = ref(true)
const products = ref([])
const totalCount = ref(0)
const selectedProduct = ref(null)

const filters = ref({
  search: '',
  is_active: '',
  is_featured: ''
})

onMounted(() => {
  fetchProducts()
})

async function fetchProducts() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.is_active) params.is_active = filters.value.is_active
    if (filters.value.is_featured) params.is_featured = filters.value.is_featured

    const response = await api.get('/users/admin/products/', { params })
    products.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to fetch products:', error)
    alert('Failed to fetch products')
  } finally {
    loading.value = false
  }
}

function editProduct(product) {
  selectedProduct.value = { ...product }
}

async function updateProduct() {
  try {
    await api.put(`/users/admin/products/${selectedProduct.value.id}/`, {
      is_active: selectedProduct.value.is_active,
      is_featured: selectedProduct.value.is_featured
    })
    alert('Product updated successfully')
    selectedProduct.value = null
    fetchProducts()
  } catch (error) {
    console.error('Failed to update product:', error)
    alert('Failed to update product')
  }
}

async function deleteProduct() {
  if (!confirm('Are you sure you want to delete this product? This action cannot be undone.')) {
    return
  }
  try {
    await api.delete(`/users/admin/products/${selectedProduct.value.id}/`)
    alert('Product deleted successfully')
    selectedProduct.value = null
    fetchProducts()
  } catch (error) {
    console.error('Failed to delete product:', error)
    alert('Failed to delete product')
  }
}
</script>
