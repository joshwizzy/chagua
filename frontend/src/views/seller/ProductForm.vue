<template>
  <div class="product-form-page">
    <div class="container">
      <h1>{{ isEdit ? 'Edit Product' : 'Add New Product' }}</h1>

      <form @submit.prevent="handleSubmit" class="product-form">
        <div class="form-section">
          <h2>Basic Information</h2>

          <div class="form-group">
            <label>Product Name*</label>
            <input v-model="form.name" type="text" required />
          </div>

          <div class="form-group">
            <label>Description*</label>
            <textarea v-model="form.description" rows="5" required></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Category*</label>
              <select v-model="form.category" required>
                <option value="">Select Category</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Price (UGX)*</label>
              <input v-model.number="form.price" type="number" min="0" step="100" required />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Stock Quantity*</label>
              <input v-model.number="form.stock_quantity" type="number" min="0" required />
            </div>

            <div class="form-group">
              <label>Availability*</label>
              <select v-model="form.availability" required>
                <option value="IN_STOCK">In Stock</option>
                <option value="OUT_OF_STOCK">Out of Stock</option>
                <option value="PRE_ORDER">Pre-order</option>
              </select>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h2>Product Images</h2>
          <div class="image-upload">
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              multiple
              @change="handleImageUpload"
              style="display: none"
            />
            <button type="button" @click="$refs.fileInput.click()" class="btn btn-secondary">
              Choose Images
            </button>
            <p class="help-text">Upload up to 5 images (JPG, PNG, max 5MB each)</p>

            <div v-if="imagePreviews.length > 0" class="image-previews">
              <div v-for="(preview, index) in imagePreviews" :key="index" class="image-preview">
                <img :src="preview" alt="Preview" />
                <button type="button" @click="removeImage(index)" class="remove-image">×</button>
              </div>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h2>SEO (Optional)</h2>

          <div class="form-group">
            <label>Meta Title</label>
            <input v-model="form.meta_title" type="text" />
          </div>

          <div class="form-group">
            <label>Meta Description</label>
            <textarea v-model="form.meta_description" rows="3"></textarea>
          </div>
        </div>

        <div class="form-section">
          <h2>Status</h2>

          <label class="checkbox-label">
            <input type="checkbox" v-model="form.is_active" />
            Product is active (visible to buyers)
          </label>

          <label class="checkbox-label">
            <input type="checkbox" v-model="form.is_featured" />
            Feature this product on homepage
          </label>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="submitting">
            {{ submitting ? 'Saving...' : (isEdit ? 'Update Product' : 'Create Product') }}
          </button>
          <router-link to="/seller/products" class="btn btn-secondary">
            Cancel
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../../services/api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const categories = ref([])
const submitting = ref(false)
const error = ref(null)
const imagePreviews = ref([])
const imageFiles = ref([])

const form = ref({
  name: '',
  description: '',
  category: '',
  price: 0,
  stock_quantity: 0,
  availability: 'IN_STOCK',
  meta_title: '',
  meta_description: '',
  is_active: true,
  is_featured: false
})

onMounted(async () => {
  await fetchCategories()

  if (isEdit.value) {
    await fetchProduct()
  }
})

async function fetchCategories() {
  try {
    const response = await api.get('/products/categories/')
    categories.value = response.data
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

async function fetchProduct() {
  try {
    const response = await api.get(`/products/seller/products/${route.params.id}/`)
    form.value = {
      name: response.data.name,
      description: response.data.description,
      category: response.data.category?.id || '',
      price: response.data.price,
      stock_quantity: response.data.stock_quantity,
      availability: response.data.availability,
      meta_title: response.data.meta_title || '',
      meta_description: response.data.meta_description || '',
      is_active: response.data.is_active,
      is_featured: response.data.is_featured
    }
  } catch (err) {
    error.value = 'Failed to load product'
  }
}

function handleImageUpload(event) {
  const files = Array.from(event.target.files)
  const maxFiles = 5 - imagePreviews.value.length

  files.slice(0, maxFiles).forEach(file => {
    if (file.size > 5 * 1024 * 1024) {
      alert(`${file.name} is too large. Max size is 5MB.`)
      return
    }

    imageFiles.value.push(file)

    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreviews.value.push(e.target.result)
    }
    reader.readAsDataURL(file)
  })
}

function removeImage(index) {
  imagePreviews.value.splice(index, 1)
  imageFiles.value.splice(index, 1)
}

async function handleSubmit() {
  submitting.value = true
  error.value = null

  try {
    let productId

    if (isEdit.value) {
      // Update existing product
      await api.put(`/products/seller/products/${route.params.id}/`, form.value)
      productId = route.params.id
    } else {
      // Create new product
      const response = await api.post('/products/seller/products/', form.value)
      productId = response.data.id
    }

    // Upload images if any
    if (imageFiles.value.length > 0) {
      for (let i = 0; i < imageFiles.value.length; i++) {
        const formData = new FormData()
        formData.append('product_id', productId)
        formData.append('image', imageFiles.value[i])
        formData.append('is_primary', i === 0) // First image is primary
        formData.append('order', i)

        await api.post('/products/images/upload/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }
    }

    router.push('/seller/products')
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to save product'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.product-form-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 2rem 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: #333;
}

.product-form {
  background: white;
  border-radius: 0.5rem;
  padding: 2rem;
}

.form-section {
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

.form-section:last-of-type {
  border-bottom: none;
}

.form-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.image-upload {
  margin-top: 1rem;
}

.help-text {
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.image-previews {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.image-preview {
  position: relative;
  aspect-ratio: 1;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 2px solid #eee;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(220, 38, 38, 0.9);
  color: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  cursor: pointer;
}

.error-message {
  padding: 1rem;
  background: #fee;
  color: #c33;
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  border: 2px solid #ddd;
  color: #666;
}

.btn-secondary:hover {
  border-color: #999;
}
</style>
