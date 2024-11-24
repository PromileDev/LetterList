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
  },
};
</script>

<template>
  <div class="card bg-darkest shadow-lg rounded-lg text-lightest border border-mid transform transition-transform hover:scale-105 flex flex-col">
    <div class="m-4" />
    <!-- Título y Most Popular -->
    <div class="flex items-center mb-6 pl-5 h-12">
      <img
        src="/fotos/light.png"
        alt="Lightbulb icon"
        class="w-8 h-8 mr-2"
      />
      <h2 class="text-2xl text-lightest font-bold flex-grow">{{ title }}</h2>
      <div v-if="popular">
        <MostPopular />
      </div>
    </div>

    <!-- Precio -->
    <p class="text-xl text-light mb-4 pl-5">${{ price }}</p>

    <!-- Lista de opciones -->
    <ul class="list-disc list-inside space-y-2 flex-grow pl-5">
      <li
        v-for="(option, index) in options"
        :key="index"
        class="text-mid"
      >
        {{ option }}
      </li>
    </ul>

    <!-- Botón -->
    <div class="flex justify-end mt-3">
      <button
        class="bg-brand text-darkest px-6 py-3 rounded-md shadow-md hover:bg-light transition-colors"
      >
        Select Plan
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
  height: 450px;
  width: 300px;
}
</style> 