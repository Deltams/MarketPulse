<template>
  <v-text-field
    v-model="inputValue"
    :label="label"
    :type="type"
    :rules="rules"
    :placeholder="placeholder"
    :disabled="disabled"
    :loading="loading"
    :readonly="readonly"
    :clearable="clearable"
    :prefix="prefix"
    :suffix="suffix"
    :prepend-icon="prependIcon"
    :append-icon="appendIcon"
    :hint="hint"
    :persistent-hint="persistentHint"
    :error-messages="errorMessages"
    :density="density"
    :variant="variant"
    :color="color"
    :bg-color="bgColor"
    :class="inputClass"
    @update:model-value="handleInput"
    @blur="handleBlur"
    @focus="handleFocus"
  ></v-text-field>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  rules: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  clearable: {
    type: Boolean,
    default: false
  },
  prefix: {
    type: String,
    default: ''
  },
  suffix: {
    type: String,
    default: ''
  },
  prependIcon: {
    type: String,
    default: ''
  },
  appendIcon: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  persistentHint: {
    type: Boolean,
    default: false
  },
  errorMessages: {
    type: [String, Array],
    default: ''
  },
  density: {
    type: String,
    default: 'default'
  },
  variant: {
    type: String,
    default: 'outlined'
  },
  color: {
    type: String,
    default: 'primary'
  },
  bgColor: {
    type: String,
    default: ''
  },
  inputClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

const inputValue = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleInput = (value: string | number) => {
  emit('update:modelValue', value)
}

const handleBlur = (event: FocusEvent) => {
  emit('blur', event)
}

const handleFocus = (event: FocusEvent) => {
  emit('focus', event)
}
</script> 