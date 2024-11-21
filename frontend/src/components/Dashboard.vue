<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const websites = ref();
const nameTitle = ref('');
const havePage = ref(false);
const loading = ref(true);
const fotos = ref(["/fotos/brand.png", "/fotos/dark.png", "/fotos/light.png", "/fotos/lightest.png"]);


const fetchWebInfo = async () => {
    loading.value = true; // Mostrar la carga
    try {
        console.log('fetching web info');
        const token = localStorage.getItem('access_token');

        const response = await axios.get("http://127.0.0.1:5000/websites", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        const data = response.data.map((website) => ({
            ...website,
            foto: fotos.value[Math.floor(Math.random() * fotos.value.length)], // Asignar una foto aleatoria
        }));

        websites.value = data;
        console.log(data);
        console.log(websites.value);
    } catch (err) {
        console.error('Error fetching user info:', err);
    } finally {
        loading.value = false; // Terminar la carga
    }
};

const showSite = (name) => {
    nameTitle.value = name;
}

const getFoto = () => {
    return fotos[Math.floor(Math.random() * fotos.length)];
}

onMounted(() => {
    fetchWebInfo();
});
</script>

<template>
    <div v-if="loading">
        Loading...
    </div>
    <div v-else-if="!loading" class="mx-auto w-11/12 min-h-[65vh] flex flex-col">
        <div class="mt-20 ml-4 text-mid text-3xl">
            <span v-if="!nameTitle">Selecciona una pagina</span>
            <span v-else>{{ nameTitle }}</span>
        </div>
        <div class="mt-10 h-40 flex gap-4">
            <a class="w-40 h-full border-2 border-light flex items-center justify-center rounded-lg hover:shadow-lg" href=""><svg  xmlns="http://www.w3.org/2000/svg"  width="40"  height="40"  viewBox="0 0 24 24"  fill="none"  stroke="white"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-plus"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 5l0 14" /><path d="M5 12l14 0" /></svg></a>
            
            <div
                @click="showSite(website.name)"
                class="w-40 h-full border-2 border-light rounded-lg hover:shadow-lg cursor-pointer flex justify-between flex-col p-1 text-mid"
                v-for="(website) in websites"
                :key="website.id"
                >
                <img :src="website.foto" class="w-[70%] mx-auto" alt="Website Image" />
                {{ website.name }}
            </div>

        </div>
    </div>
</template>