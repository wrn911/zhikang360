<template>
  <view class="container">
    <!-- 饮食信息 -->
    <view class="info-card" v-if="foodInfo">
      <view class="card-header">
		  饮食信息
		  <text class="edit-btn" @click="openFoodPopUp">修改</text>
	  </view>
      <view class="card-content">
        <text class="info-item">偏好食物：{{foodInfo.preferences || '暂无'}}</text>
        <text class="info-item">忌口食物：{{foodInfo.avoids || '暂无'}}</text>
        <text class="info-item">饮食意愿：{{ getWillingnessLabel(foodInfo.willingness) }}</text>
        <view class="time-info">最后更新：{{formatTime(foodInfo.updateTime)}}</view>
      </view>
    </view>

    <!-- 运动信息 -->
    <view class="info-card" v-if="sportInfo">
      <view class="card-header">
		  运动信息
		  <text class="edit-btn" @click="openSportPopUp">修改</text>
	  </view>
      <view class="card-content">
        <text class="info-item">运动偏好：{{sportInfo.preferences || '暂无'}}</text>
        <text class="info-item">薄弱环节：{{sportInfo.weaknesses || '未设置'}}</text>
        <text class="info-item">运动强度：{{sportInfo.intensity || '未设置'}}</text>
		<text class="info-item">健身经历：{{sportInfo.experience || '暂无'}}</text>
		<text class="info-item">尝试意愿：{{sportInfo.willingness || '未设置'}}</text>
		<text class="info-item">空闲时间：{{sportInfo.freeTimes || '未设置'}}</text>
        <view class="time-info">最后更新：{{formatTime(sportInfo.updateTime)}}</view>
      </view>
    </view>

    <!-- 睡眠信息 -->
    <view class="info-card" v-if="sleepInfo">
      <view class="card-header">
		  睡眠信息
		  <text class="edit-btn" @click="openSleepPopUp">修改</text>
	  </view>
      <view class="card-content">
        <text class="info-item">入睡时间：{{sleepInfo.sleepTime || '未记录'}}</text>
        <text class="info-item">起床时间：{{sleepInfo.wakeupTime || '未记录'}}</text>
        <text class="info-item">睡眠情绪：{{sleepInfo.emotions || '未记录'}}</text>
        <view class="time-info">最后更新：{{formatTime(sleepInfo.updateTime)}}</view>
      </view>
    </view>

    <!-- 健康信息 -->
    <view class="info-card" v-if="illnessInfo">
      <view class="card-header">
		  健康信息
		  <text class="edit-btn" @click="openIllnessPopUp">修改</text>
	  </view>
      <view class="card-content">
        <text class="info-item">过敏类型：{{illnessInfo.allergyType || '无'}}</text>
        <text class="info-item">过敏详情：{{illnessInfo.allergyDetails || '无'}}</text>
        <text class="info-item">慢性疾病：{{illnessInfo.chronicDiseases || '无'}}</text>
		<text class="info-item">健康问题：{{illnessInfo.healthIssues || '无'}}</text>
        <view class="time-info">最后更新：{{formatTime(illnessInfo.updateTime)}}</view>
      </view>
    </view>
	
	<!-- 饮食信息弹窗 -->
	    <uni-popup ref="foodDialog" type="dialog">
	      <uni-popup-dialog
	        mode="base" 
	        title="修改饮食信息"
	        class="edit-dialog food-dialog"
	        @confirm="submitFood"
	        @close="closePopup"
	      >
	        <!-- 滚动容器包裹 -->
	        <scroll-view scroll-y class="dialog-scroll">
	          <view class="input-group">
	            <!-- 偏好食物 -->
	            <view class="input-item">
	              <text class="label">偏好食物</text>
	              <textarea 
	                v-model="foodForm.preferences" 
	                placeholder="请输入常吃的食物（如：海鲜、牛肉等）"
	                class="textarea-field"
	                auto-height
	              ></textarea>
	            </view>
	    
	            <!-- 忌口食物 -->
	            <view class="input-item">
	              <text class="label">忌口食物</text>
	              <textarea
	                v-model="foodForm.avoids"
	                placeholder="请输入需要避免的食物（如：辛辣、花生等）"
	                class="textarea-field"
	                auto-height
	              ></textarea>
	            </view>
	    
	           <!-- 饮食意愿复合组件 -->
	                   <view class="input-item">
	                     
	                     <!-- 滑动条组件 -->
	                     <view class="willingness-slider">
	                       <view class="slider-header">
	                         <text>饮食调整意愿</text>
	                         <text class="slider-value">{{ willingnessLabels[foodForm.willingness - 1] }}</text>
	                       </view>
	                       
	                       <slider 
	                         :value="foodForm.willingness" 
	                         min="1" 
	                         max="5" 
	                         step="1"
	                         activeColor="#4CAF50"
	                         backgroundColor="#E0E0E0"
	                         block-color="#ffffff"
	                         block-size="28"
	                         @change="handleWillingnessChange"
	                       />
	                       
	                       <view class="slider-steps">
	                         <text 
	                           v-for="n in 5" 
	                           :key="n" 
	                           :class="{ 'step-active': foodForm.willingness === n }"
	                         >
	                           {{ n }}
	                         </text>
	                       </view>
	                     </view>
	                   </view>
	          </view>
	        </scroll-view>
	      </uni-popup-dialog>
	    </uni-popup>
	
	    <!-- 运动信息弹窗 -->
	    <uni-popup ref="sportDialog" type="dialog">
	      <uni-popup-dialog
	        mode="base"
	        title="修改运动信息"
	        class="edit-dialog sport-dialog"
	        @confirm="submitSport"
	        @close="closeSportPopup"
	      >
	        <view class="dialog-content">
	          <scroll-view class="scroll-container" scroll-y="true">
	            <view class="input-group">
	              
	              <!-- 运动偏好 -->
	              <view class="form-section">
	                <text class="section-title">运动偏好</text>
					<textarea
					  v-model="sportForm.preferences"
					  placeholder="如：跑步、游泳等"
					  class="experience-field"
					  auto-height
					/>
	              </view>
	    
	              <!-- 薄弱环节 -->
				  <view class="form-section">
	                <text class="section-title">薄弱环节</text>
					<textarea
					  v-model="sportForm.weaknesses"
					  placeholder="如：跑步、游泳等"
					  class="experience-field"
					  auto-height
					/>
	              </view>
	    
	              <!-- 新运动尝试意愿 -->
	              <view class="form-section">
	                <text class="section-title">新运动尝试意愿</text>
	                <radio-group 
	                  @change="(e) => sportForm.willingness = e.detail.value"
	                  class="radio-group"
	                >
	                  <view 
	                    v-for="item in willingnessOptions" 
	                    :key="item" 
	                    class="radio-item"
	                  >
	                    <radio 
	                      :value="item" 
	                      :checked="sportForm.willingness === item" 
	                      color="#4CAF50"
	                    />
	                    <text class="radio-label">{{item}}</text>
	                  </view>
	                </radio-group>
	              </view>
	    
	              <!-- 运动强度偏好 -->
	              <view class="form-section">
	                <text class="section-title">运动强度偏好</text>
	                <radio-group 
	                  @change="(e) => sportForm.intensity = e.detail.value"
	                  class="radio-group"
	                >
	                  <view 
	                    v-for="item in intensityOptions" 
	                    :key="item" 
	                    class="radio-item"
	                  >
	                    <radio 
	                      :value="item" 
	                      :checked="sportForm.intensity === item" 
	                      color="#4CAF50"
	                    />
	                    <text class="radio-label">{{item}}</text>
	                  </view>
	                </radio-group>
	              </view>
	    
	              <!-- 空闲时间选择 -->
	              <view class="form-section">
	                <text class="section-title">空闲时段（可多选）</text>
	                <checkbox-group 
	                  @change="(e) => sportForm.freeTimes = e.detail.value" 
	                  class="checkbox-grid"
	                >
	                  <view 
	                    v-for="item in timeOptions" 
	                    :key="item" 
	                    class="checkbox-item"
	                  >
	                    <checkbox 
	                      :value="item" 
	                      :checked="sportForm.freeTimes.includes(item)" 
	                      color="#4CAF50"
	                    />
	                    <text class="checkbox-label">{{item}}</text>
	                  </view>
	                </checkbox-group>
	              </view>
	    
	              <!-- 健身经验 -->
	              <view class="form-section">
	                <text class="section-title">健身经验</text>
	                <textarea
	                  v-model="sportForm.experience"
	                  placeholder="例如：有3年健身房训练经验，熟悉力量训练..."
	                  class="experience-field"
	                  auto-height
	                />
	              </view>
	    
	            </view>
	          </scroll-view>
	        </view>
	      </uni-popup-dialog>
	    </uni-popup>
	
	    <!-- 睡眠信息弹窗 -->
	    <uni-popup ref="sleepDialog" type="dialog">
	      <uni-popup-dialog
	        mode="base"
	        title="修改睡眠信息"
	        class="edit-dialog sleep-dialog"
	        @confirm="submitSleep"
	        @close="closeSleepPopup"
	      >
	        <view class="dialog-scroll">
	          <!-- 时间选择组 -->
	          <view class="form-section">
	            <view class="time-picker-group">
	              <!-- 入睡时间 -->
	              <view class="time-item">
	                <text class="section-title">通常入睡时间</text>
	                <picker 
	                  mode="time" 
	                  :value="sleepForm.sleepTime" 
	                  @change="(e) => sleepForm.sleepTime = e.detail.value"
	                  class="time-picker"
	                >
	                  <view class="picker-content">
	                    {{ sleepForm.sleepTime || '点击选择时间' }}
	                    <uni-icons type="arrowright" color="#66bb6a" size="18" />
	                  </view>
	                </picker>
	              </view>
	    
	              <!-- 起床时间 -->
	              <view class="time-item">
	                <text class="section-title">通常起床时间</text>
	                <picker 
	                  mode="time" 
	                  :value="sleepForm.wakeupTime" 
	                  @change="(e) => sleepForm.wakeupTime = e.detail.value"
	                  class="time-picker"
	                >
	                  <view class="picker-content">
	                    {{ sleepForm.wakeupTime || '点击选择时间' }}
	                    <uni-icons type="arrowright" color="#66bb6a" size="18" />
	                  </view>
	                </picker>
	              </view>
	            </view>
	          </view>
	    
	          <!-- 情绪选择 -->
	          <view class="form-section">
	            <text class="section-title">睡眠情绪状态</text>
	            <checkbox-group @change="(e) => sleepForm.emotions = e.detail.value">
	              <!-- 修改此处网格布局 -->
	              <view class="emotion-grid">
	                <label 
	                  v-for="item in emotionOptions" 
	                  :key="item.value" 
	                  class="emotion-item"
	                  :class="{checked: (sleepForm.emotions || []).includes(item.value)}"
	                >
	                  <checkbox 
	                    :value="item.value" 
	                    :checked="(sleepForm.emotions || []).includes(item.value)" 
	                    style="display: none;" 
	                  />
	                  <view class="emotion-content">
	                    <text class="icon">{{ item.emoji }}</text>
	                    <text class="text">{{ item.label }}</text>
	                  </view>
	                </label>
	              </view>
	            </checkbox-group>
	          </view>
	        </view>
	      </uni-popup-dialog>
	    </uni-popup>
	
	    
	    <uni-popup ref="illnessDialog" type="dialog">
	      <uni-popup-dialog
	        mode="base"
	        title="修改健康信息"
	        class="edit-dialog"
	        @confirm="submitIllness"
	        @close="closeIllnessPopup"
	      >
	        <!-- 使用 uni-forms 自带表单结构 -->
	        <uni-forms class="dialog-form" label-width="80px">
	          <scroll-view scroll-y class="form-scroll">
	            
	            <!-- 过敏类型 -->
	            <uni-forms-item label="过敏类型">
	              <uni-easyinput 
	                type="textarea"
	                v-model="illnessForm.allergyType"
	                placeholder="请输入过敏类型（如：花粉、海鲜等）"
	                :autoHeight="true"
	              ></uni-easyinput>
	            </uni-forms-item>
	    
	            <!-- 过敏详情 -->
	            <uni-forms-item label="过敏详情">
	              <uni-easyinput 
	                type="input"
	                v-model="illnessForm.allergyDetails"
	                placeholder="描述过敏症状及反应程度"
	                :autoHeight="true"
	              ></uni-easyinput>
	            </uni-forms-item>
	    
	            <!-- 慢性疾病 -->
	            <uni-forms-item label="慢性疾病">
	              <uni-easyinput 
	                type="input"
	                v-model="illnessForm.chronicDiseases"
	                placeholder="如：高血压、糖尿病等"
	                :autoHeight="true"
	              ></uni-easyinput>
	            </uni-forms-item>
	    
	            <!-- 健康问题 -->
	            <uni-forms-item label="健康问题">
	              <uni-easyinput 
	                type="input"
	                v-model="illnessForm.healthIssues"
	                placeholder="其他需要说明的健康状况"
	                :autoHeight="true"
	              ></uni-easyinput>
	            </uni-forms-item>
	    
	          </scroll-view>
	        </uni-forms>
	      </uni-popup-dialog>
	    </uni-popup>

    <view v-if="!hasData" class="empty-tip">暂无健康信息记录</view>
  </view>
</template>

<script>
import dayjs from 'dayjs'
export default {
  data() {
    return {
      foodInfo: null,
      sportInfo: null,
      sleepInfo: null,
      illnessInfo: null,
	  // 饮食表单
	  foodForm: {},
	  // 运动表单
	  sportForm: {
		  freeTimes: []  // 确保初始状态有默认值
	  },
	  // 睡眠表单
	  sleepForm: {
		  sleepTime: '',  // 必须初始化
		  wakeupTime: ''  // 保证字段存在
	  },
	  // 健康表单
	  illnessForm: {},
	  willingnessLabels: ['完全不', '不太愿意', '一般', '比较愿意', '完全可以'],
	  willingnessOptions: ['很愿意', '较愿意', '一般', '较不愿意', '很不愿意'],
	  intensityOptions: ['较强', '适中', '较弱'],
	  timeOptions: ['6:00-8:00', '8:00-10:00', '10:00-12:00', '12:00-14:00',
	                   '14:00-16:00', '16:00-18:00', '18:00-20:00'],
	  emotionOptions: [
	    { emoji: "😰", label: "经常焦虑", value: "经常焦虑" },
	    { emoji: "😖", label: "偶尔烦躁", value: "偶尔烦躁" },
	    { emoji: "😌", label: "情绪平稳", value: "情绪平稳" },
	    { emoji: "😫", label: "压力较大", value: "压力较大" },
	    { emoji: "😴", label: "精神疲惫", value: "精神疲惫" },
	    { emoji: "😊", label: "愉悦轻松", value: "愉悦轻松" }
	  ],
    }
  },
  computed: {
    hasData() {
      return this.foodInfo || this.sportInfo || this.sleepInfo || this.illnessInfo
    }
  },
  onLoad() {
    this.fetchAllInfo()
  },
  methods: {
	// 统一封装的提交方法
	  async submitFormHandler(apiPath, formData, successMsg) {
	    try {
	      this.isSubmitting = true
	      
	      const res = await this.$request.put(apiPath, formData)
	      
	      if (res.code === '200') {
	        uni.showToast({ title: successMsg, icon: 'success' })
	        this.fetchAllInfo()
	        setTimeout(this.resetForm, 3000)
	        return true
	      } else {
	        throw new Error(res.message || '提交失败')
	      }
	    } catch (error) {
	      this.submitStatus = { 
	        type: 'error',
	        message: error.message.includes('Network Error') 
	          ? '网络请求失败，请检查连接' 
	          : error.message
	      }
	      return false
	    } finally {
	      this.isSubmitting = false
	    }
	  },
	
	  // 睡眠信息提交
	  async submitSleep() {
	    const data = {
	      sleepTime: this.sleepForm.sleepTime,
	      wakeupTime: this.sleepForm.wakeupTime,
	      emotions: this.sleepForm.emotions
	    }
	    
	    const success = await this.submitFormHandler(
	      '/user-basic-info/sleep_info/update',
	      data,
	      '睡眠信息已保存'
	    )
	    
	    if (success) {
	      // 更新本地数据存储
	      this.sleepInfo = { ...this.sleepInfo, ...data }
	    }
	  },
	
	  // 运动偏好提交
	  async submitSport() {
	    const data = {
	      preferences: this.sportForm.preferences,
	      weaknesses: this.sportForm.weaknesses,
	      intensity: this.sportForm.intensity,
	      experience: this.sportForm.experience,
	      willingness: this.sportForm.willingness,
	      freeTimes: this.sportForm.freeTimes.join('、')
	    }
	    
	    const success = await this.submitFormHandler(
	      '/user-basic-info/sport_info/update',
	      data,
	      '运动偏好已保存'
	    )
	    
	    if (success) {
	      this.sportInfo = { ...this.sportInfo, ...data }
	    }
	  },
	
	  // 健康问题提交
	  async submitIllness() {
	    const data = {
	      allergyType: this.illnessForm.allergyType,
	      allergyDetails: this.illnessForm.allergyDetails,
	      chronicDiseases: this.illnessForm.chronicDiseases,
	      healthIssues: this.illnessForm.healthIssues
	    }
	    
	    const success = await this.submitFormHandler(
	      '/user-basic-info/illness_info/update',
	      data,
	      '健康信息已保存'
	    )
	    
	    if (success) {
	      this.illnessInfo = { ...this.illnessInfo, ...data }
	    }
	  },
	
	  // 饮食习惯提交
	  async submitFood() {
	    const data = {
	      preferences: this.foodForm.preferences,
	      avoids: this.foodForm.avoids,
	      willingness: this.foodForm.willingness
	    }
	    
	    const success = await this.submitFormHandler(
	      '/user-basic-info/food_info/update',
	      data,
	      '饮食偏好已保存'
	    )
	    
	    if (success) {
	      this.foodInfo = { ...this.foodInfo, ...data }
	    }
	  },
    async fetchAllInfo() {
      try {
        // 获取饮食信息
        const foodRes = await this.$request.get( '/user-basic-info/food_info/selectById' )
        this.foodInfo = foodRes.data
        
        // 获取运动信息
        const sportRes = await this.$request.get( '/user-basic-info/sport_info/selectById' )
        this.sportInfo = sportRes.data
        
        // 获取睡眠信息
        const sleepRes = await this.$request.get( '/user-basic-info/sleep_info/selectById' )
        this.sleepInfo = sleepRes.data
        
        // 获取健康信息
        const illnessRes = await this.$request.get( '/user-basic-info/illness_info/selectById' )
        this.illnessInfo = illnessRes.data
      } catch (error) {
        uni.showToast({ title: '数据加载失败', icon: 'none' })
      }
    },

    formatTime(time) {
      return time ? dayjs(time).format('YYYY-MM-DD HH:mm') : '未记录'
    },
	
	// 滑动条变化处理
	    handleWillingnessChange(e) {
	      const value = parseInt(e.detail.value)
	      this.foodForm.willingness = this.clampValue(value, 1, 5)
	    },
		
	// 数值范围限制
    clampValue(val, min, max) {
      return Math.max(min, Math.min(max, val))
    },
	
	getWillingnessLabel(value) {
	    const num = parseInt(value)
	    return Number.isInteger(num) && num >= 1 && num <= 5 
	        ? this.willingnessLabels[num - 1] 
	        : '未设置'
	},
	openFoodPopUp() {
	  // 初始化表单数据
	  this.foodForm = {
		preferences: this.foodInfo.preferences,
		avoids: this.foodInfo.avoids,
		willingness: this.foodInfo.willingness
	  }
	  // 显示弹窗（假设使用uni-popup组件）
	  this.$refs.foodDialog.open()
	},
	// 修改关闭弹窗方法
	closeFoodPopup() {
	    this.$refs.foodDialog.close()
	},
	openSportPopUp() {
	  // 初始化表单数据
	  this.sportForm = {
	    preferences: this.sportInfo.preferences,
	    weaknesses: this.sportInfo.weaknesses,
	    intensity: this.sportInfo.intensity,
	    experience: this.sportInfo.experience,
		willingness: this.sportInfo.willingness,
		freeTimes: this.sportInfo.freeTimes
	  }
	  // 显示弹窗（假设使用uni-popup组件）
	  this.$refs.sportDialog.open()
	},
	// 修改关闭弹窗方法
	closeSportPopup() {
	    this.$refs.sportDialog.close()
	},
	openSleepPopUp() {
	  // 初始化表单数据
	  this.sleepForm = {
		sleepTime: this.sleepInfo.sleepTime,
		wakeupTime: this.sleepInfo.wakeupTime,
		emotions: this.sleepInfo.emotions
	  }
	  // 显示弹窗（假设使用uni-popup组件）
	  this.$refs.sleepDialog.open()
	},
	// 修改关闭弹窗方法
	closeSleepPopup() {
	    this.$refs.sleepDialog.close()
	},
	openIllnessPopUp() {
	  // 初始化表单数据
	  this.illnessForm = {
		allergyType: this.illnessInfo.allergyType,
		allergyDetails: this.illnessInfo.allergyDetails,
		chronicDiseases: this.illnessInfo.chronicDiseases,
		healthIssues: this.illnessInfo.healthIssues
	  }
	  // 显示弹窗（假设使用uni-popup组件）
	  this.$refs.illnessDialog.open()
	},
	// 修改关闭弹窗方法
	closeFoodPopup() {
	    this.$refs.illnessDialog.close()
	}
  }
}
</script>

<style lang="scss">
/* 主色调定义 */
$primary-green: #81C784;  // 浅绿色
$accent-pink: #F48FB1;    // 粉红色
$background: #F5F5F5;     // 浅灰背景
$text-dark: #424242;      // 深灰文字
$text-light: #757575;     // 浅灰文字

.container {
  min-height: 100vh;
  padding: 20rpx;
  background: linear-gradient(180deg, #f8fff8 0%, #fff5f5 100%);
}

/* 信息卡片样式 */
.info-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 8rpx 30rpx rgba(129, 199, 132, 0.1);
  border-top: 8rpx solid $primary-green;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 8rpx;
    background: linear-gradient(90deg, $primary-green 0%, $accent-pink 100%);
  }
}

.card-header {
  padding: 28rpx 32rpx;
  font-size: 34rpx;
  color: $text-dark;
  font-weight: 600;
  background: rgba(129, 199, 132, 0.05);
  border-bottom: 2rpx solid rgba(244, 143, 177, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  &::after {
    content: '✦';
    color: $accent-pink;
    margin-left: 16rpx;
  }
}

.card-content {
  padding: 32rpx;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300rpx, 1fr));
  gap: 24rpx;
}

.info-item {
  font-size: 30rpx;
  color: $text-light;
  line-height: 1.6;
  padding-left: 40rpx;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 12rpx;
    height: 12rpx;
    background: $accent-pink;
    border-radius: 50%;
    box-shadow: 0 2rpx 6rpx rgba(244, 143, 177, 0.3);
  }
  
  &:nth-child(odd)::before {
    background: $primary-green;
  }
}

.time-info {
  grid-column: 1 / -1;
  text-align: right;
  font-size: 26rpx;
  color: #BDBDBD;
  margin-top: 20rpx;
  padding-top: 20rpx;
  border-top: 1rpx dashed rgba(189, 189, 189, 0.3);
  
  &::before {
    content: '🕒 ';
    margin-right: 8rpx;
  }
}

.empty-tip {
  text-align: center;
  padding: 80rpx;
  color: $primary-green;
  font-size: 32rpx;
  font-weight: 300;
  letter-spacing: 2rpx;
  
  &::before {
    content: '🍃';
    display: block;
    font-size: 60rpx;
    margin-bottom: 20rpx;
  }
}

/* 响应式调整 */
@media (max-width: 480px) {
  .card-content {
    grid-template-columns: 1fr;
  }
  
  .info-item {
    font-size: 28rpx;
    padding-left: 36rpx;
  }
  
  .card-header {
    font-size: 32rpx;
    padding: 24rpx;
  }
}

/* 微交互效果 */
.info-card {
  transition: transform 0.3s ease;
  
  &:active {
    transform: scale(0.98);
  }
}

.info-item::before {
  transition: all 0.3s ease;
}

.info-item:hover::before {
  transform: translateY(-50%) scale(1.2);
}


/* 所有样式通过 .food-dialog 限定作用域 */
.food-dialog {
  /* 弹窗容器基础尺寸 */
  min-width: 680rpx !important;
  max-height: 80vh;
  
  .willingness-slider {
      margin: 30rpx 0 40rpx;
      
      .slider-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20rpx;
        font-size: 28rpx;
        color: #666;
  
        .slider-value {
          color: #4CAF50;
          font-weight: bold;
        }
      }
  
      .slider-steps {
        display: flex;
        justify-content: space-between;
        margin-top: 15rpx;
  
        text {
          color: #999;
          font-size: 24rpx;
          width: 36rpx;
          text-align: center;
  
          &.step-active {
            color: #4CAF50;
            font-weight: bold;
          }
        }
      }
    }
  
    .note-field {
      margin-top: 20rpx;
      min-height: 120rpx;
      background: #f9f9f9;
    }
  
  /* 内部滚动容器 */
  .dialog-scroll {
    height: 60vh;
    padding: 0 25rpx;
  }

  /* 输入项间距 */
  .input-item {
    margin-bottom: 30rpx;
  }

  /* 标签样式 */
  .label {
    display: block;
    font-size: 30rpx;
    color: #333;
    margin-bottom: 15rpx;
    font-weight: 500;
  }

  /* 文本域核心样式 */
  .textarea-field {
    width: 450rpx;
    min-height: 85rpx;
    padding: 20rpx;
    font-size: 28rpx;
    border: 1rpx solid #e5e5e5;
    border-radius: 8rpx;
    background: #f8f8f8;
    box-sizing: border-box;
    transition: border-color 0.3s;

    /* 聚焦状态 */
    &:focus {
      border-color: #007aff;
      background: #fff;
      outline: none;
    }

    /* 占位符样式 */
    &::placeholder {
      color: #999;
      font-size: 26rpx;
    }
  }
}
/* 运动专项样式 
.sport-dialog {
	
  .dialog-scroll {
      padding: 20rpx 30rpx;
    }
  
    .form-section {
      margin-bottom: 40rpx;
      padding: 20rpx 0;
      border-bottom: 1rpx solid #eee;
  
      .section-title {
        display: block;
        font-size: 32rpx;
        color: #333;
        margin-bottom: 25rpx;
        font-weight: 600;
      }
    }
  
    /* 单选组样式 
    .radio-group {
      display: flex;
      flex-wrap: wrap;
      
      .radio-item {
        width: 33.3%;
        margin: 15rpx 0;
        display: flex;
        align-items: center;
        
        .radio-label {
          margin-left: 10rpx;
          font-size: 28rpx;
        }
      }
    }
  
    /* 多选网格布局 
    .checkbox-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20rpx;
      
      .checkbox-item {
        display: flex;
        align-items: center;
        padding: 15rpx;
        background: #f8f8f8;
        border-radius: 8rpx;
        
        .checkbox-label {
          margin-left: 10rpx;
          font-size: 28rpx;
        }
      }
    }
  
    /* 经验输入框 
    .experience-field {
      width: 100%;
      min-height: 200rpx;
      padding: 20rpx;
      border: 1rpx solid #e5e5e5;
      border-radius: 8rpx;
      font-size: 28rpx;
      line-height: 1.6;
    }
  .checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 15rpx;
  }

  .checkbox-item {
    display: flex;
    align-items: center;
    padding: 8rpx 15rpx;
    border-radius: 6rpx;
    background: #f5f5f5;
  }

  .select-field {
    width: 100%;
    padding: 12rpx;
    border: 1rpx solid #e0e0e0;
    border-radius: 8rpx;
  }

  .textarea-field {
    width: 450rpx;
    padding: 14rpx;
    border: 1rpx solid #e0e0e0;
    border-radius: 8rpx;
    min-height: 120rpx;
  }
}
.sport-dialog .scroll-container {
  max-height: 65vh;
  min-height: 300rpx;
  padding: 0 20rpx;
}*/

/* 运动专项样式 */
.sport-dialog {
  .dialog-scroll {
    padding: 20rpx 30rpx;
  }

  .form-section {
    margin-bottom: 40rpx;
    padding: 20rpx 0;
    border-bottom: 1rpx solid #eee;

    .section-title {
      display: block;
      font-size: 32rpx;
      color: #333;
      margin-bottom: 25rpx;
      font-weight: 600;  /* 保持标题加粗 */
    }
  }

  /* 单选组样式 */
  .radio-group {
    display: flex;
    flex-wrap: wrap;

    .radio-item {
      width: 33.3%;
      margin: 15rpx 0;
      display: flex;
      align-items: center;

      .radio-label {
        margin-left: 10rpx;
        font-size: 28rpx;
        font-weight: 500;  /* 新增统一中等粗细 */
      }
    }
  }

  /* 多选网格布局 */
  .checkbox-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20rpx;

    .checkbox-item {
      display: flex;
      align-items: center;
      padding: 15rpx;
      background: #f8f8f8;
      border-radius: 8rpx;

      .checkbox-label {
        margin-left: 10rpx;
        font-size: 28rpx;
        font-weight: 500;  /* 新增统一中等粗细 */
      }
    }
  }

  /* 经验输入框 */
  .experience-field {
    width: 100%;
    min-height: 70rpx;
    padding: 20rpx;
    border: 1rpx solid #e5e5e5;
    border-radius: 8rpx;
    font-size: 28rpx;
    line-height: 1.6;
    font-weight: 400;  /* 明确常规体 */
  }

  .checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 15rpx;

    .checkbox-item {
      display: flex;
      align-items: center;
      padding: 8rpx 15rpx;
      border-radius: 6rpx;
      background: #f5f5f5;
    }
  }

  .select-field {
    width: 100%;
    padding: 123rpx;
    border: 1rpx solid #e0e0e0;
    border-radius: 8rpx;
  }

  .textarea-field {
    width: 450rpx;
    padding: 14rpx;
    border: 1rpx solid #e0e0e0;
    border-radius: 8rpx;
    min-height: 1230rpx;
  }

  .scroll-container {
    max-height: 65vh;
    min-height: 300rpx;
    padding: 0 20rpx;
  }
}

.sleep-dialog {
  .dialog-scroll {
    max-height: 70vh;
    overflow-y: auto;
    padding: 0 20rpx;
  }

  .time-picker-group {
    padding: 20rpx 0;
    
    .time-item {
      margin-bottom: 30rpx;
      
      .section-title {
        font-size: 28rpx;
        color: #666;
        margin-bottom: 15rpx;
      }
      
      .picker-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20rpx;
        border: 1rpx solid #e5e5e5;
        border-radius: 8rpx;
        font-size: 28rpx;
        color: #333;
      }
    }
  }

  /* 情绪网格优化 */
  .emotion-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15rpx;
    margin: 20rpx 0;
  }

  .emotion-item {
    width: 100%;
    height: 180rpx;  /* 固定高度 */
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 16rpx;  /* 修正圆角值 */
    background: #f8f8f8;
    transition: all 0.2s;
    overflow: hidden;  /* 防止内容溢出 */
    
    /* 选中状态 */
    &.checked {
      background: #e8f5e9;
      box-shadow: 0 4rpx 12rpx rgba(102, 187, 106, 0.1);
      border: 1rpx solid #66bb6a;
    }
  }

  .emotion-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx;
    transform: scale(0.9);  /* 整体缩小10% */
    
    .icon {
      font-size: 36rpx;  /* 缩小图标 */
      margin-bottom: 8rpx;
    }
    
    .text {
      font-size: 22rpx;  /* 缩小文字 */
      color: #666;
      line-height: 1.3;
      text-align: center;
    }
  }
}

/* 调整弹窗最小宽度 */
.edit-dialog {
  min-width: 600rpx !important;
}

/* 表单项间距 */
.uni-forms-item {
  margin-bottom: 30rpx;
}

/* 滚动容器高度 */
.form-scroll {
  max-height: 70vh;
}

.input-group {
  padding: 5rpx;
  .input-item {
    margin-bottom: 30rpx;
    .label {
      font-size: 28rpx;
      color: #666;
      margin-bottom: 10rpx;
    }
    input {
      height: 80rpx;
      padding: 0 0rpx;
      border: 1rpx solid #eee;
      border-radius: 8rpx;
      font-size: 20rpx;
    }
  }
}

.edit-btn {
  display: inline-block;
  padding: 8rpx 24rpx;
  border: 1rpx solid #42b983;
  border-radius: 30rpx;
  color: #42b983;
  font-size: 26rpx;
  transition: all 0.3s;
  
  /* 激活态效果 */
  &:active {
    background: rgba(66, 185, 131, 0.1);
    transform: scale(0.96);
  }
  
  /* 禁用状态 */
  &.disabled {
    opacity: 0.6;
    pointer-events: none;
  }
}
</style>