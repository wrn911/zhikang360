<template>
	<view class="container">
		<view class="page-header">
			<text class="page-title">个人信息</text>
			<text class="page-subtitle">完善您的个人资料</text>
		</view>
		
		<view class="form-card">
			<uni-forms :modelValue="form" :rules="rules" ref="formRef" label-width="140rpx" label-align="right">
				<uni-forms-item label="头像" name="avatar">
					<view class="avatar-wrapper">
						<uni-file-picker limit="1" :image-styles="imageStyles" :del-icon="false" :disable-preview="true"
							fileMediatype="image" v-model="avatar" @select="handleAvatarUploadSuccess"></uni-file-picker>
					</view>
				</uni-forms-item>
				<uni-forms-item label="账号" name="username">
					<uni-easyinput type="text" v-model="form.username" placeholder="" disabled />
				</uni-forms-item>
				<uni-forms-item label="性别" name="gender">
					<uni-data-checkbox style="position: relative; top: 10rpx;" v-model="form.gender" :localdata="range"></uni-data-checkbox>
				</uni-forms-item>
				<uni-forms-item label="电话" name="phone">
					<uni-easyinput type="text" v-model="form.phone" placeholder="请输入电话" />
				</uni-forms-item>

				<uni-forms-item>
					<button class="save-button" @click="save">保 存</button>
				</uni-forms-item>
			</uni-forms>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				avatar: [],
				form: {},
				user: uni.getStorageSync('xm-user'),
				imageStyles: {
					"height": 80, // 边框高度
					"width": 80, // 边框宽度
					"border": { // 如果为 Boolean 值，可以控制边框显示与否
						"color": "#e0e0e0", // 边框颜色
						"width": "1px", // 边框宽度
						"style": "solid", // 边框样式
						"radius": "50%" // 边框圆角，支持百分比
					}
				},
				range: [
					{ text: '男', value: '男' },
					{ text: '女', value: '女' },
					{ text: '保密', value: '保密' },
				]
			}
		},
		onLoad() {
			this.form = JSON.parse(JSON.stringify(this.user))
			this.avatar = [{
				url: this.user.avatar
			}]
			// 新增：获取扩展的性别信息
			this.loadExtendedUserInfo()
		},
		methods: {
			// 修改后的保存方法
			async save() {
			    try {
			    // 主用户信息更新
			    const mainUpdate = await this.$request.put('/user/update', {
			        id: this.user.id,
			        name: this.form.name,
			        phone: this.form.phone,
			        avatar: this.form.avatar
			    })
			
			    // 性别信息更新
			    const sexUpdate = await this.$request.put('/user-basic-info/update', {
			        userId: this.user.id,
			        gender: this.form.gender
			    })
			
			    if (mainUpdate.code === '200' && sexUpdate.code === '200') {
			        uni.showToast({ icon: "success", title: '操作成功' })
			        // 更新本地存储的合并数据
			        uni.setStorageSync('xm-user', this.form)
			    }
			    } catch (error) {
			    uni.showToast({ icon: "error", title: '保存失败' })
			    }
			},
			// 新增：加载扩展信息方法
			async loadExtendedUserInfo() {
			    try {
			    const res = await this.$request.get(`/user-basic-info/selectById/${this.user.id}`)
				console.log('完整接口响应:', res); // 打印完整响应对象
				console.log('响应数据:', res.data); // 打印 data 字段内容
			    if (res.code === '200') {
			        // 合并性别信息到表单数据
			        //this.form.gender = res.data.gender;
					// 正确方式
					this.$set(this.form, 'gender', res.data.gender);
					console.log('性别已加载:', this.form.gender); 
			    }
			    } catch (error) {
			    uni.showToast({
			        title: '附加信息加载失败',
			        icon: 'none'
			    })
			    }
			},
			handleAvatarUploadSuccess(e) {
				let _this = this
				const filePath = e.tempFilePaths[0]
				uni.uploadFile({
					url: _this.$baseUrl + '/files/upload', //自己的后端接口（默认发送post请求）
					filePath: filePath,
					name: "file", //这里应为自己后端文件形参的名字
					success(res) {
						console.log(res)
						let url = JSON.parse(res.data || '{}').data
						_this.form.avatar = url
					}
				})
			},
		}
	}
</script>

<style>
.container {
  padding: 30rpx;
  min-height: 100vh;
  background: linear-gradient(to bottom, #f8f9fa, #e9f2ef);
}

/* 页面标题 */
.page-header {
  margin-bottom: 40rpx;
  text-align: center;
}

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

/* 表单卡片 */
.form-card {
  background-color: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  box-shadow: 0 10rpx 20rpx rgba(0, 0, 0, 0.05);
}

/* 头像上传区域 */
.avatar-wrapper {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

/* 保存按钮 */
.save-button {
  background: linear-gradient(135deg, #4CAF50, #8BC34A);
  color: white;
  border: none;
  border-radius: 50rpx;
  padding: 20rpx 0;
  font-size: 32rpx;
  width: 100%;
  margin-top: 30rpx;
  box-shadow: 0 5rpx 15rpx rgba(76, 175, 80, 0.3);
  transition: all 0.3s ease;
}

.save-button:active {
  transform: scale(0.98);
  box-shadow: 0 2rpx 8rpx rgba(76, 175, 80, 0.3);
}

/* 表单项样式优化 */
:deep(.uni-forms-item) {
  margin-bottom: 25rpx;
}

:deep(.uni-easyinput__content) {
  background-color: #f9f9f9;
  border-radius: 8rpx;
  height: 80rpx;
  border: 1px solid #e0e0e0;
}

:deep(.uni-easyinput__content-input) {
  height: 80rpx;
  padding: 0 15rpx;
}

:deep(.uni-forms-item__label) {
  font-size: 28rpx;
  color: #333;
  font-weight: 500;
}

:deep(.uni-data-checklist) {
  display: flex;
  flex-direction: row;
}

:deep(.uni-data-checklist .checklist-box) {
  margin-right: 20rpx;
  padding: 10rpx 15rpx;
  border-radius: 8rpx;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

:deep(.uni-data-checklist .checklist-box.is-checked) {
  background-color: #e8f5e9;
  border-color: #4CAF50;
}

:deep(.uni-data-checklist .checklist-text) {
  font-size: 26rpx;
  color: #333;
}

:deep(.uni-data-checklist .checklist-box.is-checked .checklist-text) {
  color: #4CAF50;
}

/* 文件上传组件样式 */
:deep(.uni-file-picker__container) {
  display: flex;
  justify-content: flex-start;
}

:deep(.uni-file-picker__upload) {
  border-color: #4CAF50;
  background-color: #e8f5e9;
}

:deep(.uni-file-picker__upload-text) {
  color: #4CAF50;
}
</style>