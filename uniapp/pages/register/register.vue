<template>
	<view class="container">
		<view class="header">
			<view class="logo-container">
				<view class="logo">智康360</view>
			</view>
		</view>
		
		<view class="form-container">
			<view class="title">欢迎注册</view>
			<view class="subtitle">加入智康360，开启健康生活</view>
			
			<uni-forms ref="form" :modelValue="form" :rules="rules" validateTrigger='blur'>
				<uni-forms-item name="username" required>
					<uni-easyinput prefixIcon="person" v-model="form.username" placeholder="请输入账号" />
				</uni-forms-item>
				<uni-forms-item name="password" required>
					<uni-easyinput prefixIcon="locked" type="password" v-model="form.password" placeholder="请输入密码" />
				</uni-forms-item>
				<uni-forms-item name="phone" required>
					<uni-easyinput prefixIcon="phone" v-model="form.phone" placeholder="请输入手机号" />
				</uni-forms-item>
				<uni-forms-item class="register-button-container">
					<button @click="register()" class="register-button">注 册</button>
				</uni-forms-item>
				<uni-forms-item class="login-navigation">
					<view class="login-text">已有账号？<navigator class="login-link" url="/pages/login/login">立即登录</navigator></view>
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
					role: 'USER'
				},
				rules: {
					// 对username字段进行必填验证
					username: {
						// username 字段的校验规则
						rules:[
							// 校验 username 不能为空
							{
								required: true,
								errorMessage: '请输入账号',
							},
							// 对username字段进行长度验证
							{
								minLength: 3,
								maxLength: 10,
								errorMessage: '账号长度在 {minLength} 到 {maxLength} 个字符',
							}
						],
					},
					password: {
						rules:[
							{
								required: true,
								errorMessage: '请输入密码',
							},
							{
								minLength: 3,
								maxLength: 10,
								errorMessage: '密码长度在 {minLength} 到 {maxLength} 个字符',
							}
						],
					},
					phone: {
						rules:[
							{
								required: true,
								errorMessage: '请输入手机号',
							},
							{
								minLength: 11,
								maxLength: 11,
								errorMessage: '手机号应为 {minLength}个字符',
							}
						],
					}
					
				}
			}
		},
		methods: {
			register() {
				this.$refs.form.validate().then(res=>{
					this.$request.post('/register', this.form).then(res => {
						if (res.code === '200') {
							uni.showToast({
								icon: 'success',
								title: '注册成功'
							})
							
							setTimeout(() => {
								// 跳转登录页面
								uni.navigateTo({
									url: '/pages/login/login'
								})
							}, 500)
						} else {
							uni.showToast({
								icon: 'error',
								title: res.msg
							})
						}
					})
				}).catch(err =>{
					console.log('表单错误信息：', err);
				})
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

/* 注册按钮样式 */
.register-button-container {
  margin-top: 40rpx;
  margin-bottom: 30rpx;
}

.register-button {
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

.register-button:active {
  transform: scale(0.98);
  box-shadow: 0 4rpx 10rpx rgba(76, 175, 80, 0.2);
}

/* 登录导航样式 */
.login-navigation {
  text-align: center;
  margin: 20rpx 0;
}

.login-text {
  color: #666;
  font-size: 28rpx;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-link {
  color: #4CAF50;
  font-weight: bold;
  margin-left: 10rpx;
  position: relative;
}

.login-link::after {
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

.login-link:hover::after {
  transform: scaleX(1);
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
