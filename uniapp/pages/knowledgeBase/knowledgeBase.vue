<template>
  <view class="container">
    <!-- 顶部栏 -->
    <view class="top-bar">
      <text class="back-btn" @click="goBack">←</text>
      <text class="title">本地知识库</text>
      <text class="add-btn" @click="showUploadOptions">+</text>
    </view>

    <!-- 文件列表 -->
    <scroll-view class="file-list" scroll-y>
      <view v-if="files.length === 0" class="empty-tip">
        <text>暂无知识库文件，请点击右上角添加</text>
      </view>
      <view v-for="file in files" :key="file.id" class="file-item">
        <view class="file-info">
          <text class="file-name">{{ file.file_name }}</text>
          <text class="file-size">{{ formatFileSize(file.file_size) }}</text>
        </view>
        <text class="delete-btn" @click="deleteFile(file.id)">删除</text>
      </view>
    </scroll-view>

    <!-- 上传选项弹出层 -->
    <uni-popup ref="uploadPopup" type="bottom">
      <view class="upload-options">
        <view class="upload-title">添加知识库文件</view>
        <view class="upload-list">
          <view class="upload-item" @click="uploadFile('document')">
            <text>上传文档</text>
          </view>
<!--          <view class="upload-item" @click="uploadFile('image')">
            <text>上传图片</text>
          </view> -->
        </view>
        <view class="upload-cancel" @click="hideUploadOptions">取消</view>
      </view>
    </uni-popup>
  </view>
</template>

<script>
export default {
  data() {
    return {
      files: [],
      baseUrl: 'http://10.27.246.45:8000'
    }
  },
  onLoad() {
    this.loadFiles()
  },
  methods: {
    // 返回上一页
    goBack() {
      uni.navigateBack()
    },

    // 加载知识库文件列表
    async loadFiles() {
      try {
        const token = uni.getStorageSync('xm-user')?.token
        const res = await uni.request({
          url: `${this.baseUrl}/knowledge/file/list`,
          method: 'GET',
          header: {
            'token': `${token}`
          }
        })
        if (res.statusCode === 200) {
          this.files = res.data.files || []
        }
      } catch (error) {
        uni.showToast({
          title: '加载文件列表失败',
          icon: 'none'
        })
      }
    },

    // 显示上传选项
    showUploadOptions() {
      this.$refs.uploadPopup.open()
    },

    // 隐藏上传选项
    hideUploadOptions() {
      this.$refs.uploadPopup.close()
    },

    // 上传文件
    async uploadFile(type) {
      this.hideUploadOptions()
      
      try {
        const token = uni.getStorageSync('xm-user')?.token
        const res = await uni.chooseFile({
          count: 1,
          type: type === 'document' ? 'all' : 'image'
        })
        
        uni.showLoading({
          title: '上传中...'
        })
        
        const uploadTask = uni.uploadFile({
          url: `${this.baseUrl}/knowledge/file/upload`,
          filePath: res.tempFilePaths[0],
          name: 'file',
          header: {
            'token': `${token}`
          },
          success: (uploadRes) => {
            if (uploadRes.statusCode === 200) {
              uni.showToast({
                title: '上传成功',
                icon: 'success'
              })
              this.loadFiles() // 重新加载文件列表
            }
          },
          fail: () => {
            uni.showToast({
              title: '上传失败',
              icon: 'none'
            })
          },
          complete: () => {
            uni.hideLoading()
          }
        })
      } catch (error) {
        console.error('选择文件失败:', error)
      }
    },

    // 删除文件
    async deleteFile(fileId) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这个文件吗？',
        success: async (res) => {
          if (res.confirm) {
            try {
              const token = uni.getStorageSync('xm-user')?.token
              const deleteRes = await uni.request({
                url: `${this.baseUrl}/knowledge/file/${fileId}`,
                method: 'DELETE',
                header: {
                  'token': `${token}`
                }
              })
              
              if (deleteRes.statusCode === 200) {
                uni.showToast({
                  title: '删除成功',
                  icon: 'success'
                })
                this.loadFiles() // 重新加载文件列表
              }
            } catch (error) {
              uni.showToast({
                title: '删除失败',
                icon: 'none'
              })
            }
          }
        }
      })
    },

    // 格式化文件大小
    formatFileSize(size) {
      if (!size) return '未知大小'
      
      const units = ['B', 'KB', 'MB', 'GB']
      let index = 0
      let fileSize = size
      
      while (fileSize >= 1024 && index < units.length - 1) {
        fileSize /= 1024
        index++
      }
      
      return fileSize.toFixed(2) + ' ' + units[index]
    }
  }
}
</script>

<style>
/* ===== 现代化知识库界面样式 ===== */
.container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f8fffe 0%, #f0fdf4 50%, #ffffff 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* ===== 现代化顶部栏 ===== */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32rpx 24rpx;
  border-bottom: 1px solid rgba(16, 185, 129, 0.08);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 1px 3px rgba(16, 185, 129, 0.05);
  position: relative;
  z-index: 10;
}

.back-btn, .add-btn {
  width: 72rpx;
  height: 72rpx;
  font-size: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #059669;
  font-weight: 600;
  border-radius: 18rpx;
  background: rgba(240, 253, 244, 0.6);
  border: 1px solid rgba(16, 185, 129, 0.15);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  backdrop-filter: blur(8px);
}

.back-btn:active, .add-btn:active {
  transform: scale(0.94);
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
}

.title {
  font-size: 32rpx;
  font-weight: 600;
  color: #065f46;
  letter-spacing: -0.02em;
  text-align: center;
  flex: 1;
}

/* ===== 现代化文件列表 ===== */
.file-list {
  flex: 1;
  padding: 24rpx;
  background: transparent;
  overflow-y: auto;
}

.empty-tip {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 400rpx;
  padding: 40rpx;
  text-align: center;
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.empty-tip text {
  color: #6b7280;
  font-size: 28rpx;
  line-height: 1.6;
  max-width: 80%;
  font-weight: 400;
}

.empty-tip::before {
  content: '📁';
  font-size: 120rpx;
  margin-bottom: 24rpx;
  opacity: 0.8;
  display: block;
}

@keyframes fadeInUp {
  from { 
    opacity: 0; 
    transform: translateY(32px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

/* ===== 现代化文件项目 ===== */
.file-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 24rpx;
  margin-bottom: 16rpx;
  border-radius: 20rpx;
  background: rgba(255, 255, 255, 0.98);
  border-left: 4px solid #10b981;
  box-shadow: 0 1px 3px rgba(16, 185, 129, 0.1);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  animation: slideIn 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  position: relative;
  overflow: hidden;
}

.file-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(236, 253, 245, 0.3) 0%, rgba(255, 255, 255, 0.1) 100%);
  pointer-events: none;
}

.file-item:active {
  transform: scale(0.98);
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
}

@keyframes slideIn {
  from { 
    opacity: 0; 
    transform: translateX(-16px); 
  }
  to { 
    opacity: 1; 
    transform: translateX(0); 
  }
}

/* ===== 现代化文件信息 ===== */
.file-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6rpx;
  position: relative;
  z-index: 1;
}

.file-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #374151;
  letter-spacing: -0.01em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 85%;
}

.file-name::before {
  content: '📄';
  margin-right: 12rpx;
  font-size: 24rpx;
  opacity: 0.8;
}

.file-size {
  font-size: 22rpx;
  color: #9ca3af;
  font-weight: 400;
  margin-left: 36rpx;
}

/* ===== 现代化删除按钮 ===== */
.delete-btn {
  color: #ef4444;
  font-size: 24rpx;
  font-weight: 500;
  padding: 10rpx 20rpx;
  border-radius: 16rpx;
  background: rgba(254, 226, 226, 0.6);
  border: 1px solid rgba(239, 68, 68, 0.15);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  z-index: 1;
  backdrop-filter: blur(8px);
}

.delete-btn:active {
  transform: scale(0.94);
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.25);
}

/* ===== 现代化上传选项弹窗 ===== */
.upload-options {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 24rpx 24rpx 0 0;
  padding: 32rpx 24rpx;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top: 1px solid rgba(16, 185, 129, 0.08);
  box-shadow: 0 -8px 32px rgba(0, 0, 0, 0.08);
  animation: slideUp 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes slideUp {
  from { 
    opacity: 0; 
    transform: translateY(40px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

.upload-title {
  text-align: center;
  padding: 16rpx 0 24rpx;
  font-weight: 600;
  font-size: 32rpx;
  color: #065f46;
  letter-spacing: -0.02em;
  position: relative;
}

.upload-title::after {
  content: '';
  position: absolute;
  bottom: 8rpx;
  left: 50%;
  transform: translateX(-50%);
  width: 48rpx;
  height: 4rpx;
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  border-radius: 2rpx;
}

/* ===== 现代化上传列表 ===== */
.upload-list {
  padding: 16rpx 0;
  gap: 12rpx;
  display: flex;
  flex-direction: column;
}

.upload-item {
  padding: 20rpx 24rpx;
  text-align: center;
  border-radius: 16rpx;
  font-size: 28rpx;
  font-weight: 500;
  color: #374151;
  background: linear-gradient(135deg, rgba(236, 253, 245, 0.4) 0%, rgba(255, 255, 255, 0.6) 100%);
  border: 1px solid rgba(16, 185, 129, 0.12);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(8px);
}

.upload-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.1), transparent);
  transition: left 0.5s ease;
}

.upload-item:active {
  transform: scale(0.98);
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
}

.upload-item:active::before {
  left: 100%;
}

/* 为不同上传类型添加图标 */
.upload-item:nth-child(1)::after {
  content: '📄';
  margin-right: 12rpx;
}

.upload-item:nth-child(2)::after {
  content: '🖼️';
  margin-right: 12rpx;
}

/* ===== 现代化取消按钮 ===== */
.upload-cancel {
  text-align: center;
  padding: 20rpx 24rpx;
  margin-top: 16rpx;
  color: #6b7280;
  font-size: 28rpx;
  font-weight: 500;
  background: rgba(248, 250, 252, 0.6);
  border-radius: 16rpx;
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  backdrop-filter: blur(8px);
}

.upload-cancel:active {
  transform: scale(0.96);
  background: rgba(243, 244, 246, 0.8);
  color: #4b5563;
}

/* ===== 响应式优化 ===== */
@media screen and (max-width: 750px) {
  .top-bar {
    padding: 28rpx 20rpx;
  }
  
  .back-btn, .add-btn {
    width: 64rpx;
    height: 64rpx;
    font-size: 28rpx;
  }
  
  .title {
    font-size: 28rpx;
  }
  
  .file-item {
    padding: 16rpx 20rpx;
    margin-bottom: 12rpx;
  }
  
  .file-name {
    font-size: 26rpx;
  }
  
  .file-size {
    font-size: 20rpx;
  }
  
  .delete-btn {
    font-size: 22rpx;
    padding: 8rpx 16rpx;
  }
  
  .upload-options {
    padding: 28rpx 20rpx;
  }
  
  .upload-title {
    font-size: 28rpx;
  }
  
  .upload-item {
    padding: 18rpx 20rpx;
    font-size: 26rpx;
  }
  
  .upload-cancel {
    padding: 18rpx 20rpx;
    font-size: 26rpx;
  }
}

/* ===== 加载动画优化 ===== */
.file-item:nth-child(1) { animation-delay: 0.1s; }
.file-item:nth-child(2) { animation-delay: 0.2s; }
.file-item:nth-child(3) { animation-delay: 0.3s; }
.file-item:nth-child(4) { animation-delay: 0.4s; }
.file-item:nth-child(5) { animation-delay: 0.5s; }

/* ===== 滚动条美化 ===== */
.file-list::-webkit-scrollbar {
  width: 6rpx;
}

.file-list::-webkit-scrollbar-track {
  background: rgba(240, 253, 244, 0.3);
  border-radius: 3rpx;
}

.file-list::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  border-radius: 3rpx;
}

.file-list::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
}

/* ===== 深色模式适配（可选） ===== */
@media (prefers-color-scheme: dark) {
  .container {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  }
  
  .top-bar {
    background: rgba(15, 23, 42, 0.95);
    border-bottom-color: rgba(16, 185, 129, 0.15);
  }
  
  .title {
    color: #10b981;
  }
  
  .back-btn, .add-btn {
    background: rgba(30, 41, 59, 0.8);
    border-color: rgba(16, 185, 129, 0.2);
    color: #10b981;
  }
  
  .file-item {
    background: rgba(30, 41, 59, 0.8);
    border-left-color: #10b981;
  }
  
  .file-name {
    color: #f1f5f9;
  }
  
  .file-size {
    color: #64748b;
  }
  
  .upload-options {
    background: rgba(15, 23, 42, 0.98);
    border-top-color: rgba(16, 185, 129, 0.15);
  }
  
  .upload-title {
    color: #10b981;
  }
  
  .upload-item {
    background: rgba(30, 41, 59, 0.6);
    border-color: rgba(16, 185, 129, 0.2);
    color: #cbd5e1;
  }
  
  .upload-cancel {
    background: rgba(30, 41, 59, 0.6);
    border-color: rgba(255, 255, 255, 0.1);
    color: #94a3b8;
  }
  
  .empty-tip text {
    color: #64748b;
  }
}
</style>