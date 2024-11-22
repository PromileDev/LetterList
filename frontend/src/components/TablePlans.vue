<template>
    <div id="detailed-pricing" class="w-full overflow-x-auto">
      <div class="overflow-hidden min-w-max px-10 pt-5">
        <!-- Header -->
        <div class="grid grid-cols-4 p-4 text-sm font-bold text-darkest bg-light border-t border-b border-mid gap-x-16">
          <div class="flex items-center">Features</div>
          <div>Basic Edition</div>
          <div>Pro Edition</div>
          <div>Enterprise Edition</div>
        </div>
  
        <!-- Rows -->
        <div
          class="grid grid-cols-4 px-4 py-5 text-sm border-b border-mid gap-x-16"
          v-for="(row, index) in rows"
          :key="index"
        >
          <div class="text-mid">
            {{ row.feature }}
            <span v-if="row.link">
              (<a href="#" class="text-darkest hover:underline">view</a>)
            </span>
          </div>
          <div v-for="status in row.status" :key="status" class="flex justify-start ml-7">
            <svg
              v-if="status"
              class="w-4 h-4 text-green-400"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 16 12"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M1 5.917 5.724 10.5 15 1.5"
              />
            </svg>
            <svg
              v-else
              class="w-4 h-4 text-red-500"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 14 14"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
              />
            </svg>
          </div>
        </div>
  
        <!-- Buttons -->
        <div class="grid grid-cols-4 py-5 text-sm border-b border-mid gap-x-16">
          <div></div>
          <div v-for="edition in editions" :key="edition">
            <a
              href="#"
              class="bg-brand text-darkest px-4 py-3 rounded-md shadow-md hover:bg-light transition-colors"
            >
              Buy now
            </a>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  const rows = [
  {
    feature: "Unlimited letters",
    status: [true, true, true],
  },
  {
    feature: "Unlimited templates",
    status: [true, true, true],
  },
  {
    feature: "Unlimited contacts",
    status: [true, true, true],
  },
  {
    feature: "Unlimited campaigns",
    status: [true, true, true],
  },
  {
    feature: "Unlimited analytics",
    status: [true, true, true],
  },
  {
    feature: "Basic Plan",
    status: [false, true, true],
  },
  {
    feature: "Custom branding",
    status: [false, true, true],
  },
  {
    feature: "Pro plan",
    status: [false, false, true],
  },
  {
    feature: "Dedicated account manager",
    status: [false, false, true],
  },
];

  
  const editions = ["basic", "pro", "enterprise"];
  </script>
  
  <style scoped>
  </style>
  