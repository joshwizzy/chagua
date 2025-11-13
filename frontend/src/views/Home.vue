<template>
  <div class="home">
    <header class="hero">
      <div class="container">
        <h1>{{ $t('app.name') }}</h1>
        <p>{{ $t('app.tagline') }}</p>
        <div class="cta-buttons">
          <router-link to="/products" class="btn btn-primary">Shop Now</router-link>
          <router-link v-if="!auth.isAuthenticated" to="/register" class="btn btn-secondary">Become a Seller</router-link>
        </div>
      </div>
    </header>

    <section class="categories">
      <div class="container">
        <h2>Shop by Category</h2>
        <div class="category-grid">
          <div v-for="category in categories" :key="category.id" class="category-card">
            <router-link :to="`/products?category=${category.id}`">
              <img v-if="category.icon" :src="category.icon" :alt="category.name" />
              <h3>{{ category.name }}</h3>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <section class="featured-products">
      <div class="container">
        <h2>Featured Products</h2>
        <div class="product-grid">
          <div v-for="product in featuredProducts" :key="product.id" class="product-card">
            <router-link :to="`/products/${product.slug}`">
              <img v-if="product.primary_image" :src="product.primary_image" :alt="product.name" />
              <h3>{{ product.name }}</h3>
              <p class="price">{{ formatPrice(product.price) }}</p>
              <div class="rating" v-if="product.average_rating">
                ⭐ {{ product.average_rating.toFixed(1) }}
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

<style scoped>
.home {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  background: white;
  color: #667eea;
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

section {
  padding: 4rem 2rem;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
}

.category-grid, .product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 2rem;
}

.category-card, .product-card {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.2s;
}

.category-card:hover, .product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.category-card a, .product-card a {
  text-decoration: none;
  color: inherit;
}

.category-card img, .product-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.category-card h3, .product-card h3 {
  padding: 1rem;
  font-size: 1.1rem;
}

.product-card .price {
  padding: 0 1rem 1rem;
  font-weight: 600;
  color: #667eea;
  font-size: 1.2rem;
}

.rating {
  padding: 0 1rem 1rem;
  color: #666;
}
</style>
