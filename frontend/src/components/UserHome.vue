<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';


const email = ref('');
const name = ref('');
const lastname = ref('');
const loading = ref(true);
const error = ref('');
const login = ref(false);
const dropDownVisible = ref(false);

const signOut = () => {
  localStorage.removeItem('access_token');
  window.location.href = '/';
};

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

const showMenu = () => {
  dropDownVisible.value = !dropDownVisible.value;
};

onMounted(() => {
  fetchUserInfo();
});
</script>

<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-if="login" @click="showMenu" class="cursor-pointer flex gap-4 justify-center items-center " type="button">
        <span class="text-lg">{{ name }} {{ lastname }}</span>
        <img src="/fotos/avatar.png" class="w-10 h-10 rounded-full" alt="">
        <div v-if="dropDownVisible"
          class="fixed top-[70px] md:right-5 bg-white divide-y divide-gray-100 rounded-lg shadow max-w-52">
          <div class="px-4 py-3 text-sm text-gray-900 dark:text-white">
            <div>{{ name }} {{ lastname }}</div>
            <div class="font-medium truncate">{{ email }}</div>
          </div>
          <ul class="py-2 text-sm text-gray-700 px-1">
            <li>
              <a href="#" class="rounded-lg block px-4 py-2 hover:bg-gray-100 ">Plans</a>

            </li>
            <li>
              <a href="/settings" class="rounded-lg block px-4 py-2 hover:bg-gray-100 ">Settings</a>
            </li>
            <li>
              <a href="#" class="rounded-lg block px-4 py-2 hover:bg-gray-100">Demos</a>
            </li>
          </ul>
          <div class="py-1 px-1">
            <button type="button" @click="signOut"
              class="w-full flex block px-4 py-2 text-sm text-gray-700 hover:bg-red-500 hover:text-white hover:rounded-lg">Sign
              out</button>
          </div>
        </div>
      </div>
      <div v-else class="flex flex-row gap-4">
        <a class="bg-darkest py-2 px-4 rounded-lg text-lightest" href="/login">Login</a>
        <a class="bg-mid py-2 px-4 rounded-lg text-darkest "href="/register">Register</a>
      </div>
    </div>
  </div>
</template>