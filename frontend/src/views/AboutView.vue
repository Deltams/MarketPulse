<template>
  <div class="about-container">
    <v-card class="about-card">
      <v-card-title class="text-h4 text-center mb-6 about-title">
        О MarketPulse
      </v-card-title>
      
      <v-card-text class="content">
        <p class="text-body-1 mb-4 main-text">
          Добро пожаловать в MarketPulse - вашу платформу для удобной торговли и покупок.
        </p>
        
        <p class="text-body-1 mb-4 main-text">
          Мы предоставляем продавцам инструменты для управления товарами и заказами, а покупателям - удобный поиск и оформление покупок.
        </p>
        
        <p class="text-body-1 mb-4 main-text">
          Наша цель - создать эффективную и прозрачную систему взаимодействия между продавцами и покупателями с полным контролем над процессом продаж.
        </p>
        
        <v-divider class="my-6"></v-divider>
        
        <div class="features">
          <h3 class="text-h5 mb-4">Наши преимущества:</h3>
          <v-row>
            <v-col cols="12" md="4">
              <div class="feature-item text-center">
                <v-icon size="48" color="primary" class="mb-3">mdi-store</v-icon>
                <h4 class="text-h6 mb-2">Удобная торговля</h4>
                <p class="text-body-2">Простое управление товарами и заказами для продавцов</p>
              </div>
            </v-col>
            <v-col cols="12" md="4">
              <div class="feature-item text-center">
                <v-icon size="48" color="primary" class="mb-3">mdi-magnify</v-icon>
                <h4 class="text-h6 mb-2">Быстрый поиск</h4>
                <p class="text-body-2">Удобный поиск и фильтрация товаров для покупателей</p>
              </div>
            </v-col>
            <v-col cols="12" md="4">
              <div class="feature-item text-center">
                <v-icon size="48" color="primary" class="mb-3">mdi-shield-check</v-icon>
                <h4 class="text-h6 mb-2">Безопасность</h4>
                <p class="text-body-2">Надежная система защиты данных и транзакций</p>
              </div>
            </v-col>
          </v-row>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
// Component logic can be added here
</script>

<style scoped>
.about-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.about-card {
  background: white !important;
  border: 2px solid #1976d2 !important;
  border-radius: 16px !important;
  box-shadow: 0 8px 32px rgba(25, 118, 210, 0.1) !important;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.about-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 48px rgba(25, 118, 210, 0.15) !important;
}

.about-title {
  color: #1976d2 !important;
  font-weight: 600 !important;
}

.content {
  line-height: 1.6;
  color: #2c3e50 !important;
}

.main-text {
  font-size: 1.1rem !important;
  line-height: 1.7 !important;
}

.feature-item {
  padding: 1rem;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.feature-item:hover {
  background-color: rgba(25, 118, 210, 0.05);
}

.feature-item h4 {
  color: #34495e !important;
}

.feature-item p {
  color: #7f8c8d !important;
}

@media (max-width: 768px) {
  .about-container {
    padding: 1rem;
  }
  
  .about-card {
    margin: 0 0.5rem;
  }
}
</style>