<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>{{ $t('app.name') }}</h3>
          <p>{{ $t('app.tagline') }}</p>
        </div>

        <div class="footer-section">
          <h4>Quick Links</h4>
          <ul>
            <li><router-link to="/products">Products</router-link></li>
            <li><router-link to="/about">About Us</router-link></li>
            <li><router-link to="/contact">Contact</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>For Sellers</h4>
          <ul>
            <li><router-link to="/register">Become a Seller</router-link></li>
            <li><router-link to="/seller/dashboard">Seller Dashboard</router-link></li>
          </ul>
        </div>

        <div class="footer-section">
          <h4>Support</h4>
          <ul>
            <li><a href="#">Help Center</a></li>
            <li><a href="#">Terms of Service</a></li>
            <li><a href="#">Privacy Policy</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2025 CHAGUA. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #2d3748;
  color: white;
  padding: 3rem 0 1rem;
  margin-top: 4rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #667eea;
}

.footer-section h4 {
  margin-bottom: 1rem;
}

.footer-section p {
  color: #cbd5e0;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 0.5rem;
}

.footer-section a {
  color: #cbd5e0;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-section a:hover {
  color: white;
}

.footer-bottom {
  border-top: 1px solid #4a5568;
  padding-top: 1rem;
  text-align: center;
  color: #cbd5e0;
}
</style>
