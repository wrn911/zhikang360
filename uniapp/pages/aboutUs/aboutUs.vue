<template>
	<view class="container">
		<view class="header">
			<text class="title">关于我们</text>
			<view class="divider">
				<view class="divider-line"></view>
				<view class="divider-dot"></view>
				<view class="divider-line"></view>
			</view>
		</view>
		
		<view class="content-card">
			<view class="paragraph">
				<text class="paragraph-text">智康360是一款专注于健康管理的应用程序，旨在帮助用户全方位管理自己的健康状况。我们提供全面的健康数据记录、分析和管理功能，让您随时掌握自己的健康状态。</text>
			</view>
			
			<view class="paragraph">
				<text class="paragraph-text">我们的应用支持多种健康数据的记录，包括体重、身高、血压、血糖等关键指标，并提供直观的数据可视化展示，帮助您更好地理解自己的健康趋势。</text>
			</view>
			
			<view class="paragraph">
				<text class="paragraph-text">智康360还提供个性化的健康建议和提醒功能，根据您的健康数据和目标，为您制定合理的健康计划，并在适当的时候提醒您进行健康检查或数据记录。</text>
			</view>
			
			<view class="paragraph">
				<text class="paragraph-text">我们致力于保护用户的隐私和数据安全，采用先进的加密技术和严格的隐私政策，确保您的健康数据得到妥善保护。感谢您选择智康360，让我们一起开启健康生活的新篇章！</text>
			</view>
		</view>
		
		<view class="footer">
			<text class="footer-text">智康360 - 您的健康管家</text>
			<text class="version">版本 1.0.0</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {}
		},
		methods: {}
	}
</script>

<style>
.container {
  padding: 30rpx;
  min-height: 100vh;
  background: linear-gradient(to bottom, #f8f9fa, #e9f2ef);
}

/* 标题样式 */
.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40rpx;
}

.title {
  font-size: 40rpx;
  font-weight: bold;
  color: #4CAF50;
  margin-bottom: 20rpx;
}

.divider {
  display: flex;
  align-items: center;
  width: 200rpx;
  margin: 10rpx 0 30rpx;
}

.divider-line {
  flex: 1;
  height: 2rpx;
  background-color: #4CAF50;
}

.divider-dot {
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
  background-color: #4CAF50;
  margin: 0 10rpx;
}

/* 内容卡片 */
.content-card {
  background-color: #fff;
  border-radius: 20rpx;
  padding: 40rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 10rpx 20rpx rgba(0, 0, 0, 0.05);
}

.paragraph {
  margin-bottom: 30rpx;
}

.paragraph:last-child {
  margin-bottom: 0;
}

.paragraph-text {
  font-size: 28rpx;
  line-height: 50rpx;
  color: #333;
  text-align: justify;
}

/* 首行缩进处理 */
.paragraph-text {
  display: block;
  text-indent: 2em;
}

/* 页脚 */
.footer {
  text-align: center;
  padding: 40rpx 0;
}

.footer-text {
  font-size: 26rpx;
  color: #4CAF50;
  display: block;
  margin-bottom: 10rpx;
}

.version {
  font-size: 24rpx;
  color: #999;
}
</style>
