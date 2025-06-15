<template>
  <view v-if="show" class="ball-wrapper" @click="showInfo = !showInfo">
    <view class="ball">
      <view class="liquid" :style="{ height: liquidHeight + '%' }"></view>
      <view class="text">{{ countdown }}s</view>
    </view>
    <view v-if="showInfo" class="info-box">
      <text>预计总生成时间：5分钟</text>
      <text>剩余时间：{{ countdown }} 秒</text>
    </view>
  </view>
</template>


<script>
export default {
  data() {
    return {
      timer: null,
      polling: null,
      countdown: 300,
      liquidHeight: 100,
      show: false,
      showInfo: false
    };
  },
  methods: {
    start() {
      if (this.show) return;

      this.show = true;
      this.countdown = 300;
      this.liquidHeight = 100;

      this.timer = setInterval(() => {
        this.countdown--;
        this.liquidHeight = (this.countdown / 300) * 100;
        if (this.countdown <= 0) this.stop("音乐生成超时");
      }, 1000);

      const token = uni.getStorageSync('xm-user');
      const userToken = token ? token.token : '';
      const baseUrl = 'http://localhost:8000';

      this.polling = setInterval(() => {
        uni.request({
          url: `${baseUrl}/music/status`,
          method: 'GET',
          header: {
            'token': userToken
          },
          success: (res) => {
            if (res.statusCode === 200) {
              this.stop("🎵 音乐已生成");
            }
          },
          fail: (err) => {
            console.error('轮询失败', err);
          }
        });
      }, 10000);
    },

    stop(message) {
      clearInterval(this.timer);
      clearInterval(this.polling);
      this.show = false;
      this.countdown = 0;
      this.liquidHeight = 0;
      this.showInfo = false;
      uni.showToast({ title: message, icon: 'none' });
    }
  }
};
</script>


<style scoped>
.ball-wrapper {
  position: fixed;
  bottom: 30px;
  right: 20px;
  z-index: 9999;
}

.ball {
  width: 100px;
  height: 100px;
  position: relative;
  border-radius: 50%;
  overflow: hidden;
  background: #e0f2f1;
  border: 3px solid #4caf50;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* ✅ 内部液体：绝对定位 + 限制边界 */
.liquid {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(to top, #4caf50, #a5d6a7);
  transition: height 1s ease-in-out;
  z-index: 1;
}

/* ✅ 倒计时文字，浮在最上层 */
.text {
  position: absolute;
  z-index: 2;
  top: 35%;
  left: 0;
  width: 100%;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #004d40;
}

/* ✅ 信息提示框 */
.info-box {
  position: absolute;
  bottom: 110px;
  right: 0;
  width: 160px;
  padding: 10px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  font-size: 14px;
  color: #333;
  line-height: 1.5;
}
</style>







