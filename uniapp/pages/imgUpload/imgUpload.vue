<template>
  <view class="container">
    <!-- 拍照区域 -->
    <view class="camera-box">
      <image 
        v-if="tempFile" 
        :src="tempFile" 
        mode="aspectFit" 
        class="preview-image"
      />
      <button 
        v-else
        class="camera-btn" 
        @click="takePhoto"
      >
        <text class="icon">📸</text>
        <text>拍摄食物</text>
      </button>
    </view>

    <!-- 食物信息修正 -->
    <view v-if="tempFile" class="form-card">
      <input 
        v-model="foodName" 
        placeholder="输入食物名称" 
        class="input" 
      />
      
      <view class="input-group">
        <input
          v-model="foodWeight"
          type="number"
          placeholder="重量(g)"
          class="input half"
        />
        <input
          v-model="foodCalories"
          type="number"
          placeholder="卡路里"
          class="input half"
        />
      </view>

      <button 
        class="submit-btn" 
        :disabled="!canSubmit" 
        @click="handleSubmit"
      >
        确认提交
      </button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      tempFile: null,
      foodName: '',
      foodWeight: '',
      foodCalories: '',
      meal_type: '' // 从路由参数获取
    }
  },
  computed: {
    canSubmit() {
      return this.foodName && this.foodWeight && this.foodCalories
    }
  },
  onLoad(options) {
    this.meal_type = options.mealType || '加餐'
  },
  methods: {
    async takePhoto() {
      try {
        const res = await uni.chooseImage({
          count: 1,
          sourceType: ['camera'],
          sizeType: ['compressed']
        })
        
        this.tempFile = res.tempFilePaths[0]
        // 调用AI识别接口
        await this.recognizeFood()
      } catch (error) {
        uni.showToast({ title: '拍照失败', icon: 'none' })
      }
    },
    async recognizeFood() {
      // 示例：调用AI识别接口
      const res = await uni.request({
        url: '/api/ai/recognize',
        filePath: this.tempFile,
        method: 'UPLOAD'
      })
      
      if(res.data.success) {
        const { name, weight, calories } = res.data.result
        this.foodName = name
        this.foodWeight = weight
        this.foodCalories = calories
      }
    },
    async handleSubmit() {
      const payload = {
        user_id: uni.getStorageSync('userId'),
        checkin_date: new Date().toISOString().split('T')[0],
        meal_type: this.meal_type,
        checkin_type: '拍照',
        food_items: JSON.stringify([{
          name: this.foodName,
          weight: this.foodWeight,
          calories: this.foodCalories
        }]),
        calories: this.foodCalories
      }

      try {
        await uni.request({
          url: '/api/checkin',
          method: 'POST',
          data: payload
        })
        uni.showToast({ title: '打卡成功' })
        setTimeout(() => uni.navigateBack(), 1500)
      } catch (error) {
        uni.showToast({ title: '提交失败', icon: 'none' })
      }
    }
  }
}
</script>

<style>
.camera-box {
  height: 500rpx;
  background: #f5f5f5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-image {
  width: 100%;
  height: 100%;
}

.camera-btn {
  padding: 40rpx;
  background: #fff;
  border-radius: 20rpx;
}

.icon {
  font-size: 60rpx;
  display: block;
  margin-bottom: 20rpx;
}

.submit-btn {
  background: #4D8AFE;
  color: #fff;
}
</style>