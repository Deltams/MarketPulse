<template>
  <div class="brands">
    <h1>Brands</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="brands-grid">
      <div v-for="brand in brands" :key="brand.id" class="brand-card">
        <h3>{{ brand.name }}</h3>
        <p>{{ brand.description }}</p>
        <router-link :to="`/brands/${brand.id}`" class="view-link">
          View Products
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../api/config';

interface Brand {
  id: number;
  name: string;
  description: string;
}

const brands = ref<Brand[]>([]);
const loading = ref(true);
const error = ref('');

const fetchBrands = async () => {
  try {
    const response = await api.get('/brandlist/');
    brands.value = response.data;
  } catch (err) {
    error.value = 'Failed to load brands';
    console.error('Error fetching brands:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchBrands();
});
</script>

<style scoped>
.brands {
  padding: 1rem;
}

.brands-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.brand-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.brand-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.brand-card p {
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