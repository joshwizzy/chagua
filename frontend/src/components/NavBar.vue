<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="logo">
        {{ $t('app.name') }}
      </router-link>

      <div class="nav-links">
        <router-link to="/">{{ $t('nav.home') }}</router-link>
        <router-link to="/products">{{ $t('nav.products') }}</router-link>

        <template v-if="auth.isAuthenticated">
          <router-link to="/cart" class="cart-link">
            {{ $t('nav.cart') }}
            <span v-if="cart.itemsCount > 0" class="cart-badge">{{ cart.itemsCount }}</span>
          </router-link>
          <router-link to="/orders">{{ $t('nav.orders') }}</router-link>

          <router-link v-if="auth.isSeller" to="/seller/dashboard">
            Seller Dashboard
          </router-link>
          <router-link v-if="auth.isAdmin" to="/admin/dashboard">
            Admin Dashboard
          </router-link>

          <div class="user-menu">
            <span>{{ auth.user?.first_name }}</span>
            <button @click="handleLogout" class="logout-btn">
              {{ $t('nav.logout') }}
            </button>
          </div>
        </template>

        <template v-else>
          <router-link to="/login">{{ $t('nav.login') }}</router-link>
          <router-link to="/register" class="btn-register">{{ $t('nav.register') }}</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useCartStore } from '../stores/cart'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const auth = useAuthStore()
const cart = useCartStore()
const router = useRouter()

onMounted(() => {
  if (auth.isAuthenticated) {
    auth.fetchProfile()
    cart.fetchCart()
  }
})

async function handleLogout() {
  await auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-links a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.2s;
  position: relative;
}

.nav-links a:hover {
  color: #667eea;
}

.cart-link {
  position: relative;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -12px;
  background: #dc2626;
  color: white;
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
  border-radius: 10px;
  font-weight: 600;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  background: transparent;
  border: 1px solid #ddd;
  padding: 0.4rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.logout-btn:hover {
  border-color: #dc2626;
  color: #dc2626;
}

.btn-register {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white !important;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
}

.btn-register:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

@media (max-width: 768px) {
  .nav-links {
    gap: 1rem;
    flex-wrap: wrap;
  }

  .nav-links a {
    font-size: 0.9rem;
  }
}
</style>
