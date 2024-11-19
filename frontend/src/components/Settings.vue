<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';

const email = ref('');
const name = ref('');
const lastname = ref('');
const error = ref('');
const successMessage = ref('');
const loading = ref(false);

const fetchUserInfo = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.href = '/';
    }

    const response = await axios.get('http://127.0.0.1:5000/protected', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    const data = response.data;
    email.value = data.email;
    name.value = data.name;
    lastname.value = data.lastname;
  } catch (err) {
    console.error('Error fetching user info:', err);
    error.value = 'Failed to load user information';
    if (err.response?.status === 401) {
      window.location.href = '/';
    }
  }
};

const handleSave = async (event) => {
  event.preventDefault(); // Evitar el comportamiento por defecto del formulario

  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.href = '/';
    }

    const response = await axios.post(
      'http://127.0.0.1:5000/settings',
      {
        name: name.value,
        lastname: lastname.value,
        email: email.value,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    successMessage.value = response.data.message;
    setTimeout(() => {
      window.location.href = '/settings';
    }, 3000);
  } catch (err) {
    console.error('Error updating user info:', err);
    error.value = 'Failed to update user information';
    if (err.response?.status === 401) {
      window.location.href = '/';
    }
  }
};

onMounted(() => {
  fetchUserInfo();
});
</script>

<template>
  <div class="flex flex-col items-center gap-10 w-full">
    <h2 class="text-light text-5xl font-bold">{{ name }} settings</h2>
    <div class="flex flex-col justify-center items-center py-4 px-3 w-full md:w-[80%] md:bg-light md:py-10 md:rounded-lg md:shadow-lg">
      <form @submit="handleSave" class="flex flex-col gap-6 w-full md:w-[80%]">
        <div class="flex justify-between w-full">
            <div class="flex flex-col w-[45%]">
                <label class="text-lightest text-xl mb-4 ml-2 md:text-darkest" for="name">Name</label>
                <input 
                    class="bg-darkest py-1 rounded-lg text-white pl-2"
                    type="text" 
                    id="name" 
                    v-model="name" 
                    required 
                >
            </div>
            <div class="flex flex-col w-[45%]">
                <label class="text-lightest text-xl mb-4 ml-2 md:text-darkest" for="name">Lastname</label>
                <input 
                    class="bg-darkest py-1 rounded-lg text-white pl-2"
                    type="text" 
                    id="lastname" 
                    v-model="lastname" 
                    required 
                >
            </div>
        </div>
        <div class="mx-auto flex flex-col w-full">
          <label class="text-lightest text-xl mb-4 ml-2 md:text-darkest" for="email">Email</label>
          <input 
            class="bg-darkest py-1 rounded-lg text-white pl-2"
            type="email" 
            id="email" 
            v-model="email" 
            required 
          >
        </div>
        <div class="mx-auto">
            <a class="text-lg text-brand md:text-dark font-bold" href="">Change Password</a>
        </div>
        <button class="mx-auto bg-brand py-2 w-[80%] rounded-full font-bold text-darkest" type="submit" :disabled="loading">
          {{ loading ? 'Loading...' : 'Save' }}
        </button>
      </form>
      <div v-if="successMessage" class="mt-4 text-green-500 font-bold">
        {{ successMessage }}
      </div>
      <div v-if="error" class="mt-4 text-red-500 font-bold">
        {{ error }}
      </div>
    </div>
  </div>
</template>
