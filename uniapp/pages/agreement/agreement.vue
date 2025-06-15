<template>
	<view class="container">
		<view class="header">
			<text class="title">用户协议</text>
			<view class="divider">
				<view class="divider-line"></view>
				<view class="divider-dot"></view>
				<view class="divider-line"></view>
			</view>
		</view>
		
		<view class="content-card">
			<view class="paragraph">
				<text class="paragraph-text">欢迎使用智康360健康管理应用。在使用本应用前，请您仔细阅读以下用户协议条款。使用本应用即表示您已同意接受本协议的所有条款和条件。本协议构成您与智康360之间就应用使用达成的协议。</text>
			</view>
			
			<view class="section">
				<text class="section-title">1. 服务条款</text>
				<text class="paragraph-text">智康360提供健康数据记录、分析和管理服务。我们保留随时修改、暂停或终止部分或全部服务的权利。服务变更或终止前，我们将通过适当方式通知您。</text>
			</view>
			
			<view class="section">
				<text class="section-title">2. 用户隐私</text>
				<text class="paragraph-text">我们重视您的隐私保护。我们会收集和使用您的健康数据以提供服务，但承诺采取合理措施保护您的个人信息安全。详细隐私政策请参阅我们的《隐私政策》。</text>
			</view>
			
			<view class="section">
				<text class="section-title">3. 用户责任</text>
				<text class="paragraph-text">您应对账号安全负责，并对使用该账号的所有活动承担责任。您同意不使用本应用从事任何违法或不当行为。</text>
			</view>
			
			<view class="section">
				<text class="section-title">4. 免责声明</text>
				<text class="paragraph-text">本应用提供的健康建议仅供参考，不构成医疗诊断或治疗建议。如有健康问题，请咨询专业医疗人员。</text>
			</view>
			
			<view class="section">
				<text class="section-title">5. 协议修改</text>
				<text class="paragraph-text">我们保留随时修改本协议的权利。修改后的协议将通过应用内通知或其他方式告知用户。继续使用本应用即表示您接受修改后的协议。</text>
			</view>
		</view>
		
		<view class="footer">
			<text class="footer-text">如有任何问题，请联系客服</text>
			<text class="contact">support@zhikang360.com</text>
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

.section {
  margin-bottom: 30rpx;
}

.section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 30rpx;
  font-weight: bold;
  color: #4CAF50;
  margin-bottom: 15rpx;
  display: block;
}

.paragraph-text {
  font-size: 28rpx;
  line-height: 50rpx;
  color: #333;
  text-align: justify;
  display: block;
}

/* 页脚 */
.footer {
  text-align: center;
  padding: 40rpx 0;
}

.footer-text {
  font-size: 26rpx;
  color: #666;
  display: block;
  margin-bottom: 10rpx;
}

.contact {
  font-size: 26rpx;
  color: #4CAF50;
  font-weight: bold;
}
</style>
