// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    '@nuxt/ui'
  ],

  css: ['~/assets/css/main.css'],

  app: {
    head: {
      title: 'Git-Komet - Team Effectiveness Analysis',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Analyze team effectiveness through Git metrics' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000/api/v1'
    }
  },

  compatibilityDate: '2024-01-01'
})
