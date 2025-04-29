<template>
	<view>
		<view class="v">
		<navigator class="food" url="/pages/food/food1"
			hover-class="navigator-hover">
			<button type="default">饮食</button>
		</navigator>
		</view>
		<view class="v">
		<navigator class="sport" url="/pages/sport/sport"
			hover-class="navigator-hover">
			<button type="default">运动</button>
		</navigator>
		</view>
		<view class="v">
		<navigator class="sleep" url="/pages/sleep/sleep"
			hover-class="navigator-hover">
			<button type="default">睡眠</button>
		</navigator>
		</view>
		<view class="v">
		<navigator class="ai" url="/pages/aihelper/aihelper"
			hover-class="navigator-hover">
			<button type="default">AI答疑助手</button>
		</navigator>
        </view>


	</view>
</template>
</template>

<script>
	export default {
		data() {
			return {

			}
		},
		methods: {

		}
	}
</script>

<style>
.v{
	height: 180rpx;
	width: 700rpx;
}	

/* 修改样式 */
.food {
  /* 布局属性 */
  width: 500rpx;
  height: 160rpx;
  margin: 80rpx auto;
  
  /* 背景样式 */
  background-color: goldenrod !important;
  border-radius: 8rpx;
  
  /* 文字相关 */
  text-align: center;
  line-height: 80rpx;
}

/* 修改按钮样式 */
.food button {
  color: white;
  font-size: 28px;
  background-color: transparent !important;
}

/* 修改样式 */
.sport {
  /* 布局属性 */
  width: 500rpx;
  height: 160rpx;
  margin: 80rpx auto;
  
  /* 背景样式 */
  background-color: cornflowerblue;
  border-radius: 8rpx;
  
  /* 文字相关 */
  text-align: center;
  line-height: 80rpx;
}

/* 修改按钮样式 */
.sport button {
  color: white;
  font-size: 28px;
  background-color: transparent !important;
}
/* 修改样式 */
.sleep {
  /* 布局属性 */
  width: 500rpx;
  height: 160rpx;
  margin: 80rpx auto;
  
  /* 背景样式 */
  background-color: springgreen !important;
  border-radius: 8rpx;
  
  /* 文字相关 */
  text-align: center;
  line-height: 80rpx;
}

/* 修改按钮样式 */
.sleep button {
  color: white;
  font-size: 28px;
  background-color: transparent !important;
}
/* 修改样式 */
.ai {
  /* 布局属性 */
  width: 500rpx;
  height: 160rpx;
  margin: 80rpx auto;
  
  /* 背景样式 */
  background-color: turquoise;
  border-radius: 8rpx;
  
  /* 文字相关 */
  text-align: center;
  line-height: 80rpx;
}

/* 修改按钮样式 */
.ai button {
  color: white;
  font-size: 28px;
  background-color: transparent !important;
}





























</style>