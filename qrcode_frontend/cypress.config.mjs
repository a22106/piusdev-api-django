import { defineConfig } from 'cypress';

export default defineConfig({
  projectId: 'g6usah',
  e2e: {
    setupNodeEvents(on, config) {
      return config;
    },
    specPattern: 'cypress/e2e/**/*.{cy,spec}.{js,jsx,ts,tsx}',
    supportFile: false,
  },
});