<template>
  <div class="admin-products">
    <div class="container">
      <div class="header">
        <h1>Product Management</h1>
        <button class="back-btn" @click="router.push('/admin/dashboard')">← Back to Dashboard</button>
      </div>

      <!-- Filters -->
      <div class="filters">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search products..."
          class="search-input"
          @input="fetchProducts"
        />
        <select v-model="filters.is_active" @change="fetchProducts" class="filter-select">
          <option value="">All Status</option>
          <option value="true">Active</option>
          <option value="false">Inactive</option>
        </select>
        <select v-model="filters.is_featured" @change="fetchProducts" class="filter-select">
          <option value="">All Products</option>
          <option value="true">Featured</option>
          <option value="false">Not Featured</option>
        </select>
      </div>

      <!-- Products Table -->
      <div class="table-container">
        <div v-if="loading" class="loading">Loading products...</div>
        <div v-else-if="products.length === 0" class="empty">No products found</div>
        <table v-else class="products-table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Seller</th>
              <th>Category</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Status</th>
              <th>Featured</th>
              <th>Views</th>
              <th>Sales</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in products" :key="product.id">
              <td>
                <div class="product-info">
                  <strong>{{ product.name }}</strong>
                </div>
              </td>
              <td>{{ product.seller_name }}</td>
              <td>{{ product.category_name || 'N/A' }}</td>
              <td>{{ product.price }}</td>
              <td>{{ product.stock_quantity }}</td>
              <td>
                <span class="status" :class="product.is_active ? 'active' : 'inactive'">
                  {{ product.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <span class="featured">{{ product.is_featured ? '⭐' : '' }}</span>
              </td>
              <td>{{ product.views_count }}</td>
              <td>{{ product.sales_count }}</td>
              <td>
                <button class="btn-small" @click="editProduct(product)">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-info" v-if="totalCount > 0">
        Showing {{ products.length }} of {{ totalCount }} products
      </div>
    </div>

    <!-- Edit Product Modal -->
    <div v-if="selectedProduct" class="modal" @click.self="selectedProduct = null">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Moderate Product</h2>
          <button class="close-btn" @click="selectedProduct = null">×</button>
        </div>
        <div class="modal-body">
          <div class="product-details">
            <h3>{{ selectedProduct.name }}</h3>
            <p><strong>Seller:</strong> {{ selectedProduct.seller_name }}</p>
            <p><strong>Price:</strong> {{ selectedProduct.price }}</p>
            <p><strong>Stock:</strong> {{ selectedProduct.stock_quantity }}</p>
            <p><strong>Views:</strong> {{ selectedProduct.views_count }}</p>
            <p><strong>Sales:</strong> {{ selectedProduct.sales_count }}</p>
          </div>
          <div class="moderation-controls">
            <div class="control-item">
              <label>
                <input type="checkbox" v-model="selectedProduct.is_active" />
                Active (Visible to buyers)
              </label>
            </div>
            <div class="control-item">
              <label>
                <input type="checkbox" v-model="selectedProduct.is_featured" />
                Featured (Show on homepage)
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-danger" @click="deleteProduct">Delete Product</button>
          <button class="btn-secondary" @click="selectedProduct = null">Cancel</button>
          <button class="btn-primary" @click="updateProduct">Save Changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'

const router = useRouter()
const loading = ref(true)
const products = ref([])
const totalCount = ref(0)
const selectedProduct = ref(null)

const filters = ref({
  search: '',
  is_active: '',
  is_featured: ''
})

onMounted(() => {
  fetchProducts()
})

async function fetchProducts() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.is_active) params.is_active = filters.value.is_active
    if (filters.value.is_featured) params.is_featured = filters.value.is_featured

    const response = await api.get('/users/admin/products/', { params })
    products.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to fetch products:', error)
    alert('Failed to fetch products')
  } finally {
    loading.value = false
  }
}

function editProduct(product) {
  selectedProduct.value = { ...product }
}

async function updateProduct() {
  try {
    await api.put(`/users/admin/products/${selectedProduct.value.id}/`, {
      is_active: selectedProduct.value.is_active,
      is_featured: selectedProduct.value.is_featured
    })
    alert('Product updated successfully')
    selectedProduct.value = null
    fetchProducts()
  } catch (error) {
    console.error('Failed to update product:', error)
    alert('Failed to update product')
  }
}

async function deleteProduct() {
  if (!confirm('Are you sure you want to delete this product? This action cannot be undone.')) {
    return
  }
  try {
    await api.delete(`/users/admin/products/${selectedProduct.value.id}/`)
    alert('Product deleted successfully')
    selectedProduct.value = null
    fetchProducts()
  } catch (error) {
    console.error('Failed to delete product:', error)
    alert('Failed to delete product')
  }
}
</script>

<style scoped>
.admin-products {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #333;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: #666;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
}

.back-btn:hover {
  background: #555;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 300px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.filter-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
  background: white;
  cursor: pointer;
}

.table-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow-x: auto;
}

.loading, .empty {
  padding: 3rem;
  text-align: center;
  color: #999;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #dee2e6;
  white-space: nowrap;
}

.products-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.product-info strong {
  display: block;
  color: #333;
  margin-bottom: 0.25rem;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.status.active {
  background: #c8e6c9;
  color: #2e7d32;
}

.status.inactive {
  background: #ffcdd2;
  color: #c62828;
}

.featured {
  font-size: 1.25rem;
}

.btn-small {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-small:hover {
  background: #5568d3;
}

.pagination-info {
  margin-top: 1rem;
  text-align: center;
  color: #666;
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #999;
  line-height: 1;
  padding: 0;
  width: 2rem;
  height: 2rem;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.product-details {
  margin-bottom: 2rem;
}

.product-details h3 {
  margin-bottom: 1rem;
  color: #333;
}

.product-details p {
  margin: 0.5rem 0;
  color: #666;
}

.moderation-controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.control-item label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
}

.control-item input[type="checkbox"] {
  width: 1.25rem;
  height: 1.25rem;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #dee2e6;
}

.btn-primary, .btn-secondary, .btn-danger {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5568d3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
}
</style>
