<template>
  <div class="orders-page">
    <div class="container">
      <h1>My Orders</h1>

      <div v-if="loading" class="loading">Loading orders...</div>

      <div v-else-if="orders.length === 0" class="empty">
        <p>You haven't placed any orders yet</p>
        <router-link to="/products" class="btn btn-primary">Start Shopping</router-link>
      </div>

      <div v-else class="orders-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <h3>Order #{{ order.tracking_number }}</h3>
            <span :class="['status', order.status.toLowerCase()]">
              {{ order.status.replace('_', ' ') }}
            </span>
          </div>

          <div class="order-details">
            <div class="detail-row">
              <span class="label">Date:</span>
              <span>{{ formatDate(order.created_at) }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Seller:</span>
              <span>{{ order.seller_name }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Total:</span>
              <span class="amount">{{ formatPrice(order.total_amount) }}</span>
            </div>
            <div class="detail-row">
              <span class="label">Payment:</span>
              <span>{{ order.payment_status }}</span>
            </div>
          </div>

          <div class="order-actions">
            <router-link :to="`/orders/${order.tracking_number}`" class="btn btn-small">
              View Details
            </router-link>
            <button
              v-if="['PENDING', 'CONFIRMED'].includes(order.status)"
              @click="cancelOrder(order.id)"
              class="btn btn-small btn-cancel"
            >
              Cancel Order
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useOrdersStore } from '../../stores/orders'

const ordersStore = useOrdersStore()

const orders = ref([])
const loading = ref(true)

onMounted(async () => {
  await ordersStore.fetchOrders()
  orders.value = ordersStore.orders
  loading.value = false
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}

async function cancelOrder(orderId) {
  if (confirm('Are you sure you want to cancel this order?')) {
    const result = await ordersStore.cancelOrder(orderId)
    if (result.success) {
      alert('Order cancelled successfully')
      orders.value = ordersStore.orders
    } else {
      alert('Failed to cancel order')
    }
  }
}
</script>

<style scoped>
.orders-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: #333;
}

.loading, .empty {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 1rem;
}

.empty p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.order-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.order-header h3 {
  font-size: 1.2rem;
  color: #333;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-weight: 500;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.status.pending {
  background: #fef3c7;
  color: #92400e;
}

.status.confirmed {
  background: #dbeafe;
  color: #1e3a8a;
}

.status.processing {
  background: #e0e7ff;
  color: #3730a3;
}

.status.shipped {
  background: #ddd6fe;
  color: #5b21b6;
}

.status.delivered {
  background: #d1fae5;
  color: #065f46;
}

.status.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.order-details {
  margin-bottom: 1.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  color: #666;
}

.detail-row .label {
  font-weight: 500;
  color: #333;
}

.detail-row .amount {
  font-weight: 600;
  color: #667eea;
  font-size: 1.1rem;
}

.order-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-block;
}

.btn-small {
  background: #667eea;
  color: white;
}

.btn-small:hover {
  background: #5568d3;
}

.btn-cancel {
  background: transparent;
  border: 1px solid #dc2626;
  color: #dc2626;
}

.btn-cancel:hover {
  background: #dc2626;
  color: white;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 2rem;
}
</style>
