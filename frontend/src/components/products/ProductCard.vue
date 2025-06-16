<template>
  <v-card
    class="product-card"
    :elevation="2"
    :hover="true"
  >
    <v-img
      :src="product.imageUrl || '/placeholder.png'"
      :alt="product.name"
      height="200"
      cover
      class="align-end"
    >
      <v-card-title class="text-white text-shadow">
        {{ product.name }}
      </v-card-title>
    </v-img>

    <v-card-text>
      <p class="text-body-2 text-medium-emphasis mb-4">
        {{ product.description }}
      </p>
      <div class="text-h6 text-primary mb-4">
        {{ formatPrice(product.price) }}
      </div>
    </v-card-text>

    <v-card-actions>
      <v-btn
        block
        color="primary"
        variant="elevated"
        @click="$emit('add-to-cart', product)"
        prepend-icon="mdi-cart-plus"
      >
        В корзину
      </v-btn>
      <v-btn
        v-if="isSeller"
        block
        color="secondary"
        variant="outlined"
        @click="$emit('edit', product)"
        prepend-icon="mdi-pencil"
        class="mt-2"
      >
        Редактировать
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface Product {
  id: number
  name: string
  description: string
  price: number
  imageUrl?: string
}

const props = defineProps<{
  product: Product
  isSeller?: boolean
}>()

const emit = defineEmits<{
  (e: 'add-to-cart', product: Product): void
  (e: 'edit', product: Product): void
}>()

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}
</script>

<style scoped>
.product-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.text-shadow {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.v-card-actions {
  margin-top: auto;
}
</style> 