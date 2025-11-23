<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Subscription Management</h1>
          <p class="mt-2 text-sm text-gray-600">Monitor and manage seller subscriptions</p>
        </div>
        <button @click="router.push('/admin/dashboard')" class="btn btn-secondary">
          ← Back to Dashboard
        </button>
      </div>

      <!-- Filters -->
      <div class="mb-6">
        <select v-model="filters.status" @change="fetchSubscriptions" class="form-select w-48">
          <option value="">All Status</option>
          <option value="ACTIVE">Active</option>
          <option value="EXPIRED">Expired</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <!-- Subscriptions Table -->
      <div class="card">
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        <div v-else-if="subscriptions.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-500">No subscriptions found</p>
        </div>
        <div v-else>
          <div class="overflow-x-auto">
            <table class="table">
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
                  <td class="font-medium text-gray-900">{{ subscription.user_name }}</td>
                  <td>
                    <span :class="[
                      'badge',
                      subscription.plan.toLowerCase() === 'basic' ? 'badge-info' :
                      subscription.plan.toLowerCase() === 'pro' ? 'badge-primary' :
                      'badge-warning'
                    ]">
                      {{ subscription.plan }}
                    </span>
                  </td>
                  <td>
                    <span :class="[
                      'badge',
                      subscription.status === 'ACTIVE' ? 'badge-success' :
                      subscription.status === 'EXPIRED' ? 'badge-danger' :
                      'bg-gray-100 text-gray-600'
                    ]">
                      {{ subscription.status }}
                    </span>
                  </td>
                  <td class="text-sm text-gray-600">{{ formatDate(subscription.start_date) }}</td>
                  <td class="text-sm text-gray-600">{{ formatDate(subscription.end_date) }}</td>
                  <td class="font-medium text-gray-900">{{ subscription.price }} {{ subscription.currency }}</td>
                  <td>
                    <span :class="[
                      'font-semibold',
                      subscription.days_remaining <= 0 ? 'text-gray-400 line-through' :
                      subscription.days_remaining <= 7 ? 'text-red-600' :
                      subscription.days_remaining <= 14 ? 'text-orange-600' :
                      'text-green-600'
                    ]">
                      {{ subscription.days_remaining }} days
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="totalCount > 0" class="px-6 py-4 border-t border-gray-200 text-sm text-gray-600">
            Showing {{ subscriptions.length }} of {{ totalCount }} subscriptions
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
</invoke>