<template>
	<view style="padding: 20rpx;">
		<view class="box">
			<uni-forms :modelValue="form" :rules="rules" ref="formRef" label-width="140rpx" label-align="right">
				<uni-forms-item label="头像" name="avatar">
					<uni-file-picker limit="1" :image-styles="imageStyles" :del-icon="false" :disable-preview="true"
						fileMediatype="image" v-model="avatar" @select="handleAvatarUploadSuccess"></uni-file-picker>

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
					<button type="primary" size="mini" @click="save">保 存</button>
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
						"color": "#eee", // 边框颜色
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

</style>