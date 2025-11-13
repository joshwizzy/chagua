<template>
  <div class="admin-subscriptions">
    <div class="container">
      <div class="header">
        <h1>Subscription Management</h1>
        <button class="back-btn" @click="router.push('/admin/dashboard')">← Back to Dashboard</button>
      </div>

      <!-- Filters -->
      <div class="filters">
        <select v-model="filters.status" @change="fetchSubscriptions" class="filter-select">
          <option value="">All Status</option>
          <option value="ACTIVE">Active</option>
          <option value="EXPIRED">Expired</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <!-- Subscriptions Table -->
      <div class="table-container">
        <div v-if="loading" class="loading">Loading subscriptions...</div>
        <div v-else-if="subscriptions.length === 0" class="empty">No subscriptions found</div>
        <table v-else class="subscriptions-table">
          <thead>
            <tr>
              <th>User</th>
              <th>Plan</th>
              <th>Status</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Price</th>
              <th>Days Remaining</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="subscription in subscriptions" :key="subscription.id">
              <td>{{ subscription.user_name }}</td>
              <td>
                <span class="badge" :class="'badge-' + subscription.plan.toLowerCase()">
                  {{ subscription.plan }}
                </span>
              </td>
              <td>
                <span class="status" :class="'status-' + subscription.status.toLowerCase()">
                  {{ subscription.status }}
                </span>
              </td>
              <td>{{ formatDate(subscription.start_date) }}</td>
              <td>{{ formatDate(subscription.end_date) }}</td>
              <td>{{ subscription.price }} {{ subscription.currency }}</td>
              <td>
                <span :class="getDaysRemainingClass(subscription.days_remaining)">
                  {{ subscription.days_remaining }} days
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-info" v-if="totalCount > 0">
        Showing {{ subscriptions.length }} of {{ totalCount }} subscriptions
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
const subscriptions = ref([])
const totalCount = ref(0)

const filters = ref({
  status: ''
})

onMounted(() => {
  fetchSubscriptions()
})

async function fetchSubscriptions() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.status) params.status = filters.value.status

    const response = await api.get('/users/admin/subscriptions/', { params })
    subscriptions.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to fetch subscriptions:', error)
    alert('Failed to fetch subscriptions')
  } finally {
    loading.value = false
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function getDaysRemainingClass(days) {
  if (days <= 0) return 'days-expired'
  if (days <= 7) return 'days-critical'
  if (days <= 14) return 'days-warning'
  return 'days-normal'
}
</script>

<style scoped>
.admin-subscriptions {
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

.subscriptions-table {
  width: 100%;
  border-collapse: collapse;
}

.subscriptions-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #dee2e6;
  white-space: nowrap;
}

.subscriptions-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.badge-basic {
  background: #e3f2fd;
  color: #1976d2;
}

.badge-pro {
  background: #f3e5f5;
  color: #7b1fa2;
}

.badge-premium {
  background: #fff3e0;
  color: #e65100;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-active {
  background: #c8e6c9;
  color: #2e7d32;
}

.status-expired {
  background: #ffcdd2;
  color: #c62828;
}

.status-cancelled {
  background: #f5f5f5;
  color: #666;
}

.days-normal {
  color: #2e7d32;
  font-weight: 500;
}

.days-warning {
  color: #f57c00;
  font-weight: 500;
}

.days-critical {
  color: #d32f2f;
  font-weight: 600;
}

.days-expired {
  color: #999;
  font-weight: 500;
  text-decoration: line-through;
}

.pagination-info {
  margin-top: 1rem;
  text-align: center;
  color: #666;
}
</style>
