<template>
  <div class="products-page">
    <div class="container">
      <h1>Товары</h1>
      
      <div v-if="loading" class="loading">
        Загрузка товаров...
      </div>
      
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      
      <div v-else class="products-grid">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
          @add-to-cart="addToCart"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useProductStore } from '@/stores/productStore'
import ProductCard from '@/components/products/ProductCard.vue'

const productStore = useProductStore()

const products = computed(() => productStore.products)
const loading = computed(() => productStore.loading)
const error = computed(() => productStore.error)

const addToCart = (product: any) => {
  // Здесь будет логика добавления в корзину
  console.log('Adding to cart:', product)
}

onMounted(async () => {
  try {
    await productStore.fetchProducts()
  } catch (err) {
    console.error('Error fetching products:', err)
  }
})
</script>

<style scoped>
.products-page {
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  text-align: center;
  padding: 2rem;
  color: #dc3545;
  background-color: #f8d7da;
  border-radius: 4px;
}
</style>