<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">User Management</h1>
          <p class="mt-2 text-sm text-gray-600">Manage all platform users</p>
        </div>
        <button @click="router.push('/admin/dashboard')" class="btn btn-secondary">
          ← Back to Dashboard
        </button>
      </div>

      <!-- Filters -->
      <div class="flex gap-4 mb-6">
        <input
          v-model="filters.search"
          type="text"
          placeholder="Search by name, email, or phone..."
          class="form-input flex-1"
          @input="fetchUsers"
        />
        <select v-model="filters.role" @change="fetchUsers" class="form-select w-48">
          <option value="">All Roles</option>
          <option value="BUYER">Buyer</option>
          <option value="SELLER">Seller</option>
          <option value="ADMIN">Admin</option>
        </select>
        <select v-model="filters.is_active" @change="fetchUsers" class="form-select w-48">
          <option value="">All Status</option>
          <option value="true">Active</option>
          <option value="false">Inactive</option>
        </select>
      </div>

      <!-- Users Table -->
      <div class="card">
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
        <div v-else-if="users.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
          </svg>
          <p class="mt-2 text-sm text-gray-500">No users found</p>
        </div>
        <div v-else>
          <div class="overflow-x-auto">
            <table class="table">
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
                  <td class="font-medium text-gray-900">{{ user.full_name }}</td>
                  <td class="text-gray-600">{{ user.phone_number }}</td>
                  <td class="text-gray-600">{{ user.email || 'N/A' }}</td>
                  <td>
                    <span :class="[
                      'badge',
                      user.role === 'BUYER' ? 'badge-info' :
                      user.role === 'SELLER' ? 'badge-primary' :
                      'badge-danger'
                    ]">
                      {{ user.role }}
                    </span>
                  </td>
                  <td>
                    <span :class="[
                      'badge',
                      user.is_active ? 'badge-success' : 'badge-danger'
                    ]">
                      {{ user.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </td>
                  <td class="text-sm text-gray-600">{{ formatDate(user.date_joined) }}</td>
                  <td>
                    <button @click="viewUser(user.id)" class="btn btn-primary btn-sm">
                      View
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="totalCount > 0" class="px-6 py-4 border-t border-gray-200 text-sm text-gray-600">
            Showing {{ users.length }} of {{ totalCount }} users
          </div>
        </div>
      </div>
    </div>

    <!-- User Detail Modal -->
    <div v-if="selectedUser" class="modal-overlay" @click.self="selectedUser = null">
      <div class="modal-content w-full max-w-2xl">
        <div class="modal-header">
          <h2 class="text-xl font-bold">User Details</h2>
          <button @click="selectedUser = null" class="text-gray-400 hover:text-gray-600 text-3xl font-light leading-none">&times;</button>
        </div>
        <div class="modal-body space-y-6">
          <!-- Basic Info -->
          <div>
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Basic Information</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="form-label">First Name</label>
                <p class="text-gray-900">{{ selectedUser.first_name }}</p>
              </div>
              <div>
                <label class="form-label">Last Name</label>
                <p class="text-gray-900">{{ selectedUser.last_name }}</p>
              </div>
              <div>
                <label class="form-label">Phone</label>
                <p class="text-gray-900">{{ selectedUser.phone_number }}</p>
              </div>
              <div>
                <label class="form-label">Email</label>
                <p class="text-gray-900">{{ selectedUser.email || 'Not provided' }}</p>
              </div>
            </div>
          </div>

          <!-- Account Settings -->
          <div>
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Account Settings</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="role" class="form-label">Role</label>
                <select id="role" v-model="selectedUser.role" class="form-select">
                  <option value="BUYER">Buyer</option>
                  <option value="SELLER">Seller</option>
                  <option value="ADMIN">Admin</option>
                </select>
              </div>
              <div class="space-y-2">
                <label class="flex items-center space-x-2 cursor-pointer">
                  <input type="checkbox" v-model="selectedUser.is_active" class="w-4 h-4 text-primary-600 rounded" />
                  <span class="text-sm font-medium text-gray-700">Active Account</span>
                </label>
                <label class="flex items-center space-x-2 cursor-pointer">
                  <input type="checkbox" v-model="selectedUser.is_verified" class="w-4 h-4 text-primary-600 rounded" />
                  <span class="text-sm font-medium text-gray-700">Verified</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Additional Info -->
          <div>
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Additional Information</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="form-label">MFA Enabled</label>
                <p class="text-gray-900">{{ selectedUser.mfa_enabled ? 'Yes' : 'No' }}</p>
              </div>
              <div>
                <label class="form-label">Joined</label>
                <p class="text-gray-900">{{ formatDate(selectedUser.date_joined) }}</p>
              </div>
              <div>
                <label class="form-label">Last Login</label>
                <p class="text-gray-900">{{ selectedUser.last_login ? formatDate(selectedUser.last_login) : 'Never' }}</p>
              </div>
            </div>
          </div>

          <!-- Profile Info -->
          <div v-if="selectedUser.profile">
            <h3 class="text-lg font-semibold mb-3 pb-2 border-b-2 border-primary-500">Profile Information</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="form-label">Country</label>
                <p class="text-gray-900">{{ selectedUser.profile.country }}</p>
              </div>
              <div>
                <label class="form-label">City</label>
                <p class="text-gray-900">{{ selectedUser.profile.city || 'N/A' }}</p>
              </div>
              <div>
                <label class="form-label">Language</label>
                <p class="text-gray-900">{{ selectedUser.profile.preferred_language }}</p>
              </div>
              <div>
                <label class="form-label">Currency</label>
                <p class="text-gray-900">{{ selectedUser.profile.preferred_currency }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="deleteUser" class="btn btn-danger">Delete User</button>
          <button @click="selectedUser = null" class="btn btn-secondary">Cancel</button>
          <button @click="updateUser" class="btn btn-primary">Save Changes</button>
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
