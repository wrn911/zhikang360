<template>
	<view>
		<view>
			<u-subsection style="margin-top: 5px;" activeColor="green" :list="list" :current="tab" @change="sectionChange"></u-subsection>
		</view>
		
		<!-- 食物计划 -->
		<scroll-view v-if="tab ===0" scroll-y>
			<view class="card calories-card">
				<view class="calories-content">
					<view class="calories-label">推荐摄入食物卡路里数</view>
					<view class="calories-value">
						{{recommendCalories}} <text class="calories-unit">kcal</text>
					</view>
					<view class="calories-decoration"></view>
				</view>
			</view>
			<!--早餐 -->
			<view class="checkin-breakfast">
				<view class="section-title">早餐推荐</view>
				<view v-for="(food, index) in recommendFoodsBreakfast" :key="index">
						<view class="food-content">
							<view class="food-name">{{food.foodName}}</view>
							<view class="food-details">
								<view class="food-grams">
								    <text class="detail-icon">⚖️</text>
								    <text>{{food.grams}} g</text>
								</view>
								<view class="food-calories">
									<text class="detail-icon">🔥</text>
									<text>{{food.calories}} kcal</text>
								</view>
							</view>
						</view>
				</view>
			</view>
			
			<!--午餐 -->
			<view class="checkin-lunch">
				<view class="section-title">午餐推荐</view>
				<view v-for="(food, index) in recommendFoodsLunch" :key="index">
						<view class="food-content">
							<view class="food-name">{{food.foodName}}</view>
							<view class="food-details">
								<view class="food-grams">
								    <text class="detail-icon">⚖️</text>
								    <text>{{food.grams}} g</text>
								</view>
								<view class="food-calories">
									<text class="detail-icon">🔥</text>
									<text>{{food.calories}} kcal</text>
								</view>
							</view>
						</view>
				</view>
			</view>	
			
			<!--晚餐 -->
			<view class="checkin-dinner">
				<view class="section-title">晚餐推荐</view>
				<view v-for="(food, index) in recommendFoodsDinner" :key="index">
						<view class="food-content">
							<view class="food-name">{{food.foodName}}</view>
							<view class="food-details">
								<view class="food-grams">
								    <text class="detail-icon">⚖️</text>
								    <text>{{food.grams}} g</text>
								</view>
								<view class="food-calories">
									<text class="detail-icon">🔥</text>
									<text>{{food.calories}} kcal</text>
								</view>
							</view>
						</view>
				</view>
			</view>	
			
		</scroll-view>
		
		<!-- 食物打卡 -->
		<scroll-view v-if="tab ===1" scroll-y>
			<view class="stats-chart">
				<ProgressChart :title="chartTitle1" :completed="completedCalories" :total="recommendCalories" />
			</view>
			<!--早餐 -->
			<view class="checkin-breakfast">
				<view class="section-title">早餐打卡</view>
				<view v-for="(food, index) in checkinFoodsBreakfast" :key="index">
						<view class="food-content">
							<view class="food-name">{{food.foodName}}</view>
							<view class="food-details">
								<view class="food-grams">
								    <text class="detail-icon">⚖️</text>
								    <text>{{food.grams}} g</text>
								</view>
								<view class="food-calories">
									<text class="detail-icon">🔥</text>
									<text>{{food.calories}} kcal</text>
								</view>
							</view>
						</view>
				</view>
			</view>
			
			<!--午餐 -->
			<view class="checkin-lunch">
				<view class="section-title">午餐打卡</view>
				<view v-for="(food, index) in checkinFoodsLunch" :key="index">
						<view class="food-content">
							<view class="food-name">{{food.foodName}}</view>
							<view class="food-details">
								<view class="food-grams">
								    <text class="detail-icon">⚖️</text>
								    <text>{{food.grams}} g</text>
								</view>
								<view class="food-calories">
									<text class="detail-icon">🔥</text>
									<text>{{food.calories}} kcal</text>
								</view>
							</view>
						</view>
				</view>
			</view>	
			
			<!--晚餐 -->
			<view class="checkin-dinner">
				<view class="section-title">晚餐打卡</view>
				<view v-for="(food, index) in checkinFoodsDinner" :key="index">
						<view class="food-content">
							<view class="food-name">{{food.foodName}}</view>
							<view class="food-details">
								<view class="food-grams">
								    <text class="detail-icon">⚖️</text>
								    <text>{{food.grams}} g</text>
								</view>
								<view class="food-calories">
									<text class="detail-icon">🔥</text>
									<text>{{food.calories}} kcal</text>
								</view>
							</view>
						</view>
				</view>
			</view>	
			
			<u-button @click="showAddFoodPacker=true" icon="plus" type="success" style="border-radius: 50%; position: fixed; bottom: 15vw; right:6vw; width: 12vw; height: 12vw;"/>
		</scroll-view>
		
		<u-picker :show="showFoodPacker" ref="uPicker" :columns="columns" @confirm="confirm" @change="changeHandler" @cancel="showFoodPacker=false"></u-picker>
		<!-- 添加uView的picker组件 -->
		<u-picker :show="showMealPicker" ref="uPicker" :columns="mealColumns" @confirm="handleMealConfirm" @change="changeMealHandler" @cancel="showMealPicker=false"></u-picker>
		<u-popup :show="showAddFoodPacker" @close="showAddFoodPacker=false" zIndex="10074" :round="16">
		    <view class="popup-container">
				<view class="popup-header">
					<view class="popup-title">请添加食物</view>
					<view class="popup-subtitle">选择食物类型和食物克数</view>
				</view>
				<view class="add-food-form">
					 <!-- 新增餐别选择项 -->
					<view class="form-item">
					    <view class="form-label">餐别：</view>
					        <view class="form-input sport-selector" @click="showMealPicker=true">
					            <view class="selected-sport" v-if="selectedMeal">
									<text class="food-meal">{{ selectedMeal }}</text>
					            </view>
					            <view class="placeholder" v-else>请选择餐别</view>
					            <text class="select-icon">▼</text>
					    </view>
					</view>
					<view class="form-item">
						<view class="form-label">食物类型：</view>
						<view class="form-input sport-selector" @click="showFoodPacker=true">
							<view class="selected-sport" v-if="curFood!=null">
								<text class="food-category">{{curFood.category}}</text>
								<text class="food-name-1">{{curFood.name}}</text>
							</view>
							<view class="placeholder" v-else>请选择食物类型</view>
							<text class="select-icon">▼</text>
						</view>
					</view>
					<view class="form-item">
						<view class="form-label">食物摄入重量：</view>
						<input class="form-input" v-model="duration" type="number" placeholder="请输入摄入食物重量（克）"/>
					</view>
				</view>
				<button class="submit-button" @click="addFood">添加食物打卡</button>
			</view>
		</u-popup>
		
        <!-- 历史饮食 -->
        <scroll-view v-if="tab ===2" scroll-y class="history-scroll">
            <!-- 月度统计保留 -->
            <view class="stats-card">
                <view class="stats-chart">
                    <ProgressChart :title="chartTitle2" :completed="checkinDays" :total="totalDays" />
                </view>
                <view class="stats-info">
                    <view class="stats-item">
                        <text class="stats-label">打卡天数</text>
                        <text class="stats-value">{{checkinDays}}<text class="stats-unit">天</text></text>
                    </view>
                    <view class="stats-item">
                        <text class="stats-label">打卡完成率</text>
                        <text class="stats-value">{{(checkinDays / totalDays * 100).toFixed(2)}}<text class="stats-unit">%</text></text>
                    </view>
                    <view class="stats-item">
                        <text class="stats-label">摄入卡路里</text>
                        <text class="stats-value">{{finalCalories}}<text class="stats-unit">kcal</text></text>
                    </view>
                </view>
            </view>
        
            <!-- 当日饮食记录 -->
            <view class="stats-card">
				<!-- 日期选择器 
				<view class="date-navigator">
				    <text class="arrow" @click="changeDay(-1)">◀</text>
				    <text class="current-date" @click="showDatePicker = true">
				        {{ selectedDate }}
				    </text>
				    <text class="arrow" @click="changeDay(1)">▶</text>
				    <u-picker 
				        :show="showDatePicker"
				        mode="time" 
				        :params="dateParams"
				        @confirm="confirmDate"
				        @cancel="showDatePicker = false"
				    ></u-picker>
				</view>-->
				<!-- 日期选择器 -->
				<view class="date-navigator">
				    <text class="arrow" @click="changeDay(-1)">◀</text>
				    <text class="current-date" @click="showCalendar = true">
				        {{ selectedDate }}
				    </text>
				    <text class="arrow" @click="changeDay(1)">▶</text>
				
				    <!-- uni-calendar 弹窗 -->
				    <uni-calendar
				        :insert="false"
				        :show="showCalendar"
				        :date="selectedDate"
				        @confirm="confirmCalendar"
				        @close="showCalendar = false"
				    />
				</view>
                <!--早餐 -->
                <view class="checkin-breakfast">
                	<view class="section-title">当天早餐打卡</view>
                	<view v-for="(food, index) in historyFoodsBreakfast" :key="index">
                			<view class="food-content">
                				<view class="food-name">{{food.foodName}}</view>
                				<view class="food-details">
                					<view class="food-grams">
                					    <text class="detail-icon">⚖️</text>
                					    <text>{{food.grams}} g</text>
                					</view>
                					<view class="food-calories">
                						<text class="detail-icon">🔥</text>
                						<text>{{food.calories}} kcal</text>
                					</view>
                				</view>
                			</view>
                	</view>
                </view>
                
                <!--午餐 -->
                <view class="checkin-lunch">
                	<view class="section-title">当天午餐打卡</view>
                	<view v-for="(food, index) in historyFoodsLunch" :key="index">
                			<view class="food-content">
                				<view class="food-name">{{food.foodName}}</view>
                				<view class="food-details">
                					<view class="food-grams">
                					    <text class="detail-icon">⚖️</text>
                					    <text>{{food.grams}} g</text>
                					</view>
                					<view class="food-calories">
                						<text class="detail-icon">🔥</text>
                						<text>{{food.calories}} kcal</text>
                					</view>
                				</view>
                			</view>
                	</view>
                </view>	
                
                <!--晚餐 -->
                <view class="checkin-dinner">
                	<view class="section-title">当天晚餐打卡</view>
                	<view v-for="(food, index) in historyFoodsDinner" :key="index">
                			<view class="food-content">
                				<view class="food-name">{{food.foodName}}</view>
                				<view class="food-details">
                					<view class="food-grams">
                					    <text class="detail-icon">⚖️</text>
                					    <text>{{food.grams}} g</text>
                					</view>
                					<view class="food-calories">
                						<text class="detail-icon">🔥</text>
                						<text>{{food.calories}} kcal</text>
                					</view>
                				</view>
                			</view>
                	</view>
                </view>	
			</view>
        </scroll-view>
		<!-- 修改后的弹窗结构 -->
		<view v-if="showMultiBadgeModal" class="badge-modal-mask">
		    <view class="multi-badge-modal">
		        <view class="modal-header">
		            <image src="/static/medal-ribbon.png" class="header-icon"/>
		            <text class="header-text">成就达成!</text>
		        </view>
		        
		        <scroll-view scroll-x class="badge-scroll" :scroll-into-view="scrollToId" enable-flex>
		            <!-- 添加外层容器确保居中 -->
		            <view class="badge-container">
		                <view 
		                    v-for="(badge, index) in newBadges" 
		                    :key="index" 
		                    class="badge-item"
		                    :style="{ marginRight: index === newBadges.length-1 ? '0' : '40px' }"
		                >
		                    <view class="badge-frame">
		                        <image :src="badge.url" mode="aspectFit" class="badge-image"/>
		                    </view>
		                    <text class="badge-name">{{ badge.name }}</text>
		                </view>
		            </view>
		        </scroll-view>
		
		        <view class="congrats-text">
		            <image src="/static/confetti.png" class="confetti-left"/>
		            <text class="congrats">🎉 恭喜获得新成就 🎉</text>
		            <image src="/static/confetti.png" class="confetti-right"/>
		        </view>
		        <button class="confirm-btn" @click="showMultiBadgeModal = false">好的，继续打卡</button>
		    </view>
		</view>
	</view>
</template>

<script>
import _ from 'lodash'
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
			list: ['今日饮食推荐', '饮食打卡', '历史饮食'],
			tab: 0 ,
			//一、推荐饮食
			recommendCalories: 2600,       // 推荐卡路里
			// 推荐数据
			recommendFoodsBreakfast: [],     // 早餐食物
			recommendFoodsLunch: [],         // 午餐食物
			recommendFoodsDinner: [],        // 晚餐食物
			
			//二、饮食打卡
			//图表标题
			chartTitle1: "卡路里摄入" ,
			// 打卡数据
			checkinFoodsBreakfast: [],     // 早餐食物
			checkinFoodsLunch: [],         // 午餐食物
			checkinFoodsDinner: [],        // 晚餐食物
			completedCalories: 0,          // 已摄入卡路里
			
			// 新增以下变量
            showMultiBadgeModal: false,
            newBadges: [],
            scrollToId: '',
			
			// 食物选择器相关
			showFoodPacker: false,         // 食物选择器显示状态
			columns: [                     // 级联选择器数据
			  ['中国', '美国'],
			  ['深圳', '厦门', '上海', '拉萨']
			],
			columnData: [                  // 级联选择器源数据
			  ['深圳', '厦门', '上海', '拉萨'],
			  ['得州', '华盛顿', '纽约', '阿拉斯加']
			],
			
			// 新增食物弹窗
			showAddFoodPacker: false,      // 新增食物弹窗状态
			selectedMeal: null,            // 当前选中餐别
			showMealPicker: false,         // 餐别选择器状态
			mealColumns: [['早餐', '午餐', '晚餐']], // 餐别数据
			curFood: null,                 // 当前选中食物
			duration: 0,                   // 食物克数
			
			//三、历史饮食
			//图表标题
			chartTitle2: "本月打卡情况" ,
			// 日期相关
			selectedDate: "2025-4-11",    // 默认值需要动态生成（示例值）
			showDatePicker: false,         // 日期选择器状态
			dateParams: {                  // 日期选择器配置
			  year: true,
			  month: true,
			  day: true
			},
			
			// 统计数据
			checkinDays: 0,                // 打卡天数
			totalDays: 10,                 // 当月天数
			finalCalories: 0,                   // 总卡路里
			historyFoodsBreakfast: [],     // 早餐食物
			historyFoodsLunch: [],         // 午餐食物
			historyFoodsDinner: [],        // 晚餐食物
			showCalendar: false,  // 控制日历显示
			// 分页查询
			selectedYear: new Date().getFullYear(),  // 当前年
			selectedMonth: new Date().getMonth() + 1 // 当前月
		}
	},
	methods: {
		sectionChange(index) {
			this.tab = index;
		},
		// 日历确认回调
		    // 日期确认回调
		        confirmCalendar(e) {
		          this.selectedDate = e.fulldate
		          this.showCalendar = false
		          this.getHistory()
		        },
			
		// 在页面或组件 methods 中
		async fetchNutritionStats() {
		  http.request({
		        url: '/foodCheckin/stat',
		        method: 'GET',
		  }).then((response) =>{
		    if (response.code === '200') {
		      this.checkinDays = response.data.checkinDays;
		      this.finalCalories = response.data.finalCalories;
		      // 保持日期同步
		      this.selectedDate = response.data.selectedDate;
			  this.totalDays = response.data.totalDays;
			  this.getHistory();
		    } else {
		      uni.showToast({ title: '数据获取失败', icon: 'none' });
		    }
		  } ).catch(err => {
		    console.error('获取列表失败', err);
		    uni.showToast({
		      title: '网络错误，请稍后重试',
		      icon: 'none'
		    });
		  });
		},
		//获取运动列表
		getFoodList() {
		  console.log('获取食物列表');
		  http.request({
		        url: '/foodCheckin/list',
		        method: 'GET',
		  }).then((res) => {
		    if (res.code === '200') {
				const foodsData = res.data;
				const foodTypes = Object.keys(foodsData);
				this.columnData = []
				for (var i=0; i<foodTypes.length; i++)
				{
					const foodType = foodTypes[i];
					const foodNames = this.extractProperty(foodsData[foodType], "name");
					this.columnData.push(foodNames)
				}
				const firstFoodType = foodTypes[0];
				const foodNames = this.extractProperty(foodsData[firstFoodType], "name");
				this.columns = [
					foodTypes,
					foodNames
				]
				// 保存完整运动列表
				this.foodsList = foodsData;
				this.foodTypes = foodTypes;
		    } else {
		      uni.showToast({
		        title: '获取食物列表失败',
		        icon: 'none'
		      });
		    }
		  }).catch(err => {
		    console.error('获取食物列表失败', err);
		    uni.showToast({
		      title: '网络错误，请稍后重试',
		      icon: 'none'
		    });
		  });
		},
		extractProperty(array, property) {
			return array.map(item => item[property]);
		},
		// 回调参数为包含columnIndex、value、values
		confirm(e) {
		    console.log('confirm', e)
			const foodTypeKey = e.value[0]
			const foodIndex = e.indexs[1]
			const food = this.foodsList[foodTypeKey][foodIndex]
			this.curFood = food
		    this.showFoodPacker = false
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
		changeMealHandler(e) {
		    const {
		        columnIndex,
		        value,
		        index,
				// 微信小程序无法将picker实例传出来，只能通过ref操作
		        picker = this.$refs.uPicker
		    } = e
		},
		
		// 获取打卡记录
		  getFoodCheckin() {
		    uni.showLoading({ title: '加载中...' });
		    
		    http.request({
		      url: '/foodCheckin/list_checkIn',
		      method: 'GET',
		    }).then(res => {
		      uni.hideLoading();
		      if (res.code === '200') {
		        // 处理服务端返回的Map结构
		        const checkinData = res.data;
		        let totalCalories = 0; // 新增卡路里累加器
		        // 转换为更清晰的键名映射（根据实际返回的key调整）
		        const keyMapping = {
		          'breakfast': 'checkinFoodsBreakfast',
		          'lunch': 'checkinFoodsLunch',
		          'dinner': 'checkinFoodsDinner',
		          // 兼容中文key的情况
		          '早餐': 'checkinFoodsBreakfast',
		          '午餐': 'checkinFoodsLunch',
		          '晚餐': 'checkinFoodsDinner'
		        };
		        
		        // 初始化数据容器
		        const result = {
		          checkinFoodsBreakfast: [],
		          checkinFoodsLunch: [],
		          checkinFoodsDinner: []
		        };
		        
		        // 遍历服务端返回的Map
		        Object.keys(checkinData).forEach(originalKey => {
		          // 统一转为小写处理键名差异
		          const normalizedKey = originalKey.toLowerCase();
		          
		          // 匹配有效数据容器
		          const targetKey = Object.keys(keyMapping).find(k => 
		            k.toLowerCase() === normalizedKey
		          );
		          
		          if (targetKey) {
		            result[keyMapping[targetKey]] = checkinData[originalKey].map(item => {
					  const calories1 = Number(item.caloriesAte) ;
					  totalCalories += calories1; // 累加到总卡路里
					  return {
						  foodName: item.foodName,
						  calories: item.caloriesAte,
						  grams:    item.gramAte,
						  // 其他需要展示的字段...
					  }
		            });
		          }
		        });
		        
		        // 更新视图数据
		        this.checkinFoodsBreakfast = result.checkinFoodsBreakfast;
		        this.checkinFoodsLunch = result.checkinFoodsLunch;
		        this.checkinFoodsDinner = result.checkinFoodsDinner;
				this.completedCalories = totalCalories; // 设置总卡路里值
		        
		      } else {
		        uni.showToast({ title: '数据获取失败', icon: 'none' });
		      }
		    }).catch(err => {
		      uni.hideLoading();
		      console.error('请求异常:', err);
		      uni.showToast({ title: '网络异常', icon: 'none' });
		    });
		  },
		  
		  // 获取历史记录
		    getHistory() {
		      uni.showLoading({ title: '加载中...' });
		      
		      http.request({
		        url: '/foodCheckin/history',
		        method: 'GET',
				data: {
					selectedDate: this.selectedDate
				}
		      }).then(res => {
		        uni.hideLoading();
		        if (res.code === '200') {
		          // 处理服务端返回的Map结构
		          const historyData = res.data;
		          // 转换为更清晰的键名映射（根据实际返回的key调整）
		          const keyMapping = {
		            'breakfast': 'historyFoodsBreakfast',
		            'lunch': 'historyFoodsLunch',
		            'dinner': 'historyFoodsDinner',
		            // 兼容中文key的情况
		            '早餐': 'historyFoodsBreakfast',
		            '午餐': 'historyFoodsLunch',
		            '晚餐': 'historyFoodsDinner'
		          };
		          
		          // 初始化数据容器
		          const result = {
		            historyFoodsBreakfast: [],
		            historyFoodsLunch: [],
		            historyFoodsDinner: []
		          };
		          
		          // 遍历服务端返回的Map
		          Object.keys(historyData).forEach(originalKey => {
		            // 统一转为小写处理键名差异
		            const normalizedKey = originalKey.toLowerCase();
		            
		            // 匹配有效数据容器
		            const targetKey = Object.keys(keyMapping).find(k => 
		              k.toLowerCase() === normalizedKey
		            );
		            
		            if (targetKey) {
		              result[keyMapping[targetKey]] = historyData[originalKey].map(item => {
		  			  return {
		  				  foodName: item.foodName,
		  				  calories: item.caloriesAte,
		  				  grams:    item.gramAte,
		  				  // 其他需要展示的字段...
		  			  }
		              });
		            }
		          });
		          
		          // 更新视图数据
		          this.historyFoodsBreakfast = result.historyFoodsBreakfast;
		          this.historyFoodsLunch = result.historyFoodsLunch;
		          this.historyFoodsDinner = result.historyFoodsDinner;
		          
		        } else {
		          uni.showToast({ title: '数据获取失败', icon: 'none' });
		        }
		      }).catch(err => {
		        uni.hideLoading();
		        console.error('请求异常:', err);
		        uni.showToast({ title: '网络异常', icon: 'none' });
		      });
		    },
			
			// 获取推荐记录
			  getRecommend() {
			    uni.showLoading({ title: '加载中...' });
			    
			    http.request({
			      url: '/foodCheckin/recommend',
			      method: 'GET'
			    }).then(res => {
			      uni.hideLoading();
			      if (res.code === '200') {
			        // 处理服务端返回的Map结构
			        const recommendData = res.data;
			        // 转换为更清晰的键名映射（根据实际返回的key调整）
			        const keyMapping = {
			          'breakfast': 'recommendFoodsBreakfast',
			          'lunch': 'recommendFoodsLunch',
			          'dinner': 'recommendFoodsDinner',
			          // 兼容中文key的情况
			          '早餐': 'recommendFoodsBreakfast',
			          '午餐': 'recommendFoodsLunch',
			          '晚餐': 'recommendFoodsDinner'
			        };
			        
			        // 初始化数据容器
			        const result = {
			          recommendFoodsBreakfast: [],
			          recommendFoodsLunch: [],
			          recommendFoodsDinner: []
			        };
			        
			        // 遍历服务端返回的Map
			        Object.keys(recommendData).forEach(originalKey => {
			          // 统一转为小写处理键名差异
			          const normalizedKey = originalKey.toLowerCase();
			          
			          // 匹配有效数据容器
			          const targetKey = Object.keys(keyMapping).find(k => 
			            k.toLowerCase() === normalizedKey
			          );
			          
			          if (targetKey) {
			            result[keyMapping[targetKey]] = recommendData[originalKey].map(item => {
						  return {
							  foodName: item.foodName,
							  calories: item.caloriesAte,
							  grams:    item.gramAte,
							  // 其他需要展示的字段...
						  }
			            });
			          }
			        });
			        
			        // 更新视图数据
			        this.recommendFoodsBreakfast = result.recommendFoodsBreakfast;
			        this.recommendFoodsLunch = result.recommendFoodsLunch;
			        this.recommendFoodsDinner = result.recommendFoodsDinner;
			        
			      } else {
			        uni.showToast({ title: '数据获取失败672', icon: 'none' });
			      }
			    }).catch(err => {
			      uni.hideLoading();
			      console.error('请求异常:', err);
			      uni.showToast({ title: '网络异常', icon: 'none' });
			    });
			  },
		// 新增餐别确认方法（修正版）
		    handleMealConfirm(e) {
		        // uView 2.x/3.x取值方式
		        const selected = e.value[0]?.label || e.value[0]
		        this.selectedMeal = selected
		        this.showMealPicker = false
		        
		        // 调试日志
		        console.log('已选择餐别:', this.selectedMeal, '原始数据:', e)
		    },
		    // 修改后的新增食物打卡方法
		    async addFood() {
		        // 防止重复提交
		        if (this.isSubmitting) return;
		        this.isSubmitting = true;
		        
		        uni.showLoading({ title: '提交中...', mask: true });
		    
		        try {
		            // 增强版验证
		            const validation = this.validateFoodInput();
		            if (!validation.isValid) {
		                uni.showToast({ title: validation.message, icon: 'none' });
		                return;
		            }
		    
		            // 安全构造请求数据
		            const postData = this.buildFoodPostData();
		            
		            // 发送请求
		            const res = await http.request({
		                url: '/foodCheckin/add',
		                method: 'POST',
		                data: postData,
		                //timeout: 30000 // 增加超时设置
		            });
		    
		            // 处理响应
		            this.handleAddResult(res);
		            
		            // 成功后更新总热量
		            this.completedCalories += postData.calories;
					
					// 获取新徽章（数组形式）
					const badgeRes = await http.request({
					    url: '/badgeStandard/selectEarnedNewBadges',
					    method: 'GET'
					});
					
					// 显示所有新徽章
					if (badgeRes.data?.length > 0) {
					    this.showNewBadgesPopup(badgeRes.data);
					};
					
					this.resetForm();
					this.refreshData();
		    
		        } catch (err) {
		            this.handleAddError(err);
		        } finally {
		            this.isSubmitting = false;
		            uni.hideLoading();
		        }
		    },
			
			// 新增展示多个徽章的方法
			showNewBadgesPopup(badges) {
			    this.newBadges = badges; // 存储徽章数组
			    this.showMultiBadgeModal = true;
			
			    // 可选：标记已读（需要新增批量标记接口）
			    /*http.request({
			        url: '/badgeStandard/batchMarkAsRead',
			        method: 'POST',
			        data: { badgeIds: badges.map(b => b.id) }
			    });*/
			},
		
		    // 增强版输入验证
		    validateFoodInput() {
		        const checks = {
		            mealType: () => (!this.selectedMeal && '请选择餐别'),
		            food: () => (!this.curFood?.id && '请选择食物'),
		            grams: () => {
		                const grams = Number(this.duration);
		                if (isNaN(grams)) return '请输入有效数字';
		                if (grams <= 0) return '重量需大于0';
		                if (grams > 5000) return '单次摄入量过大';
		                return true;
		            }
		        };
		    
		        for (const [key, check] of Object.entries(checks)) {
		            const result = check();
		            if (typeof result === 'string') {
		                return { isValid: false, message: result };
		            }
		        }
		        return { isValid: true };
		    },
		  
		    // 安全构建请求数据
		    buildFoodPostData() {
		        return {
		            foodId: this.curFood?.id ?? '',
		            foodName: this.curFood?.name || '未知食物',
		            category: this.curFood?.category || '其他',
		            grams: Math.floor(Number(this.duration)), // 取整处理
		            mealType: this.selectedMeal || '未指定',
		        };
		    },
			
			
		
		    // 卡路里计算
		    calculateCalories() {
		        return Math.round(
		            (this.curFood.caloriesPer100g / 100) * this.duration
		        )
		    },
		    // 按餐别分组
		    groupByMeal(foods) {
		        return foods.reduce((acc, food) => {
		            const meal = food.mealType || '未分类'
		            acc[meal] = acc[meal] || []
		            acc[meal].push(food)
		            return acc
		        }, {})
		    },
		// 重置表单状态
		    resetForm() {
		        this.selectedMeal = null
		        this.curFood = null
		        this.duration = 0
		        this.showAddFoodPacker = false
		    },
		
		    // 增强结果处理
		    handleAddResult(res) {
		        if (res.code === '200') {
		            uni.showToast({ 
		                title: '添加成功', 
		                icon: 'success',
		                duration: 1500,
		            });
		        } else {
		            uni.showToast({ 
		                title: `失败: ${res.msg || '服务器错误'}`, 
		                icon: 'none',
		                duration: 3000 
		            });
		        }
		    },
			
			// 增强错误处理
			handleAddError(err) {
			    console.error('提交错误:', err);
			    //const isTimeout = err.errMsg?.includes('timeout');
			    //const message = isTimeout ? '网络超时，请重试' : '网络异常，请检查连接';
			    
			    uni.showModal({
			        title: '操作失败',
			        content: message,
			        showCancel: false,
			        confirmText: '知道了'
			    });
			},
			
		 // 日期变化处理（增加防抖）
		    changeDay: _.debounce(function(offset) {
		        const date = new Date(this.selectedDate)
		        date.setDate(date.getDate() + offset)
		        this.selectedDate = this.formatDate(date)
				this.getHistory()
		    }, 300),
			
			// 日期格式化方法（新增）
			  formatDate(date) {
			    const year = date.getFullYear()
			    const month = (date.getMonth() + 1).toString().padStart(2, '0')
			    const day = date.getDate().toString().padStart(2, '0')
			    return `${year}-${month}-${day}`
			  },
		
		    // 刷新数据链
		    refreshData() {
				this.getFoodCheckin()
		        this.getHistory()
		        this.getRecommend()
				this.fetchNutritionStats()
		    },
		
		
	},
	created() {
		this.getFoodList();
		this.getRecommend();
		this.getFoodCheckin();
		this.fetchNutritionStats();
		this.getHistory();
	},
	
}
</script>

<style>
/*勋章格式*/
/* 优化后的样式 */
.badge-modal-mask {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 9999;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.75); /* 加深背景 */
    backdrop-filter: blur(5px); /* 添加背景模糊 */
    display: flex;
    justify-content: center;
    align-items: center;
}

.multi-badge-modal {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    width: 85%;
    max-width: 600px;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.badge-scroll {
	display: flex; /* 关键1: 启用flex布局 */
    width: 100%;
    white-space: nowrap;
}

/* 新增居中容器 */
.badge-container {
    display: inline-flex;
    justify-content: center;
    width: auto;
    padding: 15px 0;
}

.badge-item {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
}

.badge-frame {
    background: #fff;
    border-radius: 50%;
    padding: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin: 10px 0;
}

.badge-image {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: linear-gradient(45deg, #f3f4f6 0%, #e5e7eb 100%);
}

.badge-name {
    font-size: 16px;
    color: #2d3436;
    font-weight: 500;
    text-align: center;
    white-space: normal;
    max-width: 150px;
    margin-top: 10px;
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
}

.header-icon {
    width: 32px;
    height: 32px;
    margin-right: 10px;
}

.header-text {
    font-size: 24px;
    color: #2d3436;
    font-weight: 600;
}

.congrats-text {
    position: relative;
    margin: 25px 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.confetti-left, .confetti-right {
    width: 40px;
    height: 40px;
}

.congrats {
    font-size: 18px;
    color: #e67e22;
    margin: 0 10px;
    font-weight: bold;
}

.confirm-btn {
    background: linear-gradient(45deg, #00b894, #00cec9);
    color: white!important;
    border-radius: 30px;
    font-size: 16px;
    padding: 12px 0;
    margin-top: 15px;
    box-shadow: 0 4px 6px rgba(0,184,148,0.2);
}
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

.food-name {
    font-size: 16px;
    font-weight: bold;
    color: #333;
    margin-bottom: 8px;
}

.food-details {
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

/* 食物打卡页面样式 */
/* 公共样式 */
.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 20rpx 0;
  padding-left: 10px;
  border-left: 4px solid #4a90e2; /* 左侧装饰线 */
  line-height: 1.2;
}

/* 餐品容器 */
.checkin-breakfast,
.checkin-lunch,
.checkin-dinner {
  margin: 20px 15px;
  padding: 15px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  
  &:last-child {
    margin-bottom: 30px;
  }
}

/* 餐品项 */
.food-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  margin: 10px 0;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;

  &:active {
    background: #e9ecef;
  }
}

.food-name {
  font-size: 16px;
  color: #2d3436;
  flex: 1;
  margin-right: 15px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 热量显示 */
.food-details {
  display: flex;
  align-items: center;
  
  .food-calories {
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #e74c3c;
    background: rgba(231,76,60,0.1);
    padding: 4px 10px;
    border-radius: 20px;

    .detail-icon {
      margin-right: 6px;
      font-size: 16px;
      color: #e74c3c;
    }
  }
  
  .food-grams {
    display: flex;
    align-items: center;
    font-size: 14px;
    color: #1abc9c;          // 主色：蓝绿色
    background: rgba(26, 188, 156, 0.1); // 半透明背景
    padding: 4px 10px;
    border-radius: 20px;
    transition: all 0.3s;    // 添加过渡效果
  
    .detail-icon {
      margin-right: 6px;
      font-size: 16px;
      color: #16a085;        // 深一级的蓝绿色
      transform: scale(0.9); // 微调图标尺寸
    }
	}
}

/* 空状态提示 */
.empty-tips {
  text-align: center;
  padding: 20px;
  color: #95a5a6;
  font-size: 14px;
  background: #f8f9fa;
  border-radius: 8px;
  margin: 10px 0;
}

.food-checkin-card {
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

/* 日期选择器页面样式 */
/* 容器样式 */
.date-navigator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16rpx 32rpx;
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  border-radius: 16rpx;
  box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.05);
  margin: 20rpx;
  position: relative;
  transition: all 0.3s ease;
}

/* 悬停效果 */
.date-navigator:hover {
  transform: translateY(-2px);
  box-shadow: 0 12rpx 28rpx rgba(0, 0, 0, 0.1);
}

/* 箭头样式 */
.arrow {
  font-size: 36rpx;
  color: #1abc9c;
  padding: 16rpx 32rpx;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 8rpx;
}

.arrow:active {
  transform: scale(0.9);
  background-color: rgba(108, 117, 125, 0.1);
}

/* 当前日期样式 */
.current-date {
  font-size: 34rpx;
  font-weight: 500;
  color: #2c3e50;
  margin: 0 40rpx;
  padding: 12rpx 24rpx;
  border-radius: 8rpx;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
  border: 1rpx solid rgba(0, 0, 0, 0.05);
}

.current-date:active {
  background: rgba(245, 245, 245, 0.9);
}

/* 日期选择器弹窗样式 */
/deep/ .u-picker {
  border-radius: 24rpx !important;
  overflow: hidden;
}

/deep/ .u-picker__toolbar {
  background: #f8f9fa !important;
  border-bottom: 1rpx solid #eee;
}

/deep/ .u-picker__action:not(:first-child) {
  color: #007bff !important;
  font-weight: 500;
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

.food-category {
  color: #4CAF50;
  font-weight: 500;
  margin-right: 8rpx;
  white-space: nowrap;
  background-color: rgba(76, 175, 80, 0.1);
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
}

.food-meal {
  color: #87CEEB;              /* 文字改为天蓝色 */
  font-weight: 500;
  margin-right: 8rpx;
  white-space: nowrap;
  background-color: rgba(135, 206, 235, 0.1);  /* 背景色同步改为天蓝+透明度 */
  padding: 4rpx 123rpx;
  border-radius: 8rpx;
}

.food-category::after {
  content: ' - ';
  color: #999;
  margin: 0 4rpx;
}

.food-name-1 {
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

/* 日历样式 */
.calendar-mask {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
}

.calendar-container {
    background: #fff;
    border-radius: 12rpx;
    width: 90%;
    padding: 20rpx;
}
</style>

