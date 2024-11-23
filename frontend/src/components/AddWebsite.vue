<script setup>
import { ref } from 'vue';
import axios from 'axios';

const website_name = ref('');
const errorMessage = ref('');
const successMessage = ref('');

const addWebsite = async () => {
    // Restablecer los mensajes antes de enviar la solicitud
    errorMessage.value = '';
    successMessage.value = '';

    if (!website_name.value) {
        errorMessage.value = 'Por favor, ingresa un nombre de sitio web.';
        return;
    }

    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            errorMessage.value = 'No se encontró un token de acceso. Por favor, inicia sesión primero.';
            return;
        }

        const response = await axios.post("http://127.0.0.1:5000/website", {
            name: website_name.value
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
            }
        });

        // Suponiendo que la API devuelve un mensaje de éxito
        const data = response.data;
        successMessage.value = data.message || '¡Sitio web agregado exitosamente!';
        website_name.value = '';  // Limpiar el campo de entrada después de una solicitud exitosa

        // Redirigir a la página de edición después de un éxito
        window.location.href = '/edit';  // Redirige a la página de edición

    } catch (err) {
        console.error('Error al agregar el sitio web:', err);
        errorMessage.value = 'Ocurrió un error al agregar el sitio web. Por favor, inténtalo de nuevo.';
    
    }
};
</script>

<template>
    <div class="mt-24 mb-24 text-light mx-auto flex flex-col items-center w-full px-4 sm:px-8 lg:px-16">
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-darkest mb-4">Agregar un sitio web</h1>
        <p class="text-lg text-dark mb-6">Ingresa el nombre del sitio web que deseas agregar</p>
        
        <!-- Mensaje de error -->
        <div v-if="errorMessage" class="text-red-500 text-lg mb-4">{{ errorMessage }}</div>
        
        <!-- Mensaje de éxito -->
        <div v-if="successMessage" class="text-green-500 text-lg mb-4">{{ successMessage }}</div>

        <input v-model="website_name" 
               class="text-lg text-darkest border-2 border-mid rounded-lg py-2 px-4 w-full max-w-md mb-4 placeholder-dark opacity-70 focus:ring-2 focus:ring-brand focus:border-transparent transition duration-300" 
               placeholder="Nombre del sitio web" />

        <button @click="addWebsite" 
                class="py-2 px-6 bg-mid rounded-lg text-lightest font-semibold w-full sm:w-auto mb-10 cursor-pointer hover:bg-brand focus:outline-none focus:ring-2 focus:ring-brand focus:ring-opacity-50 transition-all ease-in-out duration-300 opacity-60 disabled:opacity-40 disabled:cursor-not-allowed"
                :class="{'opacity-100': website_name.length > 0}" 
                :disabled="!website_name">
            Agregar sitio web
        </button>
    </div>
</template>
