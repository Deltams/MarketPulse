<template>
  <v-container>
    <v-row v-if="product">
      <v-col cols="12" md="6">
        <v-img :src="product.image" max-height="400" contain></v-img>
      </v-col>
      <v-col cols="12" md="6">
        <h1 class="text-h4">{{ product.name }}</h1>
        <p>{{ product.description }}</p>
        <p><strong>Цена:</strong> {{ product.price }} руб.</p>
        <p><strong>Продавец:</strong> {{ product.seller?.name }}</p>
        <v-btn color="primary" @click="addToCart">Добавить в корзину</v-btn>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col><p>Загрузка...</p></v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="js">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api';
import { useCartStore } from '../stores/cart';

const route = useRoute();
const product = ref(null);
const cartStore = useCartStore();

const fetchProduct = async () => {
  try {
    const response = await api.get(`productlist/${route.params.id}/`);
    product.value = response.data;
  } catch (error) {
    console.error('Error fetching product:', error);
  }
};

const addToCart = () => {
  if (product.value) {
    cartStore.addItem(product.value);
    alert('Добавлено в корзину');
  }
};

onMounted(fetchProduct);
</script>