<template>
	<view class="container">
		<view class="header">
			<text class="title">{{ formattedDate }}</text>
		</view>
		<view class="search-container">
			<view class="search-box">
				<input class="search-bar" placeholder="请输入运动名称" v-model="searchText"
					@focus="showResults = true" @blur="handleBlur" ref="searchInput" />
				<view class="search-icons">
					<text class="icon-btn" @click="handleSearch">🔍</text>
					<text class="icon-btn" @click="handleReset">⟳</text>
				</view>
			</view>
			<view class="dropdown" v-show="showResults && filteredExercises.length">
				<view v-for="(exercise, index) in filteredExercises" :key="index" class="dropdown-item"
					@mousedown="selectExercise(exercise)">
					{{ exercise.name }}
				</view>
			</view>
		</view>
		<!-- 模板部分修改 -->
		<view class="common-exercises">
			<text class="subtitle">常见运动</text>

			<!-- 表格结构 -->
			<view class="exercise-table">
				<!-- 表头 -->
				<view class="table-header">
					<text class="header-item">运动id</text>
					<text class="header-item">运动名称</text>
					<text class="header-item">运动类别</text>
					<text class="header-item">单位时间消耗的热量</text>
					<text class="header-item">操作</text>
				</view>

				<!-- 表格数据 -->
				<view class="table-body">
					<view class="table-row" v-for="(exercise, index) in paginatedExercises" :key="index">
						<text class="body-item">{{ exercise.id }}</text>
						<text class="body-item">{{ exercise.name }}</text>
						<text class="body-item">{{ exercise.category }}</text>
						<text class="body-item">{{ exercise.caloriesBurnRate }} 千卡</text>
						<view class="body-item action-cell" @click="addExercise(exercise)">
							<text class="add-button">+</text>
						</view>
					</view>
				</view>
			</view>

			<!-- 分页控件 -->
			<view class="pagination">
				<view class="page-controls">
					<text class="page-arrow" :class="{ disabled: currentPage === 1 }" @click="prevPage">←</text>

					<text class="page-info">第{{ currentPage }}页/共{{ totalPages }}页</text>

					<text class="page-arrow" :class="{ disabled: currentPage === totalPages }"
						@click="nextPage">→</text>
				</view>
			</view>
		</view>
		<view class="breakfast-suggestion">
			<text class="subtitle">建议</text>
			<text>534~747 千卡</text>
			<text>已添加 {{ addedCalories }} 千卡</text>
		</view>
		<button class="complete-button">完成</button>
		<!-- 在container内添加弹出层 -->
		<uni-popup ref="popup" type="dialog">
			<view class="action-dialog">
				<button class="action-btn" @click="handleManualInput">手动输入时间</button>
			</view>
		</uni-popup>
	</view>
</template>

<script>
	import http from "@/utils/request";

	export default {
		data() {
			return {
				searchText: '',
				allExercises: [],
				isSearchActive: false, // 新增搜索状态
				filteredResults: [], // 新增搜索结果存储
				showResults: false,
				addedCalories: 115,
				currentexercise: null,
				duration: 0, // 临时存储输入的时长
				currentPage: 1, // 当前页码
				pageSize: 5, // 每页条数
				//totalPages: 0 // 总页数
			};
		},
		computed: {
			formattedDate() {
				const date = new Date();
				return `${date.getMonth() + 1}月${date.getDate()}日`;
			},
			// 新增过滤后的食物列表
			commonExercises() {
				if (!this.searchText) return this.allExercises;
				const search = this.searchText.toLowerCase();
				return this.allExercises.filter(exercise =>
					exercise.name.toLowerCase().includes(search)
				);
			},
			totalPages() {
			      const source = this.isSearchActive ? this.filteredResults : this.allExercises;
			      return Math.ceil(source.length / this.pageSize);
			},
			// 分页后的数据

			paginatedExercises() {
				const source = this.isSearchActive ? this.filteredResults : this.allExercises;
				const start = (this.currentPage - 1) * this.pageSize;
				const end = start + this.pageSize;
				return source.slice(start, end);
			},
			filteredExercises() {
				if (!this.searchText) return [];
				const keyword = this.searchText.toLowerCase();
				return this.allExercises
					.filter(exercise =>
						exercise.name.toLowerCase().includes(keyword)
					)
					.slice(0, 10); // 取前10条
			}

		},
		methods: {
			// 新增数据获取方法
			async fetchExerciseData() {
				http.request({
					url: '/exercise/selectAll',
					method: 'GET'
				}).then(response => {
					if (response.code === '200') {
						this.allExercises = response.data.map(item => ({
							id: item.exerciseId,
							name: item.exerciseName,
							category: item.exerciseCategory || '无',
							caloriesBurnRate: item.caloriesBurnRate,
						}));
						this.totalPages = Math.ceil(this.allExercises.length / this.pageSize)
					} else {
						this.showError(response.msg);
					}
				}).catch(err => {
					console.error('请求错误详情:', err);
					this.showError('网络请求失败');
				});
			},
			addExercise(exerciseItem) {
				this.currentexercise = exerciseItem
				this.$refs.popup.open()
			},
			handleManualInput() {
				uni.showModal({
					title: '输入时间（单位：分钟）',
					editable: true,
					success: (res) => {
						if (res.confirm && res.content) {
							const duration = parseFloat(res.content)
							if (!isNaN(duration) && duration > 0) {
								this.calculateCalories(duration)
							} else {
								uni.showToast({
									title: '请输入有效数字',
									icon: 'none'
								})
							}
						}
					}
				})
			},
			async calculateCalories(duration) {
				try {
					// 保存重量用于接口提交
					this.duration = duration;

					// 计算卡路里
					const calories = (this.currentexercise.calories / 100) * duration;
					this.addedCalories += Math.round(calories);

					// 调用提交接口
					const res = await http.request({
						url: '/exercise/addNewToday',
						method: 'POST',
						data: {
							exerciseId: this.currentexercise.id,
							exerciseName: this.currentexercise.name,
							exerciseCategory: this.currentexercise.category,
							caloriesBurnRate:this.currentexercise.caloriesBurnRate,
							calories:(this.duration / 10) * this.caloriesBurnRate,
							duration: this.duration,
						}
					});

					if (res.code === '200') {
						uni.showToast({
							title: `已记录 ${duration}g ${this.currentexercise.name}`,
							icon: 'none'
						});
					} else {
						this.showError(res.msg || '提交失败');
						// 回滚卡路里计算
						this.addedCalories -= Math.round(calories);
					}
				} catch (err) {
					console.error('接口错误:', err);
					this.showError('网络请求失败');
				}
			},
			handlePhotoUpload() {
				// 拍照上传逻辑
				uni.showToast({
					title: '功能开发中',
					icon: 'none'
				})
			},
			showError(msg) {
				uni.showToast({
					title: msg || '获取运动数据失败',
					icon: 'none'
				});
			},
			navigateBack() {
				uni.navigateTo({
					url: '/pages/sport/sport'
				});
			},
			prevPage() {
				if (this.currentPage > 1) {
					this.currentPage--
				}
			},
			// 下一页
			nextPage() {
				if (this.currentPage < this.totalPages) {
					this.currentPage++
				}
			},
			handleSearchClick() {
				// 确保输入框获得焦点（移动端可能需要）
				this.$nextTick(() => {
					this.$refs.searchInput.focus()
				})

				// 可选：添加点击动画效果
				this.$refs.searchInput.style.transform = 'scale(0.99)'
				setTimeout(() => {
					this.$refs.searchInput.style.transform = 'scale(1)'
				}, 100)
			},
			handleSearch() {
				if (this.searchText) {
					this.isSearchActive = true;
					this.filteredResults = this.allExercises.filter(exercise =>
						exercise.name.toLowerCase().includes(this.searchText.toLowerCase())
					);
					this.currentPage = 1; // 重置到第一页
					this.showResults = false; // 隐藏下拉框
				}
			},
			handleBlur() {
				setTimeout(() => {
					this.showResults = false;
				}, 200);
			},
			selectExercise(exercise) {
				this.searchText = exercise.name;
				this.showResults = false;
				// 可选：自动触发其他操作
			},
			handleReset() {
				this.searchText = '';
				this.isSearchActive = false;
				this.filteredResults = [];
				this.currentPage = 1;
				this.showResults = false;
			}

		},
		mounted() {
			this.fetchExerciseData();
		}
	};
</script>

<style scoped>
	.search-box {
	  position: relative;
	  display: flex;
	  align-items: center;
	  background: white;
	  border-radius: 8px;
	  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
	}
	.search-container {
		position: relative;
		margin-bottom: 15px;
	}

	.dropdown {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		max-height: 300px;
		background: #fff;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		z-index: 999;
		overflow-y: auto;
	}

	.dropdown-item {
		padding: 12px 16px;
		font-size: 14px;
		color: #333;
		text-align: left;
		border-bottom: 1px solid #eee;
		transition: background 0.2s;
	}

	.dropdown-item:last-child {
		border-bottom: none;
	}

	.dropdown-item:hover {
		background-color: #f8f9fa;
	}

	/* 新增弹窗样式 */
	.action-dialog {
		background: white;
		padding: 30rpx;
		border-radius: 16rpx;
		width: 80vw;
	}

	.action-btn {
		margin: 20rpx 0;
		padding: 20rpx;
		background-color: #4CAF50;
		color: white;
		border-radius: 8rpx;
		font-size: 28rpx;
	}

	.action-btn:active {
		opacity: 0.8;
	}

	/* 样式新增 */
	.action-cell {
		cursor: pointer;
		transition: all 0.2s;
	}

	.add-button {
		width: 26px;
		height: 26px;
		line-height: 26px;
		text-align: center;
		border-radius: 50%;
		background-color: #4CAF50;
		color: white;
		font-size: 20px;
		display: inline-block;
		transition: all 0.2s;
	}

	/* 悬停效果 */
	.action-cell:hover .add-button {
		transform: scale(1.1);
		box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3);
	}

	/* 点击效果 */
	.action-cell:active .add-button {
		transform: scale(0.95);
	}

	/* 调整列宽比例（原3列改为4列） */
	.header-item,
	.body-item {
		flex: 1;
		/* 如需强调操作列，可单独设置 flex: 0.5; */
	}

	/* 新增表格样式 */
	.food-table {
		margin-top: 15px;
		background: #fff;
		border-radius: 12px;
		overflow: hidden;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
	}

	.table-header {
		display: flex;
		background-color: #f8f9fa;
		padding: 12px 0;
		border-bottom: 1px solid #eee;
	}

	.table-row {
		display: flex;
		padding: 12px 0;
		border-bottom: 1px solid #eee;
	}

	.table-row:last-child {
		border-bottom: none;
	}

	.header-item,
	.body-item {
		flex: 1;
		text-align: center;
		font-size: 14px;
		padding: 0 5px;
	}

	.header-item {
		font-weight: 600;
		color: #333;
	}

	.body-item {
		color: #666;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	/* 分页样式修改 */
	.pagination {
		margin-top: 15px;
		padding: 8px 0;
	}

	.page-controls {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 20px;
	}

	.page-arrow {
		font-size: 24px;
		width: 36px;
		height: 36px;
		line-height: 36px;
		text-align: center;
		border-radius: 50%;
		background-color: #f0f0f0;
		color: green;
		transition: all 0.2s;
	}

	.page-arrow:active {
		background-color: #e0e0e0;
	}

	.page-arrow.disabled {
		color: #cccccc;
		background-color: #f8f8f8;
		cursor: not-allowed;
		opacity: 0.7;
	}

	.page-info {
		font-size: 14px;
		color: #666;
		min-width: 120px;
		text-align: center;
	}




	.date-picker {
		flex: 1;
	}

	.title {
		font-size: 18px;
		color: #333;
		padding: 8px 12px;
		border-radius: 8px;
		transition: all 0.2s;
	}

	.title:active {
		background-color: rgba(0, 0, 0, 0.05);
	}

	/* 调整原有.back-icon样式 */
	.back-icon {
		margin-right: 15px;
		/* 调整回合适间距 */
		/* 保持其他原有样式 */
	}

	.container {
		padding: 15px;
		background-color: #f5f5f5;
		min-height: 100vh;
	}

	/* 头部卡片 */
	.header {
		display: flex;
		align-items: center;
		padding: 15px;
		background: white;
		border-radius: 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
		margin-bottom: 15px;
	}

	/* 搜索栏卡片 */
.search-bar {
  flex: 1;
  height: 40px;
  padding: 0 15px;
  border: none;
  background: transparent;
}
.search-icons {
  display: flex;
  padding-right: 10px;
  gap: 12px;
}

.icon-btn {
  font-size: 18px;
  padding: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.icon-btn:active {
  transform: scale(0.9);
  opacity: 0.8;
}

	/* 添加聚焦状态样式 */
	.search-bar:focus {
		box-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
		border: 1px solid #4CAF50;
	}

	/* 常见食物卡片 */
	.common-foods {
		background: white;
		border-radius: 12px;
		padding: 18px;
		margin-bottom: 15px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
	}

	/* 食物项样式 */
	.food-item {
		display: flex;
		justify-content: space-between;
		padding: 14px 8px;
		border-bottom: 1px solid #eee;
		transition: all 0.2s;
	}

	.food-item:last-child {
		border-bottom: none;
	}

	/* 早餐建议卡片 */
	.breakfast-suggestion {
		background: white;
		border-radius: 12px;
		padding: 18px;
		margin-bottom: 25px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
	}

	.subtitle {
		font-size: 16px;
		color: #333;
		margin-bottom: 12px;
		font-weight: 500;
		display: block;
	}

	/* 按钮样式优化 */
	.complete-button {
		width: 100%;
		padding: 16px;
		background: linear-gradient(135deg, #4CAF50, #45a049);
		color: white;
		border-radius: 12px;
		font-size: 16px;
		box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
		transition: all 0.3s;
	}

	/* 数据展示优化 */
	.breakfast-suggestion text {
		display: block;
		margin: 6px 0;
		color: #666;
	}

	.breakfast-suggestion text:nth-child(3) {
		color: #4CAF50;
		font-weight: bold;
	}

	/* 返回图标美化 */
	.back-icon {
		margin-right: 12px;
		font-size: 24px;
		color: #666;
		width: 30px;
		height: 30px;
		text-align: center;
		line-height: 30px;
		border-radius: 50%;
		transition: all 0.2s;
	}

	.back-icon:active {
		background: #f5f5f5;
	}
</style>