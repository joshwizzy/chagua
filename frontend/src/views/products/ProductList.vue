<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Products</h1>

      <!-- Filters -->
      <div class="flex gap-4 mb-8 flex-wrap">
        <select v-model="filters.category" class="form-select w-48">
          <option value="">All Categories</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>

        <input
          v-model="filters.search"
          type="text"
          placeholder="Search products..."
          @input="debouncedSearch"
          class="form-input flex-1 min-w-[200px]"
        />

        <select v-model="filters.availability" class="form-select w-48">
          <option value="">All Availability</option>
          <option value="IN_STOCK">In Stock</option>
          <option value="OUT_OF_STOCK">Out of Stock</option>
        </select>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading products...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="products.length === 0" class="text-center py-16">
        <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path>
        </svg>
        <p class="mt-4 text-xl text-gray-600">No products found</p>
      </div>

      <!-- Product Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div v-for="product in products" :key="product.id" class="card hover:-translate-y-1 transition-transform cursor-pointer">
          <router-link :to="`/products/${product.slug}`" class="block">
            <img
              v-if="product.primary_image"
              :src="product.primary_image"
              :alt="product.name"
              class="w-full h-56 object-cover"
            />
            <div v-else class="w-full h-56 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
              <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div class="p-4">
              <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-1">{{ product.name }}</h3>
              <p class="text-sm text-gray-600 mb-3 line-clamp-2">{{ truncateText(product.description, 80) }}</p>
              <div class="flex justify-between items-center mb-2">
                <span class="text-xl font-bold text-primary-600">{{ formatPrice(product.price) }}</span>
                <span v-if="product.average_rating" class="flex items-center gap-1 text-sm text-gray-600">
                  <span class="text-yellow-500">⭐</span>
                  {{ product.average_rating.toFixed(1) }}
                </span>
              </div>
              <span class="text-xs text-gray-500">by {{ product.seller_name }}</span>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProductsStore } from '../../stores/products'

const route = useRoute()
const productsStore = useProductsStore()

const filters = reactive({
  category: route.query.category || '',
  search: '',
  availability: ''
})

const products = ref([])
const categories = ref([])
const loading = ref(false)

let searchTimeout = null

onMounted(async () => {
  await productsStore.fetchCategories()
  categories.value = productsStore.categories
  await fetchProducts()
})

watch(filters, () => {
  fetchProducts()
})

async function fetchProducts() {
  loading.value = true
  await productsStore.fetchProducts(filters)
  products.value = productsStore.products
  loading.value = false
}

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchProducts()
  }, 500)
}

function formatPrice(price) {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}

function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>
