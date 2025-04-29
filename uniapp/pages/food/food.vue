<template>
  <view class="container">
    <!-- 顶部数据展示 -->
   <view class="summary-card">
      <view class="chart-box">
        <qiun-data-charts 
          type="ring" 
          :chartData="calorieChart" 
          :opts="chartOpts"
        />
      </view>
      <view class="progress-bars">
        <view class="progress-item">
          <text>蛋白质 {{nutritionData.protein}}g</text>
          <view class="progress-bar">
            <view class="progress-inner" :style="{width: proteinPercent}"></view>
          </view>
        </view>
        <view class="progress-item">
          <text>脂肪 {{nutritionData.fat}}g</text>
          <view class="progress-bar">
            <view class="progress-inner" :style="{width: fatPercent}"></view>
          </view>
        </view>
        <view class="progress-item">
          <text>碳水 {{nutritionData.carbs}}g</text>
          <view class="progress-bar">
            <view class="progress-inner" :style="{width: carbsPercent}"></view>
          </view>
        </view>
      </view>
    </view>

    <!-- 餐次卡片 -->
    <view v-for="meal in meals" :key="meal.type" class="meal-card">
      <view class="meal-header">{{meal.name}}推荐</view>
      
      <!-- 推荐部分 -->
      <view class="recommend-section">
        <text class="calorie-tip">推荐摄入：{{meal.recommend.totalCal}}大卡</text>
        <view v-for="(food,idx) in meal.recommend.foods" :key="idx" class="food-item">
          <text>{{food.name}}</text>
          <text>{{food.weight}}g</text>
        </view>
      </view>

      <!-- 已打卡部分 -->
      <view class="checkin-section" v-if="meal.checkin">
        <view class="checkin-header">
          <text>已摄入 {{meal.checkin.totalCal}}大卡</text>
          <button @click="openCheckin(meal.type)">立即打卡</button>
        </view>
        <view v-for="(food,idx) in meal.checkin.foods" :key="idx" class="food-item">
          <text>{{food.name}}</text>
          <text>{{food.weight}}g</text>
        </view>
      </view>
      <view v-else class="no-checkin">
        <text>尚未打卡</text>
        <button @click="openCheckin(meal.type)">立即打卡</button>
      </view>
    </view>
  </view>
</template>

<script>
// 模拟接口数据
const mockRecommendations = {
  breakfast: {
    totalCal: 450,
    foods: [
      {name: "全麦面包", weight: 100, cal: 246},
      {name: "牛奶", weight: 200, cal: 108}
    ]
  },
  lunch: {/* 类似结构 */},
  dinner: {/* 类似结构 */}
}

const mockCheckins = {
  breakfast: {
    totalCal: 420,
    foods: [
      {name: "煎鸡蛋", weight: 80, cal: 196},
      {name: "燕麦粥", weight: 150, cal: 224}
    ]
  }
}

export default {
  data() {
    return {
      // 营养数据
      nutritionData: {
        totalCal: 1800,
        consumedCal: 850,
        protein: 45,
        fat: 30,
        carbs: 120
      },
      meals: [
        { type: 'breakfast', name: '早餐', recommend: {}, checkin: null },
        { type: 'lunch', name: '午餐', recommend: {}, checkin: null },
        { type: 'dinner', name: '晚餐', recommend: {}, checkin: null }
      ],
	  // 新增图表配置
	        chartOpts: {
	          title: {
	            name: "今日总摄入",
	            fontSize: 16,
	            color: "#333",
	            offsetY: 10
	          },
	          extra: {
	            ring: {
	              ringWidth: 15,
	              centerText: {
	                title: "1800大卡",
	                titleColor: "#4D8AFE",
	                titleFontSize: 18,
	                subTitle: "已摄入 850大卡",
	                subTitleColor: "#666",
	                subTitleFontSize: 12
	              },
	              labelText: false
	            },
	            legend: {
	              show: false
	            }
	          }
	        }
    }
  },
    computed: {
      calorieChart() {
        const total = this.nutritionData.totalCal
        const consumed = this.nutritionData.consumedCal
        const remaining = Math.max(total - consumed, 0)
        
        return {
          categories: ["已摄入", "剩余"],
          series: [{
            data: [
              {
                name: "已摄入",
                value: Math.min(consumed, total),
                color: consumed > total ? "#FF6B6B" : "#4D8AFE"
              },
              {
                name: "剩余",
                value: remaining,
                color: remaining > 0 ? "#EEF2FF" : "#FF6B6B"
              }
            ]
          }]
        }
      },
      // 营养百分比计算
      proteinPercent() { return (this.nutritionData.protein / 60 * 100) + '%' },
      fatPercent() { return (this.nutritionData.fat / 40 * 100) + '%' },
      carbsPercent() { return (this.nutritionData.carbs / 150 * 100) + '%' }
    },
    mounted() {
      this.initData()
      // 动态更新中间文字
      this.chartOpts.extra.ring.centerText.title = `${this.nutritionData.totalCal}大卡`
      this.chartOpts.extra.ring.centerText.subTitle = `已摄入 ${this.nutritionData.consumedCal}大卡`
    },
  methods: {
    async initData() {
      // 获取推荐数据
      this.meals.forEach(async meal => {
        const res = await this.getRecommendation(meal.type)
        meal.recommend = res
      })
      
      // 获取打卡数据
      this.meals.forEach(async meal => {
        const res = await this.getCheckinRecord(meal.type)
        meal.checkin = res
      })
    },

    // 示例接口定义
    async getRecommendation(mealType) {
      // 实际接口请求示例：
      // const res = await uni.request({
      //   url: `/api/recommendations/${mealType}`,
      //   method: 'GET'
      // })
      return mockRecommendations[mealType] || null
    },

    async getCheckinRecord(mealType) {
      // 实际接口请求示例：
      // const res = await uni.request({
      //   url: `/api/checkins?date=${today}&meal=${mealType}`,
      //   method: 'GET'
      // })
      return mockCheckins[mealType] || null
    },

    openCheckin(mealType) {
      uni.showActionSheet({
        itemList: ['手动输入', '拍照记录'],
        success: ({tapIndex}) => {
          const routes = ['/pages/manual/manual', '/pages/imgUpload/imgUpload']
          uni.navigateTo({
            url: `${routes[tapIndex]}?mealType=${mealType}`
          })
        }
      })
    }
  }
}
</script>

<style>
/* 主要样式 */
.container {
  padding: 20rpx;
}

.summary-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.chart-box {
  height: 350rpx;
  position: relative;
}

.progress-item {
  margin: 15rpx 0;}

.progress-bar {
  height: 24rpx;
  background: #f5f5f5;
  border-radius: 12rpx;
  overflow: hidden;
}

.progress-inner {
  background: #4D8AFE;
  transition: width 0.3s ease;
}

.meal-card {
  background: #fff;
  border-radius: 20rpx;
  margin-bottom: 30rpx;
  padding: 30rpx;
}

.food-item {
  display: flex;
  justify-content: space-between;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eee;
}

.checkin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20rpx 0;
}
</style>
