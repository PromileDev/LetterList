
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
                <img id="avatarButton" type="button" data-dropdown-toggle="userDropdown" data-dropdown-placement="bottom-start" class="w-10 h-10 rounded-full cursor-pointer" src="/fotos/brand.png" alt="User dropdown">
                <span>user</span>
                <!-- Dropdown menu -->
                <div id="userDropdown" class="z-10 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700 dark:divide-gray-600">
                    <div class="px-4 py-3 text-sm text-gray-900 dark:text-white">
                    <div>Bonnie Green</div>
                    <div class="font-medium truncate">name@flowbite.com</div>
                    </div>
                    <ul class="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="avatarButton">
                    <li>
                        <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Dashboard</a>
                    </li>
                    <li>
                        <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Settings</a>
                    </li>
                    <li>
                        <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Earnings</a>
                    </li>
                    </ul>
                    <div class="py-1">
                    <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Sign out</a>
                    </div>
                </div>
            </div>
            <div v-else>
                <span>TODO MAL</span>
            </div>
        </div>
    </div>
</template>
  