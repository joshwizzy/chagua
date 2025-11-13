<template>
  <div class="admin-orders">
    <div class="container">
      <div class="header">
        <h1>Order Management</h1>
        <button class="back-btn" @click="router.push('/admin/dashboard')">← Back to Dashboard</button>
      </div>

      <!-- Filters -->
      <div class="filters">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search by tracking number, buyer, or seller..."
          class="search-input"
          @input="fetchOrders"
        />
        <select v-model="filters.status" @change="fetchOrders" class="filter-select">
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
      <div class="table-container">
        <div v-if="loading" class="loading">Loading orders...</div>
        <div v-else-if="orders.length === 0" class="empty">No orders found</div>
        <table v-else class="orders-table">
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
              <td><strong>{{ order.tracking_number }}</strong></td>
              <td>{{ order.buyer_name }}</td>
              <td>{{ order.seller_name }}</td>
              <td>{{ order.items_count }}</td>
              <td>{{ order.total_amount }} {{ order.currency }}</td>
              <td>
                <div class="payment-info">
                  <span class="badge">{{ order.payment_method }}</span>
                  <span class="payment-status" :class="'payment-' + order.payment_status.toLowerCase()">
                    {{ order.payment_status }}
                  </span>
                </div>
              </td>
              <td>
                <span class="status" :class="'status-' + order.status.toLowerCase()">
                  {{ order.status }}
                </span>
              </td>
              <td>{{ formatDate(order.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-info" v-if="totalCount > 0">
        Showing {{ orders.length }} of {{ totalCount }} orders
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

<style scoped>
.admin-orders {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #333;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: #666;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
}

.back-btn:hover {
  background: #555;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
  background: white;
  cursor: pointer;
}

.table-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow-x: auto;
}

.loading, .empty {
  padding: 3rem;
  text-align: center;
  color: #999;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
}

.orders-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #dee2e6;
  white-space: nowrap;
}

.orders-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  background: #e3f2fd;
  color: #1976d2;
  width: fit-content;
}

.payment-status {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  width: fit-content;
}

.payment-status.payment-pending {
  background: #fff3cd;
  color: #856404;
}

.payment-status.payment-paid {
  background: #c8e6c9;
  color: #2e7d32;
}

.payment-status.payment-failed {
  background: #ffcdd2;
  color: #c62828;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-confirmed {
  background: #cfe2ff;
  color: #084298;
}

.status-processing {
  background: #e7f3ff;
  color: #0056b3;
}

.status-shipped {
  background: #d1ecf1;
  color: #0c5460;
}

.status-delivered {
  background: #c8e6c9;
  color: #2e7d32;
}

.status-cancelled {
  background: #ffcdd2;
  color: #c62828;
}

.pagination-info {
  margin-top: 1rem;
  text-align: center;
  color: #666;
}
</style>
