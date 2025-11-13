<template>
  <div class="dashboard">
    <div class="container">
      <h1>Seller Dashboard</h1>

      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Sales</h3>
          <p class="stat-value">0</p>
        </div>
        <div class="stat-card">
          <h3>Active Products</h3>
          <p class="stat-value">0</p>
        </div>
        <div class="stat-card">
          <h3>Pending Orders</h3>
          <p class="stat-value">0</p>
        </div>
        <div class="stat-card">
          <h3>Revenue</h3>
          <p class="stat-value">UGX 0</p>
        </div>
      </div>

      <div class="dashboard-sections">
        <section class="dashboard-section">
          <h2>Recent Orders</h2>
          <p class="placeholder">No orders yet</p>
        </section>

        <section class="dashboard-section">
          <h2>My Products</h2>
          <router-link to="/seller/products" class="btn btn-primary">
            Manage Products
          </router-link>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
// Seller dashboard - to be fully implemented
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

.placeholder {
  color: #999;
  padding: 2rem;
  text-align: center;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-block;
}
</style>
