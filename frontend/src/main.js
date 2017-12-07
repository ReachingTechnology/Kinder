/**
 * Created by HOZ on 24/08/2017.
 */

import 'babel-polyfill'
import Vue from 'vue'
import App from './App.vue'
import Vuex from 'vuex'
// import VueRouter from 'vue-router'
import router from './router'
import store from './store/store'
import Element from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import MuseUI from 'muse-ui'
import 'mint-ui/lib/style.css'
import 'muse-ui/dist/muse-ui.css'
import 'muse-ui/dist/theme-light.css'
import BaiduMap from 'vue-baidu-map'
import Moment from 'vue-moment'

Vue.use(Element)
// Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(MuseUI)
Vue.use(BaiduMap, {
  ak: 'YS2Sf5srZfCl9sItzAnu6lNABhYB4rUU'
})
Vue.use(Moment)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  store,
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
