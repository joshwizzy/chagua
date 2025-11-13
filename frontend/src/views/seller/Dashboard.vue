<template>
  <div class="dashboard">
    <div class="container">
      <h1>Seller Dashboard</h1>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📦</div>
          <div class="stat-content">
            <h3>Total Products</h3>
            <p class="stat-value">{{ stats.totalProducts }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🛒</div>
          <div class="stat-content">
            <h3>Total Orders</h3>
            <p class="stat-value">{{ stats.totalOrders }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-content">
            <h3>Pending Orders</h3>
            <p class="stat-value">{{ stats.pendingOrders }}</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-content">
            <h3>Total Revenue</h3>
            <p class="stat-value">{{ formatPrice(stats.totalRevenue) }}</p>
          </div>
        </div>
      </div>

      <div class="dashboard-sections">
        <section class="dashboard-section">
          <div class="section-header">
            <h2>Recent Orders</h2>
            <router-link to="/seller/orders" class="link">View All →</router-link>
          </div>

          <div v-if="loading" class="loading">Loading...</div>

          <div v-else-if="recentOrders.length === 0" class="placeholder">
            No orders yet
          </div>

          <div v-else class="orders-list">
            <div v-for="order in recentOrders" :key="order.id" class="order-item">
              <div class="order-info">
                <strong>#{{ order.tracking_number }}</strong>
                <span class="order-buyer">{{ order.buyer_name }}</span>
              </div>
              <div class="order-meta">
                <span :class="['status', order.status.toLowerCase()]">{{ order.status }}</span>
                <span class="order-amount">{{ formatPrice(order.total_amount) }}</span>
              </div>
              <div class="order-actions">
                <button
                  v-if="order.status === 'PENDING'"
                  @click="confirmOrder(order.id)"
                  class="btn-small btn-confirm"
                >
                  Confirm
                </button>
                <button
                  v-if="order.status === 'CONFIRMED'"
                  @click="markAsShipped(order.id)"
                  class="btn-small btn-ship"
                >
                  Mark as Shipped
                </button>
              </div>
            </div>
          </div>
        </section>

        <section class="dashboard-section">
          <div class="section-header">
            <h2>My Products</h2>
            <router-link to="/seller/products" class="link">Manage Products →</router-link>
          </div>

          <div class="quick-actions">
            <router-link to="/seller/products/create" class="action-card">
              <div class="action-icon">+</div>
              <span>Add New Product</span>
            </router-link>
            <router-link to="/seller/products" class="action-card">
              <div class="action-icon">📋</div>
              <span>View All Products</span>
            </router-link>
          </div>
        </section>

        <section class="dashboard-section">
          <h2>Quick Stats</h2>

          <div class="quick-stats">
            <div class="quick-stat-item">
              <span class="label">Active Products:</span>
              <span class="value">{{ stats.activeProducts }}</span>
            </div>
            <div class="quick-stat-item">
              <span class="label">Out of Stock:</span>
              <span class="value">{{ stats.outOfStockProducts }}</span>
            </div>
            <div class="quick-stat-item">
              <span class="label">Avg. Order Value:</span>
              <span class="value">{{ formatPrice(stats.avgOrderValue) }}</span>
            </div>
            <div class="quick-stat-item">
              <span class="label">Total Views:</span>
              <span class="value">{{ stats.totalViews }}</span>
            </div>
          </div>
        </section>
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
    await api.post(`/orders/${orderId}/status/`, {
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
    await api.post(`/orders/${orderId}/status/`, {
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

<style scoped>
.dashboard {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  gap: 1rem;
  align-items: center;
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-content h3 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 600;
  color: #667eea;
  margin: 0;
}

.dashboard-sections {
  display: grid;
  gap: 2rem;
}

.dashboard-section {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  text-decoration: underline;
}

.loading, .placeholder {
  color: #999;
  padding: 2rem;
  text-align: center;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.order-item {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 0.5rem;
  align-items: center;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.order-buyer {
  color: #666;
  font-size: 0.9rem;
}

.order-meta {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.85rem;
  font-weight: 500;
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

.status.shipped {
  background: #ddd6fe;
  color: #5b21b6;
}

.status.delivered {
  background: #d1fae5;
  color: #065f46;
}

.order-amount {
  font-weight: 600;
  color: #667eea;
}

.order-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-small {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-confirm {
  background: #667eea;
  color: white;
}

.btn-confirm:hover {
  background: #5568d3;
}

.btn-ship {
  background: #10b981;
  color: white;
}

.btn-ship:hover {
  background: #059669;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  border: 2px dashed #ddd;
  border-radius: 0.5rem;
  text-decoration: none;
  color: #333;
  transition: all 0.2s;
}

.action-card:hover {
  border-color: #667eea;
  background: #f0f4ff;
}

.action-icon {
  font-size: 2rem;
}

.quick-stats {
  display: grid;
  gap: 1rem;
}

.quick-stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem;
  background: #f9f9f9;
  border-radius: 0.25rem;
}

.quick-stat-item .label {
  color: #666;
}

.quick-stat-item .value {
  font-weight: 600;
  color: #333;
}
</style>
