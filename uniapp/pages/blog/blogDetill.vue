<template> 
    <view class="blog-detail-container">
		<!-- 主体部分 -->
		<view class="blog-content-card">
			<view class="blog-header">
				<text class="blog-author">{{ post.userName }}</text>
				<text class="blog-time">{{ formatDate(post.time) }}</text>
			</view>
			<view class="blog-title">{{ post.name }}</view>
			<view class="blog-content">
				<rich-text :nodes="post.content"></rich-text>
			</view>
		</view>
		
		<!-- 评论列表 -->
		<view id="comment" class="comment-section">
			<view class="comment-title">
				<text class="title-text">评论</text>
				<text class="comment-count">{{ post.comment || 0 }}</text>
			</view>
			<view v-if="post.comments && post.comments.length > 0" class="comment-list">
				<view v-for="c in post.comments" :key="c.id" class="comment-item">
					<view class="comment-header">
						<text class="comment-author">{{ c.userName }}</text>
						<text class="comment-time">{{ c.time }}</text>
					</view>
					<view class="comment-content">{{ c.content }}</view>
				</view>
			</view>
			<view v-else class="no-comments">
				<text>暂无评论，快来发表第一条评论吧！</text>
			</view>
		</view>
		
		<!-- 底部空间，防止内容被工具栏遮挡 -->
		<view class="bottom-space"></view>

		<!-- 互动区域（工具栏） -->
		<view class="toolbar">
		  <view class="toolbar-btn comment-write-btn" @click="showEditor = true">
			<text class="toolbar-icon">✏️</text>
			<text class="toolbar-text">写评论...</text>
		  </view>
		  <view class="toolbar-btn comment-view-btn" @click="toComments">
			<text class="toolbar-icon">💬</text>
			<text class="toolbar-text">{{ post.comment || 0 }}</text>
		  </view>
		  <view @click="likeOrUnlike(post.id)" 
			:class="['toolbar-btn', 'like-btn', post.collected === 1 ? 'liked' : '']">
			<text class="toolbar-icon">👍</text>
			<text class="toolbar-text">{{ post.collect || 0 }}</text>
		  </view>
		</view>

		<!-- 弹出评论编辑框 -->
		<u-popup :show="showEditor" @close="close" @open="open" mode="bottom" borderRadius="16">
		  <view class="comment-editor">
			<view class="editor-header">
				<text class="editor-title">发表评论</text>
				<text class="editor-close" @click="close">×</text>
			</view>
			<textarea 
				v-model="content" 
				class="comment-textarea" 
				placeholder="分享你的想法..." 
				maxlength="500"
				auto-height
			/>
			<view class="editor-footer">
				<text class="char-count">{{ content.length }}/500</text>
				<u-button @click="submitComment" class="submit-btn" :disabled="!content.trim()">发布</u-button>
			</view>
		  </view>
		</u-popup>
  </view>
</template>

<script>
import http from "@/utils/request";
export default {
	data() {
		return {
			postId:0,
			post:{},
			showEditor:false,
			user: {},
			content: '',
		}
	},
	methods: {
		getUserData() {
		  // 从本地缓存中获取数据
		  const userStr = uni.getStorageSync('user');
		  if (userStr) {
		    this.user = JSON.parse(userStr);
		  } else {
		    console.log('没有找到用户数据');
		  }
		},
		// 日期格式化
		formatDate(timestamp) {
			return new Date(timestamp).toLocaleDateString()
		},
		//获取博客
		getRecommend(){
			console.log('获取博客');
			http.request({
			      url: '/introduction/selectByIdByUser/'+String(this.postId),
			      method: 'GET',
			}).then((res) => {
			  if (res.code === '200') {
			    this.post = res.data || [];
				console.log(res.data)
			  } else {
			    uni.showToast({
			      title: '获取博客失败',
			      icon: 'none'
			    });
			  }
			}).catch(err => {
			  console.error('获取博客失败', err);
			  uni.showToast({
			    title: '网络错误，请稍后重试',
			    icon: 'none'
			  });
			});
		},
		
		//判断点赞还是取消
		likeOrUnlike(postId){
			if(this.post.collected === 1)
				this.unlikePost(postId)
			else
				this.likePost(postId)
		},
		
		// 点赞
		likePost(postId) {
			const post = this.post
			const originalLikes = post.collect || 0
			
			console.log('点赞');
			http.request({
			      url: '/introduction/likePost',
			      method: 'Post',
				  data:{
					  'introductionId': postId,
					  'userId':this.user.id
				  },
			}).then((res) => {
			  if (res.code === '200') {
			    uni.showToast({
			      title: '点赞成功',
			      icon: 'none'
			    });
				post.collected = 1
				post.collect = originalLikes + 1
			  } else {
			    uni.showToast({
			      title: '点赞失败',
			      icon: 'none'
			    });
			  }
			}).catch(err => {
			  console.error('点赞失败', err);
			  uni.showToast({
			    title: '网络错误，请稍后重试',
			    icon: 'none'
			  });
			});
		},
		
		// 取消点赞
		unlikePost(postId) {
			const post = this.post
			const originalLikes = post.collect || 0
		
			console.log('取消点赞');
			http.request({
			      url: '/introduction/unlikePost',
			      method: 'Delete',
				  data:{
					  'introductionId': postId,
					  'userId':this.user.id
				  },
			}).then((res) => {
			  if (res.code === '200') {
			    uni.showToast({
			      title: '取消点赞',
			      icon: 'none'
			    });
				post.collected = 0
				post.collect = originalLikes - 1
			  }
			})
		},
		
		//提交评论
		submitComment(){
			if (!this.content.trim()) {
				uni.showToast({
					title: '评论内容不能为空',
					icon: 'none'
				});
				return;
			}
			
			console.log('提交评论');
			http.request({
			      url: '/introduction/comment',
			      method: 'POST',
				  data:{
					  content:this.content,
					  userName:this.user.username,
					  userId:this.user.id,
					  introductionId:this.postId,
				  }
			}).then((res) => {
			  if (res.code === '200') {
			    uni.showToast({
			      title: '评论成功',
			      icon: 'success'
			    });
				this.showEditor = false
				this.content = ''
				this.getRecommend()
			  } else {
			    uni.showToast({
			      title: '评论失败',
			      icon: 'none'
			    });
			  }
			}).catch(err => {
			  console.error('评论失败', err);
			  uni.showToast({
			    title: '网络错误，请稍后重试',
			    icon: 'none'
			  });
			});
		},
		
		open() {},
		close() {
		  this.showEditor = false
		},
		toComments() {
		    // 滚动到评论区
			uni.pageScrollTo({
				selector:'#comment',
				duration: 0
			});
		},
	},
	onLoad: function (option) { //option为object类型，会序列化上个页面传递的参数
		this.postId = option.id
		
		// 检查是否需要直接滚动到评论区
		if(option.showComments === 'true') {
			// 延迟执行，确保页面已经渲染完成
			setTimeout(() => {
				this.toComments()
			}, 500)
		}
	},
	//避免在数据未加载完成时访问其属性
	onShow() {
	    this.getRecommend()
		this.getUserData()
	}
}
</script>

<style>
/* 全局动画 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20rpx); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

@keyframes float {
  0% { transform: translateY(0); }
  50% { transform: translateY(-10rpx); }
  100% { transform: translateY(0); }
}

/* 博客详情容器 */
.blog-detail-container {
  padding: 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8f4f8 50%, #f0f7ff 100%);
  background-attachment: fixed;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* 博客内容卡片 */
.blog-content-card {
  margin: 30rpx;
  padding: 40rpx;
  background: linear-gradient(to bottom right, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(10px);
  border-radius: 24rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.08), 0 1rpx 3rpx rgba(0, 0, 0, 0.03);
  animation: fadeIn 0.5s ease-out;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.7);
  position: relative;
  overflow: hidden;
}

.blog-content-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 200%;
  height: 100%;
  background: linear-gradient(90deg, 
    rgba(255, 255, 255, 0) 0%, 
    rgba(255, 255, 255, 0.2) 25%, 
    rgba(255, 255, 255, 0.2) 50%, 
    rgba(255, 255, 255, 0) 100%);
  background-size: 200% 100%;
  animation: shimmer 8s infinite linear;
  pointer-events: none;
}

/* 博客头部 */
.blog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
  padding-bottom: 20rpx;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
}

.blog-author {
  font-weight: bold;
  color: #333;
  font-size: 32rpx;
  position: relative;
  padding-left: 20rpx;
}

.blog-author::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 8rpx;
  height: 32rpx;
  background: linear-gradient(to bottom, #4CAF50, #2E7D32);
  border-radius: 4rpx;
}

.blog-time {
  color: #999;
  font-size: 26rpx;
}

/* 博客标题 */
.blog-title {
  font-size: 44rpx;
  font-weight: bold;
  margin-bottom: 40rpx;
  color: #222;
  line-height: 1.4;
  word-break: break-word;
  letter-spacing: 2rpx;
}

/* 博客内容 */
.blog-content {
  font-size: 32rpx;
  color: #444;
  line-height: 1.8;
  margin-bottom: 40rpx;
  word-break: break-word;
  text-align: justify;
  letter-spacing: 1rpx;
}

/* 评论区域 */
.comment-section {
  margin: 30rpx;
  padding: 40rpx;
  background: linear-gradient(to bottom right, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(10px);
  border-radius: 24rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.08), 0 1rpx 3rpx rgba(0, 0, 0, 0.03);
  animation: fadeIn 0.6s ease-out;
  border: 1px solid rgba(255, 255, 255, 0.7);
  position: relative;
  overflow: hidden;
}

.comment-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 200%;
  height: 100%;
  background: linear-gradient(90deg, 
    rgba(255, 255, 255, 0) 0%, 
    rgba(255, 255, 255, 0.2) 25%, 
    rgba(255, 255, 255, 0.2) 50%, 
    rgba(255, 255, 255, 0) 100%);
  background-size: 200% 100%;
  animation: shimmer 8s infinite linear;
  pointer-events: none;
}

.comment-title {
  display: flex;
  align-items: center;
  margin-bottom: 30rpx;
  padding-bottom: 20rpx;
  border-bottom: 1px solid rgba(76, 175, 80, 0.1);
}

.title-text {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  position: relative;
  padding-left: 20rpx;
}

.title-text::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 8rpx;
  height: 36rpx;
  background: linear-gradient(to bottom, #4CAF50, #2E7D32);
  border-radius: 4rpx;
}

.comment-count {
  margin-left: 16rpx;
  font-size: 28rpx;
  color: #999;
  background-color: #f0f0f0;
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
}

.comment-list {
  margin-bottom: 30rpx;
}

.comment-item {
  padding: 30rpx;
  margin-bottom: 24rpx;
  background: linear-gradient(135deg, #f9f9f9, #f5f5f5);
  border-radius: 16rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.02), 0 1px 3px rgba(0, 0, 0, 0.01);
  transition: all 0.3s ease;
  border-left: 6rpx solid rgba(76, 175, 80, 0.3);
  animation: fadeIn 0.5s ease-out;
}

.comment-item:hover {
  transform: translateY(-4rpx);
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.05);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.comment-author {
  font-weight: bold;
  color: #333;
  font-size: 30rpx;
}

.comment-time {
  color: #999;
  font-size: 24rpx;
}

.comment-content {
  color: #555;
  line-height: 1.6;
  word-break: break-word;
  font-size: 28rpx;
  padding: 10rpx 0;
}

.no-comments {
  text-align: center;
  padding: 60rpx 0;
  color: #999;
  font-size: 28rpx;
}

/* 底部空间 */
.bottom-space {
  height: 180rpx;
}

/* 工具栏样式 */
.toolbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 20rpx 30rpx;
  background: linear-gradient(to right, rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
  backdrop-filter: blur(15px);
  border-top: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.07);
  z-index: 100;
  animation: slideUp 0.3s ease-out;
}

/* 工具栏按钮样式 */
.toolbar-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16rpx 30rpx;
  border-radius: 40rpx;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08), inset 0 1px 1px rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.6);
}

.toolbar-btn:active {
  transform: scale(0.95);
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.toolbar-icon {
  margin-right: 10rpx;
  font-size: 32rpx;
}

.toolbar-text {
  font-size: 28rpx;
  color: #555;
}

.comment-write-btn {
  flex: 1.5;
  margin-right: 20rpx;
  justify-content: flex-start;
  background: linear-gradient(135deg, #f5f5f5, #f0f0f0);
  border: 1px solid rgba(238, 238, 238, 0.8);
  animation: float 3s ease-in-out infinite;
}

.comment-view-btn {
  background: linear-gradient(135deg, #f0f8f0, #e8f5e8);
  border: 1px solid rgba(76, 175, 80, 0.2);
  animation: float 3s ease-in-out infinite;
  animation-delay: 0.2s;
}

.like-btn {
  background: linear-gradient(135deg, #f0f8f0, #e8f5e8);
  border: 1px solid rgba(76, 175, 80, 0.2);
  animation: float 3s ease-in-out infinite;
  animation-delay: 0.4s;
}

.liked {
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.2), rgba(76, 175, 80, 0.1));
  border: 1px solid rgba(76, 175, 80, 0.3);
  animation: pulse 0.3s ease-out, float 3s ease-in-out infinite;
  animation-delay: 0s, 0.4s;
}

.liked .toolbar-icon {
  color: #FF5722;
}

.liked .toolbar-text {
  color: #4CAF50;
  font-weight: bold;
}

/* 评论编辑器 */
.comment-editor {
  padding: 40rpx;
  background: linear-gradient(to bottom, #ffffff, #f9f9f9);
  border-top-left-radius: 24rpx;
  border-top-right-radius: 24rpx;
  box-shadow: 0 -5rpx 25rpx rgba(0, 0, 0, 0.05);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
  padding-bottom: 20rpx;
  border-bottom: 1px solid #f0f0f0;
}

.editor-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
}

.editor-close {
  font-size: 40rpx;
  color: #999;
  padding: 0 20rpx;
}

.comment-textarea {
  width: 100%;
  min-height: 220rpx;
  padding: 24rpx;
  font-size: 28rpx;
  background: linear-gradient(to bottom, #f9f9f9, #f5f5f5);
  border-radius: 16rpx;
  margin-bottom: 30rpx;
  box-sizing: border-box;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.comment-textarea:focus {
  background: linear-gradient(to bottom, #ffffff, #f9f9f9);
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.editor-footer {
  position: relative;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-top: 10rpx;
}

.char-count {
  position: absolute;
  top: -40rpx;
  right: 10rpx;
  font-size: 24rpx;
  color: #999;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
}

.submit-btn {
  background: linear-gradient(135deg, #4CAF50, #2E7D32) !important;
  color: white !important;
  border: none !important;
  font-weight: bold !important;
  padding: 14rpx 50rpx !important;
  border-radius: 40rpx !important;
  box-shadow: 0 6rpx 12rpx rgba(76, 175, 80, 0.2) !important;
  margin-left: 30rpx;
}

.submit-btn:active {
  transform: translateY(2rpx);
  box-shadow: 0 2rpx 8rpx rgba(76, 175, 80, 0.15) !important;
}
</style>
