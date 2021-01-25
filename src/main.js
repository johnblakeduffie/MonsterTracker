import Vue from 'vue'
import App from './App.vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'




Vue.config.productionTip = false
Vue.use(Vuetify)


new Vue({
  vuetify: new Vuetify({
      theme: {
        dark: true
      }
  }),
  data: {
  },
  computed: {
  },
  render: h => h(App)
}).$mount('#app')

export const bus = new Vue();