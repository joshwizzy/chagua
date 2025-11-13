<template>
  <div class="admin-users">
    <div class="container">
      <div class="header">
        <h1>User Management</h1>
        <button class="back-btn" @click="router.push('/admin/dashboard')">← Back to Dashboard</button>
      </div>

      <!-- Filters -->
      <div class="filters">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search by name, email, or phone..."
          class="search-input"
          @input="fetchUsers"
        />
        <select v-model="filters.role" @change="fetchUsers" class="filter-select">
          <option value="">All Roles</option>
          <option value="BUYER">Buyer</option>
          <option value="SELLER">Seller</option>
          <option value="ADMIN">Admin</option>
        </select>
        <select v-model="filters.is_active" @change="fetchUsers" class="filter-select">
          <option value="">All Status</option>
          <option value="true">Active</option>
          <option value="false">Inactive</option>
        </select>
      </div>

      <!-- Users Table -->
      <div class="table-container">
        <div v-if="loading" class="loading">Loading users...</div>
        <div v-else-if="users.length === 0" class="empty">No users found</div>
        <table v-else class="users-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.full_name }}</td>
              <td>{{ user.phone_number }}</td>
              <td>{{ user.email || 'N/A' }}</td>
              <td>
                <span class="badge" :class="'badge-' + user.role.toLowerCase()">
                  {{ user.role }}
                </span>
              </td>
              <td>
                <span class="status" :class="user.is_active ? 'active' : 'inactive'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>{{ formatDate(user.date_joined) }}</td>
              <td>
                <button class="btn-small" @click="viewUser(user.id)">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-info" v-if="totalCount > 0">
        Showing {{ users.length }} of {{ totalCount }} users
      </div>
    </div>

    <!-- User Detail Modal -->
    <div v-if="selectedUser" class="modal" @click.self="selectedUser = null">
      <div class="modal-content">
        <div class="modal-header">
          <h2>User Details</h2>
          <button class="close-btn" @click="selectedUser = null">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-grid">
            <div class="detail-item">
              <label>Name:</label>
              <span>{{ selectedUser.first_name }} {{ selectedUser.last_name }}</span>
            </div>
            <div class="detail-item">
              <label>Phone:</label>
              <span>{{ selectedUser.phone_number }}</span>
            </div>
            <div class="detail-item">
              <label>Email:</label>
              <span>{{ selectedUser.email || 'Not provided' }}</span>
            </div>
            <div class="detail-item">
              <label>Role:</label>
              <select v-model="selectedUser.role" class="edit-input">
                <option value="BUYER">Buyer</option>
                <option value="SELLER">Seller</option>
                <option value="ADMIN">Admin</option>
              </select>
            </div>
            <div class="detail-item">
              <label>Active:</label>
              <input type="checkbox" v-model="selectedUser.is_active" />
            </div>
            <div class="detail-item">
              <label>Verified:</label>
              <input type="checkbox" v-model="selectedUser.is_verified" />
            </div>
            <div class="detail-item">
              <label>MFA Enabled:</label>
              <span>{{ selectedUser.mfa_enabled ? 'Yes' : 'No' }}</span>
            </div>
            <div class="detail-item">
              <label>Joined:</label>
              <span>{{ formatDate(selectedUser.date_joined) }}</span>
            </div>
            <div class="detail-item">
              <label>Last Login:</label>
              <span>{{ selectedUser.last_login ? formatDate(selectedUser.last_login) : 'Never' }}</span>
            </div>
          </div>
          <div v-if="selectedUser.profile" class="profile-section">
            <h3>Profile Information</h3>
            <div class="detail-grid">
              <div class="detail-item">
                <label>Country:</label>
                <span>{{ selectedUser.profile.country }}</span>
              </div>
              <div class="detail-item">
                <label>City:</label>
                <span>{{ selectedUser.profile.city || 'N/A' }}</span>
              </div>
              <div class="detail-item">
                <label>Language:</label>
                <span>{{ selectedUser.profile.preferred_language }}</span>
              </div>
              <div class="detail-item">
                <label>Currency:</label>
                <span>{{ selectedUser.profile.preferred_currency }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-danger" @click="deleteUser">Delete User</button>
          <button class="btn-secondary" @click="selectedUser = null">Cancel</button>
          <button class="btn-primary" @click="updateUser">Save Changes</button>
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
const users = ref([])
const totalCount = ref(0)
const selectedUser = ref(null)

const filters = ref({
  search: '',
  role: '',
  is_active: ''
})

onMounted(() => {
  fetchUsers()
})

async function fetchUsers() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.role) params.role = filters.value.role
    if (filters.value.is_active) params.is_active = filters.value.is_active

    const response = await api.get('/users/admin/users/', { params })
    users.value = response.data.results
    totalCount.value = response.data.count
  } catch (error) {
    console.error('Failed to fetch users:', error)
    alert('Failed to fetch users')
  } finally {
    loading.value = false
  }
}

async function viewUser(userId) {
  try {
    const response = await api.get(`/users/admin/users/${userId}/`)
    selectedUser.value = response.data
  } catch (error) {
    console.error('Failed to fetch user details:', error)
    alert('Failed to fetch user details')
  }
}

async function updateUser() {
  try {
    await api.put(`/users/admin/users/${selectedUser.value.id}/`, {
      role: selectedUser.value.role,
      is_active: selectedUser.value.is_active,
      is_verified: selectedUser.value.is_verified
    })
    alert('User updated successfully')
    selectedUser.value = null
    fetchUsers()
  } catch (error) {
    console.error('Failed to update user:', error)
    alert('Failed to update user')
  }
}

async function deleteUser() {
  if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
    return
  }
  try {
    await api.delete(`/users/admin/users/${selectedUser.value.id}/`)
    alert('User deleted successfully')
    selectedUser.value = null
    fetchUsers()
  } catch (error) {
    console.error('Failed to delete user:', error)
    alert(error.response?.data?.error || 'Failed to delete user')
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>

<style scoped>
.admin-users {
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

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th {
  background: #f8f9fa;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #dee2e6;
}

.users-table td {
  padding: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.badge-buyer {
  background: #e3f2fd;
  color: #1976d2;
}

.badge-seller {
  background: #f3e5f5;
  color: #7b1fa2;
}

.badge-admin {
  background: #ffebee;
  color: #c62828;
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
  max-width: 700px;
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

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
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

.edit-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
  font-size: 1rem;
}

.profile-section {
  border-top: 1px solid #dee2e6;
  padding-top: 1.5rem;
}

.profile-section h3 {
  margin-bottom: 1rem;
  color: #333;
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
