
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';


const email = ref('');
const name = ref('');
const lastname = ref('');
const loading = ref(true);
const error = ref('');

const fetchUserInfo = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.href = '/login';
      return;
    }

    const response = await axios.get('http://127.0.0.1:5000/protected', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = response.data;
    email.value = data.email;
    name.value = data.name;
    lastname.value = data.lastname;

  } catch (err) {
    console.error('Error fetching user info:', err);
    error.value = 'Failed to load user information';
    if (err.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchUserInfo();
});
</script>

<template>
    <div class="flex justify-center items-center w-full h-[90vh]">
      <div v-if="loading">Loading...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else class="flex flex-col gap-4 mt-10 items-center justify-center">
        <h1 class="text-5xl text-light font-bold mb-6">Welcome to your Dashboard</h1>
        <div class="bg-light flex flex-col items-center w-[70%] h-[40vh] rounded-lg shadow-lg">
          <h2 class="text-lg font-bold mt-2">User Information</h2>
          <div class="w-full h-[60%] flex flex-col justify-center items-center">
              <p>Email: {{ email }}</p>
              <p>Name: {{ name }}</p>
              <p>Lastname: {{ lastname }}</p>
          </div>
        </div>
      </div>
    </div>
</template>
  