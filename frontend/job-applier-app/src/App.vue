<template>
  <div class="flex flex-col justify-center items-center w-screen h-screen overflow-auto bg-linear-to-r from-gray-100 to-gray-300">
    <div class="flex flex-col gap-4 w-full max-h-[800px] overflow-auto max-w-2xl bg-white rounded shadow p-6">
      <h1 class="text-3xl font-bold">Email Writer</h1>
      <EmailForm />
    </div>
  </div>
</template>

<script setup>
import EmailForm from './components/EmailForm.vue'
</script>
