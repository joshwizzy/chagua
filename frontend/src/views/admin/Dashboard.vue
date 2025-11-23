<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
        <p class="mt-2 text-sm text-gray-600">Welcome back! Here's what's happening with CHAGUA today.</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total Users -->
        <div class="card">
          <div class="card-body">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">Total Users</p>
                <p class="mt-2 text-3xl font-bold text-gray-900">{{ stats.totalUsers }}</p>
                <p class="mt-1 text-sm text-gray-500">{{ stats.buyers }} Buyers · {{ stats.sellers }} Sellers</p>
              </div>
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Total Products -->
        <div class="card">
          <div class="card-body">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">Total Products</p>
                <p class="mt-2 text-3xl font-bold text-gray-900">{{ stats.totalProducts }}</p>
                <p class="mt-1 text-sm text-gray-500">{{ stats.activeProducts }} Active</p>
              </div>
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Total Orders -->
        <div class="card">
          <div class="card-body">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">Total Orders</p>
                <p class="mt-2 text-3xl font-bold text-gray-900">{{ stats.totalOrders }}</p>
                <p class="mt-1 text-sm text-gray-500">{{ stats.pendingOrders }} Pending</p>
              </div>
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Platform Revenue -->
        <div class="card">
          <div class="card-body">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">Subscription Revenue</p>
                <p class="mt-2 text-3xl font-bold text-gray-900">{{ formatPrice(stats.totalRevenue) }}</p>
                <p class="mt-1 text-sm text-gray-500">From subscriptions</p>
              </div>
              <div class="flex-shrink-0">
                <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
                  <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Recent Activity -->
        <div class="lg:col-span-2">
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Recent Activity</h2>
            </div>
            <div class="card-body">
              <div v-if="loading" class="flex justify-center py-12">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>
              <div v-else-if="recentActivity.length === 0" class="text-center py-12">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
                <p class="mt-2 text-sm text-gray-500">No recent activity</p>
              </div>
              <div v-else class="space-y-4">
                <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors">
                  <div class="flex-shrink-0 text-2xl">{{ activity.icon }}</div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
                    <p class="text-xs text-gray-500 mt-1">{{ activity.time }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="lg:col-span-1">
          <div class="card">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Quick Actions</h2>
            </div>
            <div class="card-body">
              <div class="space-y-3">
                <button
                  @click="router.push('/admin/users')"
                  class="w-full flex items-center justify-between px-4 py-3 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-primary-500 transition-all group"
                >
                  <span class="text-sm font-medium text-gray-700 group-hover:text-primary-600">View All Users</span>
                  <svg class="w-5 h-5 text-gray-400 group-hover:text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </button>
                <button
                  @click="router.push('/admin/products')"
                  class="w-full flex items-center justify-between px-4 py-3 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-primary-500 transition-all group"
                >
                  <span class="text-sm font-medium text-gray-700 group-hover:text-primary-600">View All Products</span>
                  <svg class="w-5 h-5 text-gray-400 group-hover:text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </button>
                <button
                  @click="router.push('/admin/orders')"
                  class="w-full flex items-center justify-between px-4 py-3 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-primary-500 transition-all group"
                >
                  <span class="text-sm font-medium text-gray-700 group-hover:text-primary-600">View All Orders</span>
                  <svg class="w-5 h-5 text-gray-400 group-hover:text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </button>
                <button
                  @click="router.push('/admin/subscriptions')"
                  class="w-full flex items-center justify-between px-4 py-3 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:border-primary-500 transition-all group"
                >
                  <span class="text-sm font-medium text-gray-700 group-hover:text-primary-600">Manage Subscriptions</span>
                  <svg class="w-5 h-5 text-gray-400 group-hover:text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                </button>
              </div>
            </div>
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
const recentActivity = ref([])

const stats = ref({
  totalUsers: 0,
  buyers: 0,
  sellers: 0,
  totalProducts: 0,
  activeProducts: 0,
  totalOrders: 0,
  pendingOrders: 0,
  totalRevenue: 0
})

onMounted(async () => {
  try {
    const response = await api.get('/users/admin/statistics/')
    const data = response.data

    stats.value = {
      totalUsers: data.users.total,
      buyers: data.users.buyers,
      sellers: data.users.sellers,
      totalProducts: data.products.total,
      activeProducts: data.products.active,
      totalOrders: data.orders.total,
      pendingOrders: data.orders.pending,
      totalRevenue: data.revenue.subscriptions
    }

    recentActivity.value = []
    if (data.recent_activity.users > 0) {
      recentActivity.value.push({
        id: 1,
        icon: '👤',
        title: `${data.recent_activity.users} new users registered`,
        time: 'Last 7 days'
      })
    }
    if (data.recent_activity.products > 0) {
      recentActivity.value.push({
        id: 2,
        icon: '📦',
        title: `${data.recent_activity.products} new products listed`,
        time: 'Last 7 days'
      })
    }
    if (data.recent_activity.orders > 0) {
      recentActivity.value.push({
        id: 3,
        icon: '🛒',
        title: `${data.recent_activity.orders} new orders placed`,
        time: 'Last 7 days'
      })
    }
  } catch (error) {
    console.error('Failed to fetch admin statistics:', error)
  } finally {
    loading.value = false
  }
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}
</script>
