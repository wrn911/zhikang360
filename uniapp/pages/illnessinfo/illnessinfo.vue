<template>
  <view class="health-form">
    <!-- 过敏情况 -->
    <view class="form-card">
      <view class="form-header">
        <text class="title">过敏情况</text>
        <text class="tip">🚨 请如实填写您的过敏史</text>
      </view>

      <!-- 过敏类型单选 -->
      <radio-group @change="handleAllergyChange">
        <view class="radio-group">
          <label v-for="item in allergyOptions" :key="item.value" class="radio-item">
            <radio :value="item.value" :checked="allergyType === item.value" color="#66bb6a"/>
            <text class="radio-label">{{item.label}}</text>
          </label>
        </view>
      </radio-group>

      <!-- 过敏详情 -->
      <view v-if="showAllergyDetails" class="multi-select">
        <view class="sub-title">选择具体过敏源（最多5项）:</view>
        <view class="tag-container">
          <checkbox-group @change="handleAllergySelect">
            <view class="tag-row">
              <view v-for="(item, index) in allergyDetails" :key="index" class="tag-wrapper">
                <label class="tag-item" :class="{checked: selectedAllergies.includes(item)}">
                  <checkbox :value="item" :checked="selectedAllergies.includes(item)" 
                    color="#66bb6a" style="display: none;"/>
                  <text class="tag-text">{{item}}</text>
                </label>
              </view>
              <input class="custom-input" v-model="customAllergy" placeholder="输入其他"
                @confirm="addCustomAllergy" :disabled="selectedAllergies.length >=5"
                placeholder-style="color:#888;font-size:26rpx"/>
            </view>
          </checkbox-group>
        </view>
      </view>
    </view>

    <!-- 慢性病史 -->
    <view class="form-card">
      <view class="form-header">
        <text class="title">慢性病史</text>
        <text class="tip">💊 可多选已确诊的疾病</text>
      </view>

      <checkbox-group @change="handleChronicSelect">
        <view class="disease-container">
          <view v-for="(item, index) in chronicOptions" :key="index" class="disease-item">
            <label class="disease-label" :class="{checked: selectedChronic.includes(item)}">
              <checkbox :value="item" :checked="selectedChronic.includes(item)" 
                color="#66bb6a" style="display: none;"/>
              <text class="disease-text">{{item}}</text>
            </label>
          </view>
          <input class="custom-input" v-model="customChronic" placeholder="输入其他疾病"
            @confirm="addCustomChronic" :disabled="selectedChronic.length >=5"
            placeholder-style="color:#888;font-size:26rpx"/>
        </view>
      </checkbox-group>
    </view>

    <!-- 其他健康问题 -->
    <view class="form-card">
      <view class="form-header">
        <text class="title">其他健康问题</text>
        <text class="tip">📝 可填写需要特别说明的情况</text>
      </view>
      
      <textarea v-model="otherHealthIssues" placeholder="例如：近期手术史、怀孕情况等..." 
        class="health-textarea" auto-height></textarea>
    </view>

    <!-- 提交按钮 -->
    <button class="submit-btn" :class="{disabled: !isFormValid}" 
      :disabled="!isFormValid" @click="handleSubmit">
      提交信息
    </button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      allergyType: null,
      allergyOptions: [
        { label: '无过敏史', value: '无过敏史' },
        { label: '食物过敏', value: '食物过敏' },
        { label: '药物过敏', value: '药物过敏' },
        { label: '其他过敏', value: '其他过敏' }
      ],
      allergyDetails: ['海鲜', '坚果', '牛奶', '花生', '青霉素'],
      selectedAllergies: [],
      customAllergy: '',
      chronicOptions: ['高血压', '糖尿病', '心脏病', '痛风', '脂肪肝'],
      selectedChronic: [],
      customChronic: '',
      otherHealthIssues: ''
    }
  },
  computed: {
    showAllergyDetails() {
      return this.allergyType && this.allergyType !== '无过敏史'
    },
    isFormValid() {
      return this.allergyType !== null
    }
  },
  methods: {
    handleAllergyChange(e) {
      this.allergyType = e.detail.value
      if (this.allergyType === '无过敏史') this.selectedAllergies = []
    },
    handleAllergySelect(e) {
      this.selectedAllergies = e.detail.value
    },
    addCustomAllergy() {
      if (this.customAllergy.trim() && this.selectedAllergies.length < 5) {
        this.allergyDetails.push(this.customAllergy.trim())
        this.customAllergy = ''
      }
    },
    handleChronicSelect(e) {
      this.selectedChronic = e.detail.value
    },
    addCustomChronic() {
      if (this.customChronic.trim() && this.selectedChronic.length < 5) {
        this.chronicOptions.push(this.customChronic.trim())
        this.customChronic = ''
      }
    },
    async handleSubmit() {
          // 基础表单验证
          if (!this.isFormValid) {
            return uni.showToast({
              title: '请先选择过敏情况',
              icon: 'none'
            });
          }
    
          // 过敏类型非空时的详细验证
          if (this.allergyType !== '无过敏史') {
            if (this.selectedAllergies.length === 0 && this.customAllergy === null) {
              return uni.showToast({
                title: '请选择至少一项过敏源',
                icon: 'none'
              });
            }
            if (this.selectedAllergies.some(item => !item.trim())) {
              return uni.showToast({
                title: '过敏源包含空内容',
                icon: 'none'
              });
            }
          }
    
          // 慢性病史验证
          if (this.selectedChronic.some(item => !item.trim())) {
            return uni.showToast({
              title: '慢性病史包含空内容',
              icon: 'none'
            });
          }
    
          // 组织提交数据
          const formData = {
            allergy: {
              type: this.allergyType,
              details: this.allergyType === '无过敏史' ? [] : [
				  ...this.selectedAllergies,
			      ...(this.customAllergy.trim() ? [this.customAllergy.trim()] : [])
			  ]
            },
            chronicDiseases: [
				...this.selectedChronic,
				...(this.customChronic.trim() ? [this.customChronic.trim()] : [])
			],
            healthIssues: this.otherHealthIssues.trim()
          };
    
          // 显示加载状态
          uni.showLoading({ title: '提交中...', mask: true });
    
          // 示例：使用uni.request发送请求
          try {
            // 表单验证
            //await this.$refs.form.validate()
            
            
          	const res = await this.$request.post('/user-basic-info/illness_info/add', formData)
          
            if (res.code === '200') {
              //uni.showToast({ title: '提交成功', icon: 'success' })
          	  //uni.switchTab({ url: '/pages/index/index' })
              //this.$refs.form.resetFields()
			  this.setifNew()
            }
          } catch (error) {
            if(error.message) {
              uni.showToast({ title: error.message, icon: 'none' })
            }
          }
    
  },
  async setifNew(){
	  try {
	  	const res = await this.$request.put('/user/update/if_new')
	    if (res.code === '200') {
	      uni.showToast({ title: '提交成功', icon: 'success' })
	  	  uni.switchTab({ url: '/pages/index/index' })
	      this.$refs.form.resetFields()
	    }
	  } catch (error) {
	    if(error.message) {
	      uni.showToast({ title: error.message, icon: 'none' })
	    }
	  }
  }
}}
</script>

<style lang="scss">
$primary-color: #66bb6a;

.health-form {
  padding: 20rpx;
  background: #f8faf8;
  min-height: 100vh;
}

.form-card {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.04);
}

.form-header {
  margin-bottom: 30rpx;
  .title {
    font-size: 34rpx;
    font-weight: 600;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
  }
  .tip {
    font-size: 26rpx;
    color: #666;
  }
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  .radio-item {
    width: 50%;
    padding: 20rpx 0;
    display: flex;
    align-items: center;
    .radio-label {
      font-size: 30rpx;
      margin-left: 16rpx;
    }
  }
}

.multi-select {
  margin-top: 20rpx;
  .sub-title {
    font-size: 28rpx;
    color: #444;
    margin-bottom: 20rpx;
  }
  .tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20rpx;
    .tag-wrapper {
      margin-bottom: 12rpx;
    }
    .tag-item {
      background: #f8faf8;
      border-radius: 40rpx;
      padding: 14rpx 28rpx;
      &.checked {
        background: #e8f5e9;
        border: 2rpx solid $primary-color;
      }
    }
  }
}

.disease-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
  .disease-item {
    width: calc(50% - 10rpx);
    .disease-label {
      display: block;
      padding: 24rpx;
      border: 2rpx solid #eee;
      border-radius: 12rpx;
      &.checked {
        border-color: $primary-color;
        background: #f0fff4;
      }
    }
  }
}

.health-textarea {
  width: 100%;
  min-height: 160rpx;
  padding: 20rpx;
  background: #f8faf8;
  border-radius: 12rpx;
  font-size: 28rpx;
}

.custom-input {
  width: 200rpx;
  height: 64rpx;
  padding: 0 20rpx;
  border: 2rpx solid #ddd;
  border-radius: 40rpx;
  font-size: 26rpx;
}

.submit-btn {
  background: $primary-color;
  color: #fff;
  border-radius: 50rpx;
  margin: 40rpx 0;
  font-size: 32rpx;
  &.disabled {
    background: #ccc;
    opacity: 0.7;
  }
}
</style>