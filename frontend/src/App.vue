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

  <div>

    <h1>Event Management System</h1>


    <div v-if="events.length === 0">

      No events found

    </div>


    <ul>

      <li 
        v-for="event in events" 
        :key="event.id"
      >

        <h3>
          {{ event.title }}
        </h3>


        <p>
          Description: {{ event.description }}
        </p>


        <p>
          Date: {{ event.date }}
        </p>


        <p>
          Location: {{ event.location }}
        </p>


      </li>

    </ul>


  </div>

</template>