<template>
  <div class="space-y-4">
    <div class="flex flex-col gap-2">
      
      <input v-model="recipient_email" placeholder="Recipient Email" class="p-2 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400" />
      <p v-if="errorObj.email" class="text-red-500">
        {{ errorObj.email }}
      </p>

      <input v-model="subject" placeholder="Subject" class="p-2 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400" />
      <p v-if="errorObj.subject" class="text-red-500">
        {{ errorObj.subject }}
      </p>

      <input v-model="company" placeholder="Company" class="p-2 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400" />
      
      <input v-model="heard_from" placeholder="Heard From" class="p-2 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400" />
      
      <textarea v-model="details" placeholder="Details / Context" rows="4" class="p-2 rounded border-2 border-gray-300 focus:outline-none focus:border-blue-400"></textarea>
      <p v-if="errorObj.details" class="text-red-500">
        {{ errorObj.details }}
      </p>  
    </div>

    <div class="flex items-center gap-3">
      <button
        @click="onSubmit"
        :disabled="loading || sending"
        :class="[ loading || sending ? 'cursor-not-allowed' : 'cursor-pointer', 'px-4 py-2 bg-blue-600 text-white rounded disabled:bg-gray-400']">
        {{ loading ? 'Generating…' : 'Generate Email' }}
      </button>

      <button @click="clear" :disabled="loading || sending" :class="[ loading || sending ? 'cursor-not-allowed' : 'cursor-pointer', 'px-3 py-2 border rounded']">Clear</button>

    </div>

    <div v-if="errorObj.generic" class="text-red-600">{{ errorObj.generic }}</div>

    <div v-if="generatedEmail" class="flex flex-col relative gap-3 p-4 rounded-lg border border-gray-300 bg-gray-200">
      <h2 class="text-xl font-semibold mb-2">Generated Email</h2>
      <pre class="whitespace-pre-wrap font-sans tracking-wide">{{ generatedEmail }}</pre>
      <div class="mt-3 flex gap-2">
        <button @click="copy" class="px-3 py-1 border rounded cursor-pointer bg-blue-600 text-white">Copy</button>
        <button @click="download" class="px-3 py-1 border rounded cursor-pointer bg-blue-600 text-white">Download .txt</button>
              
        <button
          @click="sendEmail"
          :disabled="sending"
          :class="[sending ? 'cursor-not-allowed' : 'cursor-pointer', 'px-4 py-2 bg-blue-600 text-white rounded disabled:bg-gray-400']">
          {{ sending ? 'Sending...' : 'Send Email' }}
        </button>
      
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
import { reactive, ref } from 'vue'

const recipient_email = ref('')
const subject = ref('')
const details = ref('Fullstack developer with more than 5 years of experience in building web applications. Skilled in JavaScript, Vue.js, Nuxt.js, Laravel, and Python. Looking for a challenging role to contribute my expertise and grow professionally.')
const generatedEmail = ref('')
const company = ref('')
const heard_from = ref('')
const loading = ref(false)
const sending = ref(false)


const errorObj = reactive({
  'email': '',
  'subject': '',
  'details': '',
  'generic': ''
})

let isValid = true

// const isEmailValid = computed(() => {
//   const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//   return re.test(recipient_email.value)
// })

async function onSubmit() {
  if (loading.value || sending.value) return

  // Reset errors
  Object.keys(errorObj).forEach(key => errorObj[key] = '')

  isValid = true
  

  // Validation
  if(!(/^[^\s@]+@[^\s@]+\.[^\s@]+$/).test(recipient_email.value)){
    errorObj.email = 'Invalid email address'
    isValid = false
  }
  if(subject.value.trim() === ''){
    errorObj.subject = 'Subject is required'
    isValid = false
  }
  if(details.value.trim() === ''){
    errorObj.details = 'Details are required'
    isValid = false
  }

  if(!isValid) return;

  loading.value = true
  generatedEmail.value = ''

  try {
    const res = await fetch('http://localhost:8000/api/email/generate/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recipient_email: recipient_email.value,
        subject: subject.value,
        details: details.value,
        company: company.value,
        heard_from: heard_from.value,
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Server error')
    generatedEmail.value = data.email
  } catch (err) {
    errorObj.generic = err.message
  } finally {
    loading.value = false
  }
}

async function sendEmail(){

  if (loading.value || sending.value) return
  sending.value = true
  
  try{
    const res = await fetch('http://localhost:8000/api/email/send/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recipient_email: recipient_email.value,
        subject: subject.value,
        email: generatedEmail.value
      })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Server error')
    pushToast('Email sent successfully ✓')
  } catch (err) {
    errorObj.generic = err.message
  }
  finally {
    sending.value = false
  }
}

function clear() {
  recipient_email.value = ''
  subject.value = ''
  details.value = ''
  generatedEmail.value = ''
  company.value = ''
  heard_from.value = ''
}

function copy() {
  navigator.clipboard.writeText(generatedEmail.value)
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
  const blob = new Blob([generatedEmail.value], { type: 'text/plain' })
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
