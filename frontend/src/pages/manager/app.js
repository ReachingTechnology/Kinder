/**
 * Created by HOZ on 24/08/2017.
 */

import Vue from 'vue'
import App from './manager_home.vue'
import Vuex from 'vuex'
// import VueRouter from 'vue-router'
import router from '../../router'
import store from '../../store/store'
import Element from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import MintUI from 'mint-ui'
import 'mint-ui/lib/style.css'

Vue.use(Element)
// Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(MintUI)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  store,
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
