<template>
  <v-form
    ref="form"
    v-model="isValid"
    :class="formClass"
    @submit.prevent="handleSubmit"
  >
    <slot></slot>

    <div v-if="showActions" class="form-actions">
      <BaseButton
        v-if="showCancel"
        :color="cancelColor"
        :variant="cancelVariant"
        :size="buttonSize"
        :disabled="loading"
        @click="handleCancel"
      >
        {{ cancelText }}
      </BaseButton>

      <BaseButton
        type="submit"
        :color="submitColor"
        :variant="submitVariant"
        :size="buttonSize"
        :loading="loading"
        :disabled="!isValid || loading"
      >
        {{ submitText }}
      </BaseButton>
    </div>
  </v-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from './BaseButton.vue'

const props = defineProps({
  formClass: {
    type: String,
    default: ''
  },
  showActions: {
    type: Boolean,
    default: true
  },
  showCancel: {
    type: Boolean,
    default: true
  },
  submitText: {
    type: String,
    default: 'Сохранить'
  },
  cancelText: {
    type: String,
    default: 'Отмена'
  },
  submitColor: {
    type: String,
    default: 'primary'
  },
  cancelColor: {
    type: String,
    default: 'secondary'
  },
  submitVariant: {
    type: String,
    default: 'elevated'
  },
  cancelVariant: {
    type: String,
    default: 'text'
  },
  buttonSize: {
    type: String,
    default: 'default'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

const form = ref()
const isValid = ref(false)

const handleSubmit = () => {
  if (isValid.value) {
    emit('submit')
  }
}

const handleCancel = () => {
  emit('cancel')
}

const reset = () => {
  form.value?.reset()
}

const resetValidation = () => {
  form.value?.resetValidation()
}

defineExpose({
  reset,
  resetValidation
})
</script>

<style scoped>
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}
</style> 