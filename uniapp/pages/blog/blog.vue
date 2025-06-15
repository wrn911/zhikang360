<template>
	<!-- 主页 -->
	<view class="blog-container">
		<view class="tab-section">
			<u-subsection activeColor="#4CAF50" :list="list" :current="tab" @change="sectionChange"></u-subsection>
		</view>
		
		<!-- 博客列表 -->
		<scroll-view v-if="tab ===0" scroll-y="true" class="list-container">
			<view class="search-wrapper">
				<uni-search-bar @confirm="search" :focus="true" v-model="searchValue" @blur="blur" @focus="focus" @input="input"
					@cancel="cancel" @clear="clear" placeholder="搜索博客内容" bgColor="#f8f8f8">
				</uni-search-bar>
			</view>
			<view v-for="post in posts" :key="post.id" class="post-item">
				<view class="post-header">
					<text class="username">{{ post.userName }}</text>
					<text class="post-time">{{ formatDate(post.time) }}</text>
				</view>
				
				<view class="post-content-wrapper" @click="showDetill(post.id)">
					<view class="post-text">
						<view class="post-title">{{ post.name }}</view>
						<view class="post-content">{{ post.description }}</view>
					</view>
					<image :src="post.img" class="post-image"></image>
				</view>
				<!-- 互动区域 -->
				<view class="interaction">
					<view class="comment-btn" @click="showComments(post.id)">
						<text class="icon">💬</text> {{ post.comment || 0 }}
					</view>
					<view @click="likeOrUnlike(post)" :class="['like-btn', post.collected === 1 ? 'liked' : '']">
						<text class="icon">👍</text> {{ post.collect || 0 }}
					</view>
				</view>
			</view>
		</scroll-view>
		
		
		<!-- 发布区域 -->
		<view v-if="tab ===1" class="list-container">
			<view class="post-box">
				<button @click="createPost" :disabled="posting" class="create-btn">编辑博客</button>
			</view>
			<!-- 我的发布博客历史 -->
			<view v-for="post in myPosts" :key="post.id" class="post-item">
				<view class="post-header">
					<text class="username">{{ post.userName }}</text>
					<text class="post-time">{{ formatDate(post.time) }}</text>
				</view>
				<view class="post-content-wrapper" @click="showDetill(post.id)">
					<view class="post-text">
						<view class="post-title">{{ post.name }}</view>
						<view class="post-content">{{ post.description }}</view>
					</view>
					<image :src="post.img" class="post-image"></image>
				</view>
				<!-- 互动区域 -->
				<view class="interaction">
					<view @click="editBlog(post.id)" class="edit-btn">
						<text class="icon">✏️</text> 编辑
					</view>
					<view class="comment-btn" @click="showComments(post.id)">
						<text class="icon">💬</text> {{ post.comment || 0 }}
					</view>
					<view @click="likeOrUnlike(post)" :class="['like-btn', post.collected === 1 ? 'liked' : '']">
						<text class="icon">👍</text> {{ post.collect || 0 }}
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import http from "@/utils/request";
// 接口请求示例（需创建 utils/request.js）
const BASE_URL = 'https://your-api-domain.com'
export default {
	data() {
		return {
			list: ['发现', '我的博客'],
			tab: 0 ,
			detillId: 0,
			posts: [],
			myPosts: [],
			description: null,
			commentInput: {},
			currentPage: 1,
			currentMyPage: 1,
			loading: false,
			posting: false,
			user: {},
			searchValue:'',
		}
	},
	onShow() {
		this.posts = []
		this.myPosts = []
		this.currentPage = 1
		this.currentMyPage = 1
		this.getUserData()
		this.loadPosts()
		this.loadMyPosts()
	},
	async onReachBottom() {
		// 加载更多
		if(this.tab === 0)
			this.loadPosts()
		else
			this.loadMyPosts()
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
		showDetill(id){
			uni.navigateTo({
				url: "./blogDetill?id="+String(id)
			})
		},
		showComments(id){
			uni.navigateTo({
				url: "./blogDetill?id="+String(id)+"&showComments=true"
			})
		},
		editBlog(id){
			uni.navigateTo({
				url: "./editBlog?id="+String(id)
			})
		},
		sectionChange(index) {
			this.tab = index;
		},
		// 加载博客
		async loadPosts() {
			console.log('加载博客')
			if (this.currentPage === 1) {
				let tmpPosts = []
				await http.request({
				      url: '/introduction/selectPageByUser',
				      method: 'Get',
					  data:{
						  description: this.description,
						  pageNum: this.currentPage,
					  }
				}).then((res) => {
				  if (res.code === '200') {
				    tmpPosts = res.data.list
				  }
				})
				//将数据插入到 posts 数组的开头（...this.generateMockData(15) 表示展开数据，...this.posts 表示保留现有数据）
				this.posts = [...tmpPosts, ...this.posts]
				this.currentPage++
				return
			}
			if (this.loading) return
			this.loading = true
			try {
				console.log('继续加载')
				let tmpPosts = []
				await http.request({
				      url: '/introduction/selectPage',
				      method: 'Get',
					  data:{
						  description: this.description,
						  pageNum: this.currentPage,
					  }
				}).then((res) => {
				  if (res.code === '200') {
				    tmpPosts = res.data.list
				  }
				})
				//将数据插入到 posts 数组的开头（...this.generateMockData(15) 表示展开数据，...this.posts 表示保留现有数据）
				this.posts = [...this.posts, ...tmpPosts]
				this.currentPage++
			} finally {
				this.loading = false
			}
		},
		
		// 加载我的历史博客
		async loadMyPosts() {
			console.log('加载我的历史博客')
			if (this.currentMyPage === 1) {
				let tmpPosts = []
				await http.request({
				      url: '/introduction/selectPageByUser',
				      method: 'Get',
					  data:{
						  userId: this.user.id,
						  pageNum: this.currentMyPage,
					  }
				}).then((res) => {
				  if (res.code === '200') {
				    tmpPosts = res.data.list
				  }
				})
				//将数据插入到 posts 数组的开头（...this.generateMockData(15) 表示展开数据，...this.posts 表示保留现有数据）
				this.myPosts = [...tmpPosts, ...this.myPosts]
				this.currentMyPage++
				return
			}
			if (this.loading) return
			this.loading = true
			try {
				console.log('继续加载')
				let tmpPosts = []
				await http.request({
				      url: '/introduction/selectPage',
				      method: 'Get',
					  data:{
						  userId: this.user.id,
						  pageNum: this.currentMyPage,
					  }
				}).then((res) => {
				  if (res.code === '200') {
				    tmpPosts = res.data.list
				  }
				})
				this.myPosts = [...this.myPosts, ...tmpPosts]
				this.currentMyPage++
			} finally {
				this.loading = false
			}
		},
		
		
		// 进入发布博客页面
		createPost() {
			uni.navigateTo({
				url: "./editBlog"
			})
		},
		// 日期格式化
		formatDate(timestamp) {
			return new Date(timestamp).toLocaleDateString()
		},
		
		
		//判断点赞还是取消
		likeOrUnlike(post){
			if (!post) return
			
			if(post.collected === 1)
				this.unlikePost(post)
			else
				this.likePost(post)
		},
		
		// 点赞
		likePost(post) {
			const originalLikes = post.collect || 0
			
			console.log('点赞');
			http.request({
			      url: '/introduction/likePost',
			      method: 'Post',
				  data:{
					  'introductionId': post.id,
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
		unlikePost(post) {
			const originalLikes = post.collect || 0
		
			console.log('取消点赞');
			http.request({
			      url: '/introduction/unlikePost',
			      method: 'Delete',
				  data:{
					  'introductionId': post.id,
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
		
		search(res) {
			this.description = res.value
			this.currentPage = 1
			this.posts = []
			this.loadPosts()
			
			// uni.showToast({
			// 	title: '搜索：' + res.value,
			// 	icon: 'none'
			// })
		},
		input(res) {
			// console.log('----input:', res)
		},
		clear(res) {
			// uni.showToast({
			// 	title: 'clear事件，清除值为：' + res.value,
			// 	icon: 'none'
			// })
			this.description = ''
		},
		blur(res) {
			// uni.showToast({
			// 	title: 'blur事件，输入值为：' + res.value,
			// 	icon: 'none'
			// })
		},
		focus(e) {
			// uni.showToast({
			// 	title: 'focus事件，输出值为：' + e.value,
			// 	icon: 'none'
			// })
		},
		cancel(res) {
			// uni.showToast({
			// 	title: '点击取消，输入值为：' + res.value,
			// 	icon: 'none'
			// })
		}
	}
	
}
</script>

<style>
	/* 全局容器样式 */
	.blog-container {
		padding: 20rpx;
		background: linear-gradient(135deg, #f8fafc, #f1f5f9);
		min-height: 100vh;
	}
	
	/* 标签页样式 */
	.tab-section {
		margin-bottom: 30rpx;
		padding: 16rpx;
		background: linear-gradient(135deg, #ffffff, #fafbfc);
		border-radius: 20rpx;
		box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.08);
		border: 1rpx solid rgba(226, 232, 240, 0.6);
		animation: fadeIn 0.5s ease-in-out;
	}
	
	/* 搜索框样式 */
	.search-wrapper {
		margin-bottom: 24rpx;
		position: relative;
		z-index: 1;
		animation: slideDown 0.4s ease-out;
		padding: 16rpx;
		background: linear-gradient(135deg, #ffffff, #fafbfc);
		border-radius: 20rpx;
		box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.08);
		border: 1rpx solid rgba(226, 232, 240, 0.6);
		transition: all 0.3s ease;
	}
	
	.search-wrapper:hover {
		transform: translateY(-2rpx);
		box-shadow: 0 12rpx 32rpx rgba(71, 85, 105, 0.12);
		border-color: rgba(59, 130, 246, 0.3);
	}
	
	/* 自定义uni-search-bar样式 */
	.search-wrapper :deep(.uni-searchbar) {
		padding: 10rpx 0;
	}
	
	.search-wrapper :deep(.uni-searchbar__box) {
		height: 70rpx;
		border: 1rpx solid rgba(226, 232, 240, 0.6);
		background: linear-gradient(135deg, #f8fafc, #f1f5f9) !important;
		border-radius: 16rpx;
	}
	
	.search-wrapper :deep(.uni-searchbar__box-search-input) {
		font-size: 30rpx;
		color: #334155;
	}
	
	.search-wrapper :deep(.uni-icons) {
		color: #3b82f6 !important;
	}
	
	.search-wrapper :deep(.uni-searchbar__text-placeholder) {
		font-size: 30rpx;
		color: #94a3b8;
	}
	
	.search-wrapper :deep(.uni-searchbar__cancel) {
		color: #3b82f6;
		font-size: 30rpx;
	}
	
	/* 发布按钮区域 */
	.post-box {
		margin-bottom: 36rpx;
		background: linear-gradient(135deg, #ffffff, #fafbfc);
		padding: 36rpx;
		border-radius: 20rpx;
		box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.08);
		border: 1rpx solid rgba(226, 232, 240, 0.6);
		transition: all 0.3s ease;
	}
	
	.create-btn {
		background: linear-gradient(135deg, #3b82f6, #1d4ed8);
		color: white;
		font-weight: 600;
		border-radius: 16rpx;
		height: 88rpx;
		line-height: 88rpx;
		transition: all 0.3s ease;
		box-shadow: 0 8rpx 20rpx rgba(59, 130, 246, 0.25);
		letter-spacing: 2rpx;
	}
	
	.create-btn:active {
		background: linear-gradient(135deg, #2563eb, #1e40af);
		transform: translateY(2rpx);
		box-shadow: 0 4rpx 12rpx rgba(59, 130, 246, 0.2);
	}

	.title-input {
		font-size: 32rpx;
		margin-bottom: 20rpx;
	}

	.content-input {
		height: 200rpx;
		margin-bottom: 20rpx;
	}

	.list-container {
		background: linear-gradient(135deg, #f8fafc, #f1f5f9);
		padding: 16rpx;
		animation: fadeIn 0.5s ease-in-out;
	}

	/* 博客卡片样式 */
	.post-item {
		background: linear-gradient(135deg, #ffffff, #fafbfc);
		padding: 36rpx;
		margin-bottom: 30rpx;
		border-radius: 20rpx;
		box-shadow: 0 8rpx 24rpx rgba(71, 85, 105, 0.08);
		border: 1rpx solid rgba(226, 232, 240, 0.6);
		transition: all 0.3s ease;
		animation: fadeIn 0.5s ease-in-out;
	}
	
	.post-item:active {
		transform: translateY(2rpx);
		box-shadow: 0 4rpx 12rpx rgba(71, 85, 105, 0.06);
		background: linear-gradient(135deg, #f8fafc, #f1f5f9);
	}
	
	/* 博客头部样式 */
	.post-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 20rpx;
		padding-bottom: 20rpx;
		border-bottom: 1px solid rgba(226, 232, 240, 0.6);
	}
	
	.username {
		font-weight: 600;
		color: #1e293b;
		font-size: 30rpx;
	}
	
	.post-time {
		color: #94a3b8;
		font-size: 24rpx;
	}
	
	/* 博客内容样式 */
	.post-content-wrapper {
		display: flex;
		align-items: flex-start;
		gap: 20rpx;
	}
	
	.post-text {
		flex: 1;
	}
	
	.post-title {
		font-size: 34rpx;
		font-weight: 600;
		margin-bottom: 16rpx;
		color: #0f172a;
		line-height: 1.4;
		letter-spacing: 0.5rpx;
	}
	
	.post-content {
		font-size: 28rpx;
		color: #475569;
		line-height: 1.6;
		margin-bottom: 16rpx;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 3;
		overflow: hidden;
		word-break: break-word;
		text-overflow: ellipsis;
		white-space: normal;
		max-height: 135rpx; /* 约等于 line-height * -webkit-line-clamp */
	}
	
	.post-image {
		width: 180rpx;
		height: 180rpx;
		border-radius: 16rpx;
		object-fit: cover;
		background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
		box-shadow: 0 4rpx 12rpx rgba(71, 85, 105, 0.1);
		border: 1rpx solid rgba(226, 232, 240, 0.6);
		transition: transform 0.3s ease;
	}
	
	.post-content-wrapper:active .post-image {
		transform: scale(1.02);
	}

	/* 互动区域样式 */
	.interaction {
		display: flex;
		align-items: center;
		margin-top: 24rpx;
		padding-top: 20rpx;
		border-top: 1px solid rgba(226, 232, 240, 0.6);
		gap: 36rpx;
	}
	
	.icon {
		margin-right: 6rpx;
	}
	
	.edit-btn, .comment-btn, .like-btn {
		display: flex;
		align-items: center;
		padding: 12rpx 24rpx;
		border-radius: 20rpx;
		font-size: 26rpx;
		color: #64748b;
		background: linear-gradient(135deg, #f8fafc, #f1f5f9);
		border: 1rpx solid rgba(226, 232, 240, 0.6);
		transition: all 0.3s ease;
		box-shadow: 0 2rpx 8rpx rgba(71, 85, 105, 0.05);
	}
	
	.edit-btn:active, .comment-btn:active, .like-btn:active {
		background: linear-gradient(135deg, #e2e8f0, #cbd5e1);
		transform: translateY(1rpx);
		box-shadow: 0 1rpx 4rpx rgba(71, 85, 105, 0.08);
	}
	
	.edit-btn {
		color: #3b82f6;
		background: linear-gradient(135deg, rgba(59, 130, 246, 0.08), rgba(59, 130, 246, 0.05));
		border: 1rpx solid rgba(59, 130, 246, 0.2);
	}
	
	.liked {
		color: #ef4444;
		background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
		border: 1rpx solid rgba(239, 68, 68, 0.2);
		transform: scale(1.02);
		font-weight: 600;
		box-shadow: 0 4rpx 12rpx rgba(239, 68, 68, 0.15);
	}
	
	.liked .icon {
		transform: scale(1.1);
		color: #ef4444;
		transition: transform 0.2s ease;
	}
	
	@keyframes likeAnimation {
		0% { transform: scale(1); }
		50% { transform: scale(1.2); }
		75% { transform: scale(1.05); }
		100% { transform: scale(1.1); }
	}
	
	.like-btn:active .icon {
		animation: likeAnimation 0.3s ease;
	}
	
	/* 点赞动画效果 */
	.liked .icon {
		animation: likeAnimation 0.3s ease forwards;
		color: #ef4444;
	}
	
	/* 点赞按钮悬停效果 */
	.like-btn:hover {
		background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
	}
	
	.liked:hover {
		background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.08));
	}

	.comment-input {
		flex: 1;
		border: 1rpx solid #eee;
		padding: 10rpx;
		border-radius: 8rpx;
	}

	.comments {
		margin-top: 20rpx;
		padding-top: 20rpx;
		border-top: 1rpx solid #eee;
	}

	.comment {
		font-size: 26rpx;
		color: #666;
		margin-bottom: 10rpx;
	}
	/* 动画效果 */
	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(10rpx); }
		to { opacity: 1; transform: translateY(0); }
	}
	
	@keyframes slideDown {
		from { opacity: 0; transform: translateY(-20rpx); }
		to { opacity: 1; transform: translateY(0); }
	}
</style>