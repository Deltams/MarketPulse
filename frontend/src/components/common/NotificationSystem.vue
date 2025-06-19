<template>
  <div class="notification-system">
    <v-snackbar
      v-for="notification in notificationStore.notifications"
      :key="notification.id"
      :model-value="true"
      :color="getColor(notification.type)"
      :timeout="notification.timeout"
      location="top right"
      @update:model-value="notificationStore.removeNotification(notification.id)"
    >
      <div class="d-flex align-center">
        <v-icon :icon="getIcon(notification.type)" class="mr-2"></v-icon>
        {{ notification.message }}
      </div>
      
      <template v-slot:actions>
        <v-btn
          icon
          variant="text"
          @click="notificationStore.removeNotification(notification.id)"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { useNotificationStore } from '@/stores/notificationStore'

const notificationStore = useNotificationStore()

const getColor = (type: string) => {
  const colors = {
    success: 'success',
    error: 'error',
    warning: 'warning',
    info: 'info'
  }
  return colors[type as keyof typeof colors] || 'info'
}

const getIcon = (type: string) => {
  const icons = {
    success: 'mdi-check-circle',
    error: 'mdi-alert-circle',
    warning: 'mdi-alert',
    info: 'mdi-information'
  }
  return icons[type as keyof typeof icons] || 'mdi-information'
}
</script>

<style scoped>
.notification-system {
  position: fixed;
  top: 0;
  right: 0;
  z-index: 9999;
}
</style> 