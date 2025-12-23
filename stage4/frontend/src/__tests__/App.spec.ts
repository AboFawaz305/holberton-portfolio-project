import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

const mockResults = [
  {
    id: 'grp-test',
    name: 'Test Course',
    description: 'Testing course',
    keywords: ['test'],
  },
]

describe('App', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ results: mockResults }),
      } as Response),
    ))
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the search form', () => {
    const wrapper = mount(App)
    expect(wrapper.text()).toContain('Search Courses')
    expect(wrapper.find('input[type="search"]').exists()).toBe(true)
  })

  it('shows results after a successful search', async () => {
    const wrapper = mount(App)
    await wrapper.find('input[type="search"]').setValue('test')
    await wrapper.find('form').trigger('submit.prevent')
    await vi.nextTick()

    expect(wrapper.text()).toContain('Test Course')
  })
})
