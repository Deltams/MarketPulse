<template>
  <div class="categories">
    <h1>Categories</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="categories-grid">
      <div v-for="category in categories" :key="category.id" class="category-card">
        <h3>{{ category.name }}</h3>
        <p>{{ category.description }}</p>
        <router-link :to="`/category/${category.id}`" class="view-link">
          View Products
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../api/config';

interface Category {
  id: number;
  name: string;
  description: string;
}

const categories = ref<Category[]>([]);
const loading = ref(true);
const error = ref('');

const fetchCategories = async () => {
  try {
    const response = await api.get('/categories/');
    categories.value = response.data;
  } catch (err) {
    error.value = 'Failed to load categories';
    console.error('Error fetching categories:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
.categories {
  padding: 1rem;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.category-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.category-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.category-card p {
  margin: 0 0 1rem 0;
  color: #666;
}

.view-link {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #2c3e50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.view-link:hover {
  background-color: #34495e;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #dc3545;
  text-align: center;
  padding: 1rem;
}
</style>