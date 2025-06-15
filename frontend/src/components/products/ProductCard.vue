<template>
  <div class="product-card">
    <div class="product-image">
      <img :src="product.imageUrl || '/placeholder-image.jpg'" :alt="product.name">
    </div>
    <div class="product-info">
      <h3 class="product-name">{{ product.name }}</h3>
      <p class="product-description">{{ product.description }}</p>
      <div class="product-price">{{ formatPrice(product.price) }}</div>
      <div class="product-actions">
        <button 
          v-if="isSeller" 
          @click="$emit('edit', product)" 
          class="edit-button"
        >
          Редактировать
        </button>
        <button 
          v-if="!isSeller" 
          @click="$emit('add-to-cart', product)" 
          class="add-to-cart-button"
        >
          В корзину
        </button>
      </div>
    </div>
  </div>
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
  (e: 'edit', product: Product): void
  (e: 'add-to-cart', product: Product): void
}>()

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}
</script>

<style scoped>
.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  margin: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-2px);
}

.product-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 4px;
  margin-bottom: 12px;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.product-name {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0;
}

.product-description {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.product-price {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.product-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
}

.edit-button,
.add-to-cart-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.edit-button {
  background-color: #3498db;
  color: white;
}

.add-to-cart-button {
  background-color: #2ecc71;
  color: white;
}

.edit-button:hover {
  background-color: #2980b9;
}

.add-to-cart-button:hover {
  background-color: #27ae60;
}
</style> 