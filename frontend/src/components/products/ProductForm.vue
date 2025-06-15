<template>
  <form @submit.prevent="handleSubmit" class="product-form">
    <div class="form-group">
      <label for="name">Название товара</label>
      <input
        id="name"
        v-model="formData.name"
        type="text"
        required
        class="form-input"
      >
    </div>

    <div class="form-group">
      <label for="description">Описание</label>
      <textarea
        id="description"
        v-model="formData.description"
        required
        class="form-input"
        rows="4"
      ></textarea>
    </div>

    <div class="form-group">
      <label for="price">Цена</label>
      <input
        id="price"
        v-model.number="formData.price"
        type="number"
        required
        min="0"
        step="0.01"
        class="form-input"
      >
    </div>

    <div class="form-group">
      <label for="image">Изображение</label>
      <input
        id="image"
        type="file"
        accept="image/*"
        @change="handleImageChange"
        class="form-input"
      >
      <div v-if="imagePreview" class="image-preview">
        <img :src="imagePreview" alt="Preview">
      </div>
    </div>

    <div class="form-actions">
      <button type="submit" class="submit-button">
        {{ isEditing ? 'Сохранить изменения' : 'Добавить товар' }}
      </button>
      <button type="button" @click="$emit('cancel')" class="cancel-button">
        Отмена
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Product {
  id: number
  name: string
  description: string
  price: number
  imageUrl?: string
}

interface FormData {
  name: string
  description: string
  price: number
  image?: File
}

const props = defineProps<{
  product?: Product
  isEditing?: boolean
}>()

const emit = defineEmits<{
  (e: 'submit', data: FormData): void
  (e: 'cancel'): void
}>()

const formData = ref<FormData>({
  name: '',
  description: '',
  price: 0
})

const imagePreview = ref<string | null>(null)

onMounted(() => {
  if (props.product) {
    formData.value = {
      name: props.product.name,
      description: props.product.description,
      price: props.product.price
    }
    if (props.product.imageUrl) {
      imagePreview.value = props.product.imageUrl
    }
  }
})

const handleImageChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    const file = input.files[0]
    formData.value.image = file
    
    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const handleSubmit = () => {
  emit('submit', formData.value)
}
</script>

<style scoped>
.product-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

.image-preview {
  margin-top: 10px;
  max-width: 200px;
}

.image-preview img {
  width: 100%;
  height: auto;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.submit-button,
.cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-button {
  background-color: #2ecc71;
  color: white;
}

.submit-button:hover {
  background-color: #27ae60;
}

.cancel-button {
  background-color: #e74c3c;
  color: white;
}

.cancel-button:hover {
  background-color: #c0392b;
}
</style> 