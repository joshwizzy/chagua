<template>
  <div class="seller-orders">
    <div class="container">
      <div class="header">
        <h1>My Orders</h1>
        <button class="back-btn" @click="router.push('/seller/dashboard')">← Back to Dashboard</button>
      </div>

      <!-- Filters -->
      <div class="filters">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search by tracking number or buyer name..."
          class="search-input"
          @input="fetchOrders"
        />
        <select v-model="filters.status" @change="fetchOrders" class="filter-select">
          <option value="">All Status</option>
          <option value="PENDING">Pending</option>
          <option value="CONFIRMED">Confirmed</option>
          <option value="PROCESSING">Processing</option>
          <option value="SHIPPED">Shipped</option>
          <option value="DELIVERED">Delivered</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <!-- Orders Summary -->
      <div class="summary-cards">
        <div class="summary-card">
          <span class="summary-label">Total Orders</span>
          <span class="summary-value">{{ summary.total }}</span>
        </div>
        <div class="summary-card">
          <span class="summary-label">Pending</span>
          <span class="summary-value pending">{{ summary.pending }}</span>
        </div>
        <div class="summary-card">
          <span class="summary-label">In Progress</span>
          <span class="summary-value processing">{{ summary.inProgress }}</span>
        </div>
        <div class="summary-card">
          <span class="summary-label">Completed</span>
          <span class="summary-value delivered">{{ summary.completed }}</span>
        </div>
      </div>

      <!-- Orders Table -->
      <div class="table-container">
        <div v-if="loading" class="loading">Loading orders...</div>
        <div v-else-if="orders.length === 0" class="empty">No orders found</div>
        <table v-else class="orders-table">
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
              <td><strong>{{ order.tracking_number }}</strong></td>
              <td>{{ order.buyer_name }}</td>
              <td>{{ order.items_count }} item(s)</td>
              <td>{{ formatPrice(order.total_amount) }}</td>
              <td>
                <div class="payment-info">
                  <span class="payment-method">{{ order.payment_method }}</span>
                  <span class="payment-status" :class="'payment-' + order.payment_status.toLowerCase()">
                    {{ order.payment_status }}
                  </span>
                </div>
              </td>
              <td>
                <span class="status" :class="'status-' + order.status.toLowerCase()">
                  {{ order.status }}
                </span>
              </td>
              <td>{{ formatDate(order.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button class="btn-small btn-view" @click="viewOrderDetails(order.id)">View</button>
                  <button
                    v-if="canUpdateStatus(order)"
                    class="btn-small btn-update"
                    @click="openStatusUpdate(order)"
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

    <!-- Order Detail Modal -->
    <div v-if="selectedOrder" class="modal" @click.self="closeOrderDetails">
      <div class="modal-content modal-large">
        <div class="modal-header">
          <h2>Order Details - {{ selectedOrder.tracking_number }}</h2>
          <button class="close-btn" @click="closeOrderDetails">×</button>
        </div>
        <div class="modal-body">
          <!-- Order Info -->
          <div class="detail-section">
            <h3>Order Information</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <label>Status:</label>
                <span class="status" :class="'status-' + selectedOrder.status.toLowerCase()">
                  {{ selectedOrder.status }}
                </span>
              </div>
              <div class="detail-item">
                <label>Payment Status:</label>
                <span class="payment-status" :class="'payment-' + selectedOrder.payment_status.toLowerCase()">
                  {{ selectedOrder.payment_status }}
                </span>
              </div>
              <div class="detail-item">
                <label>Payment Method:</label>
                <span>{{ selectedOrder.payment_method }}</span>
              </div>
              <div class="detail-item">
                <label>Order Date:</label>
                <span>{{ formatDateTime(selectedOrder.created_at) }}</span>
              </div>
              <div class="detail-item" v-if="selectedOrder.estimated_delivery_date">
                <label>Est. Delivery:</label>
                <span>{{ formatDate(selectedOrder.estimated_delivery_date) }}</span>
              </div>
              <div class="detail-item" v-if="selectedOrder.shipped_at">
                <label>Shipped At:</label>
                <span>{{ formatDateTime(selectedOrder.shipped_at) }}</span>
              </div>
            </div>
          </div>

          <!-- Buyer Info -->
          <div class="detail-section">
            <h3>Buyer Information</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <label>Name:</label>
                <span>{{ selectedOrder.buyer_name }}</span>
              </div>
              <div class="detail-item" v-if="selectedOrder.buyer_phone">
                <label>Phone:</label>
                <span>{{ selectedOrder.buyer_phone }}</span>
              </div>
              <div class="detail-item" v-if="selectedOrder.buyer_email">
                <label>Email:</label>
                <span>{{ selectedOrder.buyer_email }}</span>
              </div>
            </div>
          </div>

          <!-- Delivery Address -->
          <div class="detail-section" v-if="selectedOrder.delivery_address">
            <h3>Delivery Address</h3>
            <div class="address-box">
              <p>{{ selectedOrder.delivery_address.street_address }}</p>
              <p v-if="selectedOrder.delivery_address.apartment">{{ selectedOrder.delivery_address.apartment }}</p>
              <p>{{ selectedOrder.delivery_address.city }}, {{ selectedOrder.delivery_address.country }}</p>
              <p v-if="selectedOrder.delivery_address.postal_code">{{ selectedOrder.delivery_address.postal_code }}</p>
              <p v-if="selectedOrder.delivery_address.phone_number">Phone: {{ selectedOrder.delivery_address.phone_number }}</p>
            </div>
          </div>

          <!-- Order Items -->
          <div class="detail-section">
            <h3>Order Items</h3>
            <table class="items-table">
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
                  <td>{{ formatPrice(item.subtotal) }}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="3" class="text-right"><strong>Total:</strong></td>
                  <td><strong>{{ formatPrice(selectedOrder.total_amount) }}</strong></td>
                </tr>
              </tfoot>
            </table>
          </div>

          <!-- Notes -->
          <div class="detail-section" v-if="selectedOrder.buyer_notes || selectedOrder.seller_notes">
            <h3>Notes</h3>
            <div class="notes-box" v-if="selectedOrder.buyer_notes">
              <label>Buyer Notes:</label>
              <p>{{ selectedOrder.buyer_notes }}</p>
            </div>
            <div class="notes-box" v-if="selectedOrder.seller_notes">
              <label>Seller Notes:</label>
              <p>{{ selectedOrder.seller_notes }}</p>
            </div>
          </div>

          <!-- Courier Receipt -->
          <div class="detail-section" v-if="selectedOrder.courier_receipt_photo">
            <h3>Courier Receipt</h3>
            <img :src="selectedOrder.courier_receipt_photo" alt="Courier Receipt" class="receipt-image" />
          </div>

          <!-- Order History -->
          <div class="detail-section" v-if="orderHistory.length > 0">
            <h3>Order History</h3>
            <div class="history-timeline">
              <div v-for="history in orderHistory" :key="history.id" class="history-item">
                <div class="history-marker"></div>
                <div class="history-content">
                  <div class="history-header">
                    <strong>{{ history.old_status }} → {{ history.new_status }}</strong>
                    <span class="history-time">{{ formatDateTime(history.timestamp) }}</span>
                  </div>
                  <p v-if="history.notes" class="history-notes">{{ history.notes }}</p>
                  <p class="history-user">By: {{ history.changed_by_name }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            v-if="canUpdateStatus(selectedOrder)"
            class="btn-primary"
            @click="openStatusUpdateFromDetail"
          >
            Update Order Status
          </button>
          <button class="btn-secondary" @click="closeOrderDetails">Close</button>
        </div>
      </div>
    </div>

    <!-- Status Update Modal -->
    <div v-if="statusUpdateOrder" class="modal" @click.self="closeStatusUpdate">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Update Order Status</h2>
          <button class="close-btn" @click="closeStatusUpdate">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Current Status:</label>
            <span class="status" :class="'status-' + statusUpdateOrder.status.toLowerCase()">
              {{ statusUpdateOrder.status }}
            </span>
          </div>

          <div class="form-group">
            <label for="new-status">New Status: *</label>
            <select id="new-status" v-model="statusUpdateForm.status" class="form-input" required>
              <option value="">Select Status</option>
              <option value="CONFIRMED" v-if="statusUpdateOrder.status === 'PENDING'">Confirmed</option>
              <option value="PROCESSING" v-if="['CONFIRMED'].includes(statusUpdateOrder.status)">Processing</option>
              <option value="SHIPPED" v-if="['CONFIRMED', 'PROCESSING'].includes(statusUpdateOrder.status)">Shipped</option>
              <option value="DELIVERED" v-if="statusUpdateOrder.status === 'SHIPPED'">Delivered</option>
              <option value="CANCELLED" v-if="!['DELIVERED', 'CANCELLED'].includes(statusUpdateOrder.status)">Cancelled</option>
            </select>
          </div>

          <div class="form-group" v-if="statusUpdateForm.status === 'SHIPPED'">
            <label for="courier-receipt">Courier Receipt Photo:</label>
            <input
              id="courier-receipt"
              type="file"
              @change="handleFileUpload"
              accept="image/*"
              class="form-input"
            />
            <small>Upload proof of shipment</small>
          </div>

          <div class="form-group" v-if="['SHIPPED', 'PROCESSING'].includes(statusUpdateForm.status)">
            <label for="delivery-date">Estimated Delivery Date:</label>
            <input
              id="delivery-date"
              type="date"
              v-model="statusUpdateForm.estimated_delivery_date"
              class="form-input"
              :min="getTodayDate()"
            />
          </div>

          <div class="form-group">
            <label for="notes">Notes:</label>
            <textarea
              id="notes"
              v-model="statusUpdateForm.notes"
              class="form-input"
              rows="4"
              placeholder="Add any notes about this status change..."
            ></textarea>
          </div>

          <div v-if="updateError" class="error-message">{{ updateError }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeStatusUpdate">Cancel</button>
          <button
            class="btn-primary"
            @click="submitStatusUpdate"
            :disabled="!statusUpdateForm.status || updating"
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
    // Find order by ID
    const order = orders.value.find(o => o.id === orderId)
    if (!order) return

    // Fetch full order details
    const response = await api.get(`/orders/track/${order.tracking_number}/`)
    selectedOrder.value = response.data

    // Fetch order history
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

<style scoped>
.seller-orders {
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

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.summary-label {
  font-size: 0.875rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-value {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
}

.summary-value.pending {
  color: #f59e0b;
}

.summary-value.processing {
  color: #3b82f6;
}

.summary-value.delivered {
  color: #10b981;
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

.orders-table {
  width: 100%;
  border-collapse: collapse;
}

.orders-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #dee2e6;
  white-space: nowrap;
}

.orders-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.payment-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.payment-method {
  font-size: 0.875rem;
  color: #666;
}

.payment-status {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  width: fit-content;
}

.payment-status.payment-pending {
  background: #fff3cd;
  color: #856404;
}

.payment-status.payment-paid {
  background: #c8e6c9;
  color: #2e7d32;
}

.payment-status.payment-failed {
  background: #ffcdd2;
  color: #c62828;
}

.status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-confirmed {
  background: #cfe2ff;
  color: #084298;
}

.status-processing {
  background: #e7f3ff;
  color: #0056b3;
}

.status-shipped {
  background: #d1ecf1;
  color: #0c5460;
}

.status-delivered {
  background: #c8e6c9;
  color: #2e7d32;
}

.status-cancelled {
  background: #ffcdd2;
  color: #c62828;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-small {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
}

.btn-view {
  background: #667eea;
  color: white;
}

.btn-view:hover {
  background: #5568d3;
}

.btn-update {
  background: #10b981;
  color: white;
}

.btn-update:hover {
  background: #059669;
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
  overflow-y: auto;
  padding: 2rem;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  margin: auto;
}

.modal-large {
  max-width: 900px;
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

.detail-section {
  margin-bottom: 2rem;
}

.detail-section h3 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item label {
  font-weight: 600;
  color: #666;
  font-size: 0.875rem;
}

.detail-item span {
  color: #333;
}

.address-box {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 0.25rem;
  border-left: 3px solid #667eea;
}

.address-box p {
  margin: 0.25rem 0;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
}

.items-table th,
.items-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

.items-table th {
  background: #f8f9fa;
  font-weight: 600;
}

.items-table tfoot td {
  font-weight: 600;
  border-top: 2px solid #dee2e6;
}

.text-right {
  text-align: right;
}

.notes-box {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 0.25rem;
  margin-bottom: 1rem;
}

.notes-box label {
  font-weight: 600;
  color: #666;
  display: block;
  margin-bottom: 0.5rem;
}

.notes-box p {
  margin: 0;
  color: #333;
}

.receipt-image {
  max-width: 100%;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.history-timeline {
  position: relative;
  padding-left: 2rem;
}

.history-item {
  position: relative;
  padding-bottom: 1.5rem;
}

.history-marker {
  position: absolute;
  left: -2rem;
  top: 0.25rem;
  width: 1rem;
  height: 1rem;
  background: #667eea;
  border-radius: 50%;
}

.history-item:not(:last-child) .history-marker::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 1rem;
  width: 2px;
  height: calc(100% + 1rem);
  background: #dee2e6;
  transform: translateX(-50%);
}

.history-content {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 0.25rem;
}

.history-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.history-time {
  color: #666;
  font-size: 0.875rem;
}

.history-notes {
  margin: 0.5rem 0;
  color: #555;
  font-style: italic;
}

.history-user {
  margin: 0;
  font-size: 0.875rem;
  color: #666;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: #666;
  font-size: 0.875rem;
}

.error-message {
  padding: 0.75rem;
  background: #ffcdd2;
  color: #c62828;
  border-radius: 0.25rem;
  margin-top: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #dee2e6;
}

.btn-primary, .btn-secondary {
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

.btn-primary:hover:not(:disabled) {
  background: #5568d3;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}
</style>
