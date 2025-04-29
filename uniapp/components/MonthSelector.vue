<template>
  <view class="month-selector">
    <view class="month-display">
      <text class="month-text">{{ formattedDate }}</text>
    </view>
    <view class="month-controls">
      <view class="control-button" @click="prevMonth">
        <text class="control-icon">←</text>
      </view>
      <view class="control-button" @click="nextMonth">
        <text class="control-icon">→</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      currentDate: new Date(),
    };
  },
  computed: {
    formattedDate() {
      const year = this.currentDate.getFullYear();
      const month = this.currentDate.getMonth() + 1; // 月份从0开始
      return `${year}年${month}月`;
    },
  },
  methods: {
    prevMonth() {
      const date = new Date(this.currentDate);
      date.setMonth(date.getMonth() - 1);
      this.currentDate = date;
      this.emitMonthChange();
    },
    nextMonth() {
      const date = new Date(this.currentDate);
      date.setMonth(date.getMonth() + 1);
      this.currentDate = date;
      this.emitMonthChange();
    },
    emitMonthChange() {
      // 发射事件，将选择的年份和月份传递给父组件
      this.$emit('month-change', {
        year: this.currentDate.getFullYear(),
        month: this.currentDate.getMonth() + 1,
      });
    },
  },
};
</script>

<style>
.month-selector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx 30rpx;
  background-color: white;
  border-radius: 16rpx;
  margin: 16rpx 12rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.month-selector:active {
  transform: translateY(-2rpx);
  box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.1);
}

.month-selector::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  height: 4rpx;
  width: 100%;
  background: linear-gradient(to right, #4CAF50, #8BC34A);
  opacity: 0.7;
}

.month-display {
  flex: 1;
  text-align: center;
}

.month-text {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  letter-spacing: 2rpx;
}

.month-controls {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.control-button {
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 10rpx;
  color: #4CAF50;
  transition: all 0.3s ease;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.control-icon {
  font-size: 32rpx;
  font-weight: bold;
}

.control-button:active {
  transform: scale(0.9);
  background-color: #e8f5e9;
}
</style>