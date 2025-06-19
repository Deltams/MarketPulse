<template>
  <div class="brand-catalog-grid">
    <ProductFilter
      :initialBrandId="brandId"
      :hideBrandSelect="true"
      :categories="categories"
      :filters="filters"
      @filter-change="onFilterChange"
      @price-slider-start="onPriceSliderStart"
      @price-slider-end="onPriceSliderEnd"
    />
    <div v-if="products.length">
      <h2 class="section-title">Товары бренда</h2>
      <v-row>
        <v-col v-for="product in products" :key="product.id" cols="12" sm="6" md="4" lg="3">
          <ProductCard :product="product" />
        </v-col>
      </v-row>
    </div>
    <v-divider class="my-8" v-if="products.length && services.length" />
    <div v-if="services.length">
      <h2 class="section-title">Услуги бренда</h2>
      <v-row>
        <v-col v-for="service in services" :key="service.id" cols="12" sm="6" md="4" lg="3">
          <ServiceCard :service="service" />
        </v-col>
      </v-row>
    </div>
    <div v-if="!products.length && !services.length" class="empty-block">
      Нет товаров или услуг для этого бренда.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import ProductCard from '@/components/products/ProductCard.vue'
import ServiceCard from '@/components/services/ServiceCard.vue'
import ProductFilter from '@/components/products/ProductFilter.vue'
import api from '@/api/config'

interface Product {
  id: number;
  name?: string;
  description?: string;
  price?: number;
  category?: number;
  seller?: number;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
  [key: string]: any;
}

interface Service {
  id: number;
  name?: string;
  description?: string;
  price?: number;
  category?: number;
  seller?: number;
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
  [key: string]: any;
}

const props = defineProps({
  brandId: {
    type: Number,
    required: true
  }
})

const products = ref<Product[]>([])
const services = ref<Service[]>([])
const allCategories = ref<any[]>([])
const categories = ref<any[]>([])
const filters = ref({
  search: '',
  category: null,
  priceSort: null,
  priceRange: [0, 999999],
  brand: props.brandId
})

const fetchCategories = async () => {
  const res = await api.get('/categories/')
  allCategories.value = res.data
  categories.value = res.data
}

const fetchProducts = async () => {
  const params = {
    ...filters.value,
    brand: props.brandId
  }
  const res = await api.get('/productlist/', { params })
  products.value = Array.isArray(res.data) ? res.data : res.data.results || []
}

const fetchServices = async () => {
  const params = {
    ...filters.value,
    brand: props.brandId
  }
  const res = await api.get('/servicelist/', { params })
  services.value = Array.isArray(res.data) ? res.data : res.data.results || []
}

const fetchAll = async () => {
  await Promise.all([fetchProducts(), fetchServices()])
  filterCategoriesByBrand()
}

const filterCategoriesByBrand = () => {
  const productCategoryIds = products.value.map(p => p.category).filter(Boolean)
  const serviceCategoryIds = services.value.map(s => s.category).filter(Boolean)
  const usedCategoryIds = Array.from(new Set([...productCategoryIds, ...serviceCategoryIds]))

  // Фильтруем по allCategories, чтобы не терять полный список
  categories.value = Array.isArray(allCategories.value)
    ? allCategories.value.filter((cat: any) => usedCategoryIds.includes(cat.id))
    : []
}

const onFilterChange = (newFilters: any) => {
  filters.value = { ...newFilters, brand: props.brandId }
  fetchAll()
}

const onPriceSliderStart = () => {}
const onPriceSliderEnd = () => {}

watch(() => props.brandId, () => {
  filters.value.brand = props.brandId
  fetchAll()
})

onMounted(() => {
  fetchCategories()
  fetchAll()
})
</script>

<style scoped>
.brand-catalog-grid {
  width: 100%;
}
.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 2rem 0 1rem 0;
  color: #1976d2;
}
.empty-block {
  text-align: center;
  color: #888;
  margin: 2rem 0;
}
</style> 