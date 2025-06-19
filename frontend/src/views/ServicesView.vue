<template>
  <div class="services-page">
    <div class="container">
      <h1>Услуги</h1>
      
      <div v-if="loading" class="loading">
        <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        <div class="loading-text">Загрузка...</div>
      </div>
      
      <div v-else-if="error" class="error">
        <v-alert type="error" variant="tonal">
          {{ error }}
        </v-alert>
      </div>
      
      <div v-else>
        <!-- Результаты -->
        <div class="results-info">
          <v-chip color="primary" variant="tonal">
            Найдено: {{ services.length }} услуг
          </v-chip>
        </div>
        
        <!-- Сетка услуг -->
        <div class="services-grid">
          <ServiceCard
            v-for="service in services"
            :key="service.id"
            :service="service"
          />
        </div>
        
        <!-- Сообщение если ничего не найдено -->
        <div v-if="services.length === 0" class="no-results">
          <v-card class="no-results-card" variant="tonal">
            <v-card-text class="text-center">
              <v-icon size="64" color="grey" class="mb-4">mdi-handshake</v-icon>
              <h3>Услуги не найдены</h3>
              <p>Попробуйте изменить параметры поиска</p>
            </v-card-text>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useServiceStore } from '@/stores/serviceStore'
import ServiceCard from '@/components/services/ServiceCard.vue'

const serviceStore = useServiceStore()

const services = computed(() => serviceStore.services)
const loading = computed(() => serviceStore.loading)
const error = computed(() => serviceStore.error)

onMounted(async () => {
  try {
    await serviceStore.fetchServices()
  } catch (err) {
    console.error('Error fetching services:', err)
  }
})
</script>

<style scoped>
.services-page {
  padding: 2rem 0;
  background: #f5f5f5;
  min-height: 100vh;
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

.results-info {
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 4rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.loading-text {
  color: #666;
  font-size: 1.1rem;
}

.error {
  margin: 2rem 0;
}

.no-results {
  margin: 2rem 0;
}

.no-results-card {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

.no-results-card h3 {
  margin-bottom: 1rem;
  color: #333;
}

.no-results-card p {
  color: #666;
}

@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
  }
  
  .container {
    padding: 0 0.5rem;
  }
}
</style> 