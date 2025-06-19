<template>
  <v-btn
    @click="handleCartClick"
    icon
    variant="text"
    color="white"
    class="cart-btn"
  >
    <v-badge
      :content="cartStore.totalItems"
      :model-value="cartStore.totalItems > 0"
      color="error"
      location="top end"
    >
      <v-icon>mdi-cart</v-icon>
    </v-badge>
    <span v-if="cartStore.totalItems > 0" class="ml-2 text-white">
      {{ formatPrice(cartStore.totalPrice) }}
    </span>
  </v-btn>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cartStore'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notificationStore'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const handleCartClick = () => {
  if (authStore.isAuthenticated) {
    router.push('/cart')
  } else {
    notificationStore.addNotification(
      'Для просмотра корзины необходимо войти в систему',
      'warning',
      5000
    )
  }
}
</script>

<style scoped>
.cart-btn {
  display: flex;
  align-items: center;
}
</style> 