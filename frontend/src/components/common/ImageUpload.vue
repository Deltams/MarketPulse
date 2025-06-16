<template>
  <div class="image-upload">
    <v-file-input
      v-model="file"
      :label="label"
      accept="image/*"
      :rules="[
        v => !v || v.size < 5000000 || 'Размер изображения должен быть меньше 5MB',
        v => !v || v.type.startsWith('image/') || 'Файл должен быть изображением'
      ]"
      :prepend-icon="prependIcon"
      :show-size="showSize"
      :disabled="disabled"
      :loading="loading"
      @update:model-value="handleFileChange"
    ></v-file-input>

    <v-img
      v-if="previewUrl"
      :src="previewUrl"
      :max-width="maxWidth"
      :max-height="maxHeight"
      :aspect-ratio="aspectRatio"
      class="mt-4 rounded"
      :cover="cover"
    ></v-img>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: File,
    default: null
  },
  label: {
    type: String,
    default: 'Изображение'
  },
  prependIcon: {
    type: String,
    default: 'mdi-camera'
  },
  showSize: {
    type: Boolean,
    default: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  maxWidth: {
    type: [Number, String],
    default: 200
  },
  maxHeight: {
    type: [Number, String],
    default: 200
  },
  aspectRatio: {
    type: [Number, String],
    default: 1
  },
  cover: {
    type: Boolean,
    default: true
  },
  previewUrl: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const file = ref<File | null>(null)
const previewUrl = ref<string>('')

watch(() => props.modelValue, (newValue) => {
  file.value = newValue
  if (newValue) {
    previewUrl.value = URL.createObjectURL(newValue)
  } else {
    previewUrl.value = ''
  }
})

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const newFile = target.files[0]
    file.value = newFile
    previewUrl.value = URL.createObjectURL(newFile)
    emit('update:modelValue', newFile)
    emit('change', newFile)
  } else {
    file.value = null
    previewUrl.value = ''
    emit('update:modelValue', null)
    emit('change', null)
  }
}
</script>

<style scoped>
.image-upload {
  width: 100%;
}
</style> 