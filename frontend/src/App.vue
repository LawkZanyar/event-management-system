<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const events = ref([])

onMounted(async () => {
  const res = await axios.get('mindful-manifestation-production.up.railway.app/api/events')
  events.value = res.data
})
</script>

<template>
<h1>Event Management System</h1>

<ul>
<li v-for="event in events" :key="event.id">
{{ event.title }} - {{ event.location }}
</li>
</ul>

</template>
