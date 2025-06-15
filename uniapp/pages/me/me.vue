<template>
	<view class="container">
		<!-- 用户信息卡片 -->
		<view class="user-card">
			<image :src="user.avatar" class="avatar" mode="aspectFill"></image>
			<view class="user-info">
				<text class="username">{{ user.username }}</text>
				<text class="name">{{ user.name }}</text>
			</view>
		</view>
		
		<!-- 菜单列表 -->
		<view class="menu-card">
			<navigator url="/pages/person/person" class="menu-item" hover-class="menu-item-hover">
				<view class="menu-icon">
					<uni-icons type="person" size="22" color="#4CAF50"></uni-icons>
				</view>
				<text class="menu-text">个人信息</text>
				<uni-icons type="right" size="18" color="#bbb" class="arrow"></uni-icons>
			</navigator>
			
			<navigator url="/pages/allinfo/allinfo" class="menu-item" hover-class="menu-item-hover">
				<view class="menu-icon">
					<uni-icons type="heart" size="22" color="#4CAF50"></uni-icons>
				</view>
				<text class="menu-text">个性化收集</text>
				<uni-icons type="right" size="18" color="#bbb" class="arrow"></uni-icons>
			</navigator>
			
			<navigator url="/pages/mybadge/mybadge" class="menu-item" hover-class="menu-item-hover">
				<view class="menu-icon">
					<uni-icons type="medal" size="22" color="#4CAF50"></uni-icons>
				</view>
				<text class="menu-text">勋章墙</text>
				<uni-icons type="right" size="18" color="#bbb" class="arrow"></uni-icons>
			</navigator>
			
			<navigator url="/pages/feedBack/feedBack" class="menu-item" hover-class="menu-item-hover">
				<view class="menu-icon">
					<uni-icons type="help" size="22" color="#4CAF50"></uni-icons>
				</view>
				<text class="menu-text">反馈采集</text>
				<uni-icons type="right" size="18" color="#bbb" class="arrow"></uni-icons>
			</navigator>
		</view>
		
		<!-- 关于与设置 -->
		<view class="menu-card">
			<navigator url="/pages/aboutUs/aboutUs" class="menu-item" hover-class="menu-item-hover">
				<view class="menu-icon">
					<uni-icons type="info" size="22" color="#4CAF50"></uni-icons>
				</view>
				<text class="menu-text">关于我们</text>
				<uni-icons type="right" size="18" color="#bbb" class="arrow"></uni-icons>
			</navigator>
			
			<navigator url="/pages/agreement/agreement" class="menu-item" hover-class="menu-item-hover">
				<view class="menu-icon">
					<uni-icons type="info" size="22" color="#4CAF50"></uni-icons>
				</view>
				<text class="menu-text">用户协议</text>
				<uni-icons type="right" size="18" color="#bbb" class="arrow"></uni-icons>
			</navigator>
			
			<view class="menu-item logout-item" @click="showLogoutConfirm" hover-class="menu-item-hover">
				<view class="menu-icon">
					<uni-icons type="undo" size="22" color="#FF5252"></uni-icons>
				</view>
				<text class="menu-text logout-text">退出登录</text>
				<uni-icons type="right" size="18" color="#bbb" class="arrow"></uni-icons>
			</view>
		</view>
		
		<!-- 版权信息 -->
		<view class="footer">
			<text>智康360 - 您的健康管家</text>
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
.container {
  padding: 30rpx;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
}

/* 用户信息卡片 */
.user-card {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #ffffff, #fafbfc);
  border-radius: 24rpx;
  padding: 36rpx;
  margin-bottom: 32rpx;
  box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.08);
  border: 1rpx solid rgba(226, 232, 240, 0.6);
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  border: 3rpx solid rgba(59, 130, 246, 0.2);
  box-shadow: 0 6rpx 16rpx rgba(71, 85, 105, 0.12);
}

.user-info {
  flex: 1;
  margin-left: 30rpx;
}

.username {
  font-size: 36rpx;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 12rpx;
  display: block;
}

.name {
  font-size: 28rpx;
  color: #64748b;
  display: block;
}

/* 菜单卡片 */
.menu-card {
  background: linear-gradient(135deg, #ffffff, #fafbfc);
  border-radius: 24rpx;
  margin-bottom: 32rpx;
  padding: 12rpx 0;
  box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.08);
  border: 1rpx solid rgba(226, 232, 240, 0.6);
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 32rpx;
  position: relative;
  transition: all 0.3s ease;
}

.menu-item::after {
  content: '';
  position: absolute;
  left: 32rpx;
  right: 32rpx;
  bottom: 0;
  height: 1rpx;
  background: linear-gradient(90deg, transparent, rgba(226, 232, 240, 0.6), transparent);
}

.menu-item:last-child::after {
  display: none;
}

.menu-item-hover {
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
  transform: translateX(4rpx);
}

.menu-icon {
  width: 56rpx;
  height: 56rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-right: 24rpx;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.05));
  border-radius: 16rpx;
  border: 1rpx solid rgba(59, 130, 246, 0.1);
}

.menu-text {
  flex: 1;
  font-size: 30rpx;
  color: #1e293b;
  font-weight: 500;
}

.arrow {
  margin-left: 10rpx;
}

/* 退出登录按钮 */
.logout-text {
  color: #ef4444;
  font-weight: 500;
}

.logout-item .menu-icon {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(239, 68, 68, 0.05));
  border: 1rpx solid rgba(239, 68, 68, 0.1);
}

/* 页脚 */
.footer {
  text-align: center;
  padding: 48rpx 0;
  font-size: 26rpx;
  color: #94a3b8;
  font-weight: 500;
}
</style>
