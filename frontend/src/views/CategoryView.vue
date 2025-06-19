<template>
  <div class="category">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <h1>{{ category.name }}</h1>
      <p class="description">{{ category.description }}</p>
      <CategoryCatalogGrid :categoryId="category.id" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api/config';
import CategoryCatalogGrid from '@/components/common/CategoryCatalogGrid.vue';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
}

interface Category {
  id: number;
  name: string;
  description: string;
}

const route = useRoute();
const category = ref<Category | null>(null);
const loading = ref(true);
const error = ref('');

const fetchCategoryData = async () => {
  try {
    const categoryId = route.params.id;
    const categoryResponse = await api.get(`/categories/${categoryId}/`);
    category.value = categoryResponse.data;
  } catch (err) {
    error.value = 'Failed to load category data';
    console.error('Error fetching category data:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchCategoryData();
});
</script>

<style scoped>
.category {
  padding: 1rem;
}

.description {
  color: #666;
  margin-bottom: 2rem;
  font-size: 1.3rem;
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

.category h1 {
  color: #1976d2;
}
</style>