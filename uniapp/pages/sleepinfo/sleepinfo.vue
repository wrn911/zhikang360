<template>
  <view class="sleep-form">
    <!-- 睡眠时间模块 -->
    <view class="form-card">
      <view class="form-header">
        <text class="title">睡眠时间记录</text>
        <text class="tip">🌙 请根据实际情况选择</text>
      </view>

      <view class="time-picker-group">
        <!-- 入睡时间 -->
        <view class="time-item">
          <text class="label">经常入睡时间</text>
          <picker 
            mode="time" 
            :value="sleepTime" 
            @change="bindSleepTime"
            class="time-picker"
          >
            <view class="picker-content">
              {{sleepTime || '请选择时间'}}
              <uni-icons type="arrowright" color="#66bb6a" size="18"></uni-icons>
            </view>
          </picker>
        </view>

        <!-- 起床时间 -->
        <view class="time-item">
          <text class="label">通常起床时间</text>
          <picker 
            mode="time" 
            :value="wakeupTime" 
            @change="bindWakeupTime"
            class="time-picker"
          >
            <view class="picker-content">
              {{wakeupTime || '请选择时间'}}
              <uni-icons type="arrowright" color="#66bb6a" size="18"></uni-icons>
            </view>
          </picker>
        </view>
      </view>
    </view>

    <!-- 情绪状态模块 -->
    <view class="form-card">
      <view class="form-header">
        <text class="title">情绪状态评估</text>
        <text class="tip">😌 可多选最近一周的常见状态</text>
      </view>

      <checkbox-group @change="handleEmotionChange">
        <view class="emotion-grid">
          <label 
            v-for="item in emotionOptions" 
            :key="item.value" 
            class="emotion-item"
            :class="{checked: selectedEmotions.includes(item.value)}"
          >
            <checkbox 
              :value="item.value" 
              :checked="selectedEmotions.includes(item.value)" 
              color="#66bb6a"
              style="display: none;"
            />
            <view class="emotion-content">
              <text class="icon">{{item.emoji}}</text>
              <text class="text">{{item.label}}</text>
            </view>
          </label>
        </view>
      </checkbox-group>
    </view>

    <!-- 提交按钮 -->
    <button 
      class="submit-btn" 
      :class="{valid: isFormValid}"
      :disabled="!isFormValid"
      @tap="handleSubmit"
    >
      提交数据
    </button>

    <!-- 数据验证提示 -->
    <view v-if="showValidationTip" class="validation-tip">
      <uni-icons type="info" color="#ffa726" size="16"></uni-icons>
      <text>请完整填写入睡和起床时间</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      sleepTime: '',
      wakeupTime: '',
      selectedEmotions: [],
      emotionOptions: [
        { emoji: "😰", label: "经常焦虑", value: "经常焦虑" },
        { emoji: "😖", label: "偶尔烦躁", value: "偶尔烦躁" },
        { emoji: "😌", label: "情绪平稳", value: "情绪平稳" },
        { emoji: "😫", label: "压力较大", value: "压力较大" },
        { emoji: "😴", label: "精神疲惫", value: "精神疲惫" },
        { emoji: "😊", label: "愉悦轻松", value: "愉悦轻松" }
      ],
      showValidationTip: false
    }
  },
  computed: {
    isFormValid() {
      return this.sleepTime && this.wakeupTime
    }
  },
  methods: {
    bindSleepTime(e) {
      this.sleepTime = e.detail.value
      this.validateTimes()
    },
    bindWakeupTime(e) {
      this.wakeupTime = e.detail.value
      this.validateTimes()
    },
    handleEmotionChange(e) {
      this.selectedEmotions = e.detail.value
    },
    validateTimes() {
      if (this.sleepTime && this.wakeupTime) {
        const sleep = new Date(`2023-01-01 ${this.sleepTime}`)
        const wakeup = new Date(`2023-01-01 ${this.wakeupTime}`)
        this.showValidationTip = wakeup <= sleep
      }
    },
    async handleSubmit() {
      if (!this.isFormValid) return
      
      const formData = {
        sleepTime: this.sleepTime,
        wakeupTime: this.wakeupTime,
        emotions: this.selectedEmotions
      }
	  
	  console.log('提交数据内容:', JSON.stringify(formData, null, 2)) // 控制台输出
      
      try {
        // 表单验证
        //await this.$refs.form.validate()
        
        
      	const res = await this.$request.post('/user-basic-info/sleep_info/add', formData)
      
        if (res.code === '200') {
          uni.showToast({ title: '提交成功', icon: 'success' })
      		  uni.navigateTo({ url: '/pages/illnessinfo/illnessinfo' })
          this.$refs.form.resetFields()
        }
      } catch (error) {
        if(error.message) {
          uni.showToast({ title: error.message, icon: 'none' })
        }
      }
    },
	    // 新增数据预览方法
	    previewData(data) {
	      return new Promise((resolve) => {
	        uni.showModal({
	          title: '即将提交的数据',
	          content: JSON.stringify(data, null, 2),
	          confirmText: '确认提交',
	          cancelText: '再检查下',
	          success: (res) => {
	            if (res.confirm) {
	              resolve(true)
	            } else {
	              resolve(false)
	            }
	          }
	        })
	      }).then(confirm => {
	        if (!confirm) return Promise.reject('用户取消提交')
	      })
	    },
	
    resetForm() {
      this.sleepTime = ''
      this.wakeupTime = ''
      this.selectedEmotions = []
    }
    }
  }

</script>

<style lang="scss" scoped>
/* 主色调 */
$primary-color: #66bb6a;

.sleep-form {
  padding: 20rpx;
  background: #f8faf8;
}

.form-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 32rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.04);
}

.form-header {
  margin-bottom: 40rpx;
  .title {
    font-size: 34rpx;
    font-weight: 600;
    color: #333;
    display: block;
    margin-bottom: 12rpx;
  }
  .tip {
    font-size: 26rpx;
    color: #666;
  }
}

.time-picker-group {
  .time-item {
    margin-bottom: 32rpx;
    &:last-child {
      margin-bottom: 0;
    }
    .label {
      font-size: 30rpx;
      color: #444;
      display: block;
      margin-bottom: 16rpx;
    }
    .picker-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 24rpx;
      background: #f8faf8;
      border-radius: 12rpx;
      color: #666;
      font-size: 30rpx;
    }
  }
}

.emotion-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24rpx;
  .emotion-item {
    border: 2rpx solid #eee;
    border-radius: 12rpx;
    padding: 24rpx;
    transition: all 0.2s;
    
    &.checked {
      border-color: $primary-color;
      background: #f0fff4;
    }
    .emotion-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      .icon {
        font-size: 50rpx;
        margin-bottom: 16rpx;
      }
      .text {
        font-size: 26rpx;
        color: #444;
        text-align: center;
      }
    }
  }
}

.submit-btn {
  background: #e0f2e1;
  color: #66bb6a;
  font-size: 32rpx;
  border-radius: 50rpx;
  margin: 40rpx 0;
  
  &.valid {
    background: $primary-color;
    color: #fff;
  }
}

.validation-tip {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffa726;
  font-size: 26rpx;
  margin-top: -20rpx;
  padding: 16rpx;
}
</style>