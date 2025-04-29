<template>
	<view style="padding: 20rpx;">
		<view class="box">
			<view style="text-align: center; font-size: 36rpx; font-weight: bold; margin-bottom: 20rpx;">关于我们</view>
			
			<!-- 修改后的段落部分 -->
			<view class="content">
				<text class="paragraph">　　{{ paragraph1 }}</text>
				<text class="paragraph">　　{{ paragraph2 }}</text>
				<text class="paragraph">　　{{ paragraph3 }}</text>
				<text class="paragraph">　　{{ paragraph4 }}</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				// 拆分段落数据
				paragraph1: '在现代社会，人们的亚健康问题（如肥胖、失眠、慢性疲劳）普遍存在，这通常是饮食不规律，缺乏运动和错误的生活作息造成的。所以越来越多的人开始关注自身健康与身材管理问题。',
				paragraph2: '而传统的软件存在诸多问题，如：只关注体重，饮食，运动，睡眠中的一种，缺乏综合分析；软件通常提供的是通用化方案，无法提出个性化方案；激励机制较少，导致用户很难长期坚持。',
				paragraph3: '因此，迫切需要一款能够整合饮食、运动及睡眠并提供合理化建议和个性化方案的健康管理软件。',
				paragraph4: '我们致力于打造一款基于AI的智能健康管理软件，整合饮食、运动、睡眠三大模块，解决用户身材管理、作息调控和压力缓解需求，提供科学化、可持续的健康生活方式。'
			}
		}
	}
</script>

<style>
	/* 新增样式 */
	.content {
		font-size: 28rpx;
		color: #333;
	}
	
	.paragraph {
		display: block;
		line-height: 50rpx;
		margin-bottom: 30rpx;  /* 段落间距 */
		text-indent: 0;  /* 强制取消默认缩进 */
	}
	
	/* 全平台兼容的首行缩进方案 */
	.paragraph::first-line {
		text-indent: 2em;  /* H5端生效 */
	}
</style>
