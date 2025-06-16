<template>
  <div class="home">
    <!-- Hero Section -->
    <v-parallax
      src="https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?ixlib=rb-4.0.3"
      height="600"
      class="hero-section"
    >
      <div class="hero-content">
        <h1 class="text-h2 font-weight-bold text-white mb-4">
          Добро пожаловать в MarketPulse
        </h1>
        <p class="text-h5 text-white mb-6">
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
    <v-container fluid class="py-12 bg-grey-lighten-4">
      <v-container>
        <h2 class="text-h4 font-weight-bold text-center mb-8">
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
    <v-container fluid class="py-12">
      <v-container>
        <h2 class="text-h4 font-weight-bold text-center mb-8">
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
    <v-container fluid class="py-12 bg-grey-lighten-4">
      <v-container>
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

.hero-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  width: 100%;
  padding: 0 20px;
}

.text-shadow {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.category-card,
.product-card {
  transition: transform 0.3s ease;
}

.category-card:hover,
.product-card:hover {
  transform: translateY(-5px);
}

.feature-card {
  height: 100%;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}
</style> 