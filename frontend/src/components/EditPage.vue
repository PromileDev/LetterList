<template>
    <div>
        <!-- Sección del encabezado -->
        <div class="mt-24 mb-12 text-light mx-auto flex flex-col items-center w-full">
            <h1 class="text-6xl font-bold">Cafetería Pepe</h1>
            <h1 class="text-6xl font-bold">{{ sections }}</h1>


        </div>

        <!-- Tabs -->
        <div class="w-11/12 mx-auto">
            <ul class="flex flex-wrap text-sm font-medium text-center text-brand border-b border-mid cursor-pointer">
                <!-- Mostrar las tabs correctamente -->
                <li v-for="(items, section) in sections" :key="section" class="me-2">
                    <a
                        @click.prevent="changeTab(section)" 
                        :class="{'text-darkest bg-mid active': activeTab === section}" 
                        class="inline-block p-4 rounded-t-lg hover:text-darkest hover:bg-mid"
                    >
                        {{ sectionNames[section] }} <!-- Mostrar nombre de la sección -->
                    </a>
                </li>
                <!-- Botón para agregar una nueva sección -->
                <li class="me-2">
                    <a
                        @click.prevent="toggleModal"
                        class="inline-block p-4 rounded-t-lg hover:text-darkest hover:bg-mid cursor-pointer"
                    >
                        +
                    </a>
                </li>
            </ul>
        </div>

        <!-- Sección de contenido: mostrar el contenido según el tab activo -->
        <div class="w-11/12 mx-auto pt-12">
            <!-- Mostrar contenido solo de la tab activa -->
            <div
                v-for="(items, section) in sections"
                :key="section"
                v-show="activeTab === section" 
                class="bg-light p-6 rounded-lg shadow mb-6"
            >
                <h2 class="text-2xl font-bold mb-4">{{ sectionNames[section] }}</h2>
                <!-- Verificar si hay productos -->
                <div v-if="items.length > 0" class="flex flex-wrap -mx-2">
                    <!-- Mostrar los items de cada sección -->
                    <div
                        v-for="(item, index) in items"
                        :key="index"
                        class="w-1/2 px-2 mb-4"
                    >
                        <div class="bg-lightest p-4 rounded-lg shadow">
                            <h3 class="text-lg font-bold">{{ item.name }}</h3>
                            <p class="text-sm">{{ item.description }}</p>
                            <p class="text-sm font-semibold">Precio: {{ item.price }}</p>
                        </div>
                    </div>
                </div>
                <!-- Mensaje si no hay productos -->
                <div v-else class="text-center text-gray-500">
                    No hay productos disponibles en esta sección.
                </div>
            </div>
        </div>

        <!-- Modal para agregar nueva sección -->
        <div v-if="showModal" class="fixed inset-0 bg-darkest bg-opacity-50 flex justify-center items-center">
            <div class="bg-mid p-6 rounded-lg shadow-lg w-96 text-darkest">
                <h3 class="text-xl font-bold mb-4">Añadir nueva sección</h3>
                <div>
                    <label for="newSectionName" class="block text-lg font-medium mb-2 text-dark">
                        Nombre de la sección
                    </label>
                    <input
                        v-model="newSectionName"
                        type="text"
                        id="newSectionName"
                        class="p-2 border border-light rounded-lg w-full mb-4 focus:ring-0 focus:border-brand"
                        placeholder="Escribe el nombre"
                        :class="{'border-red-500': nameError}"
                    />
                    <!-- Mensaje de error si el nombre es inválido -->
                    <p v-if="nameError" class="text-red-500 text-sm">El nombre de la sección no puede estar vacío o ser duplicado.</p>
                </div>
                <div class="flex justify-between">
                    <!-- Botón Añadir -->
                    <button @click="addNewSection" class="px-4 py-2 bg-dark text-lightest rounded-lg hover:bg-brand hover:text-lightest">
                        Añadir
                    </button>

                    <!-- Botón Cancelar -->
                    <button @click="toggleModal" class="px-4 py-2 bg-darkest opacity-50 hover:opacity-100 text-lightest hover:bg-red-500 rounded-lg">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

const activeTab = ref(''); // Inicializar vacío para la primera sección dinámica
const showModal = ref(false);
const newSectionName = ref('');
const nameError = ref(false);
const sections = reactive({}); // Contendrá productos por sección
const sectionNames = ref({}); // Contendrá nombres de las secciones
const errorMessage = ref('');
const successMessage = ref('');

// Cambiar a una nueva tab
const changeTab = async (sectionId) => {
    activeTab.value = sectionId;
    if (!sections[sectionId].length) {
        await fetchProductsBySection(sectionId);  // Cargar productos si no se han cargado aún
    }
};


const fetchProductsBySection = async (sectionId) => {
    const token = localStorage.getItem('access_token');

    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/products_section",
            { section_id: sectionId },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );


        // Asocia los productos a la sección
        sections[sectionId] = response.data;
    } catch (err) {
        console.error('Error al obtener productos:', err.response?.data || err.message);
        errorMessage.value = 'Error al cargar los productos de la sección. Por favor, intenta nuevamente.';
    }
};

const fetchSectionNames = async () => {
    const token = localStorage.getItem('access_token');
    const idPage = localStorage.getItem('id_page');

    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/sections",
            { id_page: idPage },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );

        const data = response.data;

        // Inicializar las secciones con un array vacío
        sectionNames.value = {};
        data.forEach((section) => {
            sectionNames.value[section.id] = section.name;
            sections[section.id] = [];  // Inicializar con listas vacías
        });

        // Establecer la primera sección como activa, si hay secciones
        if (data.length > 0) {
            activeTab.value = data[0].id;
            await fetchProductsBySection(data[0].id);  // Cargar productos para la primera sección
        }
    } catch (err) {
        console.error('Error al obtener secciones:', err.response?.data || err.message);
        errorMessage.value = 'Error al cargar las secciones. Por favor, intenta nuevamente.';
    }
};


const toggleModal = () => {
    showModal.value = !showModal.value;
    nameError.value = false; // Resetear el error al alternar el modal
};

const addNewSection = async () => {
    if (newSectionName.value.trim() === '' || Object.values(sectionNames.value).includes(newSectionName.value)) {
        nameError.value = true;
        return;
    }

    const token = localStorage.getItem('access_token');
    const idPage = localStorage.getItem('id_page');

    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/sections/add",
            { id_page: idPage, name: newSectionName.value },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );

        // Agregar la nueva sección a las listas locales
        const newSection = response.data;
        sectionNames.value[newSection.id] = newSection.name;
        sections[newSection.id] = [];
        activeTab.value = newSection.id; // Cambiar inmediatamente a la nueva sección
        successMessage.value = 'Sección añadida exitosamente.';
        toggleModal();
    } catch (err) {
        console.error('Error al añadir nueva sección:', err.response?.data || err.message);
        errorMessage.value = 'Error al añadir la nueva sección. Por favor, intenta nuevamente.';
    }
};

// Cargar datos iniciales al montar el componente
onMounted(() => {
    fetchSectionNames();
});
</script>
