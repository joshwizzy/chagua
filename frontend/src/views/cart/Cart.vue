<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

      <div v-if="loading" class="text-center py-16 bg-white rounded-lg">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading cart...</p>
      </div>

      <div v-else-if="!cart || items.length === 0" class="text-center py-16 bg-white rounded-lg">
        <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
        </svg>
        <p class="mt-4 text-xl text-gray-600">Your cart is empty</p>
        <router-link to="/products" class="btn btn-primary mt-8 inline-block">
          Continue Shopping
        </router-link>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2">
          <div class="card">
            <div class="card-body divide-y divide-gray-200">
              <div v-for="item in items" :key="item.id" class="flex gap-6 py-6 first:pt-0">
                <img
                  :src="item.product_image"
                  :alt="item.product_name"
                  class="w-28 h-28 object-cover rounded-lg flex-shrink-0"
                />
                <div class="flex-1 flex flex-col justify-between">
                  <div>
                    <h3 class="text-lg font-semibold text-gray-900">{{ item.product_name }}</h3>
                    <p class="mt-1 text-primary-600 font-semibold">{{ formatPrice(item.unit_price) }}</p>
                  </div>
                  <div class="flex items-center gap-2">
                    <button
                      @click="updateQuantity(item.id, item.quantity - 1)"
                      class="w-8 h-8 flex items-center justify-center border border-gray-300 rounded hover:bg-gray-50 transition-colors"
                    >
                      -
                    </button>
                    <span class="w-12 text-center font-semibold">{{ item.quantity }}</span>
                    <button
                      @click="updateQuantity(item.id, item.quantity + 1)"
                      class="w-8 h-8 flex items-center justify-center border border-gray-300 rounded hover:bg-gray-50 transition-colors"
                    >
                      +
                    </button>
                  </div>
                </div>
                <div class="flex flex-col items-end justify-between">
                  <p class="text-lg font-semibold text-gray-900">{{ formatPrice(item.subtotal) }}</p>
                  <button
                    @click="removeItem(item.id)"
                    class="text-red-600 hover:text-red-800 underline text-sm font-medium"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <div class="card sticky top-8">
            <div class="card-body">
              <h2 class="text-xl font-semibold text-gray-900 mb-6">Order Summary</h2>

              <div class="flex justify-between mb-4 text-gray-600">
                <span>Items ({{ itemsCount }})</span>
                <span>{{ formatPrice(total) }}</span>
              </div>

              <div class="flex justify-between pt-4 border-t-2 border-gray-200 text-lg font-semibold text-gray-900 mb-6">
                <span>Total</span>
                <span>{{ formatPrice(total) }}</span>
              </div>

              <button @click="proceedToCheckout" class="btn btn-primary w-full mb-3">
                Proceed to Checkout
              </button>
              <button @click="handleClearCart" class="btn btn-secondary w-full">
                Clear Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../../stores/cart'

const router = useRouter()
const cartStore = useCartStore()

const cart = computed(() => cartStore.cart)
const items = computed(() => cartStore.items)
const itemsCount = computed(() => cartStore.itemsCount)
const total = computed(() => cartStore.total)
const loading = computed(() => cartStore.loading)

onMounted(async () => {
  await cartStore.fetchCart()
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}

async function updateQuantity(itemId, newQuantity) {
  if (newQuantity < 1) return
  await cartStore.updateCartItem(itemId, newQuantity)
}

async function removeItem(itemId) {
  if (confirm('Remove this item from cart?')) {
    await cartStore.removeFromCart(itemId)
  }
}

async function handleClearCart() {
  if (confirm('Clear all items from cart?')) {
    await cartStore.clearCart()
  }
}

function proceedToCheckout() {
  router.push('/checkout')
}
</script>
