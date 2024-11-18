
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';


const email = ref('');
const name = ref('');
const lastname = ref('');
const loading = ref(true);
const error = ref('');
const login = ref(false);

const fetchUserInfo = async () => {
  try {
    const token = localStorage.getItem('access_token');

    const response = await axios.get('http://127.0.0.1:5000/protected', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    const data = response.data;
    email.value = data.email;
    name.value = data.name;
    lastname.value = data.lastname;
    login.value = true;
  } catch (err) {
    console.error('Error fetching user info:', err);
    error.value = 'Failed to load user information';
    if (err.response?.status === 401) {
        login.value = false;
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
    <div class="">
        <div v-if="loading">Loading...</div>
        <div v-else>
            <div v-if="login">
                
            </div>
            <div v-else class="flex flex-row gap-4">
                <a href="/login">Login</a>
                <a href="/register">Register</a>
            </div>
        </div>
    </div>
    
</template>
  