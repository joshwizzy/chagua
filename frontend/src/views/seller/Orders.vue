<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">My Orders</h1>
          <p class="mt-2 text-sm text-gray-600">Manage and fulfill customer orders</p>
        </div>
        <button @click="router.push('/seller/dashboard')" class="btn btn-secondary">
          ← Back to Dashboard
        </button>
      </div>

      <!-- Filters -->
      <div class="flex gap-4 mb-6">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search by tracking number or buyer name..."
          class="form-input flex-1"
          @input="fetchOrders"
        />
        <select v-model="filters.status" @change="fetchOrders" class="form-select w-64">
          <option value="">All Status</option>
          <option value="PENDING">Pending</option>
          <option value="CONFIRMED">Confirmed</option>
          <option value="PROCESSING">Processing</option>
          <option value="SHIPPED">Shipped</option>
          <option value="DELIVERED">Delivered</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <!-- Summary Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div class="card">
          <div class="card-body">
            <p class="text-sm text-gray-600 mb-1">Total Orders</p>
            <p class="text-3xl font-bold text-gray-900">{{ summary.total }}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-body">
            <p class="text-sm text-gray-600 mb-1">Pending</p>
            <p class="text-3xl font-bold text-yellow-600">{{ summary.pending }}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-body">
            <p class="text-sm text-gray-600 mb-1">In Progress</p>
            <p class="text-3xl font-bold text-blue-600">{{ summary.inProgress }}</p>
          </div>
        </div>
        <div class="card">
          <div class="card-body">
            <p class="text-sm text-gray-600 mb-1">Completed</p>
            <p class="text-3xl font-bold text-green-600">{{ summary.completed }}</p>
          </div>
        </div>
      </div>

      <!-- Orders Table -->
      <div class="card">
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        <div v-else-if="orders.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-500">No orders found</p>
        </div>
        <div v-else class="overflow-x-auto">
          <table class="table">
            <thead>
              <tr>
                <th>Tracking #</th>
                <th>Buyer</th>
                <th>Items</th>
                <th>Total</th>
                <th>Payment</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td class="font-semibold">{{ order.tracking_number }}</td>
                <td>{{ order.buyer_name }}</td>
                <td>{{ order.items_count }} item(s)</td>
                <td class="font-semibold">{{ formatPrice(order.total_amount) }}</td>
                <td>
                  <div class="space-y-1">
                    <p class="text-xs text-gray-600">{{ order.payment_method }}</p>
                    <span :class="[
                      'badge',
                      order.payment_status === 'PAID' ? 'badge-success' : 'badge-warning'
                    ]">
                      {{ order.payment_status }}
                    </span>
                  </div>
                </td>
                <td>
                  <span :class="['status-badge', `status-${order.status.toLowerCase()}`]">
                    {{ order.status }}
                  </span>
                </td>
                <td class="text-sm text-gray-600">{{ formatDate(order.created_at) }}</td>
                <td>
                  <div class="flex gap-2">
                    <button @click="viewOrderDetails(order.id)" class="btn btn-primary btn-sm">
                      View
                    </button>
                    <button
                      v-if="canUpdateStatus(order)"
                      @click="openStatusUpdate(order)"
                      class="btn btn-success btn-sm"
                    >
                      Update
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Order Detail Modal -->
    <div v-if="selectedOrder" class="modal-overlay" @click.self="closeOrderDetails">
      <div class="modal-content w-full max-w-4xl">
        <div class="modal-header">
          <h2 class="text-xl font-bold">Order Details - {{ selectedOrder.tracking_number }}</h2>
          <button @click="closeOrderDetails" class="text-gray-400 hover:text-gray-600 text-3xl font-light leading-none">&times;</button>
        </div>
        <div class="modal-body space-y-6">
          <!-- Order Info -->
          <div>
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Order Information</h3>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <p class="text-sm font-medium text-gray-600">Status</p>
                <span :class="['status-badge', `status-${selectedOrder.status.toLowerCase()}`]">
                  {{ selectedOrder.status }}
                </span>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-600">Payment Status</p>
                <span :class="[
                  'badge',
                  selectedOrder.payment_status === 'PAID' ? 'badge-success' : 'badge-warning'
                ]">
                  {{ selectedOrder.payment_status }}
                </span>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-600">Payment Method</p>
                <p class="text-gray-900">{{ selectedOrder.payment_method }}</p>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-600">Order Date</p>
                <p class="text-gray-900">{{ formatDateTime(selectedOrder.created_at) }}</p>
              </div>
              <div v-if="selectedOrder.estimated_delivery_date">
                <p class="text-sm font-medium text-gray-600">Est. Delivery</p>
                <p class="text-gray-900">{{ formatDate(selectedOrder.estimated_delivery_date) }}</p>
              </div>
              <div v-if="selectedOrder.shipped_at">
                <p class="text-sm font-medium text-gray-600">Shipped At</p>
                <p class="text-gray-900">{{ formatDateTime(selectedOrder.shipped_at) }}</p>
              </div>
            </div>
          </div>

          <!-- Buyer Info -->
          <div>
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Buyer Information</h3>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <p class="text-sm font-medium text-gray-600">Name</p>
                <p class="text-gray-900">{{ selectedOrder.buyer_name }}</p>
              </div>
              <div v-if="selectedOrder.buyer_phone">
                <p class="text-sm font-medium text-gray-600">Phone</p>
                <p class="text-gray-900">{{ selectedOrder.buyer_phone }}</p>
              </div>
              <div v-if="selectedOrder.buyer_email">
                <p class="text-sm font-medium text-gray-600">Email</p>
                <p class="text-gray-900">{{ selectedOrder.buyer_email }}</p>
              </div>
            </div>
          </div>

          <!-- Delivery Address -->
          <div v-if="selectedOrder.delivery_address">
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Delivery Address</h3>
            <div class="bg-gray-50 p-4 rounded-lg border-l-4 border-primary-500">
              <p class="text-gray-900">{{ selectedOrder.delivery_address.street_address }}</p>
              <p v-if="selectedOrder.delivery_address.apartment" class="text-gray-900">{{ selectedOrder.delivery_address.apartment }}</p>
              <p class="text-gray-900">{{ selectedOrder.delivery_address.city }}, {{ selectedOrder.delivery_address.country }}</p>
              <p v-if="selectedOrder.delivery_address.postal_code" class="text-gray-600">{{ selectedOrder.delivery_address.postal_code }}</p>
              <p v-if="selectedOrder.delivery_address.phone_number" class="text-gray-600 mt-2">Phone: {{ selectedOrder.delivery_address.phone_number }}</p>
            </div>
          </div>

          <!-- Order Items -->
          <div>
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Order Items</h3>
            <table class="table">
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Quantity</th>
                  <th>Unit Price</th>
                  <th>Subtotal</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in selectedOrder.items" :key="item.id">
                  <td>{{ item.product_name }}</td>
                  <td>{{ item.quantity }}</td>
                  <td>{{ formatPrice(item.unit_price) }}</td>
                  <td class="font-semibold">{{ formatPrice(item.subtotal) }}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="border-t-2">
                  <td colspan="3" class="text-right font-bold">Total:</td>
                  <td class="font-bold text-lg">{{ formatPrice(selectedOrder.total_amount) }}</td>
                </tr>
              </tfoot>
            </table>
          </div>

          <!-- Notes -->
          <div v-if="selectedOrder.buyer_notes || selectedOrder.seller_notes">
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Notes</h3>
            <div class="space-y-3">
              <div v-if="selectedOrder.buyer_notes" class="bg-blue-50 p-3 rounded">
                <p class="text-sm font-medium text-blue-900 mb-1">Buyer Notes:</p>
                <p class="text-blue-800">{{ selectedOrder.buyer_notes }}</p>
              </div>
              <div v-if="selectedOrder.seller_notes" class="bg-green-50 p-3 rounded">
                <p class="text-sm font-medium text-green-900 mb-1">Seller Notes:</p>
                <p class="text-green-800">{{ selectedOrder.seller_notes }}</p>
              </div>
            </div>
          </div>

          <!-- Courier Receipt -->
          <div v-if="selectedOrder.courier_receipt_photo">
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Courier Receipt</h3>
            <img :src="selectedOrder.courier_receipt_photo" alt="Courier Receipt" class="max-w-full rounded-lg shadow-md" />
          </div>

          <!-- Order History -->
          <div v-if="orderHistory.length > 0">
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Order History</h3>
            <div class="relative pl-8 space-y-4">
              <div v-for="history in orderHistory" :key="history.id" class="relative">
                <div class="absolute left-[-2rem] top-1 w-3 h-3 bg-primary-600 rounded-full"></div>
                <div class="absolute left-[-1.75rem] top-4 w-0.5 h-full bg-gray-200"></div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex justify-between items-start mb-2">
                    <p class="font-semibold text-gray-900">{{ history.old_status }} → {{ history.new_status }}</p>
                    <p class="text-sm text-gray-600">{{ formatDateTime(history.timestamp) }}</p>
                  </div>
                  <p v-if="history.notes" class="text-gray-700 italic mb-2">{{ history.notes }}</p>
                  <p class="text-sm text-gray-600">By: {{ history.changed_by_name }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button v-if="canUpdateStatus(selectedOrder)" @click="openStatusUpdateFromDetail" class="btn btn-primary">
            Update Order Status
          </button>
          <button @click="closeOrderDetails" class="btn btn-secondary">Close</button>
        </div>
      </div>
    </div>

    <!-- Status Update Modal -->
    <div v-if="statusUpdateOrder" class="modal-overlay" @click.self="closeStatusUpdate">
      <div class="modal-content w-full max-w-lg">
        <div class="modal-header">
          <h2 class="text-xl font-bold">Update Order Status</h2>
          <button @click="closeStatusUpdate" class="text-gray-400 hover:text-gray-600 text-3xl font-light leading-none">&times;</button>
        </div>
        <div class="modal-body space-y-4">
          <div>
            <label class="form-label">Current Status</label>
            <span :class="['status-badge', `status-${statusUpdateOrder.status.toLowerCase()}`]">
              {{ statusUpdateOrder.status }}
            </span>
          </div>

          <div>
            <label for="new-status" class="form-label">New Status *</label>
            <select id="new-status" v-model="statusUpdateForm.status" class="form-select" required>
              <option value="">Select Status</option>
              <option value="CONFIRMED" v-if="statusUpdateOrder.status === 'PENDING'">Confirmed</option>
              <option value="PROCESSING" v-if="['CONFIRMED'].includes(statusUpdateOrder.status)">Processing</option>
              <option value="SHIPPED" v-if="['CONFIRMED', 'PROCESSING'].includes(statusUpdateOrder.status)">Shipped</option>
              <option value="DELIVERED" v-if="statusUpdateOrder.status === 'SHIPPED'">Delivered</option>
              <option value="CANCELLED" v-if="!['DELIVERED', 'CANCELLED'].includes(statusUpdateOrder.status)">Cancelled</option>
            </select>
          </div>

          <div v-if="statusUpdateForm.status === 'SHIPPED'">
            <label for="courier-receipt" class="form-label">Courier Receipt Photo</label>
            <input
              id="courier-receipt"
              type="file"
              @change="handleFileUpload"
              accept="image/*"
              class="form-input"
            />
            <p class="mt-1 text-sm text-gray-600">Upload proof of shipment</p>
          </div>

          <div v-if="['SHIPPED', 'PROCESSING'].includes(statusUpdateForm.status)">
            <label for="delivery-date" class="form-label">Estimated Delivery Date</label>
            <input
              id="delivery-date"
              type="date"
              v-model="statusUpdateForm.estimated_delivery_date"
              class="form-input"
              :min="getTodayDate()"
            />
          </div>

          <div>
            <label for="notes" class="form-label">Notes</label>
            <textarea
              id="notes"
              v-model="statusUpdateForm.notes"
              class="form-textarea"
              rows="4"
              placeholder="Add any notes about this status change..."
            ></textarea>
          </div>

          <div v-if="updateError" class="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded">
            {{ updateError }}
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeStatusUpdate" class="btn btn-secondary">Cancel</button>
          <button
            @click="submitStatusUpdate"
            :disabled="!statusUpdateForm.status || updating"
            class="btn btn-primary"
          >
            {{ updating ? 'Updating...' : 'Update Status' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'

const router = useRouter()
const loading = ref(true)
const updating = ref(false)
const orders = ref([])
const selectedOrder = ref(null)
const orderHistory = ref([])
const statusUpdateOrder = ref(null)
const updateError = ref('')

const filters = ref({
  search: '',
  status: ''
})

const statusUpdateForm = ref({
  status: '',
  courier_receipt_photo: null,
  estimated_delivery_date: '',
  notes: ''
})

const summary = computed(() => {
  return {
    total: orders.value.length,
    pending: orders.value.filter(o => o.status === 'PENDING').length,
    inProgress: orders.value.filter(o => ['CONFIRMED', 'PROCESSING', 'SHIPPED'].includes(o.status)).length,
    completed: orders.value.filter(o => o.status === 'DELIVERED').length
  }
})

onMounted(() => {
  fetchOrders()
})

async function fetchOrders() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.status) params.status = filters.value.status

    const response = await api.get('/orders/seller/', { params })
    orders.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch orders:', error)
    alert('Failed to fetch orders')
  } finally {
    loading.value = false
  }
}

async function viewOrderDetails(orderId) {
  try {
    const order = orders.value.find(o => o.id === orderId)
    if (!order) return

    const response = await api.get(`/orders/track/${order.tracking_number}/`)
    selectedOrder.value = response.data

    const historyResponse = await api.get(`/orders/${order.tracking_number}/history/`)
    orderHistory.value = historyResponse.data.results || historyResponse.data
  } catch (error) {
    console.error('Failed to fetch order details:', error)
    alert('Failed to fetch order details')
  }
}

function closeOrderDetails() {
  selectedOrder.value = null
  orderHistory.value = []
}

function openStatusUpdate(order) {
  statusUpdateOrder.value = order
  statusUpdateForm.value = {
    status: '',
    courier_receipt_photo: null,
    estimated_delivery_date: '',
    notes: ''
  }
  updateError.value = ''
}

function openStatusUpdateFromDetail() {
  statusUpdateOrder.value = selectedOrder.value
  statusUpdateForm.value = {
    status: '',
    courier_receipt_photo: null,
    estimated_delivery_date: '',
    notes: ''
  }
  updateError.value = ''
  closeOrderDetails()
}

function closeStatusUpdate() {
  statusUpdateOrder.value = null
  statusUpdateForm.value = {
    status: '',
    courier_receipt_photo: null,
    estimated_delivery_date: '',
    notes: ''
  }
  updateError.value = ''
}

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    statusUpdateForm.value.courier_receipt_photo = file
  }
}

async function submitStatusUpdate() {
  if (!statusUpdateForm.value.status) {
    updateError.value = 'Please select a status'
    return
  }

  updating.value = true
  updateError.value = ''

  try {
    const formData = new FormData()
    formData.append('status', statusUpdateForm.value.status)

    if (statusUpdateForm.value.notes) {
      formData.append('notes', statusUpdateForm.value.notes)
    }

    if (statusUpdateForm.value.courier_receipt_photo) {
      formData.append('courier_receipt_photo', statusUpdateForm.value.courier_receipt_photo)
    }

    if (statusUpdateForm.value.estimated_delivery_date) {
      formData.append('estimated_delivery_date', statusUpdateForm.value.estimated_delivery_date)
    }

    await api.put(`/orders/${statusUpdateOrder.value.id}/status/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    alert('Order status updated successfully')
    closeStatusUpdate()
    await fetchOrders()
  } catch (error) {
    console.error('Failed to update order status:', error)
    updateError.value = error.response?.data?.error || 'Failed to update order status'
  } finally {
    updating.value = false
  }
}

function canUpdateStatus(order) {
  return !['DELIVERED', 'CANCELLED'].includes(order.status)
}

function getTodayDate() {
  return new Date().toISOString().split('T')[0]
}

function formatPrice(price) {
  return new Intl.NumberFormat('en-UG', {
    style: 'currency',
    currency: 'UGX',
    minimumFractionDigits: 0
  }).format(price)
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function formatDateTime(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
