<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <header class="bg-gradient-to-br from-primary-500 to-purple-700 text-white py-16 px-8 text-center">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold mb-4">{{ $t('app.name') }}</h1>
        <p class="text-xl md:text-2xl mb-8">{{ $t('app.tagline') }}</p>
        <div class="flex gap-4 justify-center flex-wrap">
          <router-link to="/products" class="bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold transition-all hover:-translate-y-1 shadow-lg">
            Shop Now
          </router-link>
          <router-link v-if="!auth.isAuthenticated" to="/register" class="bg-transparent border-2 border-white text-white hover:bg-white hover:text-primary-600 px-8 py-3 rounded-lg font-semibold transition-all hover:-translate-y-1">
            Become a Seller
          </router-link>
        </div>
      </div>
    </header>

    <!-- Categories Section -->
    <section class="py-16 px-8 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl font-bold text-center mb-12 text-gray-900">Shop by Category</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          <div v-for="category in categories" :key="category.id" class="card hover:-translate-y-1 transition-transform cursor-pointer">
            <router-link :to="`/products?category=${category.id}`" class="block">
              <img v-if="category.icon" :src="category.icon" :alt="category.name" class="w-full h-40 object-cover" />
              <div v-else class="w-full h-40 bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
                <span class="text-4xl">📦</span>
              </div>
              <h3 class="p-4 font-semibold text-gray-900 text-center">{{ category.name }}</h3>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Products Section -->
    <section class="py-16 px-8 bg-white">
      <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl md:text-4xl font-bold text-center mb-12 text-gray-900">Featured Products</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <div v-for="product in featuredProducts" :key="product.id" class="card hover:-translate-y-1 transition-transform cursor-pointer">
            <router-link :to="`/products/${product.slug}`" class="block">
              <img v-if="product.primary_image" :src="product.primary_image" :alt="product.name" class="w-full h-48 object-cover" />
              <div v-else class="w-full h-48 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="p-4">
                <h3 class="font-semibold text-gray-900 mb-2 line-clamp-2">{{ product.name }}</h3>
                <p class="text-xl font-bold text-primary-600 mb-2">{{ formatPrice(product.price) }}</p>
                <div v-if="product.average_rating" class="flex items-center gap-1 text-sm text-gray-600">
                  <span class="text-yellow-500">⭐</span>
                  <span>{{ product.average_rating.toFixed(1) }}</span>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useProductsStore } from '../stores/products'

const auth = useAuthStore()
const productsStore = useProductsStore()

const categories = ref([])
const featuredProducts = ref([])

onMounted(async () => {
  await productsStore.fetchCategories()
  categories.value = productsStore.categories
  featuredProducts.value = await productsStore.fetchFeaturedProducts()
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}
</script>
