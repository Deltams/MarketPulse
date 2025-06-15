<template>
  <div class="product">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div class="product-details">
        <h1>{{ product.name }}</h1>
        <p class="price">${{ product.price }}</p>
        <p class="description">{{ product.description }}</p>
        
        <div class="product-meta">
          <div class="meta-item">
            <strong>Brand:</strong>
            <router-link :to="`/brands/${product.brand_id}`" class="link">
              {{ product.brand_name }}
            </router-link>
          </div>
          <div class="meta-item">
            <strong>Category:</strong>
            <router-link :to="`/category/${product.category_id}`" class="link">
              {{ product.category_name }}
            </router-link>
          </div>
        </div>

        <div class="actions">
          <button class="add-to-cart" @click="addToCart">
            Add to Cart
          </button>
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
  brand_id: number;
  brand_name: string;
  category_id: number;
  category_name: string;
}

const route = useRoute();
const product = ref<Product | null>(null);
const loading = ref(true);
const error = ref('');

const fetchProduct = async () => {
  try {
    const productId = route.params.id;
    const response = await api.get(`/productlist/${productId}/`);
    product.value = response.data;
  } catch (err) {
    error.value = 'Failed to load product';
    console.error('Error fetching product:', err);
  } finally {
    loading.value = false;
  }
};

const addToCart = () => {
  // TODO: Implement cart functionality
  console.log('Add to cart clicked');
};

onMounted(() => {
  fetchProduct();
});
</script>

<style scoped>
.product {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.product-details {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 1rem 0;
}

.description {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.product-meta {
  margin-bottom: 2rem;
}

.meta-item {
  margin-bottom: 0.5rem;
}

.link {
  color: #3498db;
  text-decoration: none;
  margin-left: 0.5rem;
}

.link:hover {
  text-decoration: underline;
}

.actions {
  margin-top: 2rem;
}

.add-to-cart {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.add-to-cart:hover {
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