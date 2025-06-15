<template>
  <div class="products">
    <h1>All Products</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="products-grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        <h3>{{ product.name }}</h3>
        <p class="price">${{ product.price }}</p>
        <p class="description">{{ product.description }}</p>
        <div class="product-meta">
          <span class="brand">Brand: {{ product.brand_name }}</span>
          <span class="category">Category: {{ product.category_name }}</span>
        </div>
        <router-link :to="`/products/${product.id}`" class="view-link">
          View Details
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../api/config';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  brand_name: string;
  category_name: string;
}

const products = ref<Product[]>([]);
const loading = ref(true);
const error = ref('');

const fetchProducts = async () => {
  try {
    const response = await api.get('/productlist/');
    products.value = response.data;
  } catch (err) {
    error.value = 'Failed to load products';
    console.error('Error fetching products:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.products {
  padding: 1rem;
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

.description {
  color: #666;
  margin-bottom: 1rem;
}

.product-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
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