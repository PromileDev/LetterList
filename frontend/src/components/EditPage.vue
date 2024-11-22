<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const website_name = ref('');
const id_page = ref('');


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
    }catch (err) {
        console.error('Error fetching user info:', err);
    }
};

onMounted(() => {
    fetchWebInfo();
});

</script>

<template>
    <div>
        {{ website_name }}
        <br>
        {{ id_page }}
    </div>
</template>