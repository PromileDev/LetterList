<script setup>
import MostPopular from "../components/MostPopular.vue";
</script>

<script>
export default {
  name: "PlanCard",
  props: {
    title: {
      type: String,
      required: true,
    },
    price: {
      type: Number,
      required: true,
    },
    options: {
      type: Array,
      required: true,
    },
    popular: {
      type: Boolean,
      default: false,
    },
    URL: {
      type: String,
      required: true,
    },
  },
};
</script>

<template>
  <div class="card bg-darkest shadow-lg rounded-lg text-lightest border border-mid transform transition-transform hover:scale-105 flex flex-col max-w-xs mx-auto">
    <div class="m-4" />
    <!-- Título -->
    <div class="flex flex-col items-center mb-6 px-4">
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-darkest mb-4">Add a website</h1>
      <p class="text-lg text-dark mb-6">Enter the name of the website you want to add</p>
      <!-- Campo de entrada -->
      <input v-model="website_name"
             class="text-lg text-darkest border-2 border-mid rounded-lg py-2 px-4 w-full mb-4 placeholder-dark opacity-70 focus:ring-2 focus:ring-brand focus:border-transparent transition duration-300"
             placeholder="Website name" />
    </div>

    <!-- Botón -->
    <div class="flex justify-center mb-6 px-4">
      <button @click="addWebsite" 
              class="py-2 px-6 bg-mid rounded-lg text-lightest font-semibold w-full sm:w-auto mb-10 cursor-pointer hover:bg-brand focus:outline-none focus:ring-2 focus:ring-brand focus:ring-opacity-50 transition-all ease-in-out duration-300 opacity-60 disabled:opacity-40 disabled:cursor-not-allowed"
              :class="{'opacity-100': website_name.length > 0}" 
              :disabled="!website_name">
        Add website
      </button>
    </div>
  </div>
</template>

<style scoped>
.card {
  background-color: var(--darkest);
  border-color: var(--mid);
  display: flex;
  flex-direction: column;
  height: 400px;
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>