<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">My Orders</h1>

      <div v-if="loading" class="text-center py-16 bg-white rounded-lg">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading orders...</p>
      </div>

      <div v-else-if="orders.length === 0" class="text-center py-16 bg-white rounded-lg">
        <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
        </svg>
        <p class="mt-4 text-xl text-gray-600">You haven't placed any orders yet</p>
        <router-link to="/products" class="btn btn-primary mt-8 inline-block">
          Start Shopping
        </router-link>
      </div>

      <div v-else class="space-y-6">
        <div v-for="order in orders" :key="order.id" class="card">
          <div class="card-body">
            <div class="flex justify-between items-center mb-6 pb-4 border-b border-gray-200">
              <h3 class="text-lg font-semibold text-gray-900">Order #{{ order.tracking_number }}</h3>
              <span :class="[
                'status-badge',
                `status-${order.status.toLowerCase()}`
              ]">
                {{ order.status.replace('_', ' ') }}
              </span>
            </div>

            <div class="space-y-3 mb-6">
              <div class="flex justify-between text-sm">
                <span class="font-medium text-gray-700">Date:</span>
                <span class="text-gray-600">{{ formatDate(order.created_at) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="font-medium text-gray-700">Seller:</span>
                <span class="text-gray-600">{{ order.seller_name }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="font-medium text-gray-700">Total:</span>
                <span class="text-lg font-semibold text-primary-600">{{ formatPrice(order.total_amount) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="font-medium text-gray-700">Payment:</span>
                <span class="text-gray-600">{{ order.payment_status }}</span>
              </div>
            </div>

            <div class="flex gap-3">
              <router-link
                :to="`/orders/${order.tracking_number}`"
                class="btn btn-primary btn-sm"
              >
                View Details
              </router-link>
              <button
                v-if="['PENDING', 'CONFIRMED'].includes(order.status)"
                @click="cancelOrder(order.id)"
                class="border border-red-600 text-red-600 hover:bg-red-600 hover:text-white px-4 py-2 rounded-lg text-sm font-semibold transition-all"
              >
                Cancel Order
              </button>
            </div>
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
