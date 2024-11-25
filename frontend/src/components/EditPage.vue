<template>
    <div>
        <!-- Sección del encabezado -->
        <div class="mt-24 mb-12 text-light mx-auto flex flex-col items-center w-full">
            <h1 class="text-6xl font-bold">Cafetería Pepe</h1>
        </div>

        <!-- Tabs -->
        <div class="w-11/12 mx-auto">
            <ul class="flex flex-wrap text-sm font-medium text-center text-brand border-b border-mid cursor-pointer">
                <!-- Mostrar las tabs correctamente -->
                <li v-for="(items, section) in sections" :key="section" class="me-2">
                    <a
                        @click.prevent="activeTab = section" 
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
                <div class="flex flex-wrap -mx-2">
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
import {ref} from 'vue';
const activeTab = ref('bebidas');
const showModal = ref(false);
const newSectionName = ref('');
const nameError = ref(false);

const sections = ref({
    bebidas: [
        { name: "Café Americano", description: "Café americano con un toque de leche", price: "1.50€" },
        { name: "Café con leche", description: "Café con leche caliente", price: "1.20€" }
    ],
    entrantes: [
        { name: "Ensalada César", description: "Lechuga, pollo, crutones y salsa césar", price: "5.50€" },
        { name: "Patatas bravas", description: "Patatas bravas con salsa picante", price: "4.00€" }
    ],
    platos: [
        { name: "Hamburguesa", description: "Hamburguesa de ternera con queso y bacon", price: "7.50€" },
        { name: "Pizza Margarita", description: "Pizza con tomate, mozzarella y albahaca", price: "6.00€" }
    ],
    postres: [
        { name: "Tarta de queso", description: "Tarta de queso con mermelada de frutos rojos", price: "3.50€" },
        { name: "Helado", description: "Helado de vainilla con sirope de chocolate", price: "2.50€" }
    ]
});

const sectionNames = ref({
    bebidas: "Bebidas y Cafés",
    entrantes: "Entrantes",
    platos: "Platos principales",
    postres: "Postres"
});

const toggleModal = () => {
    showModal.value = !showModal.value;
    nameError.value = false; // Resetear el error al alternar el modal
};

const addNewSection = () => {
    if (newSectionName.value === '' || sections.value[newSectionName.value]) {
        nameError.value = true;
    } else {
        sections.value[newSectionName.value] = [];
        sectionNames.value[newSectionName.value] = newSectionName.value;
        newSectionName.value = '';
        toggleModal();
    }
};
</script>
