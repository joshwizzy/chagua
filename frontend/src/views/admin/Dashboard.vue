<template>
  <div class="dashboard">
    <div class="container">
      <h1>Admin Dashboard</h1>

      <div class="stats-grid">
        <div class="stat-card">
          <h3>Total Users</h3>
          <p class="stat-value">0</p>
        </div>
        <div class="stat-card">
          <h3>Total Products</h3>
          <p class="stat-value">0</p>
        </div>
        <div class="stat-card">
          <h3>Total Orders</h3>
          <p class="stat-value">0</p>
        </div>
        <div class="stat-card">
          <h3>Platform Revenue</h3>
          <p class="stat-value">UGX 0</p>
        </div>
      </div>

      <div class="dashboard-sections">
        <section class="dashboard-section">
          <h2>Recent Activity</h2>
          <p class="placeholder">No recent activity</p>
        </section>

        <section class="dashboard-section">
          <h2>Pending Approvals</h2>
          <p class="placeholder">No pending items</p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
// Admin dashboard - to be fully implemented
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
</style>
