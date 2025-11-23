<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-purple-700 p-4">
    <div class="w-full max-w-md">
      <div class="bg-white rounded-2xl shadow-2xl p-8">
        <h1 class="text-3xl font-bold text-center text-gray-900 mb-8">{{ $t('auth.login') }}</h1>

        <form @submit.prevent="handleLogin" class="space-y-6">
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
            <label class="form-label">{{ $t('auth.pin') }}</label>
            <input
              v-model="form.pin"
              type="password"
              placeholder="Enter your PIN"
              minlength="4"
              maxlength="6"
              required
              class="form-input"
            />
          </div>

          <div v-if="mfaRequired">
            <label class="form-label">MFA Token</label>
            <input
              v-model="form.mfa_token"
              type="text"
              placeholder="Enter 6-digit code"
              maxlength="6"
              class="form-input"
            />
          </div>

          <div v-if="error" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary w-full" :disabled="loading">
            {{ loading ? 'Logging in...' : $t('auth.login') }}
          </button>
        </form>

        <p class="text-center mt-6 text-gray-600">
          Don't have an account?
          <router-link to="/register" class="text-primary-600 hover:text-primary-700 font-semibold hover:underline">
            {{ $t('auth.register') }}
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
  phone_number: '',
  pin: '',
  mfa_token: ''
})

const loading = ref(false)
const error = ref(null)
const mfaRequired = ref(false)

async function handleLogin() {
  loading.value = true
  error.value = null

  const result = await authStore.login(form.value)

  if (result.success) {
    router.push('/')
  } else {
    if (result.error?.mfa_token) {
      mfaRequired.value = true
      error.value = 'Please enter your MFA token'
    } else {
      error.value = typeof result.error === 'string'
        ? result.error
        : 'Invalid phone number or PIN'
    }
  }

  loading.value = false
}
</script>
