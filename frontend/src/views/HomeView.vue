<template>
  <div class="home">
    <!-- Hero Section -->
    <div class="hero-skeleton-stack">
      <v-parallax
        :src="heroImg"
        height="600"
        class="hero-section"
      >
        <div class="overlay"></div>
        <div class="hero-content">
          <h1 class="text-h2 font-weight-bold mb-4 welcome-text">
            Добро пожаловать в MarketPulse
          </h1>
          <p class="text-h5 mb-6 welcome-subtitle">
            Ваш надежный партнер в мире качественных товаров и услуг
          </p>
          <v-btn
            to="/catalog"
            color="primary"
            size="x-large"
            class="rounded-pill"
            elevation="4"
          >
            Перейти в каталог
          </v-btn>
        </div>
      </v-parallax>
      <div v-if="showSkeletons" :class="['custom-hero-skeleton', { 'fade-out': skeletonsFadingOut }]">
        <div class="hero-skeleton-img"></div>
        <div class="hero-skeleton-content">
          <div class="hero-skeleton-title"></div>
          <div class="hero-skeleton-subtitle"></div>
          <div class="hero-skeleton-btn"></div>
        </div>
      </div>
    </div>

    <!-- Featured Categories -->
    <v-container fluid class="py-12">
      <v-container class="transparent">
        <h2 class="text-h4 font-weight-bold text-center mb-8 text-shadow">
          Популярные категории
        </h2>
        <v-row>
          <v-col
            v-for="category in featuredCategories"
            :key="category.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <div class="category-skeleton-stack">
              <CategoryCard :category="category" />
              <div v-if="showSkeletons" :class="['custom-category-skeleton', { 'fade-out': skeletonsFadingOut }]">
                <div class="category-skeleton-img"></div>
                <div class="category-skeleton-title"></div>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-container>

    <!-- Featured Products -->
    <v-container fluid class="py-12">
      <v-container class="transparent">
        <h2 class="text-h4 font-weight-bold text-center mb-8 text-shadow">
          Популярные товары
        </h2>
        <v-row>
          <v-col
            v-for="(product, idx) in getProductSlots"
            :key="product.id || 'skeleton-' + idx"
            cols="12"
            sm="6"
            md="4"
            lg="3"
            class="product-col-wrapper"
          >
            <div class="product-skeleton-stack">
              <ProductCard
                v-if="product.id"
                :product="product"
                @add-to-cart="addToCart"
              />
              <div
                v-if="showSkeletons"
                :class="['custom-skeleton-card', { 'fade-out': skeletonsFadingOut }]"
              >
                <div class="skeleton-img"></div>
                <div class="skeleton-content">
                  <div class="skeleton-brand"></div>
                  <div class="skeleton-price"></div>
                  <div class="skeleton-desc"></div>
                  <div class="skeleton-title"></div>
                </div>
                <div class="skeleton-actions">
                  <div class="skeleton-btn"></div>
                </div>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-container>

    <!-- Features Section -->
    <v-container fluid class="py-12">
      <v-container class="transparent">
        <v-row>
          <v-col cols="12" md="4">
            <v-card class="feature-card text-center pa-4" elevation="0">
              <v-icon size="64" color="primary" class="mb-4">
                mdi-truck-fast
              </v-icon>
              <h3 class="text-h5 font-weight-bold mb-2">Быстрая доставка</h3>
              <p class="text-body-1">
                Доставляем заказы в любую точку России в кратчайшие сроки
              </p>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="feature-card text-center pa-4" elevation="0">
              <v-icon size="64" color="primary" class="mb-4">
                mdi-shield-check
              </v-icon>
              <h3 class="text-h5 font-weight-bold mb-2">Гарантия качества</h3>
              <p class="text-body-1">
                Все товары проходят тщательную проверку перед отправкой
              </p>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card class="feature-card text-center pa-4" elevation="0">
              <v-icon size="64" color="primary" class="mb-4">
                mdi-headset
              </v-icon>
              <h3 class="text-h5 font-weight-bold mb-2">Поддержка 24/7</h3>
              <p class="text-body-1">
                Наша служба поддержки всегда готова помочь вам
              </p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useCartStore } from '@/stores/cartStore'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/config'
import ProductCard from '@/components/products/ProductCard.vue'
import CategoryCard from '@/components/products/CategoryCard.vue'

import heroImg from '@/assets/photo-hero.jfif'
import cat1 from '@/assets/photo-cat1.jfif'
import cat2 from '@/assets/photo-cat2.jfif'
import cat3 from '@/assets/photo-cat3.jfif'
import cat4 from '@/assets/photo-cat4.jfif'

const cartStore = useCartStore()
const authStore = useAuthStore()

const featuredCategories = ref([
  {
    id: 1,
    name: 'Электроника',
    image: cat1
  },
  {
    id: 2,
    name: 'Одежда',
    image: cat2
  },
  {
    id: 3,
    name: 'Дом и быт',
    image: cat3
  },
  {
    id: 4,
    name: 'Спорт и отдых',
    image: cat4
  },
])

const featuredProducts = ref([])
const isLoadingProducts = ref(true)

let dataLoaded = false
let timerDone = false

const showProducts = ref(false)
const skeletonsFadingOut = ref(false)
const showSkeletons = ref(true)

const getProductSlots = computed(() => {
  if (featuredProducts.value.length >= SKELETON_COUNT) {
    return featuredProducts.value.slice(0, SKELETON_COUNT)
  }
  return [
    ...featuredProducts.value,
    ...Array(SKELETON_COUNT - featuredProducts.value.length).fill({})
  ]
})

const finishSkeletons = () => {
  skeletonsFadingOut.value = true
  setTimeout(() => {
    showSkeletons.value = false
  }, 400) // 400ms = время transition
}

const fetchFeaturedProducts = async () => {
  try {
    const response = await api.get('/productlist/', { params: { featured: true } })
    console.log('Featured products response:', response.data)
    featuredProducts.value = response.data.results || response.data
    if (featuredProducts.value.length > 0) {
      console.log('First product image URL:', featuredProducts.value[0].image)
    }
    dataLoaded = true
    maybeShowProducts()
  } catch (error) {
    console.error('Error fetching featured products:', error)
    dataLoaded = true
    maybeShowProducts()
  }
}

function maybeShowProducts() {
  if (dataLoaded && timerDone) {
    isLoadingProducts.value = false
    showProducts.value = true
    finishSkeletons()
  }
}

const addToCart = (product) => {
  cartStore.addToCart({
    id: product.id,
    name: product.name,
    price: product.price,
    imageUrl: product.image,
    type: 'product'
  })
}

const SKELETON_COUNT = 4

onMounted(() => {
  fetchFeaturedProducts()
  setTimeout(() => {
    timerDone = true
    maybeShowProducts()
  }, 3000)
})
</script>

<style scoped>
.hero-section {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  margin: 24px 0 48px;
}

:deep(.v-application) {
  background: transparent !important;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 0 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.welcome-text {
  background: linear-gradient(45deg, #1867C0, #5CBBF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  margin-bottom: 16px;
}

.welcome-subtitle {
  background: linear-gradient(45deg, #1867C0, #5CBBF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  margin-bottom: 32px;
}

.category-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
  transition: transform 0.2s ease;
  border-radius: 16px;
  overflow: hidden;
}

.category-card:hover {
  transform: translateY(-4px);
}

.product-card {
  background: #fff !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  border-radius: 16px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  max-width: 320px;
  margin: 0 auto;
  will-change: transform;
}

.product-card .v-img {
  height: 220px !important;
  width: 100% !important;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
}

.product-card .v-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  background: #fff;
}

.product-card .v-card-text {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-card .brand {
  color: #6b7280;
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 8px;
  letter-spacing: 0.02em;
}

.product-card .price {
  color: #222;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: 0.01em;
}

.product-card .v-card-title {
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  padding: 16px;
  font-size: 1.1rem;
  line-height: 1.4;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0,0,0,0.25);
}

.product-card .v-card-actions {
  padding: 8px 16px 16px;
}

.product-card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 8px 24px rgba(0,0,0,0.14), 0 3px 8px rgba(0,0,0,0.10);
}

.feature-card {
  background: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(10px);
  transition: transform 0.2s ease;
  border-radius: 16px;
  overflow: hidden;
}

.feature-card h3 {
  background: linear-gradient(45deg, #1867C0, #5CBBF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.feature-card p {
  background: linear-gradient(45deg, #1867C0, #5CBBF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.feature-card:hover {
  transform: translateY(-4px);
}

.text-shadow {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.v-container.fluid {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  margin: 24px 0;
  padding: 32px 0 !important;
}

.v-container.transparent {
  max-width: 1400px;
  margin: 0 auto;
}

.text-h4 {
  margin-bottom: 32px !important;
  padding: 0 24px;
}

.catalog {
  min-height: 100%;
  width: 100vw;
  margin: 0;
  padding: 0;
  position: relative;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
}

.catalog-header {
  padding: 24px 0;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.catalog-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #1a1a1a;
  text-align: center;
}

.catalog-controls {
  display: flex;
  gap: 16px;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 800px;
}

.search-field {
  max-width: 400px;
  width: 100%;
}

.catalog-content {
  width: 100%;
  padding: 0;
  margin: 0;
}

.products-container {
  position: relative;
  min-height: 400px;
  width: 100%;
  padding: 0;
  box-sizing: border-box;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin: 0 auto;
  padding: 0 24px;
  width: 100%;
  min-height: 600px;
  max-width: 1400px;
}

.v-card-actions {
  padding: 8px 16px 16px;
}

.v-card-actions .v-btn {
  background: linear-gradient(45deg, #1867C0, #5CBBF6) !important;
  color: white !important;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.v-card-actions .v-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background: linear-gradient(45deg, #1565C0, #42A5F5) !important;
}

.product-skeleton-stack {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 380px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: stretch;
}
.custom-skeleton-card {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.10), 0 1.5px 4px rgba(0,0,0,0.08);
  width: 100%;
  height: 100%;
  max-width: none;
  margin: 0;
  background: #f3f6fa;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  opacity: 1;
  transition: opacity 0.5s;
}
.custom-skeleton-card.fade-out {
  opacity: 0;
}
.skeleton-img,
.skeleton-brand,
.skeleton-price,
.skeleton-desc,
.skeleton-title,
.skeleton-btn {
  background: linear-gradient(90deg, #e0e7ef 25%, #f3f6fa 50%, #e0e7ef 75%);
  background-size: 400px 100%;
  animation: skeleton-loading 3s infinite linear;
}
.skeleton-img {
  height: 220px;
  width: 100%;
}
.skeleton-content {
  flex: 1;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.skeleton-brand, .skeleton-price, .skeleton-desc, .skeleton-title {
  height: 18px;
  border-radius: 4px;
}
.skeleton-brand { width: 60%; }
.skeleton-price { width: 40%; height: 22px; }
.skeleton-desc { width: 100%; height: 16px; }
.skeleton-title { width: 90%; height: 20px; margin-top: 8px; }
.skeleton-actions {
  padding: 8px 16px 16px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
.skeleton-btn {
  height: 48px;
  border-radius: 8px;
  width: 100%;
}
@keyframes skeleton-loading {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}

.hero-skeleton-stack {
  position: relative;
}
.custom-hero-skeleton {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 600px;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f3f6fa;
  border-radius: 16px;
  opacity: 1;
  transition: opacity 0.5s;
  overflow: hidden;
}
.custom-hero-skeleton.fade-out {
  opacity: 0;
}
.hero-skeleton-img {
  width: 100%;
  height: 100%;
  min-height: 600px;
  background: linear-gradient(90deg, #e0e7ef 25%, #f3f6fa 50%, #e0e7ef 75%);
  background-size: 400px 100%;
  animation: skeleton-loading 3s infinite linear;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  border-radius: 16px;
  z-index: 1;
}
.hero-skeleton-content {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 120px;
}
.hero-skeleton-title {
  width: 60%;
  height: 48px;
  border-radius: 8px;
  margin-bottom: 24px;
  background: linear-gradient(90deg, #e0e7ef 25%, #f3f6fa 50%, #e0e7ef 75%);
  background-size: 400px 100%;
  animation: skeleton-loading 3s infinite linear;
}
.hero-skeleton-subtitle {
  width: 50%;
  height: 32px;
  border-radius: 8px;
  margin-bottom: 32px;
  background: linear-gradient(90deg, #e0e7ef 25%, #f3f6fa 50%, #e0e7ef 75%);
  background-size: 400px 100%;
  animation: skeleton-loading 3s infinite linear;
}
.hero-skeleton-btn {
  width: 220px;
  height: 56px;
  border-radius: 28px;
  background: linear-gradient(90deg, #e0e7ef 25%, #f3f6fa 50%, #e0e7ef 75%);
  background-size: 400px 100%;
  animation: skeleton-loading 3s infinite linear;
}

.category-skeleton-stack {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 260px;
}
.custom-category-skeleton {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2;
  border-radius: 16px;
  background: #f3f6fa;
  opacity: 1;
  transition: opacity 0.5s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-end;
}
.custom-category-skeleton.fade-out {
  opacity: 0;
}
.category-skeleton-img {
  width: 100%;
  height: 200px;
  border-radius: 16px 16px 0 0;
  background: linear-gradient(90deg, #e0e7ef 25%, #f3f6fa 50%, #e0e7ef 75%);
  background-size: 400px 100%;
  animation: skeleton-loading 3s infinite linear;
}
.category-skeleton-title {
  width: 70%;
  height: 28px;
  margin: 16px auto 24px auto;
  border-radius: 8px;
  background: linear-gradient(90deg, #e0e7ef 25%, #f3f6fa 50%, #e0e7ef 75%);
  background-size: 400px 100%;
  animation: skeleton-loading 3s infinite linear;
}
@keyframes skeleton-loading {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
</style> 