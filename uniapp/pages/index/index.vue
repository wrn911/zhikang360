<template>
  <view class="container">
    <!-- 页面标题
    <view class="page-header">
      <text class="page-title">健康数据</text>
      <text class="page-subtitle">您的健康状况一目了然</text>
    </view> -->
    
    <!-- 轮播图 -->
    <swiper class="swiper" :autoplay="true" :interval="3000" :circular="true" indicator-dots indicator-color="rgba(255,255,255,0.4)" indicator-active-color="#4CAF50">
      <swiper-item v-for="(item, index) in swiperList" :key="index">
        <image :src="item.imgUrl" mode="scaleToFill" class="swiper-img" />
      </swiper-item>
    </swiper>

    <!-- 健康数据卡片 -->
    <view class="health-cards">
      <view 
        v-for="(item, index) in healthData" 
        :key="index"
        class="card"
      >
        <view class="card-icon" :class="`icon-${index}`">
          <text class="icon-text">{{ item.title.charAt(0) }}</text>
        </view>
        <view class="card-content">
          <text class="card-title">{{ item.title }}</text>
          <text class="card-value">{{ item.value }}{{ item.unit }}</text>
          <text class="card-time">更新于 {{ item.updateTime }}</text>
        </view>
      </view>
    </view>

    <!-- 页面底部装饰 -->
    <view class="page-footer">
      <text class="footer-text">智康360 - 您的健康数据中心</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      swiperList: [
        { imgUrl: '/static/imgs/1330814.png' },
        { imgUrl: '/static/imgs/1330798.png' },
        { imgUrl: '/static/imgs/1330799.png' },
        { imgUrl: '/static/imgs/1330801.png' },
		{ imgUrl: '/static/imgs/1330803.png' },
		{ imgUrl: '/static/imgs/1330806.png' },
		{ imgUrl: '/static/imgs/1346349.png' }
      ],
	  user: {},  // 移除非同步初始化
      healthData: [
        { title: '身高', value: '-', unit: 'cm', color: '#c8e6c9', updateTime: '-' },
        { title: '体重', value: '-', unit: 'kg', color: '#bbdefb', updateTime: '-' },
        { title: '血压', value: '-', unit: 'mmHg', color: '#ffccbc', updateTime: '-' },
        { title: '血糖', value: '-', unit: 'mmol/L', color: '#e1bee7', updateTime: '-' }
      ]
    }
  },

  onShow() {
	this.initializeUser()
    this.loadHealthData()
  },

  methods: {
	  // 与第二个文件相同的用户初始化逻辑
	initializeUser() {
	    const storedUser = uni.getStorageSync('xm-user')
	    if (!storedUser?.id) {
	     uni.redirectTo({ url: '/pages/login/login' })
	     return
	    }
	    this.user = JSON.parse(JSON.stringify(storedUser))
	},
    async loadHealthData() {
      try {
        // 修正1：正确处理 uni.request 返回结构（返回值是 [error, response] 数组）
		const res = await this.$request.get(`/user-basic-info/selectById/${this.user.id}`)
		console.log('响应数据:', res.data); // 打印 data 字段内容
    
        // 修正2：检查网络错误和HTTP状态码
        //if (err || response.statusCode !== 200) {
          //throw new Error('请求失败');
        //}
    
        //const res = response.data; // 这里获取真正的后端响应数据
    
        if (res.code === '200') {
          // 修正3：使用 $set 或直接赋值确保响应式更新
          this.$set(this, 'healthData', this.healthData.map(item => {
            // 修正4：处理可能不存在的字段（使用可选链和默认值）
            const mappings = {
              '身高': { value: res.data?.height ?? '暂无', time: res.data?.updateTimeH },
              '体重': { value: res.data?.weight ?? '暂无', time: res.data?.updateTimeW },
              '血压': { value: res.data?.bloodPressure ?? '暂无', time: res.data?.updateTimeBp },
              '血糖': { value: res.data?.bloodSugar ?? '暂无', time: res.data?.updateTimeBs }
            };
    
            // 修正5：防止访问不存在的映射项
            const target = mappings[item.title] || { value: '数据异常', time: null };
            
            return {
              ...item,
              value: target.value,
              updateTime: target.time ? this.formatTime(target.time) : '无记录'
            };
          }));
        } else {
          uni.showToast({ title: res.msg || '数据异常', icon: 'none' });
        }
      } catch (error) {
        console.error('健康数据加载失败:', error);
        uni.showToast({ title: '数据加载失败', icon: 'none' });
      }
    },



    /*formatTime(timestamp) {
      if (!timestamp) return '-'
      const date = new Date(timestamp)
      return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
    },*/
	// 修改后的时间格式化方法
	formatTime(timestamp) {
	  if (!timestamp) return '-'
	  const date = new Date(timestamp)
	  
	  // 补零函数
	  const pad = n => n.toString().padStart(2, '0')
	  
	  return `
	    ${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} 
	    ${pad(date.getHours())}:${pad(date.getMinutes())}
	  `.replace(/\s+/g, ' ') // 压缩多余空格
	},

  }
}
</script>

<style lang="scss">
.container {
  padding: 30rpx;
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc, #f1f5f9);
}

/* 页面标题 */
.page-header {
  margin-bottom: 30rpx;
  
  .page-title {
    font-size: 48rpx;
    font-weight: bold;
    color: #4CAF50;
    display: block;
    margin-bottom: 10rpx;
  }
  
  .page-subtitle {
    font-size: 28rpx;
    color: #666;
    display: block;
  }
}

/* 轮播图 */
.swiper {
  height: 350rpx;
  border-radius: 24rpx;
  overflow: hidden;
  box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.12);
  margin-bottom: 40rpx;
  border: 1rpx solid rgba(226, 232, 240, 0.6);
  
  &-img {
    width: 100%;
    height: 100%;
  }
}

/* 健康数据卡片 */
.health-cards {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  margin-bottom: 40rpx;
  
  .card {
    display: flex;
    align-items: center;
    padding: 36rpx;
    border-radius: 24rpx;
    background: linear-gradient(135deg, #ffffff, #fafbfc);
    box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.08);
    border: 1rpx solid rgba(226, 232, 240, 0.6);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    
    &:active {
      transform: translateY(1rpx) scale(0.99);
      box-shadow: 0 4rpx 12rpx rgba(71, 85, 105, 0.12);
    }
    
    .card-icon {
      width: 88rpx;
      height: 88rpx;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-right: 28rpx;
      box-shadow: 0 4rpx 16rpx rgba(71, 85, 105, 0.15);
      
      .icon-text {
        color: white;
        font-size: 34rpx;
        font-weight: 600;
      }
    }
    
    .icon-0 { background: linear-gradient(135deg, #3b82f6, #1d4ed8); } /* 身高 */
    .icon-1 { background: linear-gradient(135deg, #10b981, #059669); } /* 体重 */
    .icon-2 { background: linear-gradient(135deg, #f59e0b, #d97706); } /* 血压 */
    .icon-3 { background: linear-gradient(135deg, #8b5cf6, #7c3aed); } /* 血糖 */
    
    .card-content {
      flex: 1;
    }
    
    .card-title {
      display: block;
      font-size: 28rpx;
      color: #1e293b;
      font-weight: 500;
    }
    
    .card-value {
      display: block;
      font-size: 42rpx;
      font-weight: 600;
      margin: 12rpx 0 8rpx 0;
      color: #0f172a;
    }
    
    .card-time {
      font-size: 24rpx;
      color: #94a3b8;
    }
  }
}

/* 页面底部装饰 */
.page-footer {
  margin-top: 60rpx;
  padding: 40rpx 0;
  text-align: center;
  
  .footer-text {
    font-size: 28rpx;
    color: #94a3b8;
    font-weight: 500;
    opacity: 0.9;
  }
}
</style>