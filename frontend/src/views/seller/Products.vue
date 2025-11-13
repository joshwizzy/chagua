<template>
  <div class="seller-products">
    <div class="container">
      <div class="page-header">
        <h1>My Products</h1>
        <router-link to="/seller/products/create" class="btn btn-primary">
          + Add New Product
        </router-link>
      </div>

      <div v-if="loading" class="loading">Loading products...</div>

      <div v-else-if="products.length === 0" class="empty">
        <p>You haven't added any products yet</p>
        <router-link to="/seller/products/create" class="btn btn-primary">
          Add Your First Product
        </router-link>
      </div>

      <div v-else class="products-table">
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Category</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Status</th>
              <th>Views</th>
              <th>Sales</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>
                <div class="product-info">
                  <img v-if="product.primary_image" :src="product.primary_image" :alt="product.name" />
                  <span>{{ product.name }}</span>
                </div>
              </td>
              <td>{{ product.category_name }}</td>
              <td>{{ formatPrice(product.price) }}</td>
              <td>{{ product.stock_quantity }}</td>
              <td>
                <span :class="['status-badge', product.availability.toLowerCase()]">
                  {{ product.availability.replace('_', ' ') }}
                </span>
              </td>
              <td>{{ product.views_count }}</td>
              <td>{{ product.sales_count }}</td>
              <td>
                <div class="actions">
                  <router-link :to="`/seller/products/edit/${product.id}`" class="btn-small btn-edit">
                    Edit
                  </router-link>
                  <button @click="handleDelete(product.id)" class="btn-small btn-delete">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const products = ref([])
const loading = ref(true)

onMounted(async () => {
  await fetchProducts()
})

async function fetchProducts() {
  loading.value = true
  try {
    const response = await api.get('/products/seller/products/')
    products.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch products:', error)
  } finally {
    loading.value = false
  }
}

async function handleDelete(productId) {
  if (confirm('Are you sure you want to delete this product?')) {
    try {
      await api.delete(`/products/seller/products/${productId}/`)
      await fetchProducts()
    } catch (error) {
      alert('Failed to delete product')
    }
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
.seller-products {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #333;
}

.loading, .empty {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 0.5rem;
}

.empty p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.products-table {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f9f9f9;
}

th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #eee;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.product-info img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 0.25rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: uppercase;
}

.status-badge.in_stock {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.out_of_stock {
  background: #fee2e2;
  color: #991b1b;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn, .btn-small {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.75rem 1.5rem;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-edit {
  background: #667eea;
  color: white;
}

.btn-edit:hover {
  background: #5568d3;
}

.btn-delete {
  background: transparent;
  border: 1px solid #dc2626;
  color: #dc2626;
}

.btn-delete:hover {
  background: #dc2626;
  color: white;
}
</style>
