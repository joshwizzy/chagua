<template>
  <div class="checkout-page">
    <div class="container">
      <h1>Checkout</h1>

      <div class="checkout-layout">
        <div class="checkout-main">
          <!-- Step 1: Delivery Address -->
          <section class="checkout-section">
            <h2>1. Delivery Address</h2>

            <div v-if="addresses.length > 0" class="address-selection">
              <div
                v-for="address in addresses"
                :key="address.id"
                :class="['address-card', { selected: selectedAddress === address.id }]"
                @click="selectedAddress = address.id"
              >
                <input type="radio" :value="address.id" v-model="selectedAddress" />
                <div class="address-details">
                  <strong>{{ address.label }}</strong>
                  <p>{{ address.recipient_name }} - {{ address.phone_number }}</p>
                  <p>{{ address.address_line1 }}</p>
                  <p v-if="address.address_line2">{{ address.address_line2 }}</p>
                  <p>{{ address.city }}, {{ address.country }}</p>
                </div>
              </div>
            </div>

            <button @click="showAddressForm = true" class="btn btn-secondary">
              + Add New Address
            </button>

            <!-- Add Address Form -->
            <div v-if="showAddressForm" class="address-form">
              <h3>New Delivery Address</h3>
              <form @submit.prevent="handleAddAddress">
                <div class="form-row">
                  <div class="form-group">
                    <label>Label (e.g., Home, Office)*</label>
                    <input v-model="newAddress.label" type="text" required />
                  </div>
                  <div class="form-group">
                    <label>Recipient Name*</label>
                    <input v-model="newAddress.recipient_name" type="text" required />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>Phone Number*</label>
                    <input v-model="newAddress.phone_number" type="tel" required />
                  </div>
                  <div class="form-group">
                    <label>Country*</label>
                    <select v-model="newAddress.country" required>
                      <option value="UG">Uganda</option>
                      <option value="RW">Rwanda</option>
                      <option value="BI">Burundi</option>
                    </select>
                  </div>
                </div>

                <div class="form-group">
                  <label>City*</label>
                  <input v-model="newAddress.city" type="text" required />
                </div>

                <div class="form-group">
                  <label>Address Line 1*</label>
                  <input v-model="newAddress.address_line1" type="text" required />
                </div>

                <div class="form-group">
                  <label>Address Line 2</label>
                  <input v-model="newAddress.address_line2" type="text" />
                </div>

                <div class="form-actions">
                  <button type="submit" class="btn btn-primary">Save Address</button>
                  <button type="button" @click="showAddressForm = false" class="btn btn-secondary">
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </section>

          <!-- Step 2: Payment Method -->
          <section class="checkout-section">
            <h2>2. Payment Method</h2>

            <div class="payment-options">
              <label class="payment-option">
                <input type="radio" v-model="paymentMethod" value="CASH_ON_DELIVERY" />
                <div class="payment-details">
                  <strong>Cash on Delivery</strong>
                  <p>Pay when you receive your order</p>
                </div>
              </label>

              <label class="payment-option">
                <input type="radio" v-model="paymentMethod" value="AIRTEL_MONEY" />
                <div class="payment-details">
                  <strong>Airtel Money</strong>
                  <p>Pay with Airtel Mobile Money</p>
                </div>
              </label>

              <label class="payment-option">
                <input type="radio" v-model="paymentMethod" value="MTN_MOBILE_MONEY" />
                <div class="payment-details">
                  <strong>MTN Mobile Money</strong>
                  <p>Pay with MTN Mobile Money</p>
                </div>
              </label>
            </div>

            <div v-if="paymentMethod !== 'CASH_ON_DELIVERY'" class="mobile-money-input">
              <label>Mobile Money Number</label>
              <input v-model="mobileMoneyNumber" type="tel" placeholder="+256XXXXXXXXX" />
            </div>
          </section>

          <!-- Step 3: Order Notes -->
          <section class="checkout-section">
            <h2>3. Order Notes (Optional)</h2>
            <textarea
              v-model="orderNotes"
              placeholder="Any special instructions for your order..."
              rows="4"
            ></textarea>
          </section>
        </div>

        <!-- Order Summary Sidebar -->
        <div class="order-summary">
          <h2>Order Summary</h2>

          <div class="summary-items">
            <div v-for="item in cart?.items" :key="item.id" class="summary-item">
              <span>{{ item.product_name }} x{{ item.quantity }}</span>
              <span>{{ formatPrice(item.subtotal) }}</span>
            </div>
          </div>

          <div class="summary-totals">
            <div class="summary-row">
              <span>Subtotal</span>
              <span>{{ formatPrice(cart?.total || 0) }}</span>
            </div>
            <div class="summary-row">
              <span>Delivery</span>
              <span>FREE</span>
            </div>
            <div class="summary-total">
              <span>Total</span>
              <span>{{ formatPrice(cart?.total || 0) }}</span>
            </div>
          </div>

          <button
            @click="handlePlaceOrder"
            :disabled="!canPlaceOrder || placingOrder"
            class="btn btn-primary btn-full"
          >
            {{ placingOrder ? 'Placing Order...' : 'Place Order' }}
          </button>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../../stores/cart'
import api from '../../services/api'

const router = useRouter()
const cartStore = useCartStore()

const cart = computed(() => cartStore.cart)
const addresses = ref([])
const selectedAddress = ref(null)
const paymentMethod = ref('CASH_ON_DELIVERY')
const mobileMoneyNumber = ref('')
const orderNotes = ref('')
const showAddressForm = ref(false)
const placingOrder = ref(false)
const error = ref(null)

const newAddress = ref({
  label: '',
  recipient_name: '',
  phone_number: '',
  country: 'UG',
  city: '',
  address_line1: '',
  address_line2: '',
  is_default: false
})

const canPlaceOrder = computed(() => {
  return selectedAddress.value && paymentMethod.value && cart.value?.items?.length > 0
})

onMounted(async () => {
  await cartStore.fetchCart()
  await fetchAddresses()

  // Auto-select default address
  const defaultAddr = addresses.value.find(a => a.is_default)
  if (defaultAddr) {
    selectedAddress.value = defaultAddr.id
  } else if (addresses.value.length > 0) {
    selectedAddress.value = addresses.value[0].id
  }
})

async function fetchAddresses() {
  try {
    const response = await api.get('/users/addresses/')
    addresses.value = response.data
  } catch (err) {
    console.error('Failed to fetch addresses:', err)
  }
}

async function handleAddAddress() {
  try {
    const response = await api.post('/users/addresses/', newAddress.value)
    addresses.value.push(response.data)
    selectedAddress.value = response.data.id
    showAddressForm.value = false

    // Reset form
    newAddress.value = {
      label: '',
      recipient_name: '',
      phone_number: '',
      country: 'UG',
      city: '',
      address_line1: '',
      address_line2: '',
      is_default: false
    }
  } catch (err) {
    alert('Failed to add address. Please try again.')
  }
}

async function handlePlaceOrder() {
  if (!canPlaceOrder.value) return

  placingOrder.value = true
  error.value = null

  try {
    const orderData = {
      delivery_address_id: selectedAddress.value,
      payment_method: paymentMethod.value,
      buyer_notes: orderNotes.value
    }

    const response = await api.post('/orders/create/', orderData)

    if (response.data.orders && response.data.orders.length > 0) {
      // Clear cart
      await cartStore.fetchCart()

      // Redirect to order success page or orders list
      alert(`Order placed successfully! Tracking numbers: ${response.data.orders.map(o => o.tracking_number).join(', ')}`)
      router.push('/orders')
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to place order. Please try again.'
  } finally {
    placingOrder.value = false
  }
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}
</script>

<style scoped>
.checkout-page {
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

.checkout-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
}

.checkout-section {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}

.checkout-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.address-selection {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.address-card {
  border: 2px solid #ddd;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  gap: 1rem;
  transition: all 0.2s;
}

.address-card:hover {
  border-color: #667eea;
}

.address-card.selected {
  border-color: #667eea;
  background: #f0f4ff;
}

.address-details p {
  margin: 0.25rem 0;
  color: #666;
}

.address-form {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: #f9f9f9;
  border-radius: 0.5rem;
}

.address-form h3 {
  margin-bottom: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select,
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.payment-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.payment-option {
  border: 2px solid #ddd;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  transition: all 0.2s;
}

.payment-option:hover {
  border-color: #667eea;
}

.payment-option:has(input:checked) {
  border-color: #667eea;
  background: #f0f4ff;
}

.payment-details strong {
  display: block;
  margin-bottom: 0.25rem;
}

.payment-details p {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.mobile-money-input {
  margin-top: 1rem;
}

.mobile-money-input label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.mobile-money-input input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.order-summary {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  height: fit-content;
  position: sticky;
  top: 2rem;
}

.order-summary h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.summary-items {
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  color: #666;
}

.summary-totals {
  margin-bottom: 1.5rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #666;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  padding-top: 1rem;
  margin-top: 1rem;
  border-top: 2px solid #eee;
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-full {
  width: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
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
  border: 2px solid #ddd;
  color: #666;
}

.btn-secondary:hover {
  border-color: #999;
}

.error-message {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fee;
  color: #c33;
  border-radius: 0.5rem;
  font-size: 0.9rem;
}
</style>
