<template>
  <nav class="bg-white shadow-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center flex-wrap gap-4">
      <router-link to="/" class="text-2xl font-bold text-primary-500 hover:text-primary-600 transition-colors">
        {{ $t('app.name') }}
      </router-link>

      <div class="flex items-center gap-4 md:gap-8 flex-wrap text-sm md:text-base">
        <router-link to="/" class="text-gray-700 hover:text-primary-500 font-medium transition-colors">
          {{ $t('nav.home') }}
        </router-link>
        <router-link to="/products" class="text-gray-700 hover:text-primary-500 font-medium transition-colors">
          {{ $t('nav.products') }}
        </router-link>

        <template v-if="auth.isAuthenticated">
          <router-link to="/cart" class="relative text-gray-700 hover:text-primary-500 font-medium transition-colors">
            {{ $t('nav.cart') }}
            <span v-if="cart.itemsCount > 0" class="absolute -top-2 -right-3 bg-red-600 text-white text-xs font-semibold px-1.5 py-0.5 rounded-full min-w-[1.25rem] text-center">
              {{ cart.itemsCount }}
            </span>
          </router-link>
          <router-link to="/orders" class="text-gray-700 hover:text-primary-500 font-medium transition-colors">
            {{ $t('nav.orders') }}
          </router-link>

          <router-link v-if="auth.isSeller" to="/seller/dashboard" class="text-gray-700 hover:text-primary-500 font-medium transition-colors">
            Seller Dashboard
          </router-link>
          <router-link v-if="auth.isAdmin" to="/admin/dashboard" class="text-gray-700 hover:text-primary-500 font-medium transition-colors">
            Admin Dashboard
          </router-link>

          <div class="flex items-center gap-3">
            <span class="text-gray-900 font-medium">{{ auth.user?.first_name }}</span>
            <button
              @click="handleLogout"
              class="border border-gray-300 hover:border-red-600 hover:text-red-600 px-3 py-1.5 rounded text-sm font-medium transition-all"
            >
              {{ $t('nav.logout') }}
            </button>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="text-gray-700 hover:text-primary-500 font-medium transition-colors">
            {{ $t('nav.login') }}
          </router-link>
          <router-link to="/register" class="btn btn-primary px-6 py-2">
            {{ $t('nav.register') }}
          </router-link>
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
