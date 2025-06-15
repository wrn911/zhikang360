<template>
  <view class="feedback-container">
    <!-- 食物反馈 -->
    <view class="form-item">
      <text class="item-title">食物反馈</text>
      <view v-for="(item, index) in foodList" :key="item.id" class="feedback-block">
        <text>{{ item.foodName }}</text>
        <radio-group
          :disabled="feedbackExists"
          @change="e => updateFoodFeedback(index, e.detail.value)"
        >
          <label><radio value="3" :checked="item.feedback === 3"/> 喜欢</label>
          <label><radio value="2" :checked="item.feedback === 2"/> 一般</label>
          <label><radio value="1" :checked="item.feedback === 1"/> 不喜欢</label>
        </radio-group>
      </view>
    </view>

    <!-- 运动反馈 -->
    <view class="form-item">
      <text class="item-title">运动反馈</text>
      <view v-for="(item, index) in exerciseList" :key="item.id" class="feedback-block">
        <text>{{ item.exerciseName }}</text>
        <radio-group
          :disabled="feedbackExists"
          @change="e => updateExerciseFeedback(index, e.detail.value)"
        >
          <label><radio value="3" :checked="item.feedback === 3"/> 喜欢</label>
          <label><radio value="2" :checked="item.feedback === 2"/> 一般</label>
          <label><radio value="1" :checked="item.feedback === 1"/> 不喜欢</label>
        </radio-group>
      </view>
    </view>

    <button
      class="submit-btn"
      :disabled="feedbackExists"
      @click="handleSubmit"
    >
      提交反馈
    </button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      foodList: [],
      exerciseList: [],
      feedbackExists: false, // 是否已反馈
    };
  },
  async onLoad() {
    await this.loadFeedbackStatus(); // 先看今天是否反馈过
    await this.loadRecommendList(); // 再加载推荐数据
  },
  methods: {
    async loadFeedbackStatus() {
      try {
        const res = await this.$request.get('/feedback/select');
        if (res.code === '200' && res.data && res.data.foodNumber) {
          this.feedbackExists = true;
          // 拆分 foodNumber 和 sportNumber
          const foodScores = res.data.foodNumber.toString().padStart(9, '2').split('').map(Number);
          const sportScores = res.data.sportNumber.toString().padStart(3, '2').split('').map(Number);
          this.foodList.forEach((item, index) => item.feedback = foodScores[index] || 2);
          this.exerciseList.forEach((item, index) => item.feedback = sportScores[index] || 2);
        }
      } catch (err) {
        console.error('反馈状态加载失败:', err);
      }
    },

    async loadRecommendList() {
      try {
        const res = await this.$request.get('/feedback/get_user_recommend_list');
        if (res.code === '200') {
          const defaultFeedback = (this.feedbackExists ? null : 2);
          this.foodList = res.data.foodFeedbackList.map(item => ({
            ...item,
            feedback: defaultFeedback
          }));
          this.exerciseList = res.data.exerciseFeedbackList.map(item => ({
            ...item,
            feedback: defaultFeedback
          }));
        }
      } catch (err) {
        console.error('推荐列表加载失败:', err);
      }
    },

    updateFoodFeedback(index, value) {
      if (!this.feedbackExists) this.foodList[index].feedback = parseInt(value);
    },

    updateExerciseFeedback(index, value) {
      if (!this.feedbackExists) this.exerciseList[index].feedback = parseInt(value);
    },

    async handleSubmit() {
      const foodFeedbackList = this.foodList.map(item => ({
        foodRecommendListId: item.id,
        feedback: item.feedback
      }));
      const exerciseFeedbackList = this.exerciseList.map(item => ({
        exerciseRecommendListId: item.id,
        feedback: item.feedback
      }));

      const payload = {
        foodFeedbackList,
        exerciseFeedbackList
      };

      try {
        const res = await this.$request.post('/feedback/changeWeight', payload);
        if (res.code === '200') {
          uni.showToast({ title: '提交成功' });
          this.feedbackExists = true;
        } else {
          uni.showToast({ title: res.message || '提交失败', icon: 'none' });
        }
      } catch (err) {
        console.error('提交失败:', err);
        uni.showToast({ title: '网络异常', icon: 'none' });
      }
    }
  }
};
</script>

<style>
.feedback-container {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.form-item {
  margin-bottom: 30px;
}

.item-title {
  font-size: 16px;
  color: #333;
  font-weight: bold;
  margin-bottom: 12px;
  display: block;
}

.feedback-block {
  margin-bottom: 15px;
  background-color: #fff;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.submit-btn {
  background-color: #07c160;
  color: white;
  border-radius: 25px;
  margin-top: 20px;
  font-size: 16px;
  padding: 12px 0;
  width: 100%;
}

.submit-btn:disabled {
  background-color: #ccc;
}
</style>

