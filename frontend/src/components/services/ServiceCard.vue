<template>
  <v-tooltip location="top" :text="service.description" open-delay="200">
    <template #activator="{ props }">
      <v-card
        class="service-card h-100 d-flex flex-column"
        elevation="2"
        hover
        :to="`/services/${service.id}`"
        v-bind="props"
      >
        <v-card-text class="flex-grow-1">
          <div class="service-type">
            <v-chip
              color="secondary"
              size="small"
              class="mb-2"
            >
              Услуга
            </v-chip>
          </div>
          <div class="brand">
            Бренд: {{ getBrandName() }}
            <v-tooltip v-if="isBrandVerified()" location="top">
              <template #activator="{ props }">
                <v-icon
                  v-bind="props"
                  class="verified-icon"
                  color="#9c27b0"
                  size="18"
                  style="margin-left: 4px; vertical-align: middle; cursor: pointer;"
                >
                  mdi-shield-check
                </v-icon>
              </template>
              <span>Проверенный бренд</span>
            </v-tooltip>
          </div>
          <div class="price">
            {{ formatPrice(service.price) }}
          </div>
          <div class="service-title">
            {{ service.name }}
          </div>
          <div class="text-body-2 text-grey description">
            {{ service.description }}
          </div>
        </v-card-text>
        <v-card-actions class="mt-auto">
          <v-btn
            class="add-to-cart-btn"
            block
            @click.stop="handleAddToCart"
          >
            Заказать
          </v-btn>
          <v-btn
            v-if="isSeller"
            color="secondary"
            variant="text"
            @click.stop="$emit('edit', service)"
          >
            Редактировать
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </v-tooltip>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cartStore'
import { useNotificationStore } from '@/stores/notificationStore'

interface Service {
  id: number
  name: string
  description: string
  price: number
  category: number
  seller: number
  is_active: boolean
  created_at: string
  updated_at: string
  brand_name?: string
  brand_is_verified?: boolean
}

interface Props {
  service: Service
}

const props = defineProps<Props>()
const emit = defineEmits<{
  edit: [service: Service]
}>()

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()
const notificationStore = useNotificationStore()

const isSeller = computed(() => authStore.isAuthenticated && authStore.user?.role === 'seller')

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const handleAddToCart = () => {
  if (!authStore.isAuthenticated) {
    notificationStore.addNotification(
      'Для добавления услуг в корзину необходимо войти в систему',
      'warning',
      5000
    )
    return
  }

  cartStore.addToCart({
    id: props.service.id,
    name: props.service.name,
    price: props.service.price,
    type: 'service'
  })

  notificationStore.addNotification(
    `Услуга "${props.service.name}" добавлена в корзину`,
    'success',
    3000
  )
}

const getBrandName = () => {
  if (props.service.brand_name) {
    return props.service.brand_name
  }
  return 'Без бренда'
}

const isBrandVerified = () => {
  return props.service.brand_is_verified || false
}
</script>

<style scoped>
.service-card {
  background: #fff !important;
  transition: transform 0.2s ease-in-out;
  border-radius: 12px;
  overflow: hidden;
  min-height: 280px;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.service-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: #2c3e50;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 2.6em;
  min-height: unset;
}

.price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #e74c3c;
  margin-bottom: 12px;
}

.service-type {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 8px;
}

.description {
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  max-height: 4.2em;
  min-height: unset;
}

.add-to-cart-btn {
  background: linear-gradient(45deg, #9c27b0, #673ab7);
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.add-to-cart-btn:hover {
  background: linear-gradient(45deg, #7b1fa2, #5e35b1);
  transform: translateY(-1px);
}

.v-card-text {
  padding: 1rem;
  display: flex;
  flex-direction: column;
}

.v-card-actions {
  padding: 0 1rem 1rem;
  margin-top: auto;
}

.brand {
  color: #6b7280;
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 6px;
  letter-spacing: 0.02em;
  display: flex;
  align-items: center;
  gap: 4px;
  justify-content: center;
  text-align: center;
}

.verified-icon {
  margin-left: 4px;
  vertical-align: middle;
  cursor: pointer;
  transition: color 0.2s;
}

.verified-icon:hover {
  color: #7b1fa2;
}
</style> 