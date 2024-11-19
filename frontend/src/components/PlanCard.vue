<template>
  <div class="card bg-darkest shadow-lg rounded-lg p-6 text-lightest border border-mid transform transition-transform hover:scale-105 flex flex-col">
    <div class="flex items-center mb-6">
      <img
        src="/fotos/light.png"
        alt="Lightbulb icon"
        class="w-8 h-8 mr-2"
      />
      <h2 class="text-2xl text-lightest font-bold">{{ title }}</h2>
    </div>
    <p class="text-xl text-light mb-4">${{ price }}</p>
    <ul class="list-disc list-inside space-y-2 flex-grow">
      <li
        v-for="(option, index) in options"
        :key="index"
        class="text-mid"
      >
        {{ option }}
      </li>
    </ul>
    <div class="flex justify-end mt-6">
      <button
        class="bg-brand text-darkest px-6 py-3 rounded-md shadow-md hover:bg-light transition-colors"
      >
        Select Plan
      </button>
    </div>
  </div>
</template>

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
  },
};
</script>

<style scoped>
.card {
  background-color: var(--darkest);
  border-color: var(--mid);
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>
