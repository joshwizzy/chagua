<template>
  <div class="dashboard">
    <div class="container">
      <h1>Admin Dashboard</h1>

      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Users</h3>
          <p class="stat-value">{{ stats.totalUsers }}</p>
          <small>{{ stats.buyers }} Buyers, {{ stats.sellers }} Sellers</small>
        </div>
        <div class="stat-card">
          <h3>Total Products</h3>
          <p class="stat-value">{{ stats.totalProducts }}</p>
          <small>{{ stats.activeProducts }} Active</small>
        </div>
        <div class="stat-card">
          <h3>Total Orders</h3>
          <p class="stat-value">{{ stats.totalOrders }}</p>
          <small>{{ stats.pendingOrders }} Pending</small>
        </div>
        <div class="stat-card">
          <h3>Platform Revenue</h3>
          <p class="stat-value">{{ formatPrice(stats.totalRevenue) }}</p>
          <small>From subscriptions</small>
        </div>
      </div>

      <div class="dashboard-sections">
        <section class="dashboard-section">
          <h2>Recent Activity</h2>
          <div v-if="loading" class="loading">Loading...</div>
          <div v-else-if="recentActivity.length === 0" class="placeholder">
            No recent activity
          </div>
          <div v-else class="activity-list">
            <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
              <div class="activity-icon">{{ activity.icon }}</div>
              <div class="activity-details">
                <p><strong>{{ activity.title }}</strong></p>
                <small>{{ activity.time }}</small>
              </div>
            </div>
          </div>
        </section>

        <section class="dashboard-section">
          <h2>Quick Actions</h2>
          <div class="quick-actions">
            <button class="action-btn">View All Users</button>
            <button class="action-btn">View All Products</button>
            <button class="action-btn">View All Orders</button>
            <button class="action-btn">Manage Subscriptions</button>
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
  // In a real app, these would be dedicated admin endpoints
  // For now, using placeholders
  stats.value = {
    totalUsers: 0,
    buyers: 0,
    sellers: 0,
    totalProducts: 0,
    activeProducts: 0,
    totalOrders: 0,
    pendingOrders: 0,
    totalRevenue: 0
  }
  loading.value = false
})

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
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-card h3 {
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
  margin: 0.5rem 0;
}

.stat-card small {
  color: #999;
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

.dashboard-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.loading, .placeholder {
  color: #999;
  padding: 2rem;
  text-align: center;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 0.5rem;
}

.activity-icon {
  font-size: 1.5rem;
}

.activity-details p {
  margin: 0 0 0.25rem 0;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  padding: 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #5568d3;
  transform: translateY(-2px);
}
</style>
