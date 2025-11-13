<template>
  <div class="product-detail-page">
    <div v-if="loading" class="loading">Loading...</div>

    <div v-else-if="product" class="container">
      <div class="product-layout">
        <div class="product-images">
          <img :src="primaryImage" :alt="product.name" class="main-image" />
          <div class="thumbnail-grid">
            <img
              v-for="(image, index) in product.images"
              :key="index"
              :src="image.image"
              :alt="image.alt_text || product.name"
              class="thumbnail"
              @click="primaryImage = image.image"
            />
          </div>
        </div>

        <div class="product-details">
          <h1>{{ product.name }}</h1>
          <p class="seller">Sold by {{ product.seller_name }}</p>

          <div class="rating" v-if="product.average_rating">
            ⭐ {{ product.average_rating.toFixed(1) }} / 5.0
          </div>

          <div class="price">{{ formatPrice(product.price) }}</div>

          <div class="availability">
            <span :class="['status', product.availability.toLowerCase()]">
              {{ product.availability.replace('_', ' ') }}
            </span>
            <span v-if="product.stock_quantity > 0" class="stock">
              {{ product.stock_quantity }} items available
            </span>
          </div>

          <div class="description">
            <h3>Description</h3>
            <p>{{ product.description }}</p>
          </div>

          <div v-if="product.variants && product.variants.length > 0" class="variants">
            <h3>Options</h3>
            <div v-for="variant in product.variants" :key="variant.id" class="variant-option">
              <label>
                <input
                  type="radio"
                  :name="`variant-${variant.attribute}`"
                  :value="variant.id"
                  v-model="selectedVariant"
                />
                {{ variant.attribute_name }}: {{ variant.value }}
                <span v-if="variant.price_adjustment !== '0.00'">
                  (+{{ formatPrice(variant.price_adjustment) }})
                </span>
              </label>
            </div>
          </div>

          <div class="quantity-selector">
            <label>Quantity:</label>
            <input type="number" v-model.number="quantity" min="1" :max="product.stock_quantity" />
          </div>

          <div class="actions">
            <button
              @click="handleAddToCart"
              class="btn btn-primary"
              :disabled="product.availability === 'OUT_OF_STOCK' || addingToCart"
            >
              {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
            </button>
            <button @click="toggleSave" class="btn btn-secondary">
              {{ isSaved ? '❤️ Saved' : '🤍 Save' }}
            </button>
          </div>

          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProductsStore } from '../../stores/products'
import { useCartStore } from '../../stores/cart'

const route = useRoute()
const productsStore = useProductsStore()
const cartStore = useCartStore()

const product = ref(null)
const loading = ref(true)
const selectedVariant = ref(null)
const quantity = ref(1)
const addingToCart = ref(false)
const isSaved = ref(false)
const successMessage = ref('')

const primaryImage = ref('')

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}

onMounted(async () => {
  const result = await productsStore.fetchProductBySlug(route.params.slug)
  if (result.success) {
    product.value = result.data
    if (product.value.images && product.value.images.length > 0) {
      const primary = product.value.images.find(img => img.is_primary)
      primaryImage.value = primary ? primary.image : product.value.images[0].image
    }
  }
  loading.value = false
})

async function handleAddToCart() {
  addingToCart.value = true
  successMessage.value = ''

  const result = await cartStore.addToCart(
    product.value.id,
    quantity.value,
    selectedVariant.value
  )

  if (result.success) {
    successMessage.value = '✓ Added to cart successfully!'
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  }

  addingToCart.value = false
}

async function toggleSave() {
  const result = await productsStore.toggleSaveProduct(product.value.id)
  if (result.success) {
    isSaved.value = result.data.is_saved
  }
}
</script>

<style scoped>
.product-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.loading {
  text-align: center;
  padding: 4rem;
  font-size: 1.2rem;
}

.product-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  background: white;
  padding: 2rem;
  border-radius: 1rem;
}

@media (max-width: 768px) {
  .product-layout {
    grid-template-columns: 1fr;
  }
}

.product-images .main-image {
  width: 100%;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.thumbnail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 0.5rem;
}

.thumbnail {
  width: 100%;
  height: 80px;
  object-fit: cover;
  border-radius: 0.25rem;
  cursor: pointer;
  border: 2px solid transparent;
}

.thumbnail:hover {
  border-color: #667eea;
}

.product-details h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.seller {
  color: #666;
  margin-bottom: 1rem;
}

.rating {
  color: #f59e0b;
  margin-bottom: 1rem;
}

.price {
  font-size: 2rem;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 1rem;
}

.availability {
  margin-bottom: 1.5rem;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-weight: 500;
  text-transform: uppercase;
  font-size: 0.85rem;
}

.status.in_stock {
  background: #d1fae5;
  color: #065f46;
}

.status.out_of_stock {
  background: #fee2e2;
  color: #991b1b;
}

.stock {
  margin-left: 1rem;
  color: #666;
}

.description {
  margin-bottom: 2rem;
}

.description h3 {
  margin-bottom: 0.5rem;
}

.description p {
  line-height: 1.6;
  color: #555;
}

.variants {
  margin-bottom: 1.5rem;
}

.variants h3 {
  margin-bottom: 0.75rem;
}

.variant-option {
  margin-bottom: 0.5rem;
}

.variant-option label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.variant-option input[type="radio"] {
  margin-right: 0.5rem;
}

.quantity-selector {
  margin-bottom: 1.5rem;
}

.quantity-selector label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.quantity-selector input {
  width: 100px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  flex: 1;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

.success-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #d1fae5;
  color: #065f46;
  border-radius: 0.5rem;
}
</style>
