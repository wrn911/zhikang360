<template>
  <view class="container">
    <!-- 轮播图 -->
    <swiper class="swiper" :autoplay="true" :interval="3000" :circular="true">
      <swiper-item v-for="(item, index) in swiperList" :key="index">
        <image :src="item.imgUrl" mode="scaleToFill" class="swiper-img" />
      </swiper-item>
    </swiper>
	
	<view style="height: 30rpx;"></view> <!-- 换行间隙 -->

    <!-- 健康数据卡片 -->
    <view class="health-cards">
      <view 
        v-for="(item, index) in healthData" 
        :key="index"
        class="card"
        :style="{backgroundColor: item.color}"
      >
        <text class="card-title">{{ item.title }}</text>
        <text class="card-value">{{ item.value }}{{ item.unit }}</text>
        <text class="card-time">更新于 {{ item.updateTime }}</text>
      </view>
    </view>

    <!-- 底部导航 -->
    <view class="bottom-nav">
      <view class="nav-item" @click="openPopup">
        <image src="/static/icons/shengaotizhong.png" class="nav-icon" />
        <text>手动记录</text>
      </view>
      
      <navigator 
        url="/pages/index/scale" 
        class="nav-item"
        hover-class="nav-item-hover"
      >
        <image src="/static/icons/weightScale.png" class="nav-icon" />
        <text>智能秤测量</text>
      </navigator>
      
      <navigator 
        url="/pages/index/create" 
        class="nav-item"
        hover-class="nav-item-hover"
      >
        <image src="/static/icons/aiPlan.png" class="nav-icon" />
        <text>生成健康规划</text>
      </navigator>
    </view>

    <!-- 录入弹窗 -->
    <uni-popup ref="popup" type="dialog">
      <uni-popup-dialog 
        mode="base" 
        title="手动录入健康数据"
        @confirm="submitData"
        @close="closePopup"
      >
        <view class="input-group">
          <view class="input-item">
            <text class="label">身高(cm)</text>
            <input v-model="inputData.height" type="number" placeholder="请输入身高" />
          </view>
          <view class="input-item">
            <text class="label">体重(kg)</text>
            <input v-model="inputData.weight" type="number" placeholder="请输入体重" />
          </view>
          <view class="input-item">
            <text class="label">血压(mmHg)</text>
            <input v-model="inputData.bloodPressure" placeholder="格式：120/80" />
          </view>
          <view class="input-item">
            <text class="label">血糖(mmol/L)</text>
            <input v-model="inputData.bloodSugar" type="number" step="0.1" placeholder="请输入血糖值" />
          </view>
        </view>
      </uni-popup-dialog>
    </uni-popup>
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
      ],
      inputData: {
        height: '',
        weight: '',
        bloodPressure: '',
        bloodSugar: ''
      }
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

    // 修改后的submitData方法
        async submitData() {
          if (!this.validateForm()) return
    
          try {
            // 添加用户ID参数
            const payload = {
              ...this.inputData,
              userId: this.user.id
            }
    
            const res = await this.$request.put('/user-basic-info/update', payload)
    
            if (res.code === '200') {
              uni.showToast({ title: '更新成功' })
              await this.loadHealthData()  // 确保刷新数据
              this.closePopup()
            }
          } catch (error) {
            uni.showToast({ title: '更新失败', icon: 'none' })
          }
        },

    // 增强表单验证
        validateForm() {
          const validations = [
            {
              field: 'height',
              regex: /^\d{2,3}(\.\d{1,2})?$/,
              message: '身高应为100-250cm之间的数字'
            },
            {
              field: 'weight',
              regex: /^\d{2,3}(\.\d{1,2})?$/,
              message: '体重格式不正确'
            },
            {
              field: 'bloodPressure',
              regex: /^\d{1,3}\/\d{1,3}$/,
              message: '血压格式应为120/80'
            },
            {
              field: 'bloodSugar',
              regex: /^\d{1,2}(\.\d{1,2})?$/,
              message: '血糖值应在0.1-30之间'
            }
          ]
		  return validations.every(({ field, regex, message }) => {
		          const isValid = regex.test(this.inputData[field])
		          if (!isValid) {
		            uni.showToast({ title: message, icon: 'none' })
		          }
		          return isValid
		  })
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
	async openPopup() {
	  try {
		// 从healthData提取现有值填充表单
		await this.loadHealthData()
		console.log(this.healthData)
		this.healthData.forEach(item => {
		  const rawValue = item.value === '暂无' ? '' : String(item.value)
		  switch(item.title) {
			case '身高':
			  this.inputData.height = rawValue.replace('cm', '')
			  break
			case '体重':
			  this.inputData.weight = rawValue.replace('kg', '')
			  break
			case '血压':
			  this.inputData.bloodPressure = rawValue.replace('mmHg', '')
			  break
			case '血糖':
			  this.inputData.bloodSugar = rawValue.replace('mmol/L', '')
			  break
		  }
		})
		
		this.$refs.popup.open()
	  } catch (error) {
		uni.showToast({ title: '数据加载失败', icon: 'none' })
	  }
	},
    // 修改关闭弹窗方法
    closePopup() {
        this.$refs.popup.close()
    }
  }
}
</script>

<style lang="scss">
.container {
  padding: 20rpx;
}

.swiper {
  height: 350rpx;
  &-img {
    width: 100%;
    height: 100%;
    border-radius: 16rpx;
  }
}

.health-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
  .card {
    padding: 30rpx;
    border-radius: 16rpx;
    &-title {
      display: block;
      font-size: 28rpx;
      color: #666;
    }
    &-value {
      display: block;
      font-size: 40rpx;
      font-weight: bold;
      margin: 15rpx 0;
    }
    &-time {
      font-size: 24rpx;
      color: #999;
    }
  }
}

.bottom-nav {
  display: flex;
  justify-content: space-around;
  margin-top: 50rpx;
  .nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx 40rpx;
    border-radius: 12rpx;
    background-color: #f5f5f5;
    &-hover {
      background-color: #e0e0e0;
    }
    .nav-icon {
      width: 60rpx;
      height: 60rpx;
      margin-bottom: 15rpx;
    }
  }
}

.input-group {
  padding: 20rpx;
  .input-item {
    margin-bottom: 30rpx;
    .label {
      font-size: 28rpx;
      color: #666;
      margin-bottom: 10rpx;
    }
    input {
      height: 80rpx;
      padding: 0 20rpx;
      border: 1rpx solid #eee;
      border-radius: 8rpx;
      font-size: 28rpx;
    }
  }
}
</style>