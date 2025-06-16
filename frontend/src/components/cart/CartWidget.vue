<template>
  <v-menu
    v-model="isOpen"
    :close-on-content-click="false"
    location="bottom end"
    transition="scale-transition"
  >
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
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

    <v-card min-width="320" max-width="400">
      <v-card-title class="d-flex justify-space-between align-center">
        Корзина
        <v-btn
          icon
          variant="text"
          @click="isOpen = false"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text class="pa-0">
        <v-list v-if="cartStore.items.length > 0" class="cart-items">
          <v-list-item
            v-for="item in cartStore.items"
            :key="item.productId"
            class="cart-item"
          >
            <template v-slot:prepend>
              <v-img
                :src="item.imageUrl || '/placeholder.png'"
                :alt="item.name"
                width="60"
                height="60"
                cover
                class="rounded"
              ></v-img>
            </template>

            <v-list-item-title>{{ item.name }}</v-list-item-title>
            <v-list-item-subtitle>
              {{ formatPrice(item.price) }} × {{ item.quantity }}
            </v-list-item-subtitle>

            <template v-slot:append>
              <v-btn
                icon
                variant="text"
                color="error"
                size="small"
                @click="cartStore.removeFromCart(item.productId)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-list-item>
        </v-list>

        <v-card-text v-else class="text-center py-4">
          Корзина пуста
        </v-card-text>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions v-if="cartStore.items.length > 0" class="pa-4">
        <div class="d-flex justify-space-between align-center w-100">
          <div class="text-h6">
            Итого: {{ formatPrice(cartStore.totalPrice) }}
          </div>
          <v-btn
            color="primary"
            to="/cart"
            @click="isOpen = false"
          >
            Перейти в корзину
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
  </v-menu>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useCartStore } from '@/stores/cartStore'

const cartStore = useCartStore()
const isOpen = ref(false)

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}
</script>

<style scoped>
.cart-items {
  max-height: 400px;
  overflow-y: auto;
}

.cart-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.cart-item:last-child {
  border-bottom: none;
}
</style> 