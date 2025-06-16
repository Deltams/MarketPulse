<template>
  <v-container>
    <div v-if="loading" class="text-center">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
      <div class="text-h6 mt-4">Загрузка категории...</div>
    </div>

    <div v-else-if="error">
      <v-alert
        type="error"
        variant="tonal"
        class="mb-4"
      >
        {{ error }}
      </v-alert>
    </div>

    <template v-else>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-2">{{ category.name }}</h1>
          <p class="text-body-1 text-medium-emphasis mb-6">{{ category.description }}</p>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col
          v-for="product in products"
          :key="product.id"
          :cols="products.length === 1 ? 12 : 12"
          :sm="products.length === 1 ? 12 : 6"
          :md="products.length === 1 ? 12 : 6"
          :lg="products.length === 1 ? 12 : 6"
          class="d-flex"
        >
          <v-card
            class="h-100 w-100"
            :to="`/products/${product.id}`"
            hover
          >
            <v-card-title class="text-h6">
              {{ product.name }}
            </v-card-title>

            <v-card-text>
              <p class="text-h6 text-primary mb-2">
                {{ formatPrice(product.price) }}
              </p>
              <p class="text-body-2 text-medium-emphasis">
                {{ product.description }}
              </p>
            </v-card-text>

            <v-card-actions>
              <v-btn
                block
                color="primary"
                variant="text"
                :to="`/products/${product.id}`"
                class="d-flex justify-center align-center"
              >
                Подробнее
                <v-icon end icon="mdi-arrow-right" class="ml-2"></v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
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

interface Category {
  id: number;
  name: string;
  description: string;
}

const route = useRoute();
const category = ref<Category | null>(null);
const products = ref<Product[]>([]);
const loading = ref(true);
const error = ref('');

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price);
};

const fetchCategoryData = async () => {
  try {
    const categoryId = route.params.id;
    const [categoryResponse, productsResponse] = await Promise.all([
      api.get(`/categories/${categoryId}/`),
      api.get('/productlist/', { params: { category_0: categoryId } })
    ]);
    
    category.value = categoryResponse.data;
    products.value = productsResponse.data.results || productsResponse.data;
  } catch (err) {
    error.value = 'Не удалось загрузить данные категории';
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
/* Styles are now handled by Vuetify components */
</style>