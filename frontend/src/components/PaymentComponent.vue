<template>
  <main class="flex flex-col md:flex-row md:justify-between h-screen w-11/12 md:w-[80%] items-center mx-auto">
    <div class="flex justify-center flex-col items-center w-[50%] mt-[10vh] md:mt-0">
      <!-- Pasar props correctamente al PlanCard -->
      <PlanCard :title="title" :price="price" :options="options" :popular="popular" />
    </div>

    <div class="flex justify-center items-center w-11/12 md:w-[50%] mt-10 md:mt-0 flex-col">
      <PaymentForm />
    </div>
  </main>
</template>

<script setup>
import PaymentForm from "../components/PaymentForm.vue";
import PlanCard from "../components/PlanCard.vue";
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
