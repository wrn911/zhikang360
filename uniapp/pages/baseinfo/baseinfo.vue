<template>
	<view class="container">
		<uni-forms ref="form" :model="formData" :rules="rules">
			<!-- 性别选择 -->
			<uni-forms-item label="性别" required name="gender">
				<radio-group @change="handleGenderChange">
					<label class="radio-label">
						<radio value="男" color="#4CAF50" /> 男
					</label>
					<label class="radio-label">
						<radio value="女" color="#4CAF50" /> 女
					</label>
					<label class="radio-label">
						<radio value="保密" color="#4CAF50" /> 保密
					</label>
				</radio-group>
			</uni-forms-item>

			<!-- 出生日期选择 -->
			<uni-forms-item label="出生日期" required name="birthDate">
				<uni-easyinput v-model="formData.birthDate" placeholder="日期格式:YYYYMMDD" readonly
					@click.native="showCalendar = true" />
				<uni-calendar ref="calendar" :insert="false" @confirm="handleDateConfirm" />
				<button @click="open">打开日历</button>
			</uni-forms-item>

			<!-- 其他信息输入 -->
			<uni-forms-item label="身高(cm)" required name="height">
				<uni-easyinput type="digit" v-model="formData.height" placeholder="请输入身高" />
			</uni-forms-item>

			<uni-forms-item label="体重(kg)" required name="weight">
				<uni-easyinput type="digit" v-model="formData.weight" placeholder="请输入体重" />
			</uni-forms-item>

			<uni-forms-item label="血压(mmHg)" required name="bloodPressure">
				<uni-easyinput v-model="formData.bloodPressure" placeholder="格式：120/80" />
			</uni-forms-item>

			<uni-forms-item label="血糖(mmol/L)" required name="bloodSugar">
				<uni-easyinput type="digit" v-model="formData.bloodSugar" placeholder="请输入血糖值" />
			</uni-forms-item>

			<!-- 提交按钮 -->
			<button class="submit-btn" type="primary" @click="handleSubmit" :disabled="!formValid">提交信息</button>
		</uni-forms>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				formData: {
					gender: '',
					birthDate: '',
					height: '',
					weight: '',
					bloodPressure: '',
					bloodSugar: ''
				},
				showCalendar: false,
				formValid: false
			}
		},
		computed: {
			rules() {
				return {
					gender: {
						rules: [{
							required: true,
							errorMessage: '请选择性别'
						}]
					},
					birthDate: {
						rules: [{
							required: true,
							errorMessage: '请选择出生日期'
						}]
					},
					height: {
						rules: [{
								required: true,
								errorMessage: '请输入身高'
							},
							{
								format: 'number',
								errorMessage: '请输入有效数字'
							}
						]
					},
					bloodPressure: {
						rules: [{
							validateFunction: (rule, value) => {
								return /^\d{2,3}\/\d{2,3}$/.test(value)
							}
						}]
					}
				}
			}
		},
		watch: {
			formData: {
				deep: true,
				handler() {
					this.$refs.form.validate().then(res => {
						this.formValid = true
					}).catch(err => {
						this.formValid = false
					})
				}
			}
		},
		methods: {
			open() {
				this.$refs.calendar.open();
			},
			confirm(e) {
				console.log(e);
			},
			handleGenderChange(e) {
				this.formData.gender = e.detail.value
			},
			handleDateConfirm(e) {
				this.formData.birthDate = e.fulldate
				this.showCalendar = false
			},
			async handleSubmit() {
				try {

					const debugData = {
						...this.formData,
						// 格式化日期显示
						formattedDate: new Date(this.formData.birthDate).toLocaleDateString()
					}
					console.log('待提交数据:', JSON.stringify(debugData, null, 2))
					if (process.env.NODE_ENV === 'development') {
					          const confirm = await this.showDataPreview(debugData)
					          if (!confirm) return
					        }
					const data = this.formData
					const res = await this.$request.put('/user-basic-info/update', data)
					/*const res = await uni.request({
						url: '/user-basic-info/update',
						method: 'POST',
						data: this.formData,
						header: {
							'Content-Type': 'application/json'
						}
					})*/

					if (res.code === '200') {
						uni.showToast({
							title: '提交成功',
							icon: 'success'
						})
						uni.navigateTo({ url: '/pages/foodinfo/foodinfo' })
						this.$refs.form.resetFields()
					}
				} catch (error) {
					uni.showToast({
						title: '提交失败',
						icon: 'error'
					})
				}
			},
			showDataPreview(data) {
			      return new Promise((resolve) => {
			        uni.showModal({
			          title: '数据预览',
			          content: `性别: ${data.gender}\n
			出生日期: ${data.formattedDate}\n
			身高: ${data.height}cm\n
			体重: ${data.weight}kg\n
			血压: ${data.bloodPressure}mmHg\n
			血糖: ${data.bloodSugar}mmol/L`,
			          confirmText: '确认提交',
			          cancelText: '取消',
			          success: (res) => {
			            resolve(res.confirm)
			          }
			        })
			      })
			    }
		}
	}
</script>

<style scoped>
	.container {
		padding: 24rpx;
	}

	.radio-label {
		margin-right: 40rpx;
	}

	.submit-btn {
		background-color: #4CAF50 !important;
		margin-top: 40rpx;
		border-radius: 50rpx;
	}

	/* 日历样式调整 */
	:deep(.uni-calendar) {
		height: 70vh;
		border-radius: 20rpx 20rpx 0 0;
	}

	:deep(.uni-calendar__header) {
		background-color: #4CAF50;
		color: white;
	}
</style>