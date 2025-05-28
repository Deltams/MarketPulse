<template>
  <v-container>
    <h1 class="text-h4 mb-4">Каталог товаров</h1>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="Категория"
          :items="categories"
          item-title="name"
          item-value="id"
          v-model="selectedCategory"
          @update:modelValue="fetchProducts"
          clearable
        ></v-select>
      </v-col>
    </v-row>
    <v-data-table
      :items="products"
      :headers="headers"
      :page="page"
      :items-per-page="10"
      @update:page="page = $event; fetchProducts()"
      :loading="loading"
    >
      <template v-slot:item.actions="{ item }">
        <v-btn :to="`/product/${item.id}`" color="primary">Подробнее</v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="js">
import { ref, onMounted } from 'vue';
import api from '../api';

const products = ref([]);
const categories = ref([]);
const selectedCategory = ref(null);
const page = ref(1);
const loading = ref(false);

const headers = [
  { title: 'Название', key: 'name' },
  { title: 'Цена', key: 'price' },
  { title: 'Продавец', key: 'seller.name' },
];

const fetchCategories = async () => {
  try {
    const response = await api.get('categorylist/');
    categories.value = response.data;
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};

const fetchProducts = async () => {
  loading.value = true;
  try {
    const params = { page: page.value };
    if (selectedCategory.value) params.category = selectedCategory.value;
    const response = await api.get('productlist/', { params });
    products.value = response.data.results || response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchCategories();
  fetchProducts();
});
</script>