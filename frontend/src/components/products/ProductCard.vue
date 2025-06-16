<template>
  <v-card
    class="product-card"
    :elevation="2"
    :hover="true"
  >
    <v-img
      :src="product.image || '/placeholder.png'"
      :aspect-ratio="16/9"
      cover
      class="product-image"
    >
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-row>
      </template>
    </v-img>

    <v-card-title class="text-truncate">{{ product.name }}</v-card-title>
    
    <v-card-text>
      <div class="text-truncate mb-2">{{ product.description }}</div>
      <div class="text-h6 font-weight-bold">
        {{ formatPrice(product.price) }} ₽
      </div>
    </v-card-text>

    <v-card-actions>
      <BaseButton
        color="primary"
        variant="elevated"
        size="small"
        @click="$emit('add-to-cart', product)"
      >
        В корзину
      </BaseButton>

      <BaseButton
        v-if="isSeller"
        color="secondary"
        variant="text"
        size="small"
        @click="$emit('edit', product)"
      >
        Редактировать
      </BaseButton>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseButton from '../common/BaseButton.vue'

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  isSeller: {
    type: Boolean,
    default: false
  }
})

defineEmits(['add-to-cart', 'edit'])

const formatPrice = (price: number) => {
  return new Intl.NumberFormat('ru-RU').format(price)
}
</script>

<style scoped>
.product-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.product-image {
  position: relative;
}

.product-image::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50%;
  background: linear-gradient(to top, rgba(0,0,0,0.3), transparent);
  pointer-events: none;
}

.v-card-title {
  font-size: 1.1rem;
  line-height: 1.4;
  padding: 12px 16px 4px;
}

.v-card-text {
  padding: 0 16px 16px;
  flex-grow: 1;
}

.v-card-actions {
  padding: 8px 16px 16px;
  gap: 8px;
}
</style> 