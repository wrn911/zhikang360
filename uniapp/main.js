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
import GlobalMusicBall from '@/components/GlobalMusicBall.vue'

// ✅ 创建一个用于承载全局组件的容器 div（兼容 H5）
const container = document.createElement('div')
container.id = 'global-music-ball'
document.body.appendChild(container)

// ✅ 创建 Vue 实例，挂载到容器上
const GlobalBall = Vue.extend(GlobalMusicBall)
const ballInstance = new GlobalBall()
ballInstance.$mount('#global-music-ball')  // 推荐：避免破坏 Vue 根节点
// 此处的 GlobalMusicBall.vue 不再破坏页面树

// ✅ 提供全局控制方法
Vue.prototype.$global = {
  startMusicTimer(userId) {
    ballInstance.start(userId)
  },
  stopMusicTimer(msg = '已取消') {
    ballInstance.stop(msg)
  }
}






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