import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue')
  },
  {
    path: '/products',
    name: 'Products',
    component: () => import('../views/products/ProductList.vue')
  },
  {
    path: '/products/:slug',
    name: 'ProductDetail',
    component: () => import('../views/products/ProductDetail.vue')
  },
  {
    path: '/cart',
    name: 'Cart',
    component: () => import('../views/cart/Cart.vue')
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('../views/orders/OrderList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/seller/dashboard',
    name: 'SellerDashboard',
    component: () => import('../views/seller/Dashboard.vue'),
    meta: { requiresAuth: true, requiresSeller: true }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const userRole = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresSeller && userRole !== 'SELLER') {
    next('/')
  } else if (to.meta.requiresAdmin && userRole !== 'ADMIN') {
    next('/')
  } else {
    next()
  }
})

export default router
