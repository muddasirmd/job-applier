<template>
  <div class="space-y-4">
    <div class="flex flex-col gap-2">
      
      <input v-model="recipient_name" placeholder="Recipient name" class="p-2 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400" />

      <select v-model="tone" class="px-2 py-3 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400">
        <option value="">Select tone...</option>
        <option value="professional">Professional</option>
        <option value="friendly">Friendly</option>
        <option value="formal">Formal</option>
        <option value="casual">Casual</option>
        <option value="persuasive">Persuasive</option>
      </select>
    

      <input v-model="purpose" placeholder="Purpose (subject / short)" class="p-2 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400" />
      
      <textarea v-model="details" placeholder="Details / context" rows="4" class="p-2 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400"></textarea>
    </div>

    <div class="flex items-center gap-3">
      <button
        @click="onSubmit"
        :disabled="loading"
        :class="[ loading ? 'cursor-not-allowed' : 'cursor-pointer', 'px-4 py-2 bg-blue-600 text-white rounded disabled:bg-gray-400']">
        {{ loading ? 'Generating…' : 'Generate Email' }}
      </button>

      <button @click="clear" :disabled="loading" :class="[ loading ? 'cursor-not-allowed' : 'cursor-pointer', 'px-3 py-2 border rounded']">Clear</button>
    </div>

    <div v-if="error" class="text-red-600">{{ error }}</div>

    <div v-if="email" class="flex flex-col relative gap-3 p-4 rounded-lg border border-gray-300 bg-gray-200">
      <h2 class="text-xl font-semibold mb-2">Generated Email</h2>
      <pre class="whitespace-pre-wrap font-sans tracking-wide">{{ email }}</pre>
      <div class="mt-3 flex gap-2">
        <button @click="copy" class="px-3 py-1 border rounded cursor-pointer bg-blue-600 text-white">Copy</button>
        <button @click="download" class="px-3 py-1 border rounded cursor-pointer bg-blue-600 text-white">Download .txt</button>
        
        <!-- Toasts container -->
        <div class="absolute bottom-14 z-50">
          <div
            v-for="t in toasts"
            :key="t.id"
            class="bg-gray-900 text-white px-4 py-2 rounded shadow-md"
            role="status"
            aria-live="polite"
          >
            {{ t.message }}
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const recipient_name = ref('')
const purpose = ref('')
const details = ref('')
const tone = ref('')
const email = ref("")
const loading = ref(false)
const error = ref('')

async function onSubmit() {
  if (loading.value) return
  loading.value = true
  error.value = ''
  email.value = ''

  try {
    const res = await fetch('http://localhost:8000/api/email/generate/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recipient_name: recipient_name.value,
        purpose: purpose.value,
        details: details.value,
        tone: tone.value
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Server error')
    email.value = data.email
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

function clear() {
  recipient_name.value = ''
  purpose.value = ''
  details.value = ''
  email.value = ''
}

function copy() {
  navigator.clipboard.writeText(email.value)
  pushToast('Copied to clipboard ✓')
}

const toasts = ref([])

function pushToast(message, ms = 2200) {
  const id = Date.now() + Math.random()
  toasts.value.push({ id, message })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, ms)
}

function download() {
  const blob = new Blob([email.value], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'email.txt'
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
/* keep it small — Tailwind recommended in real project */
</style>
