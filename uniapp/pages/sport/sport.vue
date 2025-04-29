<template>
	<view>
		<view>
			<u-subsection style="margin-top: 5px;" activeColor="green" :list="list" :current="tab" @change="sectionChange"></u-subsection>
		</view>
		
		<!-- 运动计划 -->
		<scroll-view v-if="tab ===0" scroll-y>
			<view class="card calories-card">
				<view class="calories-content">
					<view class="calories-label">推荐运动消耗卡路里数</view>
					<view class="calories-value">
						{{recommendCalories}} <text class="calories-unit">kcal</text>
					</view>
					<view class="calories-decoration"></view>
				</view>
			</view>
			<view v-for="(sport, index) in recommendSports" :key="index">
				<view class="card sport-plan-card">
					<view class="sport-icon-container">
						<text class="sport-icon">🏃</text>
					</view>
					<view class="sport-content">
						<view class="sport-name">{{sport.exerciseName}}</view>
						<view class="sport-details">
							<view class="sport-duration">
								<text class="detail-icon">⏱️</text>
								<text>{{sport.duration}}分钟</text>
							</view>
							<view class="sport-calories">
								<text class="detail-icon">🔥</text>
								<text>{{sport.caloriesBurned}} kcal</text>
							</view>
						</view>
					</view>
				</view>
			</view>
			<u-button @click="showAddSportPacker=true" icon="plus" type="success" style="border-radius: 50%; position: fixed; bottom: 15vw; right:6vw; width: 12vw; height: 12vw;"/>
		</scroll-view>
		<u-picker :show="showSportPacker" ref="uPicker" :columns="columns" @confirm="confirm" @change="changeHandler" @cancel="showSportPacker=false"></u-picker>
		<u-popup :show="showAddSportPacker" @close="showAddSportPacker=false" zIndex="10074" :round="16">
		    <view class="popup-container">
				<view class="popup-header">
					<view class="popup-title">请添加运动计划</view>
					<view class="popup-subtitle">选择运动类型和时长</view>
				</view>
				<view class="add-sport-form">
					<view class="form-item">
						<view class="form-label">运动计划类型：</view>
						<view class="form-input sport-selector" @click="showSportPacker=true">
							<view class="selected-sport" v-if="curSport!=null">
								<text class="sport-category">{{curSport.exerciseCategory}}</text>
								<text class="sport-name-1">{{curSport.exerciseName}}</text>
							</view>
							<view class="placeholder" v-else>请选择运动类型</view>
							<text class="select-icon">▼</text>
						</view>
					</view>
					<view class="form-item">
						<view class="form-label">运动计划时长：</view>
						<input class="form-input" v-model="duration" type="number" placeholder="请输入运动时长（分钟）"/>
					</view>
				</view>
				<button class="submit-button" @click="addSport">添加运动</button>
			</view>
		</u-popup>
		
		<!-- 运动打卡 -->
		<scroll-view v-if="tab ===1" scroll-y>
			<!-- 未打卡的运动 -->
			<view class="checkin-section">
				<view class="section-title">待完成运动</view>
				<view v-for="(sport, index) in recommendSports" :key="index">
					<view v-if="sport.feedback === null" class="card sport-checkin-card">
						<view class="sport-content">
							<view class="sport-name">{{sport.exerciseName}}</view>
							<view class="sport-details">
								<view class="sport-duration">
									<text class="detail-icon">⏱️</text>
									<text>{{sport.duration}}分钟</text>
								</view>
								<view class="sport-calories">
									<text class="detail-icon">🔥</text>
									<text>{{sport.caloriesBurned}} kcal</text>
								</view>
							</view>
						</view>
						
						<checkbox-group @change="checkin" class="checkin-checkbox">
							<label class="custom-checkbox">
								<checkbox 
									:value="String(sport.checkinId)" 
									color="#4CAF50" 
									border-color="#ddd"
									active-border-color="#4CAF50"
								/>
								<text class="checkbox-text">打卡</text>
							</label>
						</checkbox-group>
					</view>
				</view>
			</view>
			
			<!-- 已打卡的运动 -->
			<view class="checkin-section completed-section" v-if="recommendSports.some(sport => sport.feedback != null)">
				<view class="section-title">已完成运动</view>
				<view v-for="(sport, index) in recommendSports" :key="index">
					<view v-if="sport.feedback != null" class="card sport-completed-card">
						<view class="sport-icon-container completed">
							<text class="sport-icon">✓</text>
						</view>
						<view class="sport-content">
							<view class="sport-name">{{sport.exerciseName}}</view>
							<view class="sport-details">
								<view class="sport-duration">
									<text class="detail-icon">⏱️</text>
									<text>{{sport.duration}}分钟</text>
								</view>
								<view class="sport-calories">
									<text class="detail-icon">🔥</text>
									<text>{{sport.caloriesBurned}} kcal</text>
								</view>
								<view class="sport-feedback">
									<text class="detail-icon">{{options[sport.feedback].emoji}}</text>
									<text>{{options[sport.feedback].text}}</text>
								</view>
							</view>
						</view>
					</view>
				</view>
			</view>
			
			<!-- 运动疲劳反馈弹框 -->
			<u-popup :show="show" @close="close" @open="open" :round="16" mode="center">
				<view class="popup-container feedback-popup">
					<view class="popup-header">
						<view class="popup-title">运动疲劳反馈</view>
						<view class="popup-subtitle">请选择本次运动后的感受</view>
					</view>
					<view class="feedback-options">
						<view 
							v-for="(option, index) in options" 
							:key="index"
							:class="['feedback-option', selectedOption === option.id ? 'active' : '']"
							@click="selectOption(option.id)"
						>
							<text class="option-emoji">{{ option.emoji }}</text>
							<text class="option-text">{{ option.text }}</text>
							<view class="option-indicator"></view>
						</view>
					</view>
					
					<button class="submit-button" @click="submitFeedback">提交打卡</button>
				</view>
			</u-popup>
		</scroll-view>
		
		<!-- 历史运动 -->
		<scroll-view v-if="tab ===2" scroll-y class="history-scroll">
			<!-- 月份选择器 -->
			<MonthSelector @month-change="handleMonthChange" />
			
			<!-- 统计卡片 -->
			<view class="stats-card">
				<view class="stats-chart">
					<ProgressChart :title="chartTitle" :completed="completedSports" :total="totalSports" />
				</view>
				<view class="stats-info">
					<view class="stats-item">
						<text class="stats-label">打卡天数</text>
						<text class="stats-value">{{checkinDays}}<text class="stats-unit">天</text></text>
					</view>
					<view class="stats-item">
						<text class="stats-label">运动完成率</text>
						<text class="stats-value">{{(completedSports / totalSports * 100).toFixed(2)}}<text class="stats-unit">%</text></text>
					</view>
					<view class="stats-item">
						<text class="stats-label">消耗卡路里</text>
						<text class="stats-value">{{calories}}<text class="stats-unit">kcal</text></text>
					</view>
					<view class="stats-item">
						<text class="stats-label">运动时长</text>
						<text class="stats-value">{{duration}}<text class="stats-unit">分钟</text></text>
					</view>
				</view>
			</view>
			
			<!-- 每日运动记录 -->
			<view v-for="(day, index) in days" :key="index" class="day-card">
				<view class="day-header">{{day}}</view>
				<view class="day-content">
					<view 
						v-for="(sport, sportIndex) in historySports[day]" 
						:key="sportIndex" 
						:class="['sport-item', sport.feedback === null ? 'sport-unchecked' : 'sport-checked']">
						<view class="sport-info">
							<view class="sport-name">{{sport.exerciseName}}</view>
							<view class="sport-details">
								<text class="sport-duration">{{sport.duration}}分钟</text>
								<text class="sport-calories">{{sport.caloriesBurned}}kcal</text>
								<text v-if="sport.feedback !== null" class="sport-feedback">
									{{options[sport.feedback].emoji}} {{options[sport.feedback].text}}
								</text>
							</view>
						</view>
						<view v-if="sport.feedback !== null" class="sport-status completed"></view>
						<view v-else class="sport-status pending"></view>
					</view>
				</view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
import http from "@/utils/request";
import MonthSelector from "../../components/MonthSelector.vue";
import ProgressChart from '@/components/ProgressChart.vue';
export default {
	components: {
	    MonthSelector,
		ProgressChart,
	  },
	data() {
		return {
			list: ['今日运动计划', '运动打卡', '历史运动'],
			tab: 0 ,
			chartTitle: "运动完成率" ,
			recommendCalories: 600,
			recommendSports: [],
			show: false,
			checkinId: 0,//需要打卡的id
			options: [
			  { id: 0, text: '轻松', emoji: '😊' },
			  { id: 1, text: '适中', emoji: '😐' },
			  { id: 2, text: '疲惫', emoji: '😩' }
			],
			selectedOption: null,
			showSportPacker: false,
			sportsList:[],
			sportTypes:[],
			columns: [
			    ['中国', '美国'],
			    ['深圳', '厦门', '上海', '拉萨']
			],
			columnData: [
			    ['深圳', '厦门', '上海', '拉萨'],
			    ['得州', '华盛顿', '纽约', '阿拉斯加']
			],
			showAddSportPacker: false,
			curSport:null,
			duration:10,
			selectedYear: new Date().getFullYear(),
			selectedMonth: new Date().getMonth() + 1,
			historySports: [],
			days: [],
			checkinDays: 0,
			totalSports: 0,
			completedSports: 0,
			calories: 0,
			duration: 0,
		}
	},
	methods: {
		sectionChange(index) {
			this.tab = index;
		},
		//获取推荐运动
		getRecommend(){
			console.log('获取推荐运动');
			
			http.request({
			      url: '/exercise/recommend',
			      method: 'GET',
				  data:{
					  expectedCalories: this.recommendCalories
				  }
			}).then((res) => {
			  if (res.code === '200') {
			    this.recommendSports = res.data || [];
			  } else {
			    uni.showToast({
			      title: '获取推荐运动失败',
			      icon: 'none'
			    });
			  }
			}).catch(err => {
			  console.error('获取推荐运动失败', err);
			  uni.showToast({
			    title: '网络错误，请稍后重试',
			    icon: 'none'
			  });
			});
		},
		//打卡
		checkin(e){
			const values = e.detail.value;
			if (values.length > 0) {
			  this.checkinId = values[0];
			  this.show = true
			}
		},
		open() {},
		close() {
		  this.show = false
		  // console.log('close');
		},
		selectOption(id) {
		  this.selectedOption = id;
		},
		submitFeedback() {
		  if (this.selectedOption != null) {
		    console.log('提交的疲劳反馈:', this.selectedOption);

			http.request({
			      url: '/exercise/checkin',
			      method: 'GET',
				  data:{
					  checkinId: this.checkinId,
					  feedback: this.selectedOption
				  }
			}).then((res) => {
			  if (res.code === '200') {
			    uni.showToast({
				  title: '打卡成功',
				  icon: 'success'
				});
				this.show = false
				this.selectedOption = null
				//刷新页面
				this.refresh()
			  } else {
			    uni.showToast({
			      title: '获取推荐运动失败',
			      icon: 'none'
			    });
			  }
			}).catch(err => {
			  console.error('获取推荐运动失败', err);
			  uni.showToast({
			    title: '网络错误，请稍后重试',
			    icon: 'none'
			  });
			});
			
		  } else {
		    uni.showToast({
		      title: '请选择疲劳反馈',
		      icon: 'none'
		    });
		  }
		},
		
		//获取运动列表
		getExerciseList() {
		  console.log('获取运动列表');
		  http.request({
		        url: '/exercise/list',
		        method: 'GET',
		  }).then((res) => {
		    if (res.code === '200') {
				const sportsData = res.data;
				const sportTypes = Object.keys(sportsData);
				this.columnData = []
				for (var i=0; i<sportTypes.length; i++)
				{
					const sportType = sportTypes[i];
					const exerciseNames = this.extractProperty(sportsData[sportType], "exerciseName");
					this.columnData.push(exerciseNames)
				}
				const firstSportType = sportTypes[0];
				const exerciseNames = this.extractProperty(sportsData[firstSportType], "exerciseName");
				this.columns = [
					sportTypes,
					exerciseNames
				]
				// 保存完整运动列表
				this.sportsList = sportsData;
				this.sportTypes = sportTypes;
		    } else {
		      uni.showToast({
		        title: '获取运动列表失败',
		        icon: 'none'
		      });
		    }
		  }).catch(err => {
		    console.error('获取运动列表失败', err);
		    uni.showToast({
		      title: '网络错误，请稍后重试',
		      icon: 'none'
		    });
		  });
		},
		changeHandler(e) {
		    const {
		        columnIndex,
		        value,
		        values, // values为当前变化列的数组内容
		        index,
				// 微信小程序无法将picker实例传出来，只能通过ref操作
		        picker = this.$refs.uPicker
		    } = e
		    // 当第一列值发生变化时，变化第二列(后一列)对应的选项
		    if (columnIndex === 0) {
		        // picker为选择器this实例，变化第二列对应的选项
		        picker.setColumnValues(1, this.columnData[index])
		    }
		},
		// 回调参数为包含columnIndex、value、values
		confirm(e) {
		    console.log('confirm', e)
			const sportTypeKey = e.value[0]
			const sportIndex = e.indexs[1]
			const sport = this.sportsList[sportTypeKey][sportIndex]
			this.curSport = sport
		    this.showSportPacker = false
		},
		extractProperty(array, property) {
			return array.map(item => item[property]);
		},
		addSport(){
			if (this.curSport) {
				console.log('添加运动计划:', this.curSport);
			
				http.request({
					url: '/exercise/addNewToday',
					method: 'POST',
					data:{
						exerciseId		:this.curSport.exerciseId,
						exerciseName    :this.curSport.exerciseName,
						exerciseCategory:this.curSport.exerciseCategory,
						caloriesBurnRate:this.curSport.caloriesBurnRate,
						duration     	:this.duration,
					}
				}).then((res) => {
				if (res.code === '200') {
					uni.showToast({
						title: '添加运动计划成功',
						icon: 'success'
					});
					this.showAddSportPacker = false
					this.curSport = null
					//刷新页面
					this.refresh()
				} else {
					uni.showToast({
					title: '添加运动计划失败',
					icon: 'none'
					});
				}
				}).catch(err => {
					console.error('添加运动计划失败', err);
					uni.showToast({
						title: '网络错误，请稍后重试',
						icon: 'none'
					});
				});
						
			} else {
			  uni.showToast({
			    title: '请选择一项运动',
			    icon: 'none'
			  });
			}
		},
		
		handleMonthChange({ year, month }) {
		    this.selectedYear = year;
		    this.selectedMonth = month;
		    console.log(`选择的月份：${year}年${month}月`);
			this.getHistory()
		},
		// 获取历史运动
		getHistory(){
			const year = String(this.selectedYear)
			const month = this.selectedMonth<10? '0' + String(this.selectedMonth):String(this.selectedMonth)
			const day = year + '-' + month + '-01'
			http.request({
				url: '/exercise/history',
				method: 'GET',
				data:{
					month: day,
				}
			}).then((res) => {
				if (res.code === '200') {
					this.historySports = res.data
					this.days = Object.keys(res.data)
					this.sportsStatistics()
				} else {
					uni.showToast({
						title: '获取历史运动失败',
						icon: 'none'
					});
				}
			}).catch(err => {
				console.error('获取历史运动失败', err);
				uni.showToast({
					title: '网络错误，请稍后重试',
					icon: 'none'
				});
			});
		},
		//运动统计
		sportsStatistics(){
			let checkinDays = 0
			let totalSports = 0
			let completedSports = 0
			let calories = 0
			let duration = 0
			this.days.forEach(item => {
				const sports = this.historySports[item]
				let checkinFlag = false
				sports.forEach(sport => {
					totalSports += 1
					if(sport.checkinDate){
						checkinFlag = true
						completedSports += 1
						calories += sport.caloriesBurned
						duration += sport.duration
					}
				})
				if(checkinFlag){
					checkinDays += 1
				}
			})
			this.checkinDays = checkinDays
			this.totalSports = totalSports
			this.completedSports = completedSports
			this.calories = calories
			this.duration = duration
		},
		//刷新页面
		refresh(){
			this.getRecommend();
			this.getHistory();
			this.duration=10
		}
		
	},
	created() {
		this.getExerciseList();
		this.getRecommend();
		this.getHistory();
	},
	
}
</script>

<style>
.card {
    background-color: white;
    border-radius: 16px;
    padding: 24px;
	margin: 16px;
    box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:active {
    transform: translateY(-2px);
    box-shadow: 0 6rpx 25rpx rgba(0, 0, 0, 0.12);
}

.center{
	display: flex;
	justify-content: space-between;
	align-items: center;
}

/* 运动计划页面样式 */
.calories-card {
    background: linear-gradient(135deg, #4CAF50, #8BC34A);
    color: white;
    position: relative;
    overflow: hidden;
}

.calories-content {
    position: relative;
    z-index: 2;
}

.calories-label {
    font-size: 14px;
    opacity: 0.9;
    margin-bottom: 8px;
}

.calories-value {
    font-size: 32px;
    font-weight: bold;
    display: flex;
    align-items: baseline;
}

.calories-unit {
    font-size: 16px;
    opacity: 0.8;
    margin-left: 4px;
}

.calories-decoration {
    position: absolute;
    top: -20px;
    right: -20px;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    z-index: 1;
}

.sport-plan-card {
    display: flex;
    align-items: center;
    padding: 16px 20px;
    border-left: 4px solid #4CAF50;
}

.sport-icon-container {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: rgba(76, 175, 80, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;
    flex-shrink: 0;
}

.sport-icon-container.completed {
    background-color: #4CAF50;
    color: white;
}

.sport-icon {
    font-size: 24px;
}

.sport-content {
    flex: 1;
}

.sport-name {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin-bottom: 8px;
}

.sport-details {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.sport-duration, .sport-calories, .sport-feedback {
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #666;
    background-color: #f5f5f5;
    padding: 4px 10px;
    border-radius: 100px;
}

.detail-icon {
    margin-right: 4px;
}

/* 运动打卡页面样式 */
.checkin-section {
    margin-bottom: 20px;
}

.section-title {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin: 16px 16px 8px;
    position: relative;
    padding-left: 12px;
}

.section-title:before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 16px;
    background: linear-gradient(to bottom, #4CAF50, #8BC34A);
    border-radius: 2px;
}

.sport-checkin-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-left: 4px solid #FFC107;
    padding: 16px 20px;
}

.sport-completed-card {
    display: flex;
    align-items: center;
    border-left: 4px solid #4CAF50;
    padding: 16px 20px;
    background-color: rgba(76, 175, 80, 0.05);
}

.checkin-checkbox {
    margin-left: 16px;
}

.custom-checkbox {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.checkbox-text {
    font-size: 12px;
    color: #4CAF50;
    margin-top: 4px;
}

.completed-section {
    opacity: 0.85;
}

/* 历史运动页面样式 */
.history-scroll {
    padding: 0 12rpx;
    background-color: #f8f8f8;
}

.stats-card {
    background-color: white;
    border-radius: 16px;
    margin: 16px 12px;
    padding: 20px;
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
    display: flex;
    flex-direction: column;
}

.stats-chart {
    margin-bottom: 20rpx;
}

.stats-info {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-top: 10rpx;
}

.stats-item {
    width: 48%;
    margin-bottom: 16rpx;
    padding: 16rpx;
    background-color: #f9f9f9;
    border-radius: 12rpx;
    display: flex;
    flex-direction: column;
}

.stats-label {
    font-size: 24rpx;
    color: #666;
    margin-bottom: 8rpx;
}

.stats-value {
    font-size: 32rpx;
    font-weight: bold;
    color: #4CAF50;
}

.stats-unit {
    font-size: 24rpx;
    font-weight: normal;
    margin-left: 4rpx;
    color: #999;
}

.day-card {
    background-color: white;
    border-radius: 16px;
    margin: 16px 12px;
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
    overflow: hidden;
}

.day-header {
    padding: 16rpx 24rpx;
    font-size: 28rpx;
    font-weight: bold;
    color: #333;
    background-color: #f5f5f5;
    border-bottom: 1px solid #eee;
}

.day-content {
    padding: 8rpx 0;
}

.sport-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16rpx 24rpx;
    border-bottom: 1px solid #f5f5f5;
    position: relative;
}

.sport-item:last-child {
    border-bottom: none;
}

.sport-info {
    flex: 1;
}

.sport-name {
    font-size: 28rpx;
    font-weight: 500;
    color: #333;
    margin-bottom: 8rpx;
}

.sport-details {
    display: flex;
    flex-wrap: wrap;
    gap: 16rpx;
    font-size: 24rpx;
    color: #666;
}

.sport-duration, .sport-calories {
    background-color: #f5f5f5;
    padding: 4rpx 12rpx;
    border-radius: 100rpx;
}

.sport-feedback {
    color: #4CAF50;
    display: flex;
    align-items: center;
}

.sport-status {
    width: 16rpx;
    height: 16rpx;
    border-radius: 50%;
    margin-left: 16rpx;
}

.sport-status.completed {
    background-color: #4CAF50;
}

.sport-status.pending {
    background-color: #FFC107;
}

.sport-checked {
    background-color: rgba(76, 175, 80, 0.05);
}

.sport-unchecked {
    opacity: 0.8;
}

.container {
  padding: 30px;
  background-color: #f8f8f8;
  min-height: 100vh;
}

.title {
  font-size: 36rpx;
  font-weight: bold;
  margin-bottom: 30rpx;
  color: #333;
  position: relative;
  padding-bottom: 16rpx;
}

.title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60rpx;
  height: 6rpx;
  background: linear-gradient(to right, #4CAF50, #8BC34A);
  border-radius: 3rpx;
}

/* 弹框容器样式 */
.popup-container {
  padding: 30rpx;
  width: 100%;
  box-sizing: border-box;
  background-color: #fff;
  border-radius: 16px 16px 0 0;
  max-width: 650rpx;
  margin: 0 auto;
}

.popup-header {
  margin-bottom: 30rpx;
  text-align: center;
  position: relative;
}

.popup-title {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 8rpx;
  position: relative;
  display: inline-block;
}

.popup-title::after {
  content: '';
  position: absolute;
  bottom: -10rpx;
  left: 50%;
  transform: translateX(-50%);
  width: 80rpx;
  height: 6rpx;
  background: linear-gradient(to right, #4CAF50, #8BC34A);
  border-radius: 3rpx;
}

.popup-subtitle {
  font-size: 24rpx;
  color: #999;
  margin-top: 16rpx;
}

.options {
  display: flex;
  gap: 16rpx;
  margin-bottom: 30rpx;
}

.feedback-popup {
  width: 90%;
  max-width: 650rpx;
  padding: 40rpx 30rpx;
}

.feedback-options {
  display: flex;
  justify-content: space-between;
  margin: 30rpx 0 40rpx;
  gap: 20rpx;
}

.feedback-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30rpx 20rpx;
  border-radius: 20rpx;
  background-color: #f8f8f8;
  box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  position: relative;
  overflow: hidden;
  border: 2rpx solid transparent;
}

.feedback-option:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6rpx;
  background: linear-gradient(to right, #4CAF50, #8BC34A);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feedback-option.active {
  background-color: rgba(76, 175, 80, 0.08);
  border-color: rgba(76, 175, 80, 0.3);
  transform: translateY(-4rpx);
  box-shadow: 0 10rpx 25rpx rgba(76, 175, 80, 0.15);
}

.feedback-option.active:before {
  opacity: 1;
}

.option-text {
  margin-top: 16rpx;
  font-size: 32rpx;
  font-weight: 500;
  color: #333;
  transition: color 0.3s ease;
}

.option-emoji {
  font-size: 60rpx;
  margin-bottom: 10rpx;
  transform: scale(1);
  transition: transform 0.3s ease;
}

.feedback-option.active .option-emoji {
  transform: scale(1.2);
}

.feedback-option.active .option-text {
  color: #4CAF50;
  font-weight: 600;
}

.option-indicator {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background-color: #4CAF50;
  position: absolute;
  top: 16rpx;
  right: 16rpx;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s ease;
}

.feedback-option.active .option-indicator {
  opacity: 1;
  transform: scale(1);
}

.submit-button {
  width: 90%;
  padding: 28rpx;
  background: linear-gradient(to right, #4CAF50, #8BC34A);
  color: white;
  border: none;
  border-radius: 100rpx;
  font-size: 32rpx;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.3s ease;
  box-shadow: 0 8rpx 20rpx rgba(76, 175, 80, 0.25);
  margin: 0 auto;
  letter-spacing: 4rpx;
  position: relative;
  overflow: hidden;
}

.submit-button:active {
  background: linear-gradient(to right, #3e8e41, #7cb342);
  transform: translateY(2px);
  box-shadow: 0 2rpx 10rpx rgba(76, 175, 80, 0.1);
}

.submit-button::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: rgba(255, 255, 255, 0.1);
  transform: rotate(45deg);
  transition: all 0.6s ease;
  opacity: 0;
}

.submit-button:active::after {
  opacity: 1;
}

.uni-list-cell {
	position: relative;
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	align-items: center;
	padding: 20rpx 0;
	border-bottom: 1px solid #f0f0f0;
}

.uni-list-cell-left {
    white-space: nowrap;
	font-size: 28rpx;
	padding: 0 30rpx;
	color: #666;
}

.uni-list-cell-db,
.uni-list-cell-right {
	flex: 1;
	font-size: 30rpx;
	color: #333;
	font-weight: 500;
}

.uni-input {
	padding: 20rpx;
	border: 1px solid #e0e0e0;
	border-radius: 8px;
	margin: 20rpx 0;
	font-size: 28rpx;
}

/* 添加运动弹框样式 */
.add-sport-form {
  padding: 0 20rpx;
  margin-bottom: 40rpx;
}

.form-item {
  margin-bottom: 30rpx;
}

.form-label {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 16rpx;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.form-label::before {
  content: '';
  display: inline-block;
  width: 8rpx;
  height: 28rpx;
  background-color: #4CAF50;
  margin-right: 12rpx;
  border-radius: 4rpx;
}

.form-input {
  height: 100rpx;
  border: 1px solid #e0e0e0;
  border-radius: 16rpx;
  font-size: 28rpx;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
  padding: 0 24rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.form-input:focus {
  border-color: #4CAF50;
  box-shadow: 0 0 0 2rpx rgba(76, 175, 80, 0.2);
}

.sport-selector {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 24rpx;
  background-color: #f5f5f5;
  border-radius: 16rpx;
  box-shadow: inset 0 2rpx 6rpx rgba(0, 0, 0, 0.05);
}

.selected-sport {
  display: flex;
  align-items: center;
  flex-wrap: nowrap;
}

.sport-category {
  color: #4CAF50;
  font-weight: 500;
  margin-right: 8rpx;
  white-space: nowrap;
  background-color: rgba(76, 175, 80, 0.1);
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
}

.sport-category::after {
  content: ' - ';
  color: #999;
  margin: 0 4rpx;
}

.sport-name-1 {
  color: #333;
  font-weight: 500;
  margin-right: 8rpx;
  white-space: nowrap;
  padding: 4rpx 0;
}

.placeholder {
  color: #999;
  padding: 4rpx 0;
  font-size: 26rpx;
}

.select-icon {
  color: #4CAF50;
  font-size: 24rpx;
  background-color: rgba(76, 175, 80, 0.1);
  width: 40rpx;
  height: 40rpx;
  line-height: 40rpx;
  text-align: center;
  border-radius: 50%;
}
</style>

