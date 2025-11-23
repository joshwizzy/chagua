<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ isEdit ? 'Edit Product' : 'Add New Product' }}</h1>

      <form @submit.prevent="handleSubmit" class="card">
        <div class="card-body space-y-8">
          <!-- Basic Information -->
          <div class="pb-8 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Basic Information</h2>

            <div class="space-y-6">
              <div>
                <label class="form-label">Product Name*</label>
                <input v-model="form.name" type="text" required class="form-input" />
              </div>

              <div>
                <label class="form-label">Description*</label>
                <textarea v-model="form.description" rows="5" required class="form-input"></textarea>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="form-label">Category*</label>
                  <select v-model="form.category" required class="form-select">
                    <option value="">Select Category</option>
                    <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                      {{ cat.name }}
                    </option>
                  </select>
                </div>

                <div>
                  <label class="form-label">Price (UGX)*</label>
                  <input v-model.number="form.price" type="number" min="0" step="100" required class="form-input" />
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="form-label">Stock Quantity*</label>
                  <input v-model.number="form.stock_quantity" type="number" min="0" required class="form-input" />
                </div>

                <div>
                  <label class="form-label">Availability*</label>
                  <select v-model="form.availability" required class="form-select">
                    <option value="IN_STOCK">In Stock</option>
                    <option value="OUT_OF_STOCK">Out of Stock</option>
                    <option value="PRE_ORDER">Pre-order</option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <!-- Product Images -->
          <div class="pb-8 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Product Images</h2>

            <div class="space-y-4">
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                multiple
                @change="handleImageUpload"
                class="hidden"
              />
              <button type="button" @click="$refs.fileInput.click()" class="btn btn-secondary">
                Choose Images
              </button>
              <p class="text-sm text-gray-600">Upload up to 5 images (JPG, PNG, max 5MB each)</p>

              <div v-if="imagePreviews.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                <div v-for="(preview, index) in imagePreviews" :key="index" class="relative aspect-square rounded-lg overflow-hidden border-2 border-gray-200">
                  <img :src="preview" alt="Preview" class="w-full h-full object-cover" />
                  <button
                    type="button"
                    @click="removeImage(index)"
                    class="absolute top-2 right-2 w-8 h-8 rounded-full bg-red-600 hover:bg-red-700 text-white font-bold flex items-center justify-center text-xl leading-none transition-colors"
                  >
                    ×
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- SEO (Optional) -->
          <div class="pb-8 border-b border-gray-200">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">SEO (Optional)</h2>

            <div class="space-y-6">
              <div>
                <label class="form-label">Meta Title</label>
                <input v-model="form.meta_title" type="text" class="form-input" />
              </div>

              <div>
                <label class="form-label">Meta Description</label>
                <textarea v-model="form.meta_description" rows="3" class="form-input"></textarea>
              </div>
            </div>
          </div>

          <!-- Status -->
          <div>
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Status</h2>

            <div class="space-y-3">
              <label class="flex items-center space-x-3 cursor-pointer">
                <input type="checkbox" v-model="form.is_active" class="w-4 h-4 text-primary-600 rounded focus:ring-2 focus:ring-primary-500" />
                <span class="text-sm font-medium text-gray-700">Product is active (visible to buyers)</span>
              </label>

              <label class="flex items-center space-x-3 cursor-pointer">
                <input type="checkbox" v-model="form.is_featured" class="w-4 h-4 text-primary-600 rounded focus:ring-2 focus:ring-primary-500" />
                <span class="text-sm font-medium text-gray-700">Feature this product on homepage</span>
              </label>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {{ error }}
          </div>

          <!-- Form Actions -->
          <div class="flex gap-4 pt-4">
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Saving...' : (isEdit ? 'Update Product' : 'Create Product') }}
            </button>
            <router-link to="/seller/products" class="btn btn-secondary">
              Cancel
            </router-link>
          </div>
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
