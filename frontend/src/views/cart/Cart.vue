<template>
  <div class="cart-page">
    <div class="container">
      <h1>Shopping Cart</h1>

      <div v-if="loading" class="loading">Loading cart...</div>

      <div v-else-if="!cart || items.length === 0" class="empty-cart">
        <p>Your cart is empty</p>
        <router-link to="/products" class="btn btn-primary">Continue Shopping</router-link>
      </div>

      <div v-else class="cart-layout">
        <div class="cart-items">
          <div v-for="item in items" :key="item.id" class="cart-item">
            <img :src="item.product_image" :alt="item.product_name" />
            <div class="item-details">
              <h3>{{ item.product_name }}</h3>
              <p class="price">{{ formatPrice(item.unit_price) }}</p>
              <div class="quantity-control">
                <button @click="updateQuantity(item.id, item.quantity - 1)">-</button>
                <span>{{ item.quantity }}</span>
                <button @click="updateQuantity(item.id, item.quantity + 1)">+</button>
              </div>
            </div>
            <div class="item-actions">
              <p class="subtotal">{{ formatPrice(item.subtotal) }}</p>
              <button @click="removeItem(item.id)" class="remove-btn">Remove</button>
            </div>
          </div>
        </div>

        <div class="cart-summary">
          <h2>Order Summary</h2>
          <div class="summary-row">
            <span>Items ({{ itemsCount }})</span>
            <span>{{ formatPrice(total) }}</span>
          </div>
          <div class="summary-total">
            <span>Total</span>
            <span>{{ formatPrice(total) }}</span>
          </div>
          <button @click="proceedToCheckout" class="btn btn-primary btn-full">
            Proceed to Checkout
          </button>
          <button @click="handleClearCart" class="btn btn-secondary btn-full">
            Clear Cart
          </button>
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

<style scoped>
.cart-page {
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

.loading, .empty-cart {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 1rem;
}

.empty-cart p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.cart-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
}

.cart-items {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
}

.cart-item {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem 0;
  border-bottom: 1px solid #eee;
}

.cart-item:last-child {
  border-bottom: none;
}

.cart-item img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.item-details {
  flex: 1;
}

.item-details h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.price {
  color: #667eea;
  font-weight: 600;
  margin-bottom: 1rem;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quantity-control button {
  width: 32px;
  height: 32px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 1.2rem;
}

.quantity-control button:hover {
  background: #f5f5f5;
}

.quantity-control span {
  min-width: 40px;
  text-align: center;
  font-weight: 600;
}

.item-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
}

.subtotal {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.remove-btn {
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}

.remove-btn:hover {
  color: #991b1b;
}

.cart-summary {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  height: fit-content;
}

.cart-summary h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  color: #666;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  padding-top: 1rem;
  border-top: 2px solid #eee;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #333;
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

.btn-full {
  width: 100%;
  margin-bottom: 0.75rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  border: 2px solid #ddd;
  color: #666;
}

.btn-secondary:hover {
  border-color: #999;
  color: #333;
}
</style>
