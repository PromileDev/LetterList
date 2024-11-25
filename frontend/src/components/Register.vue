<script setup>
import { ref } from 'vue';
import axios from 'axios';

const name = ref('');
const lastname = ref('');
const email = ref('');
const password = ref('');
const confirmPassowrd = ref('');
const loading = ref(false);
const error = ref('');

const handleRegister = async () => {

    try {
        if (password.value !== confirmPassowrd.value) {
            throw new Error('Passwords do not match');
        }
        loading.value = true;
        error.value = '';

        const response = await axios.post('http://127.0.0.1:5000/register', {
            email: email.value,
            password: password.value,
            name: name.value,
            lastname: lastname.value
        });

        window.location.href = '/login';
    } catch (err) {
        error.value = err.response?.data?.message || 'An error occurred during login';
    } finally {
        loading.value = false;
    }
    };
</script>

<template>
    <div class="flex flex-col justify-center items-center py-4 px-3 w-full md:w-[80%] md:bg-light md:py-10 md:rounded-lg md:shadow-lg">
      <form @submit.prevent="handleRegister" class="flex flex-col gap-6 w-full md:w-[80%]">        
        <div class="flex justify-between w-full">
            <div class="flex flex-col w-[45%]">
                <label class="ml-2 text-lg text-dark md:text-lightest dark:md:text-dark dark:text-lightest" for="name">Name</label>
                <input 
                    class="md:bg-darkest text-darkest md:text-light bg-light focus:ring-darkest focus:border-darkest md:focus:ring-mid md:focus:border-mid border-transparent rounded-lg"
                    type="text" 
                    id="name" 
                    v-model="name" 
                    required 
                >
            </div>
            <div class="flex flex-col w-[45%]">
                <label class="ml-2 text-lg text-dark md:text-lightest dark:md:text-dark dark:text-lightest" for="name">Lastname</label>
                <input 
                    class="md:bg-darkest text-darkest md:text-light bg-light focus:ring-darkest focus:border-darkest md:focus:ring-mid md:focus:border-mid border-transparent rounded-lg"                    type="text" 
                    id="lastname" 
                    v-model="lastname" 
                    required 
                >
            </div>
        </div>
        
        <div class="mx-auto flex flex-col w-full">
          <label class="ml-2 text-lg text-dark md:text-lightest dark:md:text-dark dark:text-lightest" for="email">Email</label>
          <input 
            class="md:bg-darkest text-darkest md:text-light bg-light focus:ring-darkest focus:border-darkest md:focus:ring-mid md:focus:border-mid border-transparent rounded-lg"
            type="email" 
            id="email" 
            v-model="email" 
            required 
          >
        </div>
  
        <div class="mx-auto flex flex-col w-full">
          <label class="ml-2 text-lg text-dark md:text-lightest dark:md:text-dark dark:text-lightest" for="password">Password</label>
          <input
            class="md:bg-darkest text-darkest md:text-light bg-light focus:ring-darkest focus:border-darkest md:focus:ring-mid md:focus:border-mid border-transparent rounded-lg"
            type="password" 
            id="password" 
            v-model="password" 
            required 
          >
        </div>
        <div class="mx-auto flex flex-col w-full">
          <label class="ml-2 text-lg text-dark md:text-lightest dark:md:text-dark dark:text-lightest" for="password">Confirm password</label>
          <input
            class="md:bg-darkest text-darkest md:text-light bg-light focus:ring-darkest focus:border-darkest md:focus:ring-mid md:focus:border-mid border-transparent rounded-lg"
            type="password" 
            id="password" 
            v-model="confirmPassowrd" 
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
  
