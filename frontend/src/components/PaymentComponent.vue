<template>
  <main class="flex flex-col md:flex-row md:justify-between  w-11/12 md:w-[80%] items-center mx-auto">
    <div class="flex justify-center flex-col items-center w-[50%] mt-[10vh] md:mt-0">
      <!-- Mostrar el plan seleccionado -->
      <PlanCard :title="selectedPlan.title" :price="selectedPlan.price" :options="selectedPlan.options" :popular="selectedPlan.popular" />
    </div>

    <div class="flex justify-center items-center w-11/12 md:w-[50%] mt-10 md:mt-0 flex-col">
      <!-- Formulario de pago -->
      <PaymentForm />
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import PaymentForm from "../components/PaymentForm.vue";
import PlanCard from "../components/PlanCard.vue";
import Plans from "../Plans.json"; // Asegúrate de la ruta correcta

// Variable reactiva para almacenar el plan seleccionado
const selectedPlan = ref({
  title: "No plan selected",
  price: 0,
  options: [],
  popular: false,
});

// Recuperar el título del plan seleccionado de localStorage
onMounted(() => {
  const title = localStorage.getItem("title_plan");
  if (title) {
    const plan = Plans.find((plan) => plan.title === title);
    if (plan) {
      selectedPlan.value = plan;
    }
  }
});
</script>

<style scoped>
/* Estilos personalizados si los necesitas */
</style>
