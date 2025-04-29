
<style lang="scss" scoped>
.diet-form {
  padding: 30upx;
  background: #f8fff8;
}

.form-section {
  margin-bottom: 50upx;
  padding: 30upx;
  background: white;
  border-radius: 20upx;
  box-shadow: 0 4upx 12upx rgba(0, 0, 0, 0.05);
}

.section-title {
  display: block;
  font-size: 34upx;
  color: #2d4059;
  margin-bottom: 30upx;
  font-weight: 600;
}

.checkbox-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20upx;
}

.checkbox-item {
  flex: 0 0 calc(50% - 10upx);
  display: flex;
  align-items: center;
  padding: 20upx;
  border: 2upx solid #e0e0e0;
  border-radius: 12upx;
  transition: all 0.3s ease;

  &.checked {
    border-color: #4CAF50;
    background: #f0fff4;
  }
}

.checkbox-label {
  margin-left: 15upx;
  font-size: 28upx;
}

.custom-input {
  margin-top: 30upx;
  padding: 24upx;
  border: 2upx solid #e0e0e0;
  border-radius: 12upx;
  font-size: 28upx;
}

.slider-container {
  width: 100%;  /* 新增 */
  slider {
    flex: 1;  /* 关键 */
    width: 100%;  /* 确保撑满 */
  }
  text {  /* 防止挤压滑块 */
    flex-shrink: 0;  
  }
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 20upx;
  text {
    font-size: 24upx;
    color: #666;
    &.active {
      color: #4CAF50;
      font-weight: bold;
    }
  }
}

.submit-btn {
  background: #4CAF50;
  color: white;
  font-size: 32upx;
  border-radius: 12upx;
  padding: 28upx;
  margin: 40upx 0;

  &[disabled] {
    background: #cccccc;
  }
}

.status-message {
  padding: 30upx;
  border-radius: 12upx;
  text-align: center;
  &.success {
    background: #e8f5e9;
    color: #45a049;
  }
  &.error {
    background: #ffebee;
    color: #ff4444;
  }
}
</style>



<template>
  <view class="diet-form">
    <!-- 饮食喜好 -->
    <view class="form-section">
      <text class="section-title">饮食喜好（可多选）</text>
      <checkbox-group @change="handleDietPreference">
        <view class="checkbox-grid">
          <label 
            v-for="item in dietOptions" 
            :key="item.value" 
            class="checkbox-item"
            :class="{checked: dietPreferences.includes(item.value)}"
          >
            <checkbox 
              :value="item.value" 
              :checked="dietPreferences.includes(item.value)" 
              color="#4CAF50"
            />
            <text class="checkbox-label">{{ item.label }}</text>
          </label>
        </view>
      </checkbox-group>
	  <!--<input
	    v-model="customDiet" 
	    placeholder="其他饮食习惯..." 
	    class="custom-input"
	    @confirm="addCustomDiet"
	  />
      <textarea class="card-title">{{this.customDiet}}</textarea>-->
	  <textarea v-model="customDiet" placeholder="其他饮食喜好..."
	    class="texta" auto-height></textarea>
    </view>

    <!-- 忌口选项 -->
    <view class="form-section">
      <text class="section-title">忌口要求（可多选）</text>
      <checkbox-group @change="handleAvoidFood">
        <view class="checkbox-grid">
          <label 
            v-for="item in avoidOptions" 
            :key="item.value" 
            class="checkbox-item"
            :class="{checked: avoidFoods.includes(item.value)}"
          >
            <checkbox 
              :value="item.value" 
              :checked="avoidFoods.includes(item.value)" 
              color="#4CAF50"
            />
            <text class="checkbox-label">{{ item.label }}</text>
          </label>
        </view>
      </checkbox-group>
	  <textarea v-model="customAvoid" placeholder="其他忌口要求..."
	    class="texta" auto-height></textarea>
    </view>

    <!-- 改变意愿程度 -->
    <view class="form-section">
      <text class="section-title">改变意愿程度</text>
      <view class="slider-container">
        <text>1</text>
        <slider 
          :value="willingness" 
          min="1" 
          max="5" 
          step="1" 
          activeColor="#4CAF50"
          backgroundColor="#E0E0E0"
          block-color="#ffffff"
          block-size="28"
          @changing="handleSliderChange"
        />
        <text>5</text>
      </view>
      <view class="slider-labels">
        <text 
          v-for="n in 5" 
          :key="n" 
          :class="{active: willingness === n}"
        >
          {{ getLabel(n) }}
        </text>
      </view>
    </view>

    <!-- 提交按钮 -->
    <button 
      class="submit-btn" 
      :disabled="!isFormValid" 
      :loading="isSubmitting"
      @tap="handleSubmit"
    >
      提交饮食信息
    </button>

    <!-- 状态提示 -->
    <view v-if="submitStatus" :class="['status-message', submitStatus.type]">
      {{ submitStatus.message }}
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      dietPreferences: [],
      avoidFoods: [],
      willingness: 3,
      customDiet: '',
      customAvoid: '',
      dietOptions: [
        { value: '高蛋白', label: '高蛋白' },
        { value: '低脂', label: '低脂' },
        { value: '无糖', label: '无糖' },
        { value: '清淡', label: '清淡' },
        { value: '辣', label: '辣' }
      ],
      avoidOptions: [
        { value: '海鲜', label: '海鲜' },
        { value: '坚果', label: '坚果' },
        { value: '牛奶', label: '牛奶' },
		{ value: '暂无请忽略', label: '无' }
      ],
      submitStatus: null,
      isSubmitting: false
    }
  },
  computed: {
    isFormValid() {
      return this.dietPreferences.length > 0 || this.avoidFoods.length > 0
    }
  },
  methods: {
    handleDietPreference(e) {
      this.dietPreferences = e.detail.value
    },
    handleAvoidFood(e) {
      this.avoidFoods = e.detail.value
    },
    handleSliderChange(e) {
      this.willingness = e.detail.value
    },
    addCustomDiet() {
      if (this.customDiet.trim()) {
        this.dietPreferences.push(this.customDiet.trim())
        this.customDiet = ''
      }
    },
    addCustomAvoid() {
      if (this.customAvoid.trim()) {
        this.avoidFoods.push(this.customAvoid.trim())
        this.customAvoid = ''
      }
    },
    getLabel(n) {
      const labels = ['完全不', '不太愿意', '一般', '比较愿意', '完全可以']
      return labels[n - 1]
    },
    async handleSubmit() {
      if (!this.isFormValid) return
      
      this.isSubmitting = true
      this.submitStatus = null
      
      try {
		  
		 // 构建数据部分
	  const preferences = [
		...this.dietPreferences,
		...(this.customDiet.trim() ? [this.customDiet.trim()] : [])
	  ];
	  
	  const avoids = [
		...this.avoidFoods,
		...(this.customAvoid.trim() ? [this.customAvoid.trim()] : [])
	  ];
	
	  const data = {
		preferences,
		avoids,
		willingness: this.willingness
	  };
        
		const res = await this.$request.post('/user-basic-info/food_info/add', data)

        if (res.code === '200') {
          uni.showToast({ title: '提交成功', icon: 'success' })
          uni.navigateTo({ url: '/pages/sportinfo/sportinfo' })
          setTimeout(this.resetForm, 3000)
        } else {
          throw new Error(res.message || '提交失败')
        }
      } catch (error) {
        this.submitStatus = { 
          type: 'error', 
          message: error.message || '网络请求失败，请检查连接' 
        }
      } finally {
        this.isSubmitting = false
      }
    },
    resetForm() {
      this.dietPreferences = []
      this.avoidFoods = []
      this.willingness = 3
      this.customDiet = ''
      this.customAvoid = ''
      this.submitStatus = null
    }
  }
}
</script>

<style lang="scss" scoped>
/* 新增placeholder样式 */
.placeholder-style {
  color: #bdbdbd;
  font-size: 28upx;
}

.diet-form {
  padding: 30upx;
  background: #f8fff8;
}

.form-section {
  margin-bottom: 50upx;
  padding: 30upx;
  background: white;
  border-radius: 20upx;
  box-shadow: 0 4upx 12upx rgba(0, 0, 0, 0.05);
}

.checkbox-item {
  flex: 0 0 calc(50% - 10upx);
  display: flex;
  align-items: center;
  padding: 20upx;
  border: 2upx solid #e0e0e0;
  border-radius: 12upx;
  transition: all 0.3s ease;

  &.checked {
    border-color: #4CAF50;
    background: #f0fff4;
  }
}

.checkbox-label {
  margin-left: 15upx;
  font-size: 28upx;
}

.custom-input {
  margin-top: 30upx;
  padding: 24upx;
  border: 2upx solid #e0e0e0;
  border-radius: 12upx;
  font-size: 28upx;
}

.slider-container {
  width: 100%;  /* 新增 */
  slider {
    flex: 1;  /* 关键 */
    width: 100%;  /* 确保撑满 */
  }
  text {  /* 防止挤压滑块 */
    flex-shrink: 0;  
  }
}

.slider-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 20upx;
  text {
    font-size: 24upx;
    color: #666;
    &.active {
      color: #4CAF50;
      font-weight: bold;
    }
  }
}

.submit-btn {
  background: #4CAF50;
  color: white;
  font-size: 32upx;
  border-radius: 12upx;
  padding: 28upx;
  margin: 40upx 0;

  &[disabled] {
    background: #cccccc;
  }
}

.status-message {
  padding: 30upx;
  border-radius: 12upx;
  text-align: center;
  &.success {
    background: #e8f5e9;
    color: #45a049;
  }
  &.error {
    background: #ffebee;
    color: #ff4444;
  }
}

.texta {
  /* 间距控制 */
  margin-top: 8px;  /* 新增：与上方元素保持2px间距 */
  
  /* 修正异常值 */
  min-height: 60px;
  padding: 12px 16px;    /* 原123px改为12px */
  font-size: 14px;       /* 原123px改为14px */

  /* 保留原有合理样式 */
  width: 100%;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-family: 'Segoe UI', system-ui, sans-serif;
  line-height: 1.5;
  color: #333;
  background-color: #f8f9fa;
  resize: vertical;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

  &:disabled {
    background-color: #f1f3f5;
    opacity: 0.7;
    cursor: not-allowed;
  }

  &:focus {
    outline: none;
    border-color: #4dabf7;
    box-shadow: 0 0 0 3px rgba(77, 171, 247, 0.15);
    background-color: #fff;
  }

  &::placeholder {
    color: #adb5bd;
    font-style: italic;
  }

  @media (prefers-color-scheme: dark) {
    border-color: #495057;
    background-color: #212529;  /* 修正颜色值 #2123529 → #212529 */
    color: #e9ecef;
    
    &::placeholder {
      color: #6c757d;
    }
  }
}
</style>