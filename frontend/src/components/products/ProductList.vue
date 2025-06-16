<template>
  <div class="product-list">
    <div v-if="loading" class="d-flex justify-center align-center pa-4">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </div>

    <div v-else-if="products.length === 0" class="text-center pa-4">
      <p class="text-h6 text-medium-emphasis">Товары не найдены</p>
      <BaseButton
        v-if="isSeller"
        color="primary"
        variant="elevated"
        class="mt-4"
        @click="$emit('add')"
      >
        Добавить товар
      </BaseButton>
    </div>

    <v-row v-else>
      <v-col
        v-for="product in products"
        :key="product.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <ProductCard
          :product="product"
          :is-seller="isSeller"
          @add-to-cart="$emit('add-to-cart', product)"
          @edit="$emit('edit', product)"
        />
      </v-col>
    </v-row>

    <div v-if="showPagination" class="d-flex justify-center mt-4">
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        :total-visible="7"
        @update:model-value="$emit('page-change', currentPage)"
      ></v-pagination>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import ProductCard from './ProductCard.vue'
import BaseButton from '../common/BaseButton.vue'

const props = defineProps({
  products: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  isSeller: {
    type: Boolean,
    default: false
  },
  totalItems: {
    type: Number,
    default: 0
  },
  itemsPerPage: {
    type: Number,
    default: 12
  },
  currentPage: {
    type: Number,
    default: 1
  }
})

const emit = defineEmits(['add', 'edit', 'add-to-cart', 'page-change'])

const totalPages = computed(() => Math.ceil(props.totalItems / props.itemsPerPage))
const showPagination = computed(() => totalPages.value > 1)
</script>

<style scoped>
.product-list {
  min-height: 200px;
}
</style> 