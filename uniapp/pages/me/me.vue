<template>
	<view style="padding: 20rpx;">
		<view class="box" style="display: flex; align-items: center; margin-bottom: 20rpx;">
			<image :src="user.avatar" style="width: 150rpx; border-radius: 50%;" mode="widthFix"></image>
			<view style="flex: 1; margin-left: 30rpx;">
				<view style="margin-bottom: 20rpx; font-size: 32rpx;">{{ user.username }}</view>
				<view style="color: #888;">{{ user.name }}</view>
			</view>
		</view>
		
	
		
		<view class="box">
			<navigator url="/pages/person/person" style="padding: 15rpx; border-bottom: 2rpx solid #eee;">
				<uni-icons type="person" size="18"></uni-icons>
				<text style="margin-left: 10rpx;">个人信息</text>
				<uni-icons type="right" color="#999" style="float: right;"></uni-icons>
			</navigator>
			<navigator url="/pages/allinfo/allinfo" style="padding: 15rpx; border-bottom: 2rpx solid #eee;">
				<uni-icons type="heart" size="18"></uni-icons>
				<text style="margin-left: 10rpx;">个性化收集</text>
				<uni-icons type="right" color="#999" style="float: right;"></uni-icons>
			</navigator>
			<navigator url="/pages/mybadge/mybadge" style="padding: 15rpx; border-bottom: 2rpx solid #eee;">
				<uni-icons type="medal" size="18"></uni-icons>
				<text style="margin-left: 10rpx;">勋章墙</text>
				<uni-icons type="right" color="#999" style="float: right;"></uni-icons>
			</navigator>
			<navigator url="/pages/aboutUs/aboutUs" style="padding: 15rpx; border-bottom: 2rpx solid #eee;">
				<uni-icons type="help" size="18"></uni-icons>
				<text style="margin-left: 10rpx;">关于我们</text>
				<uni-icons type="right" color="#999" style="float: right;"></uni-icons>
			</navigator>
			<navigator url="/pages/agreement/agreement" style="padding: 15rpx; border-bottom: 2rpx solid #eee;">
				<uni-icons type="info" size="18"></uni-icons>
				<text style="margin-left: 10rpx;">用户协议</text>
				<uni-icons type="right" color="#999" style="float: right;"></uni-icons>
			</navigator>
            <!-- 修改退出登录部分 -->
			<view style="padding: 15rpx; border-bottom: 2rpx solid #eee;" @click="showLogoutConfirm">
				<uni-icons type="undo" size="18"></uni-icons>
				<text style="margin-left: 10rpx;">退出登录</text>
				<uni-icons type="right" color="#999" style="float: right;"></uni-icons>
			</view>
		</view>
		
	</view>
</template>

<script>
	export default {
		data() {
			return {
				user: uni.getStorageSync('xm-user')
			}
		},
		onShow() {
			this.user = uni.getStorageSync('xm-user')
		},
		methods: {
            // 新增确认弹窗方法
			showLogoutConfirm() {
				uni.showModal({
					title: '退出确认',
					content: '确定要退出当前账号吗？',
					confirmColor: '#DD524D',
					success: (res) => {
						if (res.confirm) {
							this.doLogout()
						}
					}
				})
			},
			// 拆分退出逻辑
			doLogout() {
				uni.removeStorageSync('xm-user')
				uni.redirectTo({
					url: '/pages/login/login'
				})
				uni.$showMsg('已安全退出')
			}
		}
	}
</script>

<style>
.me-item {
	flex: 1; 
	display: flex; 
	flex-direction: column; 
	align-items: center;
	grid-gap: 10rpx;
}
</style>
