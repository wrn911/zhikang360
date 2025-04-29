<template>
	<view class="edit-blog-container">
		<view class="blog-card">
			<view class="card-header">
				<text class="card-title">编辑博客</text>
			</view>
			
			<view class="form-item">
				<text class="form-label">博客标题</text>
				<input class="title-input" v-model="newPost.name" placeholder="请输入博客标题" />
			</view>
			
			<view class="form-item editor-container">
				<text class="form-label">博客内容</text>
				<rich-text-editor v-model="newPost.content" class="rich-editor"></rich-text-editor>
			</view>
			
			<view class="form-item">
				<text class="form-label">封面图片</text>
				<view class="upload-container">
					<uni-file-picker limit="1" v-model="imgs" title="上传封面图片" @select="insertImage"></uni-file-picker>
				</view>
			</view>
			
			<view class="submit-container">
				<button class="submit-btn" @click="submitPost">发布博客</button>
			</view>
		</view>
	</view>
</template>


<script>
import richTextEditor from '../../components/editor/editor.vue';
import http from "@/utils/request";
export default {

	//注册
	components: {
		richTextEditor
	},
	data() {
		return {
			imgs:[],
			newPost:{
				img:'',
				name:'',
				content:'',
				userId:'',
			},
			user: {},
			serverUrl: 'http://localhost:9090/files/upload',
			postId:-1,
		};
	},
	onLoad(option) { //option为object类型，会序列化上个页面传递的参数
		console.log('onLoad触发，参数:', option);
		if(option && option.id){
			this.postId = option.id;
			// 立即获取用户数据
			this.getUserData();
			// 立即加载博客数据
			this.$nextTick(() => {
				this.getBlog();
			});
		}
	},
	onShow() {
		// 如果不是编辑模式，则只获取用户数据
		if(this.postId < 0){
			this.getUserData();
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
		// 发布博客
		submitPost() {
			if (!this.newPost.name.trim() || !this.newPost.content.trim()) {
				return uni.showToast({
					title: '请输入标题和内容',
					icon: 'none'
				})
			}
			
			this.newPost.userId = this.user.id
			console.log('编辑器内容:', this.newPost.content);
			http.request({
			      url: this.newPost.id?  '/introduction/update' : '/introduction/add',
			      method: this.newPost.id? 'Put' : 'Post',
				  data:this.newPost
			}).then((res) => {
			  if (res.code === '200') {
			    uni.switchTab({
			    	url: "/pages/blog/blog"
			    })
			  } else {
			    uni.showToast({
			      title: '发布博客失败',
			      icon: 'none'
			    });
			  }
			}).catch(err => {
			  console.error('发布博客失败', err);
			  uni.showToast({
			    title: '网络错误，请稍后重试',
			    icon: 'none'
			  });
			});
		},
		
		
		insertImage(e) {
		    let _this = this//确保异步上下文正确
		    const filePath = e.tempFilePaths[0]
		    uni.uploadFile({
		    	url: _this.serverUrl, //自己的后端接口（默认发送post请求）
		    	filePath: filePath,
		    	name: "file", //这里应为自己后端文件形参的名字
				header: {token: uni.getStorageSync('xm-user')?.token},
		    	success(res) {
		    		console.log(res)
		    		let url = JSON.parse(res.data || '{}').data
		    		_this.newPost.img = url
		    	}
		    })
			
		  },
		  
		  //获取博客
		  getBlog(){
		  	console.log('获取博客ID:', this.postId);
		  	http.request({
		  	      url: '/introduction/selectByIdByUser/'+String(this.postId),
		  	      method: 'GET',
		  	}).then((res) => {
		  	  if (res.code === '200') {
				// 先清空现有内容
				this.newPost = {
					img: '',
					name: '',
					content: '',
					userId: ''
				};
				
				// 确保数据完整后再更新
				this.$nextTick(() => {
					// 使用解构赋值确保id也被保留
					this.newPost = {...res.data};
					
					// 更新图片显示
					if(this.newPost.img) {
						this.imgs = [{url: this.newPost.img}];
					}
					console.log('博客数据加载完成:', this.newPost);
				});
				
				// 显示成功提示
				uni.showToast({
					title: '博客加载成功',
					icon: 'none'
				});
				
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
	},
}
</script>


<style>
.edit-blog-container {
	min-height: 100vh;
	padding: 30rpx;
	background: linear-gradient(to bottom, #f8f8f8, #e8f5e9);
}

.blog-card {
	background-color: #fff;
	border-radius: 20rpx;
	box-shadow: 0 4rpx 30rpx rgba(0, 0, 0, 0.1);
	padding: 40rpx 30rpx;
	margin-bottom: 30rpx;
	transition: all 0.3s ease;
}

.card-header {
	margin-bottom: 40rpx;
	border-bottom: 2rpx solid #eee;
	padding-bottom: 20rpx;
}

.card-title {
	font-size: 36rpx;
	font-weight: bold;
	color: #4CAF50;
}

.form-item {
	margin-bottom: 30rpx;
}

.form-label {
	display: block;
	font-size: 28rpx;
	color: #666;
	margin-bottom: 15rpx;
	font-weight: 500;
}

.title-input {
	height: 80rpx;
	width: 100%;
	border: 2rpx solid #e0e0e0;
	border-radius: 10rpx;
	padding: 0 20rpx;
	font-size: 28rpx;
	background-color: #f9f9f9;
	transition: border-color 0.3s;
}

.title-input:focus {
	border-color: #4CAF50;
	background-color: #fff;
}

.editor-container {
	margin-bottom: 40rpx;
}

.rich-editor {
	border: 2rpx solid #e0e0e0;
	border-radius: 10rpx;
	background-color: #fff;
	min-height: 400rpx;
}

.upload-container {
	background-color: #f9f9f9;
	border-radius: 10rpx;
	padding: 20rpx;
	border: 2rpx dashed #e0e0e0;
}

.submit-container {
	display: flex;
	justify-content: center;
	margin-top: 50rpx;
}

.submit-btn {
	background: linear-gradient(to right, #4CAF50, #8BC34A);
	color: #fff;
	border: none;
	border-radius: 50rpx;
	padding: 20rpx 60rpx;
	font-size: 32rpx;
	font-weight: bold;
	box-shadow: 0 8rpx 16rpx rgba(76, 175, 80, 0.3);
	transition: all 0.3s ease;
}

.submit-btn:active {
	transform: translateY(3rpx);
	box-shadow: 0 4rpx 8rpx rgba(76, 175, 80, 0.3);
}
</style>
