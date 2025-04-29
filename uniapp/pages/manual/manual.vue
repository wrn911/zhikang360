<template>
  <view class="container">
    <view class="form-card">
      <!-- 基础信息 -->
      <view class="form-item">
        <text class="label">餐次类型</text>
        <picker 
          :value="mealIndex" 
          :range="mealTypes"
          @change="handleMealChange"
        >
          <view class="picker">{{ formData.meal_type || '请选择' }}</view>
        </picker>
      </view>

      <!-- 食物录入区 -->
      <view class="food-list">
        <view v-for="(item, index) in formData.food_items" :key="index" class="food-item">
          <view class="item-header">
            <text>食物 {{ index + 1 }}</text>
            <text @click="removeFood(index)" class="delete-btn">×</text>
          </view>
          <input v-model="item.name" placeholder="食物名称" class="input" />
          <view class="input-group">
            <input 
              v-model="item.weight" 
              type="number" 
              placeholder="重量(g)" 
              class="input half" 
            />
            <input 
              v-model="item.calories" 
              type="number" 
              placeholder="卡路里" 
              class="input half" 
            />
          </view>
        </view>
        <button @click="addFoodItem" class="add-btn">+ 添加食物</button>
      </view>

      <!-- 提交按钮 -->
      <button 
        class="submit-btn" 
        :disabled="!canSubmit" 
        @click="handleSubmit"
      >
        提交打卡
      </button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      mealTypes: ['早餐', '午餐', '晚餐', '加餐'],
      mealIndex: -1,
      formData: {
        meal_type: '',
        food_items: [],
        total_calories: 0
      }
    }
  },
  computed: {
    canSubmit() {
      return this.formData.meal_type && 
             this.formData.food_items.length > 0 &&
             this.formData.food_items.every(item => 
               item.name && item.weight && item.calories
             )
    }
  },
  methods: {
    handleMealChange(e) {
      this.mealIndex = e.detail.value
      this.formData.meal_type = this.mealTypes[this.mealIndex]
    },
    addFoodItem() {
      this.formData.food_items.push({
        name: '',
        weight: '',
        calories: ''
      })
    },
    removeFood(index) {
      this.formData.food_items.splice(index, 1)
    },
    async handleSubmit() {
      const payload = {
        user_id: uni.getStorageSync('userId'),
        checkin_date: this.getCurrentDate(),
        meal_type: this.formData.meal_type,
        checkin_type: '手动',
        food_items: JSON.stringify(this.formData.food_items),
        calories: this.calculateTotalCalories()
      }

      try {
        const res = await uni.request({
          url: '/api/checkin',
          method: 'POST',
          data: payload
        })
        
        if(res.data.code === 200) {
          uni.showToast({ title: '打卡成功' })
          setTimeout(() => uni.navigateBack(), 1500)
        }
      } catch (error) {
        uni.showToast({ title: '提交失败', icon: 'none' })
      }
    },
    calculateTotalCalories() {
      return this.formData.food_items.reduce((sum, item) => 
        sum + Number(item.calories || 0), 0
      )
    },
    getCurrentDate() {
      const date = new Date()
      return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
    }
  }
}
</script>

<style>
.form-card {
  padding: 30rpx;
  background: #fff;
  border-radius: 20rpx;
}

.form-item {
  margin-bottom: 40rpx;
}

.input {
  height: 80rpx;
  padding: 0 20rpx;
  border: 1rpx solid #eee;
  border-radius: 10rpx;
  margin-bottom: 20rpx;
}

.input-group {
  display: flex;
  gap: 20rpx;
}

.half {
  flex: 1;
}

.add-btn {
  margin: 20rpx 0;
  background: #f5f5f5;
}

.submit-btn {
  background: #4D8AFE;
  color: #fff;
}
</style>