<template>
  <view class="container">
    <view class="header">
      <view class="logo-container">
        <view class="logo">智康360</view>
      </view>
    </view>
    
    <view class="form-container">
      <view class="title">欢迎登录</view>
      <view class="subtitle">健康生活，从智康开始</view>
      
      <uni-forms ref="form" :modelValue="form" :rules="rules" validateTrigger="blur">
        <!-- 动态切换账号/手机号输入 -->
        <uni-forms-item v-if="!seen" name="phone" required>
          <uni-easyinput prefixIcon="phone" v-model="form.phone" placeholder="请输入手机号" />
        </uni-forms-item>
        <uni-forms-item v-else name="username" required>
          <uni-easyinput prefixIcon="person" v-model="form.username" placeholder="请输入账号" />
        </uni-forms-item>

        <!-- 密码固定显示 -->
        <uni-forms-item name="password" required>
          <uni-easyinput type="password" prefixIcon="locked" v-model="form.password" placeholder="请输入密码" />
        </uni-forms-item>

        <!-- 验证码 -->
        <uni-forms-item name="captcha" required>
          <view class="captcha-container">
            <uni-easyinput
              prefixIcon="star-filled"
              v-model="form.captcha"
              placeholder="请输入验证码"
              style="flex: 1;"
            />
            <view
              @click="generateCaptcha"
              :style="`
                background: linear-gradient(45deg, ${color1}, ${color2});
              `"
              class="captcha-code"
            >
              <view class="captcha-text">{{ displayCode }}</view>
            </view>
          </view>
        </uni-forms-item>

        <!-- 登录按钮 -->
        <uni-forms-item class="login-button-container">
          <button @click="login()" class="login-button">登 录</button>
        </uni-forms-item>

        <!-- 注册导航 -->
        <uni-forms-item class="register-navigation">
          <view class="register-text">
            还没有账号？
            <navigator url="/pages/register/register" class="register-link">立即注册</navigator>
          </view>
        </uni-forms-item>

        <!-- 切换登录方式 -->
        <uni-forms-item>
          <button class="switch-login-btn" @click="onchange()">
            {{ seen ? '使用手机号登录' : '使用账号登录' }}
          </button>
        </uni-forms-item>
      </uni-forms>
    </view>
    
    <view class="footer">
      <text>© 2023 智康360 - 您的健康管家</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      form: {
        role: 'USER',
        captcha: ''
      },
      rules: {},
      seen: true,
      captchaCode: '',
      color1: '#4CAF50',
      color2: '#8BC34A',
      rotate: -5,
      displayCode: ''
    }
  },
  watch: {
    seen() {
      this.updateRules()
    }
  },
  mounted() {
    this.updateRules()
    this.generateCaptcha()
  },
  beforeDestroy() {
    clearTimeout(this.timer)
  },
  methods: {
    updateRules() {
      const baseRules = this.seen ? {
        username: {
          rules: [
            { required: true, errorMessage: '请输入账号' },
            { minLength: 3, maxLength: 10, errorMessage: '账号长度在3到10个字符' }
          ]
        },
        password: {
          rules: [
            { required: true, errorMessage: '请输入密码' },
            { minLength: 3, maxLength: 10, errorMessage: '密码长度在3到10个字符' }
          ]
        }
      } : {
        phone: {
          rules: [
            { required: true, errorMessage: '请输入手机号' },
            { minLength: 11, maxLength: 11, errorMessage: '手机号应为11个字符' }
          ]
        },
        password: {
          rules: [
            { required: true, errorMessage: '请输入密码' },
            { minLength: 3, maxLength: 10, errorMessage: '密码长度在3到10个字符' }
          ]
        }
      }

      baseRules.captcha = {
        rules: [
          { required: true, errorMessage: '请输入验证码' },
          { minLength: 4, maxLength: 4, errorMessage: '验证码必须为4位' }
        ]
      }

      this.rules = baseRules
    },

    generateCaptcha() {
      const code = Math.floor(Math.random() * 9000 + 1000).toString()
      
      this.color1 = `#4CAF50`
      this.color2 = `#8BC34A`
      this.rotate = (Math.random() * 15 - 7).toFixed(1)
      
      const letters = code.split('')
      this.captchaCode = code
      
      this.displayCode = letters.map(char => {
        return Math.random() > 0.5 ? char : `${char}\u200A` 
      }).join('')
  
      clearTimeout(this.timer)
      this.timer = setTimeout(this.generateCaptcha, 60000)
    },

    login() {
      const inputCode = this.form.captcha.replace(/\s/g, '')
      if (inputCode !== this.captchaCode) {
        uni.showToast({ icon: 'none', title: '验证码错误' })
        this.generateCaptcha()
        this.form.captcha = ''
        return
      }

      const params = {
        password: this.form.password,
        role: this.form.role
      }

      if (this.seen) {
        params.username = this.form.username
      } else {
        params.phone = this.form.phone
      }

      this.$request.post('/login', params).then(res => {
        if (res.code === '200') {
          uni.showToast({ icon: 'success', title: '登录成功' })
          uni.setStorageSync('xm-user', res.data)
		  uni.setStorageSync('user', JSON.stringify(res.data))
		  if(res.data.if_new === false){
			  uni.switchTab({ url: '/pages/index/index' })
		  }else{
			  uni.redirectTo({ url: '/pages/baseinfo/baseinfo' }) // 关闭当前页，不可返回
		  }
          
        } else {
          uni.showToast({ icon: 'error', title: res.msg })
        }
      }).catch(err => {
        console.log('表单验证失败:', err)
      })
    },

    onchange() {
      this.seen = !this.seen
      if (this.seen) {
        this.form.phone = ''
      } else {
        this.form.username = ''
      }
      this.$refs.form.clearValidate()
      this.generateCaptcha()
    }
  }
}
</script>

<style>
/* 全局样式 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.container {
  padding: 0;
  background: linear-gradient(to bottom, #f8f9fa, #e9f2ef);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 头部样式 */
.header {
  padding: 60rpx 40rpx 20rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-container {
  text-align: center;
}

.logo {
  font-size: 60rpx;
  font-weight: bold;
  color: #4CAF50;
  text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
  letter-spacing: 4rpx;
}

/* 表单容器 */
.form-container {
  flex: 1;
  background-color: #fff;
  border-radius: 30rpx 30rpx 0 0;
  box-shadow: 0 -10rpx 30rpx rgba(0, 0, 0, 0.05);
  padding: 60rpx 40rpx;
  margin-top: 40rpx;
}

.title {
  text-align: center;
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.subtitle {
  text-align: center;
  font-size: 28rpx;
  color: #666;
  margin-bottom: 60rpx;
}

/* 表单样式 */
uni-forms {
  width: 100%;
}

/* 输入框样式调整 */
uni-forms-item {
  margin-bottom: 30rpx;
}

uni-easyinput {
  width: 100%;
  background-color: #f9f9f9;
  border-radius: 16rpx;
  font-size: 32rpx;
  box-shadow: inset 0 2rpx 5rpx rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* 验证码样式 */
.captcha-container {
  display: flex;
  align-items: center;
}

.captcha-code {
  margin-left: 20rpx;
  padding: 10rpx 30rpx;
  border-radius: 16rpx;
  font-size: 36rpx;
  letter-spacing: 8rpx;
  position: relative;
  color: #fff;
  text-shadow: 1rpx 1rpx 2rpx rgba(0, 0, 0, 0.2);
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
  min-width: 160rpx;
  height: 80rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
}

.captcha-code:active {
  transform: scale(0.98);
}

.captcha-text {
  position: relative;
  z-index: 1;
}

/* 登录按钮样式 */
.login-button-container {
  margin-top: 40rpx;
  margin-bottom: 30rpx;
}

.login-button {
  width: 100%;
  height: 90rpx;
  line-height: 90rpx;
  background: linear-gradient(45deg, #4CAF50, #8BC34A);
  border: none;
  border-radius: 45rpx;
  font-size: 36rpx;
  color: white;
  font-weight: bold;
  box-shadow: 0 8rpx 20rpx rgba(76, 175, 80, 0.3);
  transition: all 0.3s ease;
}

.login-button:active {
  transform: scale(0.98);
  box-shadow: 0 4rpx 10rpx rgba(76, 175, 80, 0.2);
}

/* 注册导航样式 */
.register-navigation {
  text-align: center;
  margin: 20rpx 0;
}

.register-text {
  color: #666;
  font-size: 28rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-link {
  color: #4CAF50;
  font-weight: bold;
  margin-left: 10rpx;
  position: relative;
}

.register-link::after {
  content: '';
  position: absolute;
  bottom: -4rpx;
  left: 0;
  width: 100%;
  height: 2rpx;
  background-color: #4CAF50;
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.register-link:hover::after {
  transform: scaleX(1);
}

/* 切换登录方式按钮 */
.switch-login-btn {
  height: 60rpx;
  line-height: 60rpx;
  background-color: transparent;
  color: #4CAF50;
  font-size: 28rpx;
  display: block;
  text-align: center;
  padding: 0;
  border: none;
  box-shadow: none;
  width: 100%;
  margin-top: 20rpx;
}

/* 页脚样式 */
.footer {
  padding: 30rpx;
  text-align: center;
  font-size: 24rpx;
  color: #999;
  background-color: #fff;
}
</style>