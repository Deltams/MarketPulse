<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Корзина</h1>
      </v-col>
    </v-row>

    <v-row v-if="cartStore.items.length === 0">
      <v-col cols="12" class="text-center">
        <v-card class="pa-6">
          <v-icon size="64" color="grey" class="mb-4">mdi-cart-off</v-icon>
          <h2 class="text-h5 mb-4">Корзина пуста</h2>
          <p class="text-body-1 mb-6">Добавьте товары или услуги в корзину, чтобы оформить заказ</p>
          <v-btn
            color="primary"
            to="/products"
            size="large"
            class="mr-4"
          >
            Перейти к товарам
          </v-btn>
          <v-btn
            color="secondary"
            to="/services"
            size="large"
          >
            Перейти к услугам
          </v-btn>
        </v-card>
      </v-col>
    </v-row>

    <template v-else>
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-list>
              <v-list-item
                v-for="item in cartStore.items"
                :key="`${item.type}-${item.productId || item.serviceId}`"
                class="cart-item"
              >
                <template v-slot:prepend>
                  <v-img
                    v-if="item.type === 'product' && (item.imageUrl || item.product_image)"
                    :src="item.imageUrl || item.product_image || '/placeholder.png'"
                    :alt="item.name"
                    width="100"
                    height="100"
                    cover
                    class="rounded"
                  ></v-img>
                  <div
                    v-else
                    class="service-placeholder rounded d-flex align-center justify-center"
                    style="width: 100px; height: 100px; background: #f5f5f5;"
                  >
                    <v-icon size="48" color="grey">mdi-cog</v-icon>
                  </div>
                </template>

                <v-list-item-title class="text-h6 mb-2">
                  {{ item.name }}
                  <v-chip
                    :color="item.type === 'product' ? 'primary' : 'secondary'"
                    size="small"
                    class="ml-2"
                  >
                    {{ item.type === 'product' ? 'Товар' : 'Услуга' }}
                  </v-chip>
                </v-list-item-title>

                <v-list-item-subtitle class="text-subtitle-1 mb-4">
                  {{ formatPrice(getItemPrice(item)) }}
                </v-list-item-subtitle>

                <template v-slot:append>
                  <div class="d-flex align-center">
                    <v-btn
                      icon
                      variant="text"
                      @click="updateQuantity(item, item.quantity - 1)"
                      :disabled="item.quantity <= 1"
                    >
                      <v-icon>mdi-minus</v-icon>
                    </v-btn>

                    <span class="mx-4 text-h6">{{ item.quantity }}</span>

                    <v-btn
                      icon
                      variant="text"
                      @click="updateQuantity(item, item.quantity + 1)"
                    >
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>

                    <v-btn
                      icon
                      variant="text"
                      color="error"
                      class="ml-4"
                      @click="removeFromCart(item)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </div>
                </template>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="12" md="4">
          <v-card class="sticky-card">
            <v-card-title class="text-h5">
              Итого
            </v-card-title>

            <v-card-text>
              <div class="d-flex justify-space-between mb-2">
                <span>Товары и услуги ({{ cartStore.totalItems }})</span>
                <span>{{ formatPrice(cartStore.totalPrice) }}</span>
              </div>
              <v-divider class="my-4"></v-divider>
              <div class="d-flex justify-space-between text-h6">
                <span>К оплате</span>
                <span>{{ formatPrice(cartStore.totalPrice) }}</span>
              </div>
            </v-card-text>

            <v-card-actions>
              <v-btn
                block
                color="primary"
                size="large"
                @click="checkout"
              >
                Оформить заказ
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script setup lang="ts">
import { useCartStore } from '@/stores/cartStore'

const cartStore = useCartStore()

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB'
  }).format(price)
}

const getItemPrice = (item: any) => {
  if (item.type === 'product') {
    return item.product_price || item.price
  } else {
    return item.service_price || item.price
  }
}

const updateQuantity = (item: any, quantity: number) => {
  if (quantity > 0) {
    const itemId = item.type === 'product' ? item.productId : item.serviceId
    cartStore.updateQuantity(itemId, quantity, item.type)
  }
}

const removeFromCart = (item: any) => {
  const itemId = item.type === 'product' ? item.productId : item.serviceId
  cartStore.removeFromCart(itemId, item.type)
}

const checkout = () => {
  // TODO: Implement checkout logic
  console.log('Checkout clicked')
}
</script>

<style scoped>
.cart-item {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.cart-item:last-child {
  border-bottom: none;
}

.sticky-card {
  position: sticky;
  top: 20px;
}
</style> 