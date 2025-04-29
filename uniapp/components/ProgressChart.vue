<template>
  <view class="chart-wrapper">
		<view class="chart-title">{{ title }}</view>
		<view class="progress-container">
			<canvas 
			  canvas-id="progressCanvas" 
			  class="progress-canvas"
			  @touchstart.prevent
			></canvas>
			<view class="progress-text">{{ percentage }}<text class="percentage-symbol">%</text></view>
			<view class="progress-label">已完成 {{ completed }}/{{ total }}</view>
		</view>
  </view>
</template>

<script>
export default {
  props: {
	title: {
	  type: String,
	  required: true
	},
    completed: {
      type: Number,
      required: true
    },
    total: {
      type: Number,
      required: true
    }
  },
  computed: {
    percentage() {
      return Math.round((this.completed / this.total) * 100);
    }
  },
  mounted() {
    this.drawProgress();
  },
  methods: {
    drawProgress() {
      const ctx = uni.createCanvasContext('progressCanvas', this);
      // 使用容器尺寸的一半作为圆心坐标，确保居中
      const canvasSize = 200;
      const centerX = canvasSize / 2;
      const centerY = canvasSize / 2;
      const radius = 80;
      const lineWidth = 15;
      
      // 绘制背景圆环
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
      ctx.setStrokeStyle('#e0e0e0');
      ctx.setLineWidth(lineWidth);
      ctx.setLineCap('round');
      ctx.stroke();
      
      // 绘制进度圆环
      const percentage = this.percentage / 100;
      const startAngle = -0.5 * Math.PI; // 从顶部开始
      const endAngle = startAngle + (percentage * 2 * Math.PI);
      
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, startAngle, endAngle);
      ctx.setStrokeStyle('#4caf50'); // 绿色
      ctx.setLineWidth(lineWidth);
      ctx.setLineCap('round');
      ctx.stroke();
      
      // 绘制中心圆形填充
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius - lineWidth, 0, 2 * Math.PI);
      ctx.setFillStyle('#ffffff');
      ctx.fill();
      
      ctx.draw();
    }
  },
  watch: {
    completed() {
      this.drawProgress();
    },
    total() {
      this.drawProgress();
    }
  }
}
</script>

<style scoped>
.chart-wrapper {
  padding: 24rpx;
  border-radius: 16rpx;
  background-color: white;
  box-shadow: none;
}

.chart-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 30rpx;
  text-align: center;
  position: relative;
  padding-bottom: 16rpx;
}

.chart-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60rpx;
  height: 6rpx;
  background: linear-gradient(to right, #4CAF50, #8BC34A);
  border-radius: 3rpx;
}

.progress-container {
  position: relative;
  width: 200px;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
}

.progress-canvas {
  width: 200px;
  height: 200px;
}

.progress-text {
  position: absolute;
  font-size: 48rpx;
  font-weight: bold;
  color: #4CAF50;
  display: flex;
  align-items: center;
  justify-content: center;
}

.percentage-symbol {
  font-size: 28rpx;
  margin-left: 4rpx;
  font-weight: normal;
  opacity: 0.8;
}

.progress-label {
  position: absolute;
  bottom: -40rpx;
  font-size: 24rpx;
  color: #666;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  text-align: center;
  width: 100%;
  left: 0;
}
</style>