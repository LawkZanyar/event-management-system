<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const events = ref([])

const API_URL =
  "mindful-manifestation-production.up.railway.app/api/events"


onMounted(async () => {

  try {

    const response = await axios.get(API_URL)

    console.log(response.data)

    events.value = response.data

  } catch(error) {

    console.log(error)

  }

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