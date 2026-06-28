<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const events = ref([])

const API_URL =
  "https://mindful-manifestation-production.up.railway.app/api/events"

onMounted(async () => {
  try {
    const response = await axios.get(API_URL)
    console.log("API DATA:", response.data)
    events.value = response.data
  } catch (error) {
    console.error("API ERROR:", error)
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
          <p class="header-sub">Browse all upcoming events</p>
        </div>
      </div>
    </header>

    <main class="main">

      <div v-if="events.length === 0" class="empty">
        <div class="empty-icon">🗓️</div>
        <p class="empty-text">No events found</p>
        <p class="empty-hint">Events you create via the API will appear here.</p>
      </div>

      <div class="grid">
        <div
          class="card"
          v-for="event in events"
          :key="event.id"
        >
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

/* ── Header ── */
.header {
  background-color: #1c2e4a;
  padding: 24px 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.header-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo {
  font-size: 36px;
  line-height: 1;
}

.header-title {
  font-size: 24px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.3px;
}

.header-sub {
  font-size: 13px;
  color: #94b4cc;
  margin-top: 3px;
}

/* ── Main ── */
.main {
  flex: 1;
  max-width: 1100px;
  width: 100%;
  margin: 40px auto;
  padding: 0 24px;
}

/* ── Empty state ── */
.empty {
  text-align: center;
  padding: 80px 20px;
  color: #64748b;
}

.empty-icon {
  font-size: 56px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 20px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 14px;
  color: #94a3b8;
}

/* ── Grid ── */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

/* ── Card ── */
.card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.07);
  border: 1px solid #e2e8f0;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
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

.card-id {
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
}

.card-badge {
  background-color: #e0f2fe;
  color: #0369a1;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  margin-bottom: 18px;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid #f1f5f9;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
}

.meta-icon {
  font-size: 15px;
}

/* ── Footer ── */
.footer {
  background-color: #1c2e4a;
  text-align: center;
  padding: 16px;
  font-size: 12px;
  color: #64748b;
}
</style>