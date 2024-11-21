<script setup>
import { ref } from 'vue';
import axios from 'axios';

const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

const handleLogin = async () => {
  try {
    loading.value = true;
    error.value = '';

    const response = await axios.post('http://127.0.0.1:5000/login', {
      email: email.value,
      password: password.value
    });

    const token = response.data.access_token
    if (!token){
      throw new Error('Invalid token');
    }

    localStorage.setItem("access_token", token);
    
    window.location.href = '/';
  } catch (err) {
    error.value = err.response?.data?.message || 'An error occurred during login';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
    <div class="flex flex-col py-4 px-3 w-full md:w-[80%]">
      <form @submit.prevent="handleLogin" class="flex flex-col gap-10 md:bg-light md:py-10 md:rounded-lg md:shadow-lg">        
        <div class="mx-auto flex flex-col w-[80%]">
          <label class="text-lightest text-xl mb-4 ml-2 md:text-darkest" for="email">Email</label>
          <input 
            class="bg-darkest py-1 rounded-lg text-white pl-2"
            type="email" 
            id="email" 
            v-model="email" 
            required 
          >
        </div>
  
        <div class="mx-auto flex flex-col w-[80%]">
          <label class="text-lightest text-xl mb-4 ml-2 md:text-darkest" for="password">Password</label>
          <input
            class="bg-darkest py-1 rounded-lg text-white pl-2"
            type="password" 
            id="password" 
            v-model="password" 
            required 
          >
        </div>
  
        <button class="mx-auto bg-brand py-2 w-[80%] rounded-full font-bold text-darkest" type="submit" :disabled="loading">
          {{ loading ? 'Loading...' : 'Sign In' }}
        </button>
  
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </template>
  
