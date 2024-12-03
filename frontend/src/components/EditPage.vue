<template>
    <div>
        <!-- Sección del encabezado -->
        <div class="mt-24 mb-12 text-light mx-auto flex flex-col items-center w-full">
            <h1 class="text-6xl font-bold">{{ websiteName }}</h1>

        </div>

        <!-- Tabs -->
        <div class="w-11/12 mx-auto">
            <ul class="flex flex-wrap text-sm font-medium text-center text-brand border-b border-mid cursor-pointer">
                <!--Mostrar todos los productos (All)-->
                <li>
                    <a
                        @click.prevent="changeTab('All')"
                        :class="{'text-darkest bg-mid active': activeTab === 'All'}"
                        class="inline-block p-4 rounded-t-lg hover:text-darkest hover:bg-mid"
                    >
                        All
                    </a>
                </li>
                
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
                        @click.prevent="toggleModalSection"
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
                <!--Boton añadir producto-->
                <a @click.prevent="toggleModalProduct" class="cursor-pointer w-full sm:w-auto px-4 py-2 bg-dark text-lightest rounded-lg hover:bg-brand hover:text-lightest transition-all">
                    Añadir producto
                </a>

                <!-- Verificar si hay productos -->
                <div v-if="items.length > 0" class="flex flex-wrap -mx-2 mt-4">
                    <!-- Mostrar los items de cada sección -->
                    <div v-for="(item, index) in items" :key="index" class="w-full sm:w-1/2 px-2 mb-4">
                        <div class="bg-lightest p-4 rounded-lg shadow">
                            <h3 class="text-lg font-bold">{{ item.name }}</h3>
                            <p class="text-sm">{{ item.description }}</p>
                            <p class="text-sm font-semibold">Precio: {{ item.price }}</p>
                            <div class="flex justify-end mt-3">
                            </div>
                            <div class="flex justify-end mt-3 space-x-2">
                                <!-- Botón Trash -->
                                <a @click.prevent="deleteProduct(item.id)" class="bg-red-500 text-lightest p-2 rounded-full shadow-md hover:bg-red-600 transition-colors" aria-label="Eliminar">
                                    <Trash class="w-4 h-4" />

                                </a>
                                <!-- Botón Edit -->
                                <a @click.prevent="prepareEditProduct(item)" class="bg-brand text-darkest p-2 rounded-full shadow-md hover:bg-brand-light transition-colors" aria-label="Editar">
                                    <Edit class="w-4 h-4" />
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Mensaje si no hay productos -->
                <div v-else class="text-center text-yellow-500 mt-4">
                    No hay productos disponibles en esta sección.
                </div>
            </div>
        </div>

        <!--Sección de All-->
        <div v-show="activeTab === 'All'" class="w-11/12 mx-auto pt-12">
            <div class="bg-light p-6 rounded-lg shadow mb-6">
                <h2 class="text-2xl font-bold mb-4">Todos los productos</h2>
                <div v-if="Object.keys(products).length > 0" class="flex flex-wrap -mx-2 mt-4">
                    <div v-for="(product, index) in products" :key="index" class="w-full sm:w-1/2 px-2 mb-4">
                        <div class="bg-lightest p-4 rounded-lg shadow">
                            <h3 class="text-lg font-bold">{{ product.name }}</h3>
                            <p class="text-sm">{{ product.description }}</p>
                            <p class="text-sm font-semibold">Precio: {{ product.price }}</p>
                            <p class="text-sm font-semibold">Sección: {{ sectionNames[product.section_id] }}</p>
                            <div class="flex justify-end mt-3">
                                <a @click.prevent="deleteProduct(product.id)" class="bg-red-500 text-lightest p-2 rounded-full shadow-md hover:bg-red-600 transition-colors" aria-label="Eliminar">
                                    <Trash class="w-4 h-4" />
                                </a>
                                <a @click.prevent="prepareEditProduct(product)" class="bg-brand text-darkest p-2 rounded-full shadow-md hover:bg-brand-light transition-colors" aria-label="Editar">
                                    <Edit class="w-4 h-4" />
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else class="text-center text-yellow-500 mt-4">
                    No hay productos disponibles.
                </div>
            </div>
        </div>

        <!-- Modal para agregar nueva sección -->
        <div v-if="showModalSection" class="fixed inset-0 bg-darkest bg-opacity-50 flex justify-center items-center">
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
                    <button @click="toggleModalSection" class="px-4 py-2 bg-darkest opacity-50 hover:opacity-100 text-lightest hover:bg-red-500 rounded-lg">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
        <!--Modal para agregar un nuevo producto-->
        <div v-if="showModalProduct" class="fixed inset-0 bg-darkest bg-opacity-50 flex justify-center items-center">
            <div class="bg-mid p-6 rounded-lg shadow-lg w-96 text-darkest">
                <h3 class="text-xl font-bold mb-4">Añadir nuevo producto</h3>
                <!--Nombre-->
                <div>
                    <label for="newProductName" class="block text-lg font-medium mb-2 text-dark">
                        Nombre del producto
                    </label>
                    <input
                        v-model="newProductName"
                        type="text"
                        id="newProductName"
                        class="p-2 border border-light rounded-lg w-full mb-4 focus:ring-0 focus:border-brand"
                        placeholder="Escribe el nombre"
                        :class="{'border-red-500': nameError}"
                    />
                    <!-- Mensaje de error si el nombre es inválido -->
                    <p v-if="nameError" class="text-red-500 text-sm">El nombre del producto no puede estar vacío o ser duplicado.</p>
                </div>
                <!--Precio-->
                <div>
                    <label for="newProductPrice" class="block text
                    -lg font-medium mb-2 text-dark">
                        Precio del producto
                    </label>
                    <input
                        v-model="newProductPrice"
                        type="text"
                        id="newProductPrice"
                        class="p-2 border border-light rounded-lg w-full mb-4 focus:ring-0 focus:border-brand"
                        placeholder="Escribe el precio"
                        :class="{'border-red-500': nameError}"
                    />
                    <!-- Mensaje de error si el precio es inválido -->
                    <p v-if="nameError" class="text-red-500 text-sm">El precio del producto no puede estar vacío o ser duplicado.</p>
                </div>
                <!--Botón añadir-->
                <div class="flex justify-between">
                    <button @click="addNewProduct" class="px-4 py-2 bg-dark text-lightest rounded-lg hover:bg-brand hover:text-lightest">
                        Añadir
                    </button>
                    <!-- Botón Cancelar -->
                    <button @click="toggleModalProduct" class="px-4 py-2 bg-darkest opacity-50 hover:opacity-100 text-lightest hover:bg-red-500 rounded-lg">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>

        <!-- Modal para editar un producto -->
        <div v-if="showModalEditProduct" class="fixed inset-0 bg-darkest bg-opacity-50 flex justify-center items-center">
            <div class="bg-mid p-6 rounded-lg shadow-lg w-96 text-darkest">
                <h3 class="text-xl font-bold mb-4">Editar producto</h3>
                <div>
                    <label for="editProductName" class="block text-lg font-medium mb-2 text-dark">
                        Nombre del producto
                    </label>
                    <input
                        v-model="editProductName"
                        type="text"
                        id="editProductName"
                        class="p-2 border border-light rounded-lg w-full mb-4 focus:ring-0 focus:border-brand"
                        placeholder="Escribe el nombre"
                        :class="{'border-red-500': nameError}"
                    />
                    <!-- Mensaje de error si el nombre es inválido -->
                    <p v-if="nameError" class="text-red-500 text-sm">El nombre del producto no puede estar vacío o ser duplicado.</p>
                </div>
                <div>
                    <label for="editProductPrice" class="block text-lg font-medium mb-2 text-dark">
                        Precio del producto
                    </label>
                    <input
                        v-model="editProductPrice"
                        type="text"
                        id="editProductPrice"
                        class="p-2 border border-light rounded-lg w-full mb-4 focus:ring-0 focus:border-brand"
                        placeholder="Escribe el precio"
                        :class="{'border-red-500': nameError}"
                    />

                    <label for="editProductSection" class="block text-lg font-medium mb-2 text-dark">
                        Sección del producto
                    </label>
                    <select
                        v-model="editProductSection"
                        id="editProductSection"
                        class="p-2 border border-light rounded-lg w-full mb-4 focus:ring-0 focus:border-brand"
                    >
                        <option v-for="(sectionName, sectionId) in sectionNames" :key="sectionId" :value="sectionId">
                            {{ sectionName }}
                        </option>
                    </select>

                    <!-- Mensaje de error si el precio es inválido -->
                    <p v-if="nameError" class="text-red-500 text-sm">El precio del producto no puede estar vacío o ser duplicado.</p>
                </div>
                <div class="flex justify-between">
                    <!-- Botón Guardar -->
                    <button @click="editProduct" class="px-4 py-2 bg-dark text-lightest rounded-lg hover:bg-brand hover:text-lightest">
                        Guardar
                    </button>
                    <!-- Botón Cancelar -->
                    <button @click="toggleModalEditProduct" class="px-4 py-2 bg-darkest opacity-50 hover:opacity-100 text-lightest hover:bg-red-500 rounded-lg">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import axios, { all } from 'axios';
import Trash from "./icons/Trash.vue";
import Edit from './icons/Edit.vue';

 
// Variables reactivas
const websiteName = ref(''); // Nombre de la página
const activeTab = ref(''); // Inicializar vacío para la primera sección dinámica
const showModalSection = ref(false);
const showModalProduct = ref(false);
const newProductName = ref('');
const newProductPrice = ref('');
const newSectionName = ref('');
const showModalEditProduct = ref(false);
const editProductName = ref('');
const editProductPrice = ref('');
const editProductSection = ref('');
const editProductId = ref(null)
const nameError = ref(false);
const products = reactive({}); // Contendrá todos los productos
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

const fetchProducts = async() => {
    const token = localStorage.getItem('access_token');
    const idPage = localStorage.getItem('id_page');

    console.log("Token:", token);  // Verificar que el token está en localStorage
    console.log("idPage:", idPage);  // Verificar que el idPage está en localStorage

    if (!token || !idPage) {
        console.error("Token o id_page no están presentes en localStorage");
        return;
    }

    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/products/list",
            { id_page: idPage },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        const data = response.data;

        // Guardar los productos en la variable reactiva
        data.forEach((product) => {
            products[product.id] = product;
        });

        // Organizar los productos por sección
        for (const product of data) {
            if (sections[product.section_id]) {
                sections[product.section_id].push(product);
            }
        }

    } catch (err) {
        console.error('Error al obtener productos:', err.response?.data || err.message);
        errorMessage.value = 'Error al cargar los productos. Por favor, intenta nuevamente.';
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


const toggleModalSection = () => {
    showModalSection.value = !showModalSection.value;
    nameError.value = false; // Resetear el error al alternar el modal
};

const toggleModalProduct = () => {
    showModalProduct.value = !showModalProduct.value;
    nameError.value = false; // Resetear el error al alternar el modal
};

const toggleModalEditProduct = () => {
    showModalEditProduct.value = !showModalEditProduct.value;
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
            "http://127.0.0.1:5000/section/add",
            { id_page: idPage, name: newSectionName.value },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );

        // Agregar la nueva sección a las listas locales
        fetchSectionNames(); // Actualizar las secciones
        fetchProducts(); // Actualizar los productos   
        newSectionName.value = ''; // Limpiar el campo
        successMessage.value = 'Sección añadida correctamente.';
        toggleModalSection();
    } catch (err) {
        console.error('Error al añadir nueva sección:', err.response?.data || err.message);
        errorMessage.value = 'Error al añadir la nueva sección. Por favor, intenta nuevamente.';
    }
};

const addNewProduct = async () => {
    if (newProductName.value.trim() === '' || Object.values(products).includes(newProductName.value)) {
        nameError.value = true;
        return;
    }
    if (newProductPrice.value.trim() === '') {
        nameError.value = true;
        return;
    }	
    const token = localStorage.getItem('access_token');
    const idPage = localStorage.getItem('id_page');
    const sectionId = activeTab.value;

    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/products",
            { website: idPage, name: newProductName.value, price: newProductPrice.value, section_id: sectionId },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );// Nuevo producto recibido del backend
        const newProduct = {
            name: newProductName.value,
            price: newProductPrice.value,
            section_id: sectionId,
            ...response.data, // Incluye cualquier otra información que devuelva el backend
        };

        // Actualiza el estado local de la sección activa
        sections[sectionId].push(newProduct);
        products[newProduct.name] = newProduct; // Añade el producto al listado general

        // Limpia los campos del formulario
        newProductName.value = '';
        newProductPrice.value = '';
        successMessage.value = 'Producto añadido correctamente.';
        toggleModalProduct();
    } catch (err) {
        console.error('Error al añadir nuevo producto:', err.response?.data || err.message);
        errorMessage.value = 'Error al añadir el nuevo producto. Por favor, intenta nuevamente.';
    }
};

const deleteProduct = async (id_Product) => {
    const token = localStorage.getItem('access_token');
    const idProduct = id_Product;

    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/product/delete",
            { id: idProduct },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
    
       //Borrar el producto de la lista local
        const product = products[idProduct];
        const sectionId = product.section_id;
        const index = sections[sectionId].findIndex((item) => item.id === idProduct);
        sections[sectionId].splice(index, 1);
        delete products[idProduct];
        successMessage.value = 'Producto eliminado correctamente.';


    } catch (err) {
    
        console.error('Error al eliminar el producto:', err.response?.data || err.message);
        errorMessage.value = 'Error al eliminar el producto. Por favor, intenta nuevamente.';
    }
};       

const prepareEditProduct = (product) => {
    editProductId.value = product.id; // Se asigna el ID del producto seleccionado.
    editProductName.value = product.name; // Se asigna el nombre actual.
    editProductPrice.value = product.price; // Se asigna el precio actual.
    editProductSection.value = product.section_id; // Se asigna la sección actual.
    toggleModalEditProduct(); // Abre el modal.
};


const editProduct = async() =>{
    const token = localStorage.getItem('access_token');

    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/product/edit",
            { id: editProductId.value, name: editProductName.value, price: editProductPrice.value, section_id: editProductSection.value },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        );
        // Actualizar el producto en la lista local
        const product = products[editProductId.value];
        product.name = editProductName.value;
        product.price = editProductPrice.value;
        product.section_id = editProductSection.value;
        successMessage.value = 'Producto editado correctamente.';
        toggleModalEditProduct();
    } catch (err) {
        console.error('Error al editar el producto:', err.response?.data || err.message);
        errorMessage.value = 'Error al editar el producto. Por favor, intenta nuevamente.';
    }
};

const getwebsiteName = async()=> {
    const token = localStorage.getItem('access_token');
    const idPage = localStorage.getItem('id_page');

    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/website/single',
            { id_page: idPage },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
        websiteName.value = response.data.name;
    } catch (err) {
        console.error('Error al obtener el nombre de la página:', err.response?.data || err.message);
        errorMessage.value = 'Error al cargar el nombre de la página. Por favor, intenta nuevamente.';
    }
};


// Cargar datos iniciales al montar el componente
onMounted(() => {
    fetchSectionNames();
    fetchProducts();
    getwebsiteName();
});
</script>
