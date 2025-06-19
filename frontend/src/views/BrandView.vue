<template>
  <div class="brand">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <h1>{{ brand.name }}</h1>
      <p class="description">{{ brand.description }}</p>
      <BrandCatalogGrid :brandId="brand.id" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api/config';
import BrandCatalogGrid from '@/components/common/BrandCatalogGrid.vue';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
}

interface Brand {
  id: number;
  name: string;
  description: string;
}

const route = useRoute();
const brand = ref<Brand | null>(null);
const loading = ref(true);
const error = ref('');

const fetchBrandData = async () => {
  try {
    const brandId = route.params.id;
    const brandResponse = await api.get(`/brandlist/${brandId}/`);
    brand.value = brandResponse.data;
  } catch (err) {
    error.value = 'Failed to load brand data';
    console.error('Error fetching brand data:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchBrandData();
});
</script>

<style scoped>
.brand {
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

.brand h1 {
  color: #1976d2;
}
</style>