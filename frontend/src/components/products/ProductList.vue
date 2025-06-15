<template>
  <div class="product-list">
    <div class="filters">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск товаров..."
        class="search-input"
        @input="handleSearch"
      >
      <div class="price-filter">
        <input
          v-model="minPrice"
          type="number"
          placeholder="Мин. цена"
          class="price-input"
          @input="handleFilter"
        >
        <input
          v-model="maxPrice"
          type="number"
          placeholder="Макс. цена"
          class="price-input"
          @input="handleFilter"
        >
      </div>
    </div>

    <div v-if="!Array.isArray(products)" class="loading">
      Загрузка...
    </div>

    <div v-else-if="filteredProducts.length === 0" class="no-products">
      Товары не найдены
    </div>

    <div v-else class="products-grid">
      <ProductCard
        v-for="product in filteredProducts"
        :key="product.id"
        :product="product"
        :is-seller="isSeller"
        @edit="handleEdit"
        @add-to-cart="handleAddToCart"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import ProductCard from './ProductCard.vue'

interface Product {
  id: number
  name: string
  description: string
  price: number
  imageUrl?: string
}

const props = defineProps<{
  products: Product[]
  isSeller?: boolean
}>()

const emit = defineEmits<{
  (e: 'edit', product: Product): void
  (e: 'add-to-cart', product: Product): void
}>()

const searchQuery = ref('')
const minPrice = ref<number | null>(null)
const maxPrice = ref<number | null>(null)

// Добавляем наблюдатель за изменениями в products
watch(() => props.products, (newProducts) => {
  console.log('ProductList: products updated:', newProducts)
}, { deep: true })

const filteredProducts = computed(() => {
  console.log('ProductList: filtering products:', props.products)
  if (!Array.isArray(props.products)) {
    return []
  }
  
  return props.products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesPrice = (!minPrice.value || product.price >= minPrice.value) &&
                        (!maxPrice.value || product.price <= maxPrice.value)

    return matchesSearch && matchesPrice
  })
})

const handleSearch = () => {
  // Можно добавить debounce здесь
}

const handleFilter = () => {
  // Можно добавить debounce здесь
}

const handleEdit = (product: Product) => {
  emit('edit', product)
}

const handleAddToCart = (product: Product) => {
  emit('add-to-cart', product)
}
</script>

<style scoped>
.product-list {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  min-width: 300px;
}

.price-filter {
  display: flex;
  gap: 8px;
}

.price-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  width: 120px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.loading,
.no-products {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .search-input {
    min-width: 100%;
  }
  
  .price-filter {
    width: 100%;
  }
  
  .price-input {
    flex: 1;
  }
}
</style> 