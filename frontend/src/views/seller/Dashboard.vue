<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Seller Dashboard</h1>
        <p class="mt-2 text-sm text-gray-600">Manage your products and orders</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total Products -->
        <div class="card">
          <div class="card-body">
            <div class="flex items-center">
              <div class="flex-shrink-0 text-4xl mr-4">📦</div>
              <div>
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">Total Products</p>
                <p class="mt-1 text-3xl font-bold text-gray-900">{{ stats.totalProducts }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Total Orders -->
        <div class="card">
          <div class="card-body">
            <div class="flex items-center">
              <div class="flex-shrink-0 text-4xl mr-4">🛒</div>
              <div>
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">Total Orders</p>
                <p class="mt-1 text-3xl font-bold text-gray-900">{{ stats.totalOrders }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Pending Orders -->
        <div class="card">
          <div class="card-body">
            <div class="flex items-center">
              <div class="flex-shrink-0 text-4xl mr-4">⏳</div>
              <div>
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">Pending Orders</p>
                <p class="mt-1 text-3xl font-bold text-yellow-600">{{ stats.pendingOrders }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Total Revenue -->
        <div class="card">
          <div class="card-body">
            <div class="flex items-center">
              <div class="flex-shrink-0 text-4xl mr-4">💰</div>
              <div>
                <p class="text-sm font-medium text-gray-600 uppercase tracking-wide">Total Revenue</p>
                <p class="mt-1 text-3xl font-bold text-green-600">{{ formatPrice(stats.totalRevenue) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Recent Orders -->
        <div class="lg:col-span-2">
          <div class="card">
            <div class="card-header flex justify-between items-center">
              <h2 class="text-lg font-semibold text-gray-900">Recent Orders</h2>
              <router-link to="/seller/orders" class="text-sm font-medium text-primary-600 hover:text-primary-700">
                View All →
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="loading" class="flex justify-center py-12">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>

              <div v-else-if="recentOrders.length === 0" class="text-center py-12">
                <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                </svg>
                <p class="mt-2 text-sm text-gray-500">No orders yet</p>
              </div>

              <div v-else class="space-y-3">
                <div v-for="order in recentOrders" :key="order.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div class="flex-1">
                    <p class="font-semibold text-gray-900">#{{ order.tracking_number }}</p>
                    <p class="text-sm text-gray-600">{{ order.buyer_name }}</p>
                  </div>
                  <div class="flex items-center gap-4">
                    <span :class="[
                      'status-badge',
                      `status-${order.status.toLowerCase()}`
                    ]">
                      {{ order.status }}
                    </span>
                    <span class="font-semibold text-gray-900">{{ formatPrice(order.total_amount) }}</span>
                  </div>
                  <div class="ml-4">
                    <button
                      v-if="order.status === 'PENDING'"
                      @click="confirmOrder(order.id)"
                      class="btn btn-primary btn-sm"
                    >
                      Confirm
                    </button>
                    <button
                      v-if="order.status === 'CONFIRMED'"
                      @click="markAsShipped(order.id)"
                      class="btn btn-success btn-sm"
                    >
                      Mark Shipped
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Stats -->
          <div class="card mt-8">
            <div class="card-header">
              <h2 class="text-lg font-semibold text-gray-900">Quick Stats</h2>
            </div>
            <div class="card-body">
              <div class="grid grid-cols-2 gap-4">
                <div class="p-4 bg-gray-50 rounded-lg">
                  <p class="text-sm text-gray-600">Active Products</p>
                  <p class="text-2xl font-bold text-gray-900">{{ stats.activeProducts }}</p>
                </div>
                <div class="p-4 bg-gray-50 rounded-lg">
                  <p class="text-sm text-gray-600">Out of Stock</p>
                  <p class="text-2xl font-bold text-red-600">{{ stats.outOfStockProducts }}</p>
                </div>
                <div class="p-4 bg-gray-50 rounded-lg">
                  <p class="text-sm text-gray-600">Avg. Order Value</p>
                  <p class="text-2xl font-bold text-gray-900">{{ formatPrice(stats.avgOrderValue) }}</p>
                </div>
                <div class="p-4 bg-gray-50 rounded-lg">
                  <p class="text-sm text-gray-600">Total Views</p>
                  <p class="text-2xl font-bold text-gray-900">{{ stats.totalViews }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- My Products -->
        <div class="lg:col-span-1">
          <div class="card">
            <div class="card-header flex justify-between items-center">
              <h2 class="text-lg font-semibold text-gray-900">My Products</h2>
              <router-link to="/seller/products" class="text-sm font-medium text-primary-600 hover:text-primary-700">
                Manage →
              </router-link>
            </div>
            <div class="card-body">
              <div class="space-y-3">
                <router-link
                  to="/seller/products/create"
                  class="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all group"
                >
                  <div class="text-4xl mb-2 group-hover:scale-110 transition-transform">+</div>
                  <span class="text-sm font-medium text-gray-700 group-hover:text-primary-600">Add New Product</span>
                </router-link>
                <router-link
                  to="/seller/products"
                  class="flex flex-col items-center justify-center p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-primary-500 hover:bg-primary-50 transition-all group"
                >
                  <div class="text-4xl mb-2">📋</div>
                  <span class="text-sm font-medium text-gray-700 group-hover:text-primary-600">View All Products</span>
                </router-link>
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
import api from '../../services/api'

const loading = ref(true)
const recentOrders = ref([])

const stats = ref({
  totalProducts: 0,
  activeProducts: 0,
  outOfStockProducts: 0,
  totalOrders: 0,
  pendingOrders: 0,
  totalRevenue: 0,
  avgOrderValue: 0,
  totalViews: 0
})

onMounted(async () => {
  await Promise.all([
    fetchStats(),
    fetchRecentOrders()
  ])
  loading.value = false
})

async function fetchStats() {
  try {
    const [productsRes, ordersRes] = await Promise.all([
      api.get('/products/seller/products/'),
      api.get('/orders/seller/')
    ])

    const products = productsRes.data.results || productsRes.data
    const orders = ordersRes.data.results || ordersRes.data

    stats.value.totalProducts = products.length
    stats.value.activeProducts = products.filter(p => p.is_active).length
    stats.value.outOfStockProducts = products.filter(p => p.availability === 'OUT_OF_STOCK').length
    stats.value.totalViews = products.reduce((sum, p) => sum + p.views_count, 0)

    stats.value.totalOrders = orders.length
    stats.value.pendingOrders = orders.filter(o => o.status === 'PENDING').length
    stats.value.totalRevenue = orders
      .filter(o => o.status !== 'CANCELLED')
      .reduce((sum, o) => sum + parseFloat(o.total_amount), 0)
    stats.value.avgOrderValue = orders.length > 0
      ? stats.value.totalRevenue / orders.length
      : 0
  } catch (err) {
    console.error('Failed to fetch stats:', err)
  }
}

async function fetchRecentOrders() {
  try {
    const response = await api.get('/orders/seller/')
    const allOrders = response.data.results || response.data
    recentOrders.value = allOrders.slice(0, 5)
  } catch (err) {
    console.error('Failed to fetch orders:', err)
  }
}

async function confirmOrder(orderId) {
  try {
    await api.put(`/orders/${orderId}/status/`, {
      status: 'CONFIRMED'
    })
    await fetchRecentOrders()
    await fetchStats()
  } catch (err) {
    alert('Failed to confirm order')
  }
}

async function markAsShipped(orderId) {
  try {
    await api.put(`/orders/${orderId}/status/`, {
      status: 'SHIPPED'
    })
    await fetchRecentOrders()
    await fetchStats()
  } catch (err) {
    alert('Failed to update order')
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
