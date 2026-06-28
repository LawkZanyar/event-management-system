<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const BASE_URL = "https://mindful-manifestation-production.up.railway.app/api"

const view = ref('login')
const currentUser = ref(null)
const events = ref([])
const loadingEvents = ref(false)

const loginForm = ref({ email: '', password: '' })
const registerForm = ref({ name: '', email: '', password: '' })
const authError = ref('')
const authSuccess = ref('')

const registeringFor = ref(null)
const regMessage = ref('')

async function loadEvents() {
  loadingEvents.value = true
  try {
    const res = await axios.get(`${BASE_URL}/events`)
    events.value = res.data
  } catch (e) {
    console.error("API ERROR:", e)
  } finally {
    loadingEvents.value = false
  }
}

async function login() {
  authError.value = ''
  try {
    const res = await axios.post(`${BASE_URL}/login`, loginForm.value)
    currentUser.value = res.data.user
    localStorage.setItem('user', JSON.stringify(res.data.user))
    view.value = 'events'
    loadEvents()
  } catch (e) {
    authError.value = e.response?.data?.detail || 'Login failed'
  }
}

async function register() {
  authError.value = ''
  authSuccess.value = ''
  try {
    await axios.post(`${BASE_URL}/register`, registerForm.value)
    authSuccess.value = 'Account created! You can now log in.'
    registerForm.value = { name: '', email: '', password: '' }
    setTimeout(() => { view.value = 'login'; authSuccess.value = '' }, 1500)
  } catch (e) {
    authError.value = e.response?.data?.detail || 'Registration failed'
  }
}

async function registerForEvent(eventId) {
  regMessage.value = ''
  try {
    await axios.post(`${BASE_URL}/events/${eventId}/attendees`, {
      name: currentUser.value.name,
      email: currentUser.value.email,
      registered_at: new Date().toISOString().split('T')[0]
    })
    regMessage.value = 'Successfully registered for event!'
    registeringFor.value = null
  } catch (e) {
    regMessage.value = e.response?.data?.detail || 'Registration failed'
  }
}

function logout() {
  currentUser.value = null
  events.value = []
  loginForm.value = { email: '', password: '' }
  localStorage.removeItem('user')
  view.value = 'login'
}

onMounted(() => {
  const saved = localStorage.getItem('user')
  if (saved) {
    currentUser.value = JSON.parse(saved)
    view.value = 'events'
    loadEvents()
  }
})
</script>

<template>
  <div class="page">

    <header class="header">
      <div class="header-inner">
        <div class="logo">📅</div>
        <div>
          <h1 class="header-title">Event Management System</h1>
          <p class="header-sub">Web Technologies Project</p>
        </div>
        <div class="header-right" v-if="currentUser">
          <span class="welcome">👤 {{ currentUser.name }}</span>
          <button class="btn-logout" @click="logout">Logout</button>
        </div>
      </div>
    </header>

    <main class="main">

      <div v-if="view === 'login'" class="auth-wrapper">
        <div class="auth-card">
          <h2 class="auth-title">Welcome Back</h2>
          <p class="auth-sub">Sign in to view and register for events</p>

          <div v-if="authError" class="alert alert-error">{{ authError }}</div>

          <div class="form-group">
            <label>Email</label>
            <input v-model="loginForm.email" type="email" placeholder="you@example.com" />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="loginForm.password" type="password" placeholder="••••••••" />
          </div>

          <button class="btn-primary" @click="login">Sign In</button>

          <p class="auth-switch">
            Don't have an account?
            <span class="link" @click="view = 'register'; authError = ''">Register here</span>
          </p>
        </div>
      </div>

      <div v-if="view === 'register'" class="auth-wrapper">
        <div class="auth-card">
          <h2 class="auth-title">Create Account</h2>
          <p class="auth-sub">Register to join and attend events</p>

          <div v-if="authError" class="alert alert-error">{{ authError }}</div>
          <div v-if="authSuccess" class="alert alert-success">{{ authSuccess }}</div>

          <div class="form-group">
            <label>Full Name</label>
            <input v-model="registerForm.name" type="text" placeholder="Your name" />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="registerForm.email" type="email" placeholder="you@example.com" />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="registerForm.password" type="password" placeholder="••••••••" />
          </div>

          <button class="btn-primary" @click="register">Create Account</button>

          <p class="auth-switch">
            Already have an account?
            <span class="link" @click="view = 'login'; authError = ''">Sign in</span>
          </p>
        </div>
      </div>

      <div v-if="view === 'events'">

        <div class="events-header">
          <h2 class="events-title">Upcoming Events</h2>
          <p class="events-sub">Click "Register" on any event to sign up</p>
        </div>

        <div v-if="regMessage" class="alert alert-success reg-alert">{{ regMessage }}</div>

        <div v-if="loadingEvents" class="empty">
          <div class="empty-icon">⏳</div>
          <p class="empty-text">Loading events...</p>
        </div>

        <div v-else-if="events.length === 0" class="empty">
          <div class="empty-icon">🗓️</div>
          <p class="empty-text">No events found</p>
          <p class="empty-hint">Events created via the API will appear here.</p>
        </div>

        <div v-else class="grid">
          <div class="card" v-for="event in events" :key="event.id">

            <div class="card-header">
              <span class="card-id">#{{ event.id }}</span>
              <span class="card-badge">Event</span>
            </div>

            <h2 class="card-title">{{ event.title }}</h2>
            <p class="card-description">{{ event.description }}</p>

            <div class="card-meta">
              <div class="meta-item">
                <span class="meta-icon">📆</span>
                <span>{{ event.date }}</span>
              </div>
              <div class="meta-item">
                <span class="meta-icon">📍</span>
                <span>{{ event.location }}</span>
              </div>
            </div>

            <div class="card-actions">
              <button
                class="btn-register"
                @click="registeringFor = event.id; regMessage = ''"
                v-if="registeringFor !== event.id"
              >
                Register for Event
              </button>

              <div v-if="registeringFor === event.id" class="confirm-box">
                <p class="confirm-text">
                  Register as <strong>{{ currentUser.name }}</strong>?
                </p>
                <div class="confirm-buttons">
                  <button class="btn-confirm" @click="registerForEvent(event.id)">Confirm</button>
                  <button class="btn-cancel" @click="registeringFor = null">Cancel</button>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>

    </main>

    <footer class="footer">
      <p>Event Management System &mdash; Web Technologies Project</p>
    </footer>

  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.page {
  min-height: 100vh;
  background-color: #f1f5f9;
  font-family: 'Segoe UI', Arial, sans-serif;
  color: #1e293b;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #1c2e4a;
  padding: 20px 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.header-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo { font-size: 32px; }

.header-title {
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
}

.header-sub {
  font-size: 12px;
  color: #94b4cc;
  margin-top: 2px;
}

.header-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 14px;
}

.welcome {
  font-size: 13px;
  color: #94b4cc;
}

.btn-logout {
  background: transparent;
  border: 1px solid #64748b;
  color: #94b4cc;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.15s;
}

.btn-logout:hover {
  background: #ffffff15;
  color: #ffffff;
}

.main {
  flex: 1;
  max-width: 1100px;
  width: 100%;
  margin: 40px auto;
  padding: 0 24px;
}

.auth-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.auth-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #e2e8f0;
}

.auth-title {
  font-size: 22px;
  font-weight: 700;
  color: #1c2e4a;
  margin-bottom: 6px;
}

.auth-sub {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 24px;
}

.form-group { margin-bottom: 16px; }

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  outline: none;
  transition: border 0.15s;
}

.form-group input:focus { border-color: #0d7377; }

.btn-primary {
  width: 100%;
  background-color: #1c2e4a;
  color: #ffffff;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.15s;
}

.btn-primary:hover { background-color: #0d7377; }

.auth-switch {
  text-align: center;
  font-size: 13px;
  color: #64748b;
  margin-top: 18px;
}

.link {
  color: #0d7377;
  font-weight: 600;
  cursor: pointer;
}

.link:hover { text-decoration: underline; }

.alert {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 16px;
}

.alert-error {
  background: #fee2e2;
  color: #b91c1c;
  border: 1px solid #fca5a5;
}

.alert-success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #86efac;
}

.reg-alert { margin-bottom: 20px; }

.events-header { margin-bottom: 28px; }

.events-title {
  font-size: 24px;
  font-weight: 700;
  color: #1c2e4a;
}

.events-sub {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

.empty {
  text-align: center;
  padding: 80px 20px;
  color: #64748b;
}

.empty-icon { font-size: 52px; margin-bottom: 14px; }
.empty-text { font-size: 20px; font-weight: 600; color: #334155; margin-bottom: 6px; }
.empty-hint { font-size: 14px; color: #94a3b8; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.07);
  border: 1px solid #e2e8f0;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card-id { font-size: 12px; color: #94a3b8; font-weight: 600; }

.card-badge {
  background-color: #e0f2fe;
  color: #0369a1;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 20px;
  text-transform: uppercase;
}

.card-title {
  font-size: 18px;
  font-weight: 700;
  color: #1c2e4a;
  margin-bottom: 10px;
  line-height: 1.3;
}

.card-description {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
  margin-bottom: 16px;
  flex: 1;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 14px;
  border-top: 1px solid #f1f5f9;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
}

.meta-icon { font-size: 15px; }

.card-actions { margin-top: auto; }

.btn-register {
  width: 100%;
  background-color: #0d7377;
  color: #ffffff;
  border: none;
  padding: 10px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-register:hover { background-color: #0a5c60; }

.confirm-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
}

.confirm-text {
  font-size: 13px;
  color: #475569;
  margin-bottom: 10px;
  text-align: center;
}

.confirm-buttons {
  display: flex;
  gap: 8px;
}

.btn-confirm {
  flex: 1;
  background: #166534;
  color: white;
  border: none;
  padding: 8px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-confirm:hover { background: #14532d; }

.btn-cancel {
  flex: 1;
  background: #e2e8f0;
  color: #475569;
  border: none;
  padding: 8px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-cancel:hover { background: #cbd5e1; }

.footer {
  background-color: #1c2e4a;
  text-align: center;
  padding: 16px;
  font-size: 12px;
  color: #64748b;
}
</style>