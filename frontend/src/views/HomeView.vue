<template>
  <div class="home">
    <!-- Hero Section -->
    <v-parallax
      src="https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?ixlib=rb-4.0.3"
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
            <v-card
              :to="'/category/' + category.id"
              class="category-card h-100"
              elevation="2"
              hover
            >
              <v-img
                :src="category.image"
                height="200"
                cover
                class="align-end"
              >
                <v-card-title class="text-white text-shadow">
                  {{ category.name }}
                </v-card-title>
              </v-img>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-container>

    <!-- Featured Products -->
    <v-container fluid class="py-12" v-if="featuredProducts.length > 0">
      <v-container class="transparent">
        <h2 class="text-h4 font-weight-bold text-center mb-8 text-shadow">
          Популярные товары
        </h2>
        <v-row>
          <v-col
            v-for="product in featuredProducts"
            :key="product.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card class="product-card h-100" elevation="2" hover>
              <v-img
                :src="product.image"
                height="200"
                cover
                class="align-end"
              >
                <v-card-title class="text-white text-shadow">
                  {{ product.name }}
                </v-card-title>
              </v-img>
              <v-card-text>
                <div class="text-h6 font-weight-bold mb-2">
                  {{ product.price }} ₽
                </div>
                <div class="text-body-2 text-grey">
                  {{ product.description }}
                </div>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  color="primary"
                  variant="tonal"
                  block
                  @click="addToCart(product)"
                >
                  В корзину
                </v-btn>
              </v-card-actions>
            </v-card>
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
import { ref, onMounted } from 'vue'
import { useCartStore } from '@/stores/cartStore'
import api from '@/api/config'

const cartStore = useCartStore()

const featuredCategories = ref([
  {
    id: 1,
    name: 'Электроника',
    image: 'https://images.unsplash.com/photo-1498049794561-7780e7231661?ixlib=rb-4.0.3'
  },
  {
    id: 2,
    name: 'Одежда',
    image: 'https://images.unsplash.com/photo-1445205170230-053b83016050?ixlib=rb-4.0.3'
  },
  {
    id: 3,
    name: 'Дом и сад',
    image: 'https://images.unsplash.com/photo-1484101403633-562f891dc89a?ixlib=rb-4.0.3'
  },
  {
    id: 4,
    name: 'Спорт',
    image: 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?ixlib=rb-4.0.3'
  }
])

const featuredProducts = ref([])

const fetchFeaturedProducts = async () => {
  try {
    const response = await api.get('/productlist/', { params: { featured: true } })
    featuredProducts.value = response.data.results || response.data
  } catch (error) {
    console.error('Error fetching featured products:', error)
  }
}

const addToCart = (product) => {
  cartStore.addItem(product)
}

onMounted(() => {
  fetchFeaturedProducts()
})
</script>

<style scoped>
.hero-section {
  position: relative;
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
}

.category-card:hover {
  transform: translateY(-4px);
}

.product-card {
  background: rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
  transition: transform 0.2s ease;
}

.product-card:hover {
  transform: translateY(-4px);
}

.feature-card {
  background: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(10px);
  transition: transform 0.2s ease;
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

.transparent {
  background: transparent !important;
}

.v-container {
  background: transparent !important;
}

.v-container--fluid {
  background: transparent !important;
}

.v-row {
  background: transparent !important;
}

.v-col {
  background: transparent !important;
}

.text-shadow {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  color: white;
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
</style> 