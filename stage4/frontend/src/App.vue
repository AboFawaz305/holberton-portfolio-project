<script setup lang="ts">
import { ref } from 'vue'

type Group = {
  id: string
  name: string
  description: string
  keywords: string[]
}

const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const keyword = ref('')
const results = ref<Group[]>([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)

const search = async () => {
  error.value = ''
  searched.value = false

  const query = keyword.value.trim()
  if (!query) {
    error.value = 'Please enter a keyword to search.'
    return
  }

  loading.value = true
  try {
    const response = await fetch(
      `${apiBase}/groups/search?keyword=${encodeURIComponent(query)}`,
    )
    if (!response.ok) {
      throw new Error('Unable to fetch courses. Please try again.')
    }
    const data = await response.json()
    results.value = data.results ?? []
  } catch (err: unknown) {
    error.value = err instanceof Error ? err.message : 'Unexpected error occurred.'
    results.value = []
  } finally {
    loading.value = false
    searched.value = true
  }
}
</script>

<template>
  <main class="page">
    <section class="panel">
      <header class="panel__header">
        <h1>Search Courses</h1>
        <p>Find groups by name or keyword.</p>
      </header>

      <form class="search" @submit.prevent="search">
        <input
          v-model="keyword"
          type="search"
          name="keyword"
          placeholder="Enter a course or keyword (e.g. python, web, UX)"
          aria-label="Search for courses"
        />
        <button type="submit" :disabled="loading">
          {{ loading ? 'Searching...' : 'Search' }}
        </button>
      </form>

      <p v-if="error" class="status status--error">{{ error }}</p>
      <p v-if="!error && searched && !loading && results.length === 0" class="status">
        No courses found.
      </p>

      <ul v-if="results.length" class="results">
        <li v-for="group in results" :key="group.id" class="result">
          <h2>{{ group.name }}</h2>
          <p class="description">{{ group.description }}</p>
          <p class="keywords">
            <strong>Keywords:</strong> {{ group.keywords.join(', ') }}
          </p>
        </li>
      </ul>
    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fb;
  padding: 2rem;
  color: #0f172a;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
    'Roboto', 'Helvetica Neue', Arial, sans-serif;
}

.panel {
  width: min(960px, 100%);
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(15, 23, 42, 0.1);
  padding: 2rem;
}

.panel__header h1 {
  margin: 0 0 0.4rem;
  font-size: 1.8rem;
}

.panel__header p {
  margin: 0;
  color: #475569;
}

.search {
  display: flex;
  gap: 0.75rem;
  margin: 1.5rem 0;
  flex-wrap: wrap;
}

.search input {
  flex: 1 1 340px;
  padding: 0.9rem 1rem;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  font-size: 1rem;
}

.search input:focus {
  outline: 2px solid #2563eb;
  background: #fff;
}

.search button {
  padding: 0.9rem 1.5rem;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.search button[disabled] {
  opacity: 0.7;
  cursor: not-allowed;
}

.search button:not([disabled]):hover {
  background: #1d4ed8;
}

.status {
  margin: 0 0 1rem;
  color: #475569;
}

.status--error {
  color: #b91c1c;
  font-weight: 600;
}

.results {
  list-style: none;
  padding: 0;
  margin: 1rem 0 0;
  display: grid;
  gap: 1rem;
}

.result {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.25rem;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.result h2 {
  margin: 0 0 0.35rem;
  font-size: 1.1rem;
}

.description {
  margin: 0 0 0.35rem;
  color: #334155;
}

.keywords {
  margin: 0;
  color: #475569;
  font-size: 0.95rem;
}
</style>
