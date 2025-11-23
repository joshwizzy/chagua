<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div v-if="loading" class="text-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">Loading product...</p>
    </div>

    <div v-else-if="product" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 bg-white p-8 rounded-2xl shadow-md">
        <!-- Product Images -->
        <div>
          <img :src="primaryImage" :alt="product.name" class="w-full rounded-lg mb-4" />
          <div class="grid grid-cols-4 gap-2">
            <img
              v-for="(image, index) in product.images"
              :key="index"
              :src="image.image"
              :alt="image.alt_text || product.name"
              class="w-full h-20 object-cover rounded cursor-pointer border-2 border-transparent hover:border-primary-500 transition-colors"
              @click="primaryImage = image.image"
            />
          </div>
        </div>

        <!-- Product Details -->
        <div class="space-y-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ product.name }}</h1>
            <p class="text-gray-600">Sold by {{ product.seller_name }}</p>
          </div>

          <div v-if="product.average_rating" class="flex items-center gap-2 text-yellow-500">
            ⭐ <span class="text-gray-700">{{ product.average_rating.toFixed(1) }} / 5.0</span>
          </div>

          <div class="text-3xl font-bold text-primary-600">{{ formatPrice(product.price) }}</div>

          <div class="flex items-center gap-4">
            <span :class="[
              'px-3 py-1 rounded font-medium uppercase text-sm',
              product.availability === 'IN_STOCK' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            ]">
              {{ product.availability.replace('_', ' ') }}
            </span>
            <span v-if="product.stock_quantity > 0" class="text-gray-600">
              {{ product.stock_quantity }} items available
            </span>
          </div>

          <div class="border-t border-gray-200 pt-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Description</h3>
            <p class="text-gray-700 leading-relaxed">{{ product.description }}</p>
          </div>

          <div v-if="product.variants && product.variants.length > 0" class="border-t border-gray-200 pt-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Options</h3>
            <div class="space-y-2">
              <label v-for="variant in product.variants" :key="variant.id" class="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  :name="`variant-${variant.attribute}`"
                  :value="variant.id"
                  v-model="selectedVariant"
                  class="w-4 h-4 text-primary-600"
                />
                <span class="text-gray-700">
                  {{ variant.attribute_name }}: {{ variant.value }}
                  <span v-if="variant.price_adjustment !== '0.00'" class="text-primary-600">
                    (+{{ formatPrice(variant.price_adjustment) }})
                  </span>
                </span>
              </label>
            </div>
          </div>

          <div class="border-t border-gray-200 pt-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Quantity:</label>
            <input
              type="number"
              v-model.number="quantity"
              min="1"
              :max="product.stock_quantity"
              class="w-24 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div class="flex gap-4">
            <button
              @click="handleAddToCart"
              class="btn btn-primary flex-1"
              :disabled="product.availability === 'OUT_OF_STOCK' || addingToCart"
            >
              {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
            </button>
            <button
              @click="toggleSave"
              class="btn btn-secondary px-6"
            >
              {{ isSaved ? '❤️ Saved' : '🤍 Save' }}
            </button>
          </div>

          <div v-if="successMessage" class="p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg">
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
