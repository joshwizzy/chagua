<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-card">
        <h1>{{ $t('auth.register') }}</h1>

        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label>{{ $t('auth.firstName') }}</label>
            <input
              v-model="form.first_name"
              type="text"
              required
            />
          </div>

          <div class="form-group">
            <label>{{ $t('auth.lastName') }}</label>
            <input
              v-model="form.last_name"
              type="text"
              required
            />
          </div>

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
            <label>{{ $t('auth.email') }} (Optional)</label>
            <input
              v-model="form.email"
              type="email"
            />
          </div>

          <div class="form-group">
            <label>I want to be a:</label>
            <select v-model="form.role" required>
              <option value="BUYER">Buyer</option>
              <option value="SELLER">Seller</option>
            </select>
          </div>

          <div class="form-group">
            <label>{{ $t('auth.pin') }}</label>
            <input
              v-model="form.pin"
              type="password"
              placeholder="4-6 digit PIN"
              minlength="4"
              maxlength="6"
              required
            />
          </div>

          <div class="form-group">
            <label>Confirm PIN</label>
            <input
              v-model="form.pin_confirm"
              type="password"
              placeholder="Re-enter your PIN"
              minlength="4"
              maxlength="6"
              required
            />
          </div>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Creating account...' : $t('auth.register') }}
          </button>
        </form>

        <p class="auth-footer">
          Already have an account?
          <router-link to="/login">{{ $t('auth.login') }}</router-link>
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
  max-width: 500px;
}

.auth-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0,0,0,0.1);
  max-height: 90vh;
  overflow-y: auto;
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

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
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
