<template>
  <!-- 保持原有模板结构不变 -->
  <view class="container">
    <!-- 轮播图 -->
    <swiper class="swiper" :autoplay="true" :interval="3000" :circular="true">
      <swiper-item v-for="(item, index) in swiperList" :key="index">
        <image :src="item.imgUrl" mode="scaleToFill" class="swiper-img" />
      </swiper-item>
    </swiper>

    <view style="height: 30rpx;"></view>

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
      <!-- 保持原有导航项不变 -->
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
          <!-- 保持原有输入项结构 -->
        </view>
      </uni-popup-dialog>
    </uni-popup>
  </view>
</template>

<script>
export default {
  data() {
    return {
      swiperList: [/* 图片数据不变 */],
      user: {},
      healthData: [/* 初始结构不变 */],
      inputData: {
        height: '',
        weight: '',
        bloodPressure: '',
        bloodSugar: ''
      },
      // 新增原始数据存储
      originalData: {
        height: null,
        weight: null,
        bloodPressure: null,
        bloodSugar: null
      }
    }
  },

  onShow() {
    this.initializeUser()
    this.loadHealthData()
  },

  methods: {
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
        const res = await this.$request.get(`/user-basic-info/selectById/${this.user.id}`)
        
        if (res.code === '200') {
          // 存储原始数据（数值类型处理）
          this.originalData = {
            height: this.parseNumber(res.data?.height),
            weight: this.parseNumber(res.data?.weight),
            bloodPressure: res.data?.bloodPressure || null,
            bloodSugar: this.parseNumber(res.data?.bloodSugar)
          }

          // 更新健康卡片数据
          this.healthData = this.healthData.map(item => {
            const mappings = {
              '身高': { 
                value: res.data?.height ?? '暂无',
                time: res.data?.updateTimeH 
              },
              '体重': { 
                value: res.data?.weight ?? '暂无',
                time: res.data?.updateTimeW 
              },
              '血压': { 
                value: res.data?.bloodPressure ?? '暂无',
                time: res.data?.updateTimeBp 
              },
              '血糖': { 
                value: res.data?.bloodSugar ?? '暂无',
                time: res.data?.updateTimeBs 
              }
            }

            const target = mappings[item.title] || { value: '数据异常', time: null }
            
            return {
              ...item,
              value: target.value,
              updateTime: target.time ? this.formatTime(target.time) : '无记录'
            }
          })
        }
      } catch (error) {
        console.error('健康数据加载失败:', error)
        uni.showToast({ title: '数据加载失败', icon: 'none' })
      }
    },

    // 新增数值解析方法
    parseNumber(value) {
      if (value === null || value === undefined) return null
      const num = parseFloat(value)
      return isNaN(num) ? null : num
    },

    async openPopup() {
      try {
        await this.loadHealthData()
        
        // 填充表单数据（处理单位）
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

    // 修改检测方法
    getModifiedFields() {
      const input = this.inputData
      const original = this.originalData

      return {
        isHeightModified: this.compareValue(input.height, original.height),
        isWeightModified: this.compareValue(input.weight, original.weight),
        isBloodPressureModified: this.compareValue(input.bloodPressure, original.bloodPressure),
        isBloodSugarModified: this.compareValue(input.bloodSugar, original.bloodSugar)
      }
    },

    // 通用比较方法
    compareValue(inputVal, originalVal) {
      if (inputVal === '') return false // 空输入视为未修改
      if (originalVal === null) return !!inputVal // 从未记录过的情况

      // 数值类型比较
      if (typeof originalVal === 'number') {
        const numInput = parseFloat(inputVal)
        return !isNaN(numInput) && numInput !== originalVal
      }
      
      // 字符串比较（血压）
      return inputVal !== originalVal.toString()
    },

    async submitData() {
      // 获取修改状态
      const modified = this.getModifiedFields()
      
      // 检查是否有实际修改
      if (!Object.values(modified).some(v => v)) {
        uni.showToast({ title: '未修改任何数据', icon: 'none' })
        return
      }

      // 增强验证（仅验证修改字段）
      if (!this.validateForm(modified)) return

      try {
        const payload = {
          userId: this.user.id,
          ...this.filterModifiedData(this.inputData, modified),
          ...modified
        }

        const res = await this.$request.put('/user-basic-info/update', payload)
        
        if (res.code === '200') {
          uni.showToast({ title: '更新成功' })
          await this.loadHealthData()
          this.closePopup()
        }
      } catch (error) {
        uni.showToast({ title: '更新失败', icon: 'none' })
      }
    },

    // 过滤未修改字段
    filterModifiedData(data, modified) {
      return Object.keys(data).reduce((acc, key) => {
        const modifiedKey = `is${key[0].toUpperCase()}${key.slice(1)}Modified`
        if (modified[modifiedKey]) {
          acc[key] = data[key]
        }
        return acc
      }, {})
    },

    // 增强验证方法
    validateForm(modified) {
      const validations = {
        height: {
          regex: /^(1[0-9]{2}|2[0-4][0-9]|250)(\.\d{1,2})?$/,
          message: '身高应为100-250cm'
        },
        weight: {
          regex: /^[1-9]\d*(\.\d{1,2})?$/,
          message: '体重应为正数'
        },
        bloodPressure: {
          regex: /^\d{1,3}\/\d{1,3}$/,
          message: '格式：120/80'
        },
        bloodSugar: {
          regex: /^(?:[0-9]|1[0-9]|2[0-9]|30)(\.\d{1,2})?$/,
          message: '血糖值0-30'
        }
      }

      return Object.keys(validations).every(field => {
        if (!modified[`is${field[0].toUpperCase()}${field.slice(1)}Modified`]) return true
        
        const isValid = validations[field].regex.test(this.inputData[field])
        if (!isValid) {
          uni.showToast({ title: validations[field].message, icon: 'none' })
        }
        return isValid
      })
    },

    // 完整时间格式化
    formatTime(timestamp) {
      if (!timestamp) return '-'
      const date = new Date(timestamp)
      const pad = n => n.toString().padStart(2, '0')
      return `${date.getFullYear()}-${pad(date.getMonth()+1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`
    },

    closePopup() {
      this.$refs.popup.close()
      // 清空表单数据
      this.inputData = {
        height: '',
        weight: '',
        bloodPressure: '',
        bloodSugar: ''
      }
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