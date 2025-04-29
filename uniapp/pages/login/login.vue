<template>
  <view style="padding: 40rpx;">
    <view style="padding: 20rpx; margin: 80rpx 0; background-color: #fff; box-shadow: 0 2rpx 10rpx rgba(0,0,0,.1); border-radius: 10rpx;">
      <view style="margin: 50rpx 30rpx; font-size: 40rpx;">欢迎登录</view>
      <uni-forms ref="form" :modelValue="form" :rules="rules" validateTrigger='blur'>
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
          <view style="display: flex; align-items: center;">
            <uni-easyinput 
              prefixIcon="star-filled" 
              v-model="form.captcha" 
              placeholder="请输入验证码" 
              style="flex: 1;"
            />
            <view 
              @click="generateCaptcha" 
              :style="`
                margin-left: 20rpx; 
                padding: 10rpx 30rpx; 
                border-radius: 16rpx; 
                font-size: 36rpx; 
                letter-spacing: 8rpx; 
                position: relative;
                background: linear-gradient(45deg, ${color1}, ${color2});
                transform: rotate(${rotate}deg);
                color: #fff;
                text-shadow: 2rpx 2rpx 4rpx rgba(0,0,0,.2);
                box-shadow: 0 4rpx 12rpx rgba(0,0,0,.1);
              `"
            >
              <!-- 验证码文字 -->
              <view style="position: relative; z-index: 1;">{{ displayCode }}</view>
              
              <!-- 背景干扰元素 -->
              <view 
                style="
                  position: absolute;
                  top: 0;
                  left: 0;
                  right: 0;
                  bottom: 0;
                  background: repeating-linear-gradient(
                    -45deg,
                    transparent,
                    transparent 10rpx,
                    rgba(255,255,255,.3) 10rpx,
                    rgba(255,255,255,.3) 20rpx
                  );
                  mix-blend-mode: overlay;
                "
              ></view>
              
              <!-- 模糊滤镜 -->
              <view 
                style="
                  position: absolute;
                  top: -10rpx;
                  left: -10rpx;
                  right: -10rpx;
                  bottom: -10rpx;
                  backdrop-filter: blur(4rpx);
                  z-index: 0;
                "
              ></view>
            </view>
          </view>
        </uni-forms-item>

        <!-- 登录按钮 -->
        <uni-forms-item>
          <button @click="login()" style="background-color: #71d017; border-color: #71d017; height: 70rpx; line-height: 70rpx;">登 录</button>
        </uni-forms-item>

        <!-- 注册导航 -->
        <uni-forms-item>
          <view style="text-align: right;">
            还没有账号？去 
            <navigator style="display: inline-block; color: dodgerblue; margin-left: 4rpx;" url="/pages/register/register">注册</navigator>
          </view>
        </uni-forms-item>

        <!-- 切换登录方式 -->
        <uni-forms-item>
          <button class="switch-login-btn" @click="onchange()" hover-class="none">
            {{ seen ? '使用手机号登录' : '使用账号登录' }}
          </button>
        </uni-forms-item>
      </uni-forms>
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
      color1: '#FF6B6B',
      color2: '#4ECDC4',
      rotate: -5,
      displayCode: '' // 新增显示用验证码字段
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
      
      this.color1 = `hsl(${Math.random() * 360}, 70%, 60%)`
      this.color2 = `hsl(${Math.random() * 360}, 70%, 60%)`
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
.switch-login-btn {
  height: 60rpx !important;
  line-height: 60rpx !important;
  min-width: 240rpx !important;
  background-color: #fff !important;
  border: none !important;
  color: #666 !important;
  font-size: 26rpx !important;
  display: block;
  margin: 20rpx auto 0;
  padding: 0 30rpx;
  border-radius: 0;
  box-shadow: none;
}
</style>
