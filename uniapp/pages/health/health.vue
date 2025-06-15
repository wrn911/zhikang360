<template>
	<view class="container">
		<view class="header">
			<view class="title">健康管理</view>
			<view class="subtitle">选择您需要的健康服务</view>
		</view>
		
		<view class="card-container">
			<!-- 手动录入健康数据卡片 -->
			<view class="card data-input-card" @click="openPopup" hover-class="card-hover">
				<view class="card-icon">
					<text class="iconfont">📊</text>
				</view>
				<view class="card-content">
					<text class="card-title">手动录入健康数据</text>
					<text class="card-desc">记录身高、体重、血压、血糖</text>
				</view>
			</view>
			
			<!-- 饮食卡片 -->
			<navigator class="card food-card" url="/pages/food/food1" hover-class="card-hover">
				<view class="card-icon">
					<text class="iconfont">🍎</text>
				</view>
				<view class="card-content">
					<text class="card-title">饮食管理</text>
					<text class="card-desc">健康饮食，合理搭配</text>
				</view>
			</navigator>
			
			<!-- 运动卡片 -->
			<navigator class="card sport-card" url="/pages/sport/sport" hover-class="card-hover">
				<view class="card-icon">
					<text class="iconfont">🏃</text>
				</view>
				<view class="card-content">
					<text class="card-title">运动记录</text>
					<text class="card-desc">科学运动，强身健体</text>
				</view>
			</navigator>
			
			<!-- 睡眠卡片 -->
			<navigator class="card sleep-card" url="/pages/sleep/sleep" hover-class="card-hover">
				<view class="card-icon">
					<text class="iconfont">🌙</text>
				</view>
				<view class="card-content">
					<text class="card-title">睡眠监测</text>
					<text class="card-desc">良好睡眠，健康生活</text>
				</view>
			</navigator>
			
			<!-- AI助手卡片 -->
			<navigator class="card ai-card" url="/pages/aihelper/aihelper" hover-class="card-hover">
				<view class="card-icon">
					<text class="iconfont">🤖</text>
				</view>
				<view class="card-content">
					<text class="card-title">AI答疑助手</text>
					<text class="card-desc">智能解答，专业指导</text>
				</view>
			</navigator>
		</view>

		<!-- 录入弹窗 -->
		<uni-popup ref="popup" type="dialog">
			<uni-popup-dialog 
				mode="base" 
				title="手动录入健康数据"
				@confirm="submitData"
				@close="closePopup"
			>
				<view class="input-group">
					<view class="input-item">
						<text class="label">身高(cm)</text>
						<input v-model="inputData.height" type="number" placeholder="请输入身高" />
					</view>
					<view class="input-item">
						<text class="label">体重(kg)</text>
						<input v-model="inputData.weight" type="number" placeholder="请输入体重" />
					</view>
					<view class="input-item">
						<text class="label">血压(mmHg)</text>
						<input v-model="inputData.bloodPressure" placeholder="格式：120/80" />
					</view>
					<view class="input-item">
						<text class="label">血糖(mmol/L)</text>
						<input v-model="inputData.bloodSugar" type="number" step="0.1" placeholder="请输入血糖值" />
					</view>
				</view>
			</uni-popup-dialog>
		</uni-popup>
		
		<view class="footer">
			<text>智康360 - 您的健康管家</text>
		</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			user: {},
			inputData: {
				height: '',
				weight: '',
				bloodPressure: '',
				bloodSugar: ''
			}
		}
	},

	onShow() {
		this.initializeUser()
	},

	methods: {
		// 用户初始化逻辑
		initializeUser() {
			const storedUser = uni.getStorageSync('xm-user')
			if (!storedUser?.id) {
				uni.redirectTo({ url: '/pages/login/login' })
				return
			}
			this.user = JSON.parse(JSON.stringify(storedUser))
		},

		// 提交数据方法
		async submitData() {
			if (!this.validateForm()) return

			try {
				// 添加用户ID参数
				const payload = {
					...this.inputData,
					userId: this.user.id
				}

				const res = await this.$request.put('/user-basic-info/update', payload)

				if (res.code === '200') {
					uni.showToast({ title: '更新成功' })
					this.closePopup()
					// 清空表单
					this.inputData = {
						height: '',
						weight: '',
						bloodPressure: '',
						bloodSugar: ''
					}
				}
			} catch (error) {
				uni.showToast({ title: '更新失败', icon: 'none' })
			}
		},

		// 表单验证
		validateForm() {
			const validations = [
				{
					field: 'height',
					regex: /^\d{2,3}(\.\d{1,2})?$/,
					message: '身高应为100-250cm之间的数字'
				},
				{
					field: 'weight',
					regex: /^\d{2,3}(\.\d{1,2})?$/,
					message: '体重格式不正确'
				},
				{
					field: 'bloodPressure',
					regex: /^\d{1,3}\/\d{1,3}$/,
					message: '血压格式应为120/80'
				},
				{
					field: 'bloodSugar',
					regex: /^\d{1,2}(\.\d{1,2})?$/,
					message: '血糖值应在0.1-30之间'
				}
			]
			return validations.every(({ field, regex, message }) => {
				const isValid = regex.test(this.inputData[field])
				if (!isValid) {
					uni.showToast({ title: message, icon: 'none' })
				}
				return isValid
			})
		},

		// 打开弹窗
		openPopup() {
			this.$refs.popup.open()
		},

		// 关闭弹窗
		closePopup() {
			this.$refs.popup.close()
		}
	}
}
</script>

<style>
/* 全局样式 */
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  padding: 40rpx 30rpx;
  display: flex;
  flex-direction: column;
}

/* 头部样式 */
.header {
  margin-bottom: 60rpx;
  text-align: center;
}

.title {
  font-size: 52rpx;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 16rpx;
  text-shadow: 0 2rpx 8rpx rgba(71, 85, 105, 0.1);
}

.subtitle {
  font-size: 30rpx;
  color: #64748b;
  opacity: 0.9;
}

/* 卡片容器 */
.card-container {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

/* 卡片通用样式 */
.card {
  display: flex;
  align-items: center;
  padding: 36rpx;
  border-radius: 24rpx;
  background: linear-gradient(135deg, #ffffff, #fafbfc);
  box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.08);
  border: 1rpx solid rgba(226, 232, 240, 0.6);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-hover {
  transform: translateY(-2rpx);
  box-shadow: 0 12rpx 32rpx rgba(71, 85, 105, 0.12);
  border-color: rgba(59, 130, 246, 0.2);
}

.card-icon {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 28rpx;
  font-size: 44rpx;
  box-shadow: 0 4rpx 16rpx rgba(71, 85, 105, 0.15);
}

.card-content {
  flex: 1;
}

.card-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 8rpx;
  display: block;
}

.card-desc {
  font-size: 26rpx;
  color: #64748b;
  display: block;
  opacity: 0.9;
}

/* 各卡片特殊样式 */
.data-input-card .card-icon {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.food-card .card-icon {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.sport-card .card-icon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.sleep-card .card-icon {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
}

.ai-card .card-icon {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

/* 页脚样式 */
.footer {
  margin-top: auto;
  padding-top: 60rpx;
  text-align: center;
  font-size: 28rpx;
  color: #94a3b8;
  opacity: 0.9;
  font-weight: 500;
}

/* 输入表单样式 */
.input-group {
  padding: 24rpx;
  
  .input-item {
    margin-bottom: 32rpx;
    
    .label {
      font-size: 28rpx;
      color: #1e293b;
      margin-bottom: 12rpx;
      display: block;
      font-weight: 500;
    }
    
    input {
      height: 84rpx;
      padding: 0 24rpx;
      border: 1rpx solid rgba(226, 232, 240, 0.6);
      border-radius: 16rpx;
      font-size: 28rpx;
      background: linear-gradient(135deg, #ffffff, #fafbfc);
      transition: all 0.3s ease;
      
      &:focus {
        border-color: #3b82f6;
        background-color: #fff;
        box-shadow: 0 0 0 4rpx rgba(59, 130, 246, 0.1);
      }
      
      &::placeholder {
        color: #94a3b8;
      }
    }
  }
}
</style>