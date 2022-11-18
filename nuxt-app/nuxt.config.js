// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({

    app: {
      head: {
          charset: 'utf-16',
          viewport: 'width=500, initial-scale=1',
          title: 'Weather Records App',
          link: [
            { rel: "stylesheet", href: "https://use.typekit.net/smj0uzc.css" }
          ]
        },
    },

    css: ["@/assets/css/styles.css", '@mdi/font/css/materialdesignicons.min.css', 'vuetify/lib/styles/main.sass'],

    postcss: {
      plugins: {
        tailwindcss: {},
        autoprefixer: {},
      },
    },

    build: {
      transpile: ['vuetify'],
    },

    vite: {
      define: {
        'process.env.DEBUG': false,
      },
    },

    ssr: false,


})