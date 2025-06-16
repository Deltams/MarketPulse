<template>
  <BaseForm
    ref="form"
    :loading="loading"
    :submit-text="submitText"
    @submit="handleSubmit"
    @cancel="$emit('cancel')"
  >
    <BaseInput
      v-model="formData.name"
      label="Название товара"
      :rules="[v => !!v || 'Обязательное поле']"
      prepend-icon="mdi-tag"
    />

    <BaseInput
      v-model="formData.description"
      label="Описание"
      type="textarea"
      :rules="[v => !!v || 'Обязательное поле']"
      prepend-icon="mdi-text"
    />

    <BaseInput
      v-model.number="formData.price"
      label="Цена"
      type="number"
      :rules="[
        v => !!v || 'Обязательное поле',
        v => v > 0 || 'Цена должна быть больше 0'
      ]"
      prepend-icon="mdi-currency-rub"
    />

    <ImageUpload
      v-model="formData.image"
      label="Изображение товара"
      :max-width="300"
      :max-height="300"
      :aspect-ratio="16/9"
    />
  </BaseForm>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import BaseForm from '../common/BaseForm.vue'
import BaseInput from '../common/BaseInput.vue'
import ImageUpload from '../common/ImageUpload.vue'

const props = defineProps({
  product: {
    type: Object,
    default: () => ({
      name: '',
      description: '',
      price: 0,
      image: null
    })
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

const form = ref()
const formData = ref({ ...props.product })

const submitText = computed(() => props.product.id ? 'Сохранить' : 'Создать')

const handleSubmit = async () => {
  const { valid } = await form.value.validate()
  if (valid) {
    emit('submit', formData.value)
  }
}

const reset = () => {
  form.value?.reset()
  formData.value = { ...props.product }
}

defineExpose({
  reset
})
</script>

<style scoped>
.product-form {
  max-width: 600px;
  margin: 0 auto;
}
</style> 