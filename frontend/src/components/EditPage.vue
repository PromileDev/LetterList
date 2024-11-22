<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const website_name = ref('');
const id_page = ref('');
const sections = ref([]);

const fetchWebInfo = async () => {
    try {
        const token = localStorage.getItem('access_token');
        id_page.value = localStorage.getItem('id_page');

        const response = await axios.post("http://127.0.0.1:5000/website_edit", {
            id_page: id_page.value
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
            }
        });
        const data = response.data;
        console.log(data);
        website_name.value = data.name;

        const response_sections = await axios.post("http://127.0.0.1:5000/sections", {
            id_page: id_page.value
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
            }
        });
        const data_sections = response_sections.data;
        sections.value = data_sections;
        console.log(data_sections);
    }catch (err) {
        console.error('Error fetching user info:', err);
    }
};


onMounted(() => {
    fetchWebInfo();
});

</script>

<template>
    <div class="mt-24 mb-24 text-light mx-auto flex flex-col items-center w-full">
        <h1 class="text-6xl font-bold">Web info:</h1>
        <span class="text-lg">Name: {{ website_name }}</span>
        <span class="text-lg">id: {{ id_page }}</span>
        <div>
            <h2>Sections:</h2>
            <div 
            v-for="(sections) in sections" 
            :key="sections.id"
            >
            <span>{{ sections.name }}</span>
            </div>
        </div>
    </div>
</template>