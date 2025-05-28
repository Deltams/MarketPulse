<template>
  <v-container>
    <h1>Каталог товаров</h1>
    <v-data-table :items="products" :headers="headers">
      <template v-slot:item.actions="{ item }">
        <v-btn :to="`/product/${item.id}`">Подробнее</v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../api';

const products = ref([]);
const headers = [
  { title: 'Название', key: 'name' },
  { title: 'Цена', key: 'price' }
];

const fetchProducts = async () => {
  try {
    const response = await api.get('products/');
    products.value = response.data;
  } catch (error) {
    console.error('Ошибка:', error);
  }
};

onMounted(fetchProducts);
</script>