<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <h1>{{ $t('auth.login') }}</h1>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>{{ $t('auth.phone') }}</label>
            <input
              v-model="form.phone_number"
              type="tel"
              placeholder="+256XXXXXXXXX"
              required
            />
          </div>

          <div class="form-group">
            <label>{{ $t('auth.pin') }}</label>
            <input
              v-model="form.pin"
              type="password"
              placeholder="Enter your PIN"
              minlength="4"
              maxlength="6"
              required
            />
          </div>

          <div v-if="mfaRequired" class="form-group">
            <label>MFA Token</label>
            <input
              v-model="form.mfa_token"
              type="text"
              placeholder="Enter 6-digit code"
              maxlength="6"
            />
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Logging in...' : $t('auth.login') }}
          </button>
        </form>

        <p class="auth-footer">
          Don't have an account?
          <router-link to="/register">{{ $t('auth.register') }}</router-link>
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

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.auth-container {
  width: 100%;
  max-width: 400px;
}

.auth-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
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
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.auth-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>
