import { defineStore } from 'pinia'
import { ref } from 'vue'

interface Notification {
  id: number
  message: string
  type: 'success' | 'error' | 'warning' | 'info'
  timeout?: number
}

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([])
  let nextId = 1

  const addNotification = (message: string, type: Notification['type'] = 'info', timeout: number = 4000) => {
    const notification: Notification = {
      id: nextId++,
      message,
      type,
      timeout
    }
    
    notifications.value.push(notification)
    
    if (timeout > 0) {
      setTimeout(() => {
        removeNotification(notification.id)
      }, timeout)
    }
  }

  const removeNotification = (id: number) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const clearAll = () => {
    notifications.value = []
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    clearAll
  }
}) 