import App from './App'

// #ifndef VUE3
import Vue from 'vue'
import uView from './uni_modules/uview-ui'
Vue.use(uView)
import './uni.promisify.adaptor'
import '@/static/css/global.css'
import { uCharts } from '@qiun/ucharts'
import request from '@/utils/request.js'
import apiConfig from '@/config.js'
const baseUrl = process.env.NODE_ENV === "development" ? apiConfig.dev.baseUrl : apiConfig.prod.baseUrl

Vue.config.productionTip = false
Vue.prototype.$request = request
Vue.prototype.$baseUrl = baseUrl
// 全局注册组件
//Vue.component('qiun-data-charts', uCharts)

App.mpType = 'app'
const app = new Vue({
  ...App
})
app.$mount()
// #endif

// #ifdef VUE3
import { createSSRApp } from 'vue'
export function createApp() {
  const app = createSSRApp(App)
  return {
    app
  }
}
// #endif