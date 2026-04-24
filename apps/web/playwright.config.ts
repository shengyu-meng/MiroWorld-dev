import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './src/test/e2e',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    trace: 'retain-on-failure',
  },
  webServer: [
    {
      command: 'python -m uvicorn --app-dir apps/api/src main:app --host 127.0.0.1 --port 8000',
      port: 8000,
      cwd: '../../',
      reuseExistingServer: !process.env.CI,
      timeout: 120000,
    },
    {
      command: 'npm run dev',
      port: 4173,
      cwd: '.',
      reuseExistingServer: !process.env.CI,
      timeout: 120000,
    },
  ],
})
