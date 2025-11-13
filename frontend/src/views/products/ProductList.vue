<template>
  <div class="products-page">
    <div class="container">
      <h1>Products</h1>

      <div class="filters">
        <select v-model="filters.category">
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
        />

        <select v-model="filters.availability">
          <option value="">All Availability</option>
          <option value="IN_STOCK">In Stock</option>
          <option value="OUT_OF_STOCK">Out of Stock</option>
        </select>
      </div>

      <div v-if="loading" class="loading">
        Loading products...
      </div>

      <div v-else-if="products.length === 0" class="no-products">
        No products found
      </div>

      <div v-else class="product-grid">
        <div v-for="product in products" :key="product.id" class="product-card">
          <router-link :to="`/products/${product.slug}`">
            <img v-if="product.primary_image" :src="product.primary_image" :alt="product.name" />
            <div class="product-info">
              <h3>{{ product.name }}</h3>
              <p class="description">{{ truncateText(product.description, 80) }}</p>
              <div class="product-meta">
                <span class="price">{{ formatPrice(product.price) }}</span>
                <span v-if="product.average_rating" class="rating">
                  ⭐ {{ product.average_rating.toFixed(1) }}
                </span>
              </div>
              <span class="seller">by {{ product.seller_name }}</span>
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

<style scoped>
.products-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: #333;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filters select,
.filters input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 1rem;
  background: white;
}

.filters input {
  flex: 1;
  min-width: 200px;
}

.loading,
.no-products {
  text-align: center;
  padding: 4rem;
  color: #666;
  font-size: 1.2rem;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
}

.product-card {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.product-card a {
  text-decoration: none;
  color: inherit;
}

.product-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.product-info {
  padding: 1rem;
}

.product-info h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.description {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.price {
  font-weight: 600;
  color: #667eea;
  font-size: 1.2rem;
}

.rating {
  color: #666;
  font-size: 0.9rem;
}

.seller {
  color: #999;
  font-size: 0.85rem;
}
</style>
