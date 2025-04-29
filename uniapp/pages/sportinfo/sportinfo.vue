<template>
  <view class="container">
    <uni-forms ref="form" :model="formData" :rules="rules">
      <!-- 运动偏好 -->
      <uni-forms-item label="运动偏好" name="preferences">
        <uni-easyinput
          v-model="formData.preferences"
          placeholder="多个项目用顿号分隔"
        />
      </uni-forms-item>

      <!-- 不擅长运动 -->
      <uni-forms-item label="不擅长运动" name="weaknesses">
        <uni-easyinput
          v-model="formData.weaknesses"
          placeholder="多个项目用顿号分隔"
        />
      </uni-forms-item>

      <!-- 新运动尝试意愿 -->
      <uni-forms-item label="新运动尝试意愿" required name="willingness">
        <radio-group @change="(e) => formData.willingness = e.detail.value">
          <label class="radio-item" v-for="item in willingnessOptions" :key="item">
            <radio :value="item" :checked="formData.willingness === item" color="#4CAF50"/>
            <text>{{item}}</text>
          </label>
        </radio-group>
      </uni-forms-item>

      <!-- 健身经验 -->
      <uni-forms-item label="健身经验" name="experience">
        <uni-easyinput
          type="textarea"
          v-model="formData.experience"
          placeholder="请描述您的健身经历"
        />
      </uni-forms-item>

      <!-- 运动强度偏好 -->
      <uni-forms-item label="运动强度偏好" required name="intensity">
        <radio-group @change="(e) => formData.intensity = e.detail.value">
          <label class="radio-item" v-for="item in intensityOptions" :key="item">
            <radio :value="item" :checked="formData.intensity === item" color="#4CAF50"/>
            <text>{{item}}</text>
          </label>
        </radio-group>
      </uni-forms-item>

      <!-- 空闲时间 -->
      <uni-forms-item label="空闲时间" required name="freeTime">
        <checkbox-group @change="(e) => formData.freeTime = e.detail.value">
          <label class="checkbox-item" v-for="item in timeOptions" :key="item">
            <checkbox :value="item" :checked="formData.freeTime.includes(item)" color="#4CAF50"/>
            <text>{{item}}</text>
          </label>
        </checkbox-group>
      </uni-forms-item>

      <!-- 提交按钮 -->
      <button 
        class="submit-btn" 
        type="primary" 
        @click="handleSubmit"
        :style="{backgroundColor: formValid ? '#4CAF50' : '#BDBDBD'}"
      >提交信息</button>
    </uni-forms>
  </view>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        preferences: '',
        weaknesses: '',
        willingness: '',
        experience: '',
        intensity: '',
        freeTime: []
      },
      willingnessOptions: ['很愿意', '较愿意', '一般', '较不愿意', '很不愿意'],
      intensityOptions: ['较强', '适中', '较弱'],
      timeOptions: ['6:00-8:00', '8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00', '18:00-20:00' ],
      rules: {
        willingness: {
          rules: [{ required: true, errorMessage: '请选择尝试意愿' }]
        },
        intensity: {
          rules: [{ required: true, errorMessage: '请选择强度偏好' }]
        },
        freeTime: {
          rules: [{ required: true, errorMessage: '请选择空闲时间' }]
        }
      }
    }
  },
  computed: {
    formValid() {
      return this.formData.willingness && 
             this.formData.intensity.length > 0 &&
             this.formData.freeTime.length > 0
    }
  },
  methods: {
    async handleSubmit() {
      try {
        // 表单验证
        await this.$refs.form.validate()
        
        // 处理多选数据
		const data = this.formData
		const res = await this.$request.post('/user-basic-info/sport_info/add', data)

        if (res.code === '200') {
          uni.showToast({ title: '提交成功', icon: 'success' })
		  uni.navigateTo({ url: '/pages/sleepinfo/sleepinfo' })
          this.$refs.form.resetFields()
        }
      } catch (error) {
        if(error.message) {
          uni.showToast({ title: error.message, icon: 'none' })
        }
      }
    }
  }
}
</script>

<style lang="scss">
$primary-color: #4CAF50;
$card-bg: #ffffff;

.container {
  padding: 20rpx;
  background: #f5f7f8;
  min-height: 100vh;
}

/* 新增卡片容器样式 */
.uni-forms {
  background: transparent !important;
}

.uni-forms-item {
  margin-bottom: 20rpx;
  padding: 30rpx;
  background: $card-bg;
  border-radius: 16rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.06);
  
  /* 调整标签布局为上下两行 */
  &__label {
    display: block !important;
    width: 100% !important;
    margin-bottom: 20rpx !important;
    font-size: 32rpx !important;
    font-weight: 600;
    color: #2d3436;
  }
}

/* 优化输入框样式 */
.uni-easyinput {
  &__content {
    border-radius: 12rpx !important;
    background: #f8faf8 !important;
    padding: 20rpx !important;
  }
  
  &__placeholder-class {
    color: #a4b0be !important;
  }
}

/* 调整单选/复选布局 */
.radio-item, .checkbox-item {
  margin-right: 40rpx;
  margin-bottom: 25rpx;
  display: inline-flex;
  align-items: center;
  
  text {
    margin-left: 12rpx;
    font-size: 30rpx;
    color: #57606f;
  }
}

/* 优化文本域样式 */
.uni-textarea {
  height: 240rpx !important;
  padding: 20rpx !important;
  line-height: 1.6;
  background: #f8faf8 !important;
  border-radius: 12rpx;
}

/* 增强按钮交互效果 */
.submit-btn {
  margin: 60rpx 0 30rpx;
  border-radius: 12rpx;
  height: 90rpx;
  font-size: 34rpx;
  font-weight: 500;
  letter-spacing: 2rpx;
  transition: all 0.3s ease;
  
  &:active {
    transform: scale(0.98);
  }
  
  &[disabled] {
    filter: grayscale(80%);
    opacity: 0.8;
  }
}

/* 新增响应式布局 */
@media (max-width: 480px) {
  .radio-item, .checkbox-item {
    width: 48%;
    margin-right: 0;
    justify-content: flex-start;
  }
  
  .uni-forms-item {
    padding: 25rpx;
  }
}

/* 优化焦点状态 */
.uni-input-input:focus, 
.uni-textarea-textarea:focus {
  border-color: $primary-color !important;
  box-shadow: 0 0 8rpx rgba($primary-color, 0.2);
}
</style>
