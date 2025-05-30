import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
  state: () => ({
    carts: {} as Record<number, { items: any[]; total: number }>,
  }),
  actions: {
    addItem(product) {
      const sellerId = product.seller.id;
      if (!this.carts[sellerId]) {
        this.carts[sellerId] = { items: [], total: 0 };
      }
      const existingItem = this.carts[sellerId].items.find((i) => i.id === product.id);
      if (existingItem) {
        existingItem.quantity = (existingItem.quantity || 1) + 1;
      } else {
        this.carts[sellerId].items.push({ ...product, quantity: 1 });
      }
      this.carts[sellerId].total += product.price;
    },
    removeItem(sellerId, productId) {
      const item = this.carts[sellerId].items.find((i) => i.id === productId);
      if (item) {
        this.carts[sellerId].total -= item.price * item.quantity;
        this.carts[sellerId].items = this.carts[sellerId].items.filter((i) => i.id !== productId);
        if (this.carts[sellerId].items.length === 0) {
          delete this.carts[sellerId];
        }
      }
    },
    updateQuantity(sellerId, productId, quantity) {
      const item = this.carts[sellerId].items.find((i) => i.id === productId);
      if (item && quantity > 0) {
        this.carts[sellerId].total += (quantity - item.quantity) * item.price;
        item.quantity = quantity;
      }
    },
  },
}); 