<template>
  <div class="product-list">
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="searchQuery"
                  label="Поиск товаров"
                  prepend-inner-icon="mdi-magnify"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                  @update:model-value="handleSearch"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-row>
                  <v-col cols="6">
                    <v-text-field
                      v-model="minPrice"
                      label="Мин. цена"
                      type="number"
                      variant="outlined"
                      density="comfortable"
                      hide-details
                      @update:model-value="handleFilter"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field
                      v-model="maxPrice"
                      label="Макс. цена"
                      type="number"
                      variant="outlined"
                      density="comfortable"
                      hide-details
                      @update:model-value="handleFilter"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="!Array.isArray(products)">
      <v-col cols="12" class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="64"
        ></v-progress-circular>
        <div class="text-h6 mt-4">Загрузка...</div>
      </v-col>
    </v-row>

    <v-row v-else-if="filteredProducts.length === 0">
      <v-col cols="12" class="text-center">
        <v-icon
          size="64"
          color="grey"
          class="mb-4"
        >
          mdi-package-variant-closed
        </v-icon>
        <div class="text-h6">Товары не найдены</div>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col
        v-for="product in filteredProducts"
        :key="product.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <ProductCard
          :product="product"
          :is-seller="isSeller"
          @edit="handleEdit"
          @add-to-cart="handleAddToCart"
        />
      </v-col>
    </v-row>
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
</style> 