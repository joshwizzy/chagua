<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-purple-700 p-4">
    <div class="w-full max-w-lg">
      <div class="bg-white rounded-2xl shadow-2xl p-8 max-h-[90vh] overflow-y-auto">
        <h1 class="text-3xl font-bold text-center text-gray-900 mb-8">{{ $t('auth.register') }}</h1>

        <form @submit.prevent="handleRegister" class="space-y-6">
          <div>
            <label class="form-label">{{ $t('auth.firstName') }}</label>
            <input
              v-model="form.first_name"
              type="text"
              required
              class="form-input"
            />
          </div>

          <div>
            <label class="form-label">{{ $t('auth.lastName') }}</label>
            <input
              v-model="form.last_name"
              type="text"
              required
              class="form-input"
            />
          </div>

          <div>
            <label class="form-label">{{ $t('auth.phone') }}</label>
            <input
              v-model="form.phone_number"
              type="tel"
              placeholder="+256XXXXXXXXX"
              required
              class="form-input"
            />
          </div>

          <div>
            <label class="form-label">{{ $t('auth.email') }} (Optional)</label>
            <input
              v-model="form.email"
              type="email"
              class="form-input"
            />
          </div>

          <div>
            <label class="form-label">I want to be a:</label>
            <select v-model="form.role" required class="form-select">
              <option value="BUYER">Buyer</option>
              <option value="SELLER">Seller</option>
            </select>
          </div>

          <div>
            <label class="form-label">{{ $t('auth.pin') }}</label>
            <input
              v-model="form.pin"
              type="password"
              placeholder="4-6 digit PIN"
              minlength="4"
              maxlength="6"
              required
              class="form-input"
            />
          </div>

          <div>
            <label class="form-label">Confirm PIN</label>
            <input
              v-model="form.pin_confirm"
              type="password"
              placeholder="Re-enter your PIN"
              minlength="4"
              maxlength="6"
              required
              class="form-input"
            />
          </div>

          <div v-if="error" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Creating account...' : $t('auth.register') }}
          </button>
        </form>

        <p class="text-center mt-6 text-gray-600">
          Already have an account?
          <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-semibold hover:underline">
            {{ $t('auth.login') }}
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  first_name: '',
  last_name: '',
  phone_number: '',
  email: '',
  role: 'BUYER',
  pin: '',
  pin_confirm: ''
})

const loading = ref(false)
const error = ref(null)

async function handleRegister() {
  // Validate PIN match
  if (form.value.pin !== form.value.pin_confirm) {
    error.value = 'PINs do not match'
    return
  }

  loading.value = true
  error.value = null

  const result = await authStore.register(form.value)

  if (result.success) {
    router.push('/')
  } else {
    error.value = typeof result.error === 'string'
      ? result.error
      : JSON.stringify(result.error)
  }

  loading.value = false
}
</script>
