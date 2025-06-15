<template>
  <div class="brand">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <h1>{{ brand.name }}</h1>
      <p class="description">{{ brand.description }}</p>
      
      <div class="products-grid">
        <div v-for="product in products" :key="product.id" class="product-card">
          <h3>{{ product.name }}</h3>
          <p class="price">${{ product.price }}</p>
          <p class="description">{{ product.description }}</p>
          <router-link :to="`/products/${product.id}`" class="view-link">
            View Details
          </router-link>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api/config';

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
const products = ref<Product[]>([]);
const loading = ref(true);
const error = ref('');

const fetchBrandData = async () => {
  try {
    const brandId = route.params.id;
    const [brandResponse, productsResponse] = await Promise.all([
      api.get(`/brandlist/${brandId}/`),
      api.get(`/productlist/?brand=${brandId}`)
    ]);
    
    brand.value = brandResponse.data;
    products.value = productsResponse.data;
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
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.product-card h3 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.price {
  font-weight: bold;
  color: #2c3e50;
  margin: 0.5rem 0;
}

.view-link {
  display: inline-block;
  padding: 0.5rem 1rem;
  background-color: #2c3e50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
  margin-top: 1rem;
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