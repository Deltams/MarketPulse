<template>
  <v-form @submit.prevent="handleSubmit" class="product-form">
    <v-card>
      <v-card-title class="text-h5">
        {{ isEditing ? 'Редактирование товара' : 'Добавление товара' }}
      </v-card-title>

      <v-card-text>
        <v-text-field
          v-model="formData.name"
          label="Название товара"
          required
          variant="outlined"
          density="comfortable"
        ></v-text-field>

        <v-textarea
          v-model="formData.description"
          label="Описание"
          required
          variant="outlined"
          density="comfortable"
          rows="4"
          auto-grow
        ></v-textarea>

        <v-text-field
          v-model.number="formData.price"
          label="Цена"
          type="number"
          required
          min="0"
          step="0.01"
          variant="outlined"
          density="comfortable"
          prefix="₽"
        ></v-text-field>

        <v-file-input
          accept="image/*"
          label="Изображение"
          variant="outlined"
          density="comfortable"
          prepend-icon="mdi-camera"
          @change="handleImageUpload"
          :show-size="1000"
        ></v-file-input>

        <v-img
          v-if="imagePreview"
          :src="imagePreview"
          max-width="200"
          class="mx-auto mt-4 rounded"
          cover
        ></v-img>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="grey"
          variant="text"
          @click="$emit('cancel')"
        >
          Отмена
        </v-btn>
        <v-btn
          color="primary"
          type="submit"
          :loading="loading"
        >
          {{ isEditing ? 'Сохранить изменения' : 'Добавить товар' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

interface Product {
  id?: number
  name: string
  description: string
  price: number
  imageUrl?: string
}

const props = defineProps<{
  product?: Product
  isEditing?: boolean
}>()

const emit = defineEmits<{
  (e: 'submit', product: Product, imageFile?: File): void
  (e: 'cancel'): void
}>()

const formData = reactive<Product>({
  name: '',
  description: '',
  price: 0,
  imageUrl: ''
})

const imagePreview = ref<string | null>(null)
const imageFile = ref<File | null>(null)
const loading = ref(false)

onMounted(() => {
  if (props.product) {
    Object.assign(formData, props.product)
    if (props.product.imageUrl) {
      imagePreview.value = props.product.imageUrl
    }
  }
})

const handleImageUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    imageFile.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    await emit('submit', { ...formData }, imageFile.value || undefined)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.product-form {
  max-width: 600px;
  margin: 0 auto;
}
</style> 