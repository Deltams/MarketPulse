import { mount } from '@vue/test-utils'
import BrandsView from '../views/BrandsView.vue'
import { nextTick } from 'vue'

jest.mock('../api/config', () => ({ get: jest.fn() }))
const api = require('../api/config')

describe('BrandsView.vue (integration)', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('shows loader while waiting for API, then renders brands', async () => {
    let resolveApi
    const apiPromise = new Promise(resolve => { resolveApi = resolve })
    api.get.mockImplementation(() => apiPromise)
    const wrapper = mount(BrandsView, { global: { stubs: { RouterLink: true } } })

    expect(wrapper.find('.loading').exists()).toBe(true)
    expect(wrapper.find('.brands-grid').exists()).toBe(false)

    const brands = [
      { id: 1, name: 'Nike', description: 'Shoes' },
      { id: 2, name: 'Adidas', description: 'Sport' }
    ]
    resolveApi({ data: brands })
    await nextTick(); await nextTick();

    expect(wrapper.find('.loading').exists()).toBe(false)
    const cards = wrapper.findAll('.brand-card')
    expect(cards).toHaveLength(2)
    expect(cards[0].text()).toContain('Nike')
    expect(cards[1].text()).toContain('Adidas')
  })

  it('shows error if API fails', async () => {
    let rejectApi
    const apiPromise = new Promise((_, reject) => { rejectApi = reject })
    api.get.mockImplementation(() => apiPromise)
    const wrapper = mount(BrandsView, { global: { stubs: { RouterLink: true } } })

    expect(wrapper.find('.loading').exists()).toBe(true)

    rejectApi(new Error('fail'))
    await nextTick(); await nextTick();

    expect(wrapper.find('.loading').exists()).toBe(false)
    expect(wrapper.find('.error').exists()).toBe(true)
    expect(wrapper.find('.error').text()).toContain('Failed to load brands')
  })

  it('renders correct router-link for each brand', async () => {
    api.get.mockResolvedValueOnce({ data: [
      { id: 42, name: 'TestBrand', description: 'Desc' }
    ] })
    const wrapper = mount(BrandsView, { global: { stubs: { RouterLink: true } } })
    await nextTick(); await nextTick();

    const link = wrapper.find('.brand-card .view-link')
    expect(link.exists()).toBe(true)
    expect(link.attributes('to')).toBe('/brands/42')
  })
}) 