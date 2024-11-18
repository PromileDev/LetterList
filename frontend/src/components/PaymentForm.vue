<script setup>
import { ref } from 'vue';

// Campos del formulario
const full_name = ref('');
const card_number = ref('');
const card_expiration = ref('');
const cvv = ref('');
const loading = ref(false);
const error = ref('');

// Manejo del envío de formulario (Simulación)
const handlePayment = async () => {
  try {
    loading.value = true;
    error.value = '';

    // Simulación de procesamiento de pago
    await new Promise((resolve) => setTimeout(resolve, 2000)); // Simula una espera de 2 segundos

    // Generar una respuesta exitosa o fallida
    const isSuccess = true; // Cambiar a `true` para simular un pago exitoso
    if (isSuccess) {
      alert('Payment processed successfully!');
      // Reiniciar campos si es necesario
      full_name.value = '';
      card_number.value = '';
      card_expiration.value = '';
      cvv.value = '';
    } else {
      throw new Error('Payment failed. Please try again.');
    }
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="mx-auto max-w-screen-xl px-4 2xl:px-0">
    <div class="mx-auto max-w-5xl">
      <h1 class="font-bold text-lightest text-xl md:text-light md:text-6xl">Payment amount:</h1>
      <h1 class="font-bold text-lightest text-xl md:text-6xl md:text-light md:mb-2">30 €</h1>
      <div class="mt-6 sm:mt-8 lg:flex lg:items-start lg:gap-12">
        <form
          @submit.prevent="handlePayment"
          class="w-full rounded-lg md:bg-light p-4 shadow-sm sm:p-6 lg:max-w-xl lg:p-8"
        >
          <!-- Nombre completo -->
          <div class="mb-6">
            <label for="full_name" class="font-semibold text-lightest text-xl mb-4 ml-2 md:text-darkest">
              Full name*
            </label>
            <input
              type="text"
              id="full_name"
              v-model="full_name"
              class="block w-full rounded-lg bg-darkest text-white p-2.5 text-sm focus:ring-brand focus:border-brand"
              placeholder="Bonnie Green"
              pattern="[A-Za-z ]+" 
              required
            />
          </div>

          <!-- Número de tarjeta -->
          <div class="mb-6">
            <label for="card_number" class="font-semibold text-lightest text-xl mb-4 ml-2 md:text-darkest">
              Card number*
            </label>
            <input
              type="text"
              id="card_number"
              v-model="card_number"
              class="block w-full rounded-lg bg-darkest text-white p-2.5 text-sm focus:ring-brand focus:border-brand"
              placeholder="xxxx-xxxx-xxxx-xxxx"
              pattern="[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}"
              required
            />
          </div>

          <!-- Fecha de expiración -->
          <div class="mb-6 grid grid-cols-2 gap-4">
            <div>
              <label for="card_expiration" class="font-semibold text-lightest text-xl mb-4 ml-2 md:text-darkest">
                Expiration*
              </label>
              <input
                type="text"
                id="card_expiration"
                v-model="card_expiration"
                class="block w-full rounded-lg bg-darkest text-white p-2.5 text-sm focus:ring-brand focus:border-brand"
                placeholder="MM/YY"
                pattern="(0[1-9]|1[0-2])\/[0-9]{2}"
                required
              />
            </div>

            <!-- CVV -->
            <div>
              <label for="cvv" class="font-semibold text-lightest text-xl mb-4 ml-2 md:text-darkest">
                CVV*
              </label>
              <input
                type="text"
                id="cvv"
                v-model="cvv"
                class="block w-full rounded-lg bg-darkest text-white p-2.5 text-sm focus:ring-brand focus:border-brand"
                placeholder="•••"
                required
              />
            </div>
          </div>

          <!-- Botón de pago -->
          <button
            type="submit"
            class="mx-auto bg-brand py-2 w-full rounded-full font-bold text-darkest"
            :disabled="loading"
          >
            {{ loading ? 'Processing...' : 'Pay now' }}
          </button>

          <!-- Mensaje de error -->
          <p v-if="error" class="mt-4 text-red-500 text-sm">{{ error }}</p>
        </form>
      </div>

      <!-- Logos de tarjetas -->
      <div class="flex justify-center items-center mt-3 mb-5">
        <img src="/fotos/Mastercard.png" class="w-[75px] mx-2" alt="Mastercard logo">
        <img src="/fotos/Visa.png" class="w-[75px] mx-2" alt="Visa logo">
      </div>
    </div>
  </div>
</template>
