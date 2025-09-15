<template>
  <div>
    <h1>{{ message }}</h1>
    <button @click="fetchMessage">Fetch Message from FastAPI</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const message = ref('Hello from Vue!');

const fetchMessage = async () => {
  try {
    // The request URL should be the address of your FastAPI backend.
    // When using Docker, this will likely be the name of the backend service.
    // For local development, it might be http://localhost:8000
    const response = await axios.get('/vue-deploy-test/api/message');
    message.value = response.data.message;
  } catch (error) {
    console.error('Error fetching message:', error);
    message.value = 'Failed to fetch message from backend.';
  }
};
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
