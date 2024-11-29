<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const websites = ref();
const nameTitle = ref('');
const id_page = ref('');
const loading = ref(true);
const fotos = ref(["/fotos/brand.png", "/fotos/light.png", "/fotos/lightest.png"]);


const fetchWebInfo = async () => {
    loading.value = true; // Mostrar la carga
    try {
        const token = localStorage.getItem('access_token');

        const response = await axios.get("http://127.0.0.1:5000/websites", {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        const data = response.data.map((website) => ({
            ...website,
            foto: fotos.value[Math.floor(Math.random() * (fotos.value.length) )], // Asignar una foto aleatoria
        }));

        websites.value = data;
    } catch (err) {
        console.error('Error fetching user info:', err);
    } finally {
        loading.value = false; // Terminar la carga
    }
};

const showSite = (name, id) => {
    nameTitle.value = name;
    id_page.value = id;
}

onMounted(() => {
    fetchWebInfo();
});

const editPage = (id) => {
    localStorage.setItem('id_page', id.id_page);
    window.location.href = '/edit';
}

const viewPage = async(id) => {
    const id_user = 0;
    const token = localStorage.getItem('access_token');
    const response = await axios.get("http://127.0.0.1:5000/user/id",{
        headers: {
            Authorization: `Bearer ${token}`,
        }
    });
    const data = response.data;
    id_user = data.id;
}

const deletePage = async (id) => {
    try{
        const token = localStorage.getItem('access_token');
        await axios.post("http://127.0.0.1:5000/website/delete", {
            id: id.id_page
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
            }
        });
        alert("Page deleted successfully");
        window.location.href = '/';
    }catch(err){
        console.error('Error fetching user info:', err);
    }
}

</script>

<template>
    <div v-if="loading" class="w-full h-[65vh] flex justify-center items-center">
        <svg fill="hsl(32, 18%, 69%)" width="200"  height="200" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z" opacity=".25"/><path d="M12,4a8,8,0,0,1,7.89,6.7A1.53,1.53,0,0,0,21.38,12h0a1.5,1.5,0,0,0,1.48-1.75,11,11,0,0,0-21.72,0A1.5,1.5,0,0,0,2.62,12h0a1.53,1.53,0,0,0,1.49-1.3A8,8,0,0,1,12,4Z"><animateTransform attributeName="transform" type="rotate" dur="0.75s" values="0 12 12;360 12 12" repeatCount="indefinite"/></path></svg>
    </div>
    <div v-else-if="!loading" class="mx-auto w-11/12 flex flex-col">
        <div class="md:mt-20 ml-4 dark:text-light md:text-mid text-darkest text-3xl">
            <span v-if="!nameTitle">Selecciona una pagina</span>
            <span v-else>{{ nameTitle }}</span>
        </div>
        <div  class="mt-10 md:h-40 flex flex-col md:flex-row gap-4">
            <a class="w-full md:w-40 h-52 md:h-full border-2 border-light flex items-center justify-center rounded-lg hover:shadow-lg" href="website"><svg  xmlns="http://www.w3.org/2000/svg"  width="40"  height="40"  viewBox="0 0 24 24"  fill="none"  stroke="white"  stroke-width="2"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-plus"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M12 5l0 14" /><path d="M5 12l14 0" /></svg></a>
            <div
                @click="showSite(website.name, website.id)"
                class="w-full md:w-40 h-52 md:h-full border-2 border-light rounded-lg hover:shadow-lg cursor-pointer flex justify-between flex-col p-1 dark:text-light md:text-mid text-darkest"
                v-for="(website) in websites"
                :key="website.id"
                >
                <img :src="website.foto" class="w-[150px] md:w-[100px] mx-auto" alt="Website Image" />
                <span>{{ website.name }}</span>
            </div>
        </div>
        <div v-if="nameTitle" class="mt-14 md:mt-0 flex md:flex-row flex-col gap-4">
            <button @click="editPage({ id_page })" type="button" class="text-lightest md:text-darkest dark:text-darkest md:ml-4 py-2 px-3 bg-darkest md:bg-mid dark:bg-mid rounded-lg md:mt-10 w-full md:w-auto md:mb-10">
                Edit Page
            </button>
            <button @click="deletePage({id_page})" class="text-lightest md:text-darkest dark:text-darkest py-2 px-3 bg-darkest md:bg-mid dark:bg-mid rounded-lg md:mt-10 w-full md:w-auto md:mb-10">
                Delate Page
            </button>
            <button @click="viewPage({id_page})" class="text-lightest md:text-darkest dark:text-darkest py-2 px-3 bg-darkest md:bg-mid dark:bg-mid rounded-lg md:mt-10 w-full md:w-auto md:mb-10">
                View Page
            </button>
        </div>
        <div v-else class="mt-14 md:mt-0">
            <button type="button" class="text-lightest md:text-darkest dark:text-dark md:ml-4 cursor-not-allowed opacity-50 py-2 px-3 bg-darkest md:bg-mid dark:bg-mid rounded-lg md:mt-10 w-full md:w-auto mb-10">
                Edit Page
            </button>
        </div>
    </div>
</template>