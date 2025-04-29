<<template>
  <view class="container">
    <view class="header">
      <text class="title">🏅 勋章墙</text>
    </view>
    
    <!-- 勋章展示区 -->
    <view class="badge-grid">
      <view v-for="badge in allBadges" :key="badge.id" class="badge-item">
        <!-- 图片交互区 -->
        <view class="image-wrapper" @touchstart="showDescription(badge)" @touchend="hideDescription">
          <image 
            :src="badge.url" 
            :class="['badge-image', { 'grayscale': !badge.isEarned }]"
            mode="aspectFit"
          />
        </view>
        <text class="badge-name">{{ badge.name }}</text>
        
        <!-- 描述浮层 -->
        <view v-if="activeDescription === badge.id" class="description-box">
          {{ badge.description }}
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      allBadges: [],       // 合并后的勋章列表
      activeDescription: null, // 当前显示的描述ID
      timer: null         // 用于延迟隐藏
    };
  },
  mounted() {
    this.loadBadges();
  },
  methods: {
    async loadBadges() {
      try {
        const res = await this.$request.get(
           '/badgeStandard/selectByUserId'
        );
        if(res.code === '200'){
			// 合并数据并添加状态标识
			const earnedIds = new Set(res.data.earned.map(b => b.id));
			this.allBadges = [
			  ...res.data.earned.map(b => ({ ...b, isEarned: true })),
			  ...res.data.unowned.map(b => ({ ...b, isEarned: false }))
			];
		}else{
			uni.showToast({ title: '数据加载失败', icon: 'none' });
		}
      } catch (err) {
        uni.showToast({ title: '数据加载失败', icon: 'none' });
      }
    },
    showDescription(badge) {
      this.activeDescription = badge.id;
      // 3秒后自动隐藏
      this.timer = setTimeout(() => {
        this.activeDescription = null;
      }, 3000);
    },
    hideDescription() {
      clearTimeout(this.timer);
      this.activeDescription = null;
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20rpx;
  background: #f5f5f5;
  min-height: 100vh;
}

.header {
  text-align: center;
  padding: 40rpx 0;
}

.title {
  font-size: 44rpx;
  font-weight: bold;
  color: #333;
}

.badge-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 20rpx;
}

.badge-item {
  width: 220rpx;
  margin: 20rpx;
  position: relative;
  text-align: center;
}

.image-wrapper {
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.image-wrapper:active {
  transform: scale(0.95);
}

.badge-image {
  width: 160rpx;
  height: 160rpx;
}

.grayscale {
  filter: grayscale(100%);
  opacity: 0.7;
}

.badge-name {
  display: block;
  margin-top: 20rpx;
  font-size: 28rpx;
  color: #666;
}

.description-box {
  position: absolute;
  bottom: 120%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 16rpx 24rpx;
  border-radius: 8rpx;
  font-size: 24rpx;
  white-space: nowrap;
  z-index: 10;
}

.description-box::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -8rpx;
  border: 8rpx solid transparent;
  border-top-color: rgba(0,0,0,0.8);
}
</style>