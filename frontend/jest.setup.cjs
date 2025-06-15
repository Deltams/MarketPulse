const { config } = require('@vue/test-utils')
const { createApp } = require('vue')

// Configure global test options
config.global = {
  ...config.global,
  stubs: {
    RouterLink: true
  },
  mocks: {
    $route: {
      params: {}
    },
    $router: {
      push: jest.fn()
    }
  }
}

// Add global variables
global.Vue = { createApp } 