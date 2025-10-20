/**
 * Configuration globale des tests Vitest
 */
import { beforeAll, afterEach } from 'vitest'
import { cleanup } from '@vue/test-utils'

// Cleanup après chaque test
afterEach(() => {
  cleanup()
})

// Setup global
beforeAll(() => {
  // Mock localStorage
  global.localStorage = {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn()
  } as any
})

