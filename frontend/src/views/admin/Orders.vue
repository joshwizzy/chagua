<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Order Management</h1>
          <p class="mt-2 text-sm text-gray-600">Monitor and manage all platform orders</p>
        </div>
        <button @click="router.push('/admin/dashboard')" class="btn btn-secondary">
          ← Back to Dashboard
        </button>
      </div>

      <!-- Filters -->
      <div class="flex gap-4 mb-6">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search by tracking number, buyer, or seller..."
          class="form-input flex-1"
          @input="fetchOrders"
        />
        <select v-model="filters.status" @change="fetchOrders" class="form-select w-48">
          <option value="">All Status</option>
          <option value="PENDING">Pending</option>
          <option value="CONFIRMED">Confirmed</option>
          <option value="PROCESSING">Processing</option>
          <option value="SHIPPED">Shipped</option>
          <option value="DELIVERED">Delivered</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <!-- Orders Table -->
      <div class="card">
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        <div v-else-if="orders.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-500">No orders found</p>
        </div>
        <div v-else>
          <div class="overflow-x-auto">
            <table class="table">
              <thead>
                <tr>
                  <th>Tracking #</th>
                  <th>Buyer</th>
                  <th>Seller</th>
                  <th>Items</th>
                  <th>Total</th>
                  <th>Payment</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in orders" :key="order.id">
                  <td class="font-semibold text-gray-900">{{ order.tracking_number }}</td>
                  <td class="text-gray-600">{{ order.buyer_name }}</td>
                  <td class="text-gray-600">{{ order.seller_name }}</td>
                  <td class="text-gray-600">{{ order.items_count }}</td>
                  <td class="font-medium text-gray-900">{{ order.total_amount }} {{ order.currency }}</td>
                  <td>
                    <div class="flex flex-col gap-1">
                      <span class="badge badge-info">{{ order.payment_method }}</span>
                      <span :class="[
                        'badge',
                        order.payment_status === 'PENDING' ? 'badge-warning' :
                        order.payment_status === 'PAID' ? 'badge-success' :
                        'badge-danger'
                      ]">
                        {{ order.payment_status }}
                      </span>
                    </div>
                  </td>
                  <td>
                    <span :class="[
                      'status-badge',
                      `status-${order.status.toLowerCase()}`
                    ]">
                      {{ order.status }}
                    </span>
                  </td>
                  <td class="text-sm text-gray-600 whitespace-nowrap">{{ formatDate(order.created_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="totalCount > 0" class="px-6 py-4 border-t border-gray-200 text-sm text-gray-600">
            Showing {{ orders.length }} of {{ totalCount }} orders
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'

const router = useRouter()
const loading = ref(true)
const orders = ref([])
const totalCount = ref(0)

const filters = ref({
  search: '',
  status: ''
})

onMounted(() => {
  fetchOrders()
})

async function fetchOrders() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.status) params.status = filters.value.status

    const response = await api.get('/users/admin/orders/', { params })
    orders.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to fetch orders:', error)
    alert('Failed to fetch orders')
  } finally {
    loading.value = false
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
