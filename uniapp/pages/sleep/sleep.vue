<template>
  <view class="container">
    <!-- 睡眠推荐卡片 -->
    <view class="recommend-card">
      <view class="header">
        <text class="title">今日睡眠推荐</text>
        <text class="date">{{ currentDate }}</text>
      </view>
      <!-- 主要睡眠时间 -->
      <view class="time-section">
        <view class="time-item night">
          <text class="label">晚间睡眠</text>
          <view class="time-group">
            <text class="time">{{ recommendation.recommended_sleep_time }}</text>
            <text class="separator">-</text>
            <text class="time">{{ recommendation.recommended_wake_time }}</text>
          </view>
          <text class="duration">推荐时长 {{ nightSleepDuration }} 小时</text>
        </view>
        <!-- 午睡时间（可选） -->
        <view v-if="hasNap" class="time-item nap">
          <text class="label">午间小憩</text>
          <view class="time-group">
            <text class="time">{{ recommendation.recommended_nap_time }}</text>
          </view>
          <text class="duration">推荐时长 {{ napDuration }} 分钟</text>
        </view>
      </view>
    </view>

    <!-- 功能卡片网格 -->
    <view class="grid">
      <view
        v-for="item in features"
        :key="item.type"
        class="card"
        @click="handleFeatureClick(item)"
      >
        <view class="icon-box" :style="`background-color: ${item.color};`">
          <text class="iconfont" :class="item.icon"></text>
        </view>
        <text class="card-title">{{ item.title }}</text>
        <text class="card-desc">{{ item.desc }}</text>
      </view>
    </view>
	
	<!-- 修改后的弹窗组件 -->
	<uni-popup ref="playlistPopup" type="center">
	  <view class="popup-content">
		<!-- 🎵 新增导入按钮 -->
		<view class="import-wrapper" @click.stop="handleOpenImport">
		    <uni-icons type="plus-filled" size="24" color="#4a90e2"></uni-icons>
		    <text class="import-text">导入音乐</text>
		</view>
	    <text class="popup-title">播放列表</text>
	    <!-- 隐藏的文件选择器 -->
		<uni-file-picker 
		  ref="filePicker"
		  v-if="showFilePicker"
		  limit="10"
		  file-mediatype="all"
		  :image-styles="{}"
		  :del-icon="false"
		  @select="handleFileSelect"
		  @fail="handleUploadError"
		></uni-file-picker>
		
	    <!-- 固定表头 -->
	    <view class="popup-header">
	      <text class="header-name">歌名</text>
	      <text class="header-duration">时长</text>
	      <text class="header-genre">类型</text>
	      <text class="header-action">操作</text>
	    </view>
	
	    <!-- 可滚动区域 -->
	    <scroll-view 
	      class="scroll-list"
	      scroll-y 
	      :show-scrollbar="true"
	      :enable-flex="true"
		   @touchstart="handleTouchStart"   <!-- 新增触摸事件处理 -->
	    
	      <view 
	        v-for="(song, index) in personPlaylist" 
	        :key="index" 
	        class="popup-item"
	      >
	        <text class="item-name">{{ song.name }}</text>
	        <text class="item-duration">{{ song.duration }}</text>
	        <text class="item-genre">{{ song.genre }}</text>
	        <!--view class="item-action" @click.stop="handleAddClick(song)">
	          <uni-icons type="plus" size="20" color="#4a90e2"></uni-icons>
	        </view>-->
			<view class="item-action" @click.stop="handleAddClick(song)">
			  <uni-icons 
			    type="plus" 
			    size="20" 
			    class="action-icon"
			  ></uni-icons>
			</view>
	      </view>
	    </scroll-view>
	
	    <button class="popup-close" @click="closePopup">关闭</button>
	  </view>
	</uni-popup>

    <!-- 底部播放器控制条 -->
    <view class="player-bar" :class="{ expanded: showPlaylist }">
      <view class="player-controls" @click="togglePlaylist">
        <!-- 当前播放信息 -->
        <view class="now-playing">
          <view class="song-info">
            <text class="song-title">{{ currentSong.title || '未播放歌曲' }}</text>
            <text class="song-type">{{ currentSong.type || '未知类型' }}</text>
          </view>
		  
		  <!-- 新增时间显示和进度条 -->
		      <view class="progress-container">
		        <text class="time-text">{{ formatDuration(currentTime) }}</text>
		        <slider 
		          class="progress-bar"
		          :value="currentTime" 
		          :max="duration"
		          block-size="16"
		          activeColor="#4a90e2"
		          @change="onSeek"
		          @changing="onSeeking"
		        />
		        <text class="time-text">{{ formatDuration(duration) }}</text>
		      </view>
        </view>
        <!-- 修改播放控制按钮部分 -->
        <view class="control-buttons">
          <button @click.stop="handlePlayControl">
            <image 
              class="play-icon"
              :src="isPlaying 
                ? '/static/icons/play.svg' 
                : '/static/icons/pause.svg'"
              mode="aspectFit"
            />
          </button>
        </view>
      </view>
	  <!-- 播放列表面板 -->
	    <transition name="slide-up">
	        <view class="playlist-panel" v-show="showPlaylist">
	          <!-- 选项卡 -->
	          <view class="playlist-tabs">
	            <button
	              :class="{ active: activeTab === 'current' }"
	              @click="activeTab = 'current'"
	            >
	              当前播放 ({{ nowPlaylist.songs.length }})
	            </button>
	            <button
	              :class="{ active: activeTab === 'history' }"
	              @click="activeTab = 'history'"
	            >
	              播放历史 ({{ historyPlaylist.songs.length }})
	            </button>
	          </view>
	    
	          <!-- 通用表头 -->
	          <view class="table-header">
	            <text class="header-item num">序号</text>
	            <text class="header-item title">歌曲名称</text>
	            <text class="header-item type">类型</text>
	            <text class="header-item favorite">收藏</text>
	            <text class="header-item duration">时长</text>
	          </view>
	    
	          <!-- 内容区域，用 scroll-view 实现滚动 -->
	          <view class="playlist-content">
	            <!-- 当前播放列表 -->
	            <scroll-view
	              v-show="activeTab === 'current'"
	              class="playlist-scroll"
	              scroll-y="true"
	            >
	              <view class="song-list">
	                <view
	                  v-for="(song, index) in nowPlaylist.songs"
	                  :key="song.id"
	                  class="song-item"
	                >
	                  <text class="song-num">{{ index + 1 }}.</text>
	                  <text class="song-title">{{ song.title }}</text>
	                  <text class="song-type">{{ song.type }}</text>
	    
	                  <view class="favorite-icon" @click.stop="toggleFavorite(song)">
	                    <image
	                      :src="song.ifFavorite
	                        ? '/static/icons/icon-star-active.png'
	                        : '/static/icons/icon-star-inactive.png'"
	                      class="star-icon"
	                    />
	                  </view>
	    
	                  <text class="song-duration">{{ formatDuration(song.duration) }}</text>
	                </view>
	              </view>
	            </scroll-view>
	    
	            <!-- 历史播放列表 -->
	            <scroll-view
	              v-show="activeTab === 'history'"
	              class="playlist-scroll"
	              scroll-y="true"
	            >
	              <view class="song-list">
	                <view
	                  v-for="(song, index) in historyPlaylist.songs"
	                  :key="song.id"
	                  class="song-item"
	                >
	                  <text class="song-num">{{ index + 1 }}.</text>
	                  <text class="song-title">{{ song.title }}</text>
	                  <text class="song-type">{{ song.type }}</text>
	    
	                  <view class="favorite-icon" @click.stop="toggleFavorite(song)">
	                    <image
	                      :src="song.ifFavorite
	                        ? '/static/icons/icon-star-active.png'
	                        : '/static/icons/icon-star-inactive.png'"
	                      class="star-icon"
	                      mode="aspectFit"
	                    />
	                  </view>
	    
	                  <text class="song-duration">{{ formatDuration(song.duration) }}</text>
	                </view>
	              </view>
	            </scroll-view>
	          </view>
	        </view>
	      </transition>
    </view>
  </view>
</template>

<script>
import axios from '@/utils/request';
export default {
  data() {
    return {
	  showFilePicker: false,
	  user: {},  // 移除非同步初始化
      showPlaylist: false,
      activeTab: 'current',
      isPlaying: false,
      currentIndex: -1,
	  currentSong: {}, 
	  currentTime: 0,  // 当前播放时间（秒）
	  duration: 0,     // 总时长（秒）
	  isSeeking: false, // 是否正在拖拽进度条
      audioElement: null,
      recommendation: {
        recommended_sleep_time: '23:00',
        recommended_wake_time: '07:00',
        recommended_nap_time: '13:30'
      },
	  personPlaylist: [
      { id:'无', name: '宁静之夜', duration: '03:45', genre: '自然', url: '111' },
      { id:'无',name: '钢琴协奏曲', duration: '05:20', genre: '古典', url: '111' },
      { id:'无',name: '海浪冥想', duration: '04:15', genre: '放松', url: '111' }
      ],
      nowPlaylist: { id: null, songs: [] },
      historyPlaylist: { id: null, songs: [] },
      features: [
        { title: '助眠音乐', icon: 'icon-moon', color: '#8A2BE2', desc: '智能生成助眠白噪音', type: 'sleep' },
        { title: '放松音乐', icon: 'icon-spa', color: '#00BFFF', desc: '缓解压力背景音乐', type: 'relax' },
        { title: '我的音乐', icon: 'icon-music', color: '#FF69B4', desc: '播放已保存歌单', type: 'playlist' },
        { title: '午睡音乐', icon: 'icon-nap', color: '#32CD32', desc: '短时休息背景音', type: 'nap' }
      ]
    };
  },
  computed: {
	handleTouchStart(e) {
	    this.startY = e.touches[0].clientY
	  },
	  
	  handleTouchMove(e) {
	    const deltaY = e.touches[0].clientY - this.startY
	    const element = e.currentTarget
	    
	    // 检测滚动边界
	    const isTop = element.scrollTop === 0
	    const isBottom = element.scrollHeight - element.scrollTop === element.clientHeight
	    
	    // 阻止边缘滚动传播
	    if ((isTop && deltaY > 0) || (isBottom && deltaY < 0)) {
	      e.preventDefault()
	    }
	  },
	toggleFavorite(song) {
	    console.log('收藏歌曲:', song)
	    // 这里添加实际收藏操作
	    // this.updateFavoriteStatus(song.id, song.ifFavorite)
	},
    currentDate() {
      return new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
    },
    hasNap() {
      return !!this.recommendation.recommended_nap_time;
    },
    nightSleepDuration() {
      const [h1] = this.recommendation.recommended_sleep_time.split(':');
      const [h2] = this.recommendation.recommended_wake_time.split(':');
      const start = parseInt(h1, 10), end = parseInt(h2, 10);
      return end >= start ? end - start : end + 24 - start;
    },
    napDuration() {
      return this.hasNap ? 30 : 0;
    }
  },
  
  
  methods: {
	  
	  
	// 存储用户
	initializeUser() {
	    const storedUser = uni.getStorageSync('xm-user')
	    if (!storedUser?.id) {
	     uni.redirectTo({ url: '/pages/login/login' })
	     return
	    }
	    this.user = JSON.parse(JSON.stringify(storedUser))
	},
	
	
	// 点击不同模块（例如个人导入、解乏音乐等）所产生的跳转页面或弹窗效果
	handleFeatureClick(item) {
	  if (item.type === 'playlist') {
	    this.$refs.playlistPopup.open()
	  } else {
	    const routes = {
	      sleep: '/pages/music/sleep',
	      relax: '/pages/music/relax',
	      nap: '/pages/music/nap'
	    };
	    uni.navigateTo({ url: routes[item.type] });
	  }
	},
	
	
	// 关闭个人导入的弹窗
	closePopup() {
	  this.$refs.playlistPopup.close()
	},
	
	
	// 音乐进度条拖拽事件
	onSeeking(e) {
	    this.isSeeking = true;
	    this.currentTime = e.detail.value;
	},
	
	
	// 音乐进度条释放事件
	onSeek(e) {
	    this.isSeeking = false;
	    // 实际音频跳转逻辑（根据使用的音频API调整）
	    // 直接操作现有音频对象
	    if (this.audioElement) {
	        const wasPlaying = !this.audioElement.paused;
	        
	    // 设置播放进度
	    this.audioElement.currentTime = e.detail.value;
	        
	    // 恢复播放状态
	    if (wasPlaying) {
	        this.audioElement.play().catch(error => {
	        console.warn('播放恢复失败:', error);
	       });
	    }
	    }
	},
	
	
	// 显示界面中隐藏的文件上传按钮
	handleOpenImport() {
	  this.showFilePicker = true
	  this.$nextTick(() => {
		this.$refs.filePicker.open()
	  })
	},	
	
	
	// 音乐文件上传功能
	async handleFileSelect(e) {
	  try {
	    const files = e.tempFiles
	
	    // 文件数量校验（保持原有格式）
	    if (files.length !== 1) {
	      uni.showToast({ title: '请选择一首MP3文件', icon: 'none' })
	      return
	    }
	
	    const file = files[0]
	    
	    // 格式校验（保持原有缩进）
	    if (!file.name.toLowerCase().endsWith('.mp3')) {
	      uni.showToast({ title: '仅支持MP3格式', icon: 'none' })
	      return
	    }
	
	    uni.showLoading({ title: '上传中...', mask: true })
	
	    // 上传逻辑（严格匹配Result结构）
	    const res = await new Promise((resolve, reject) => {
	      uni.uploadFile({
	        url: this.$baseUrl + '/files/music/upload',
	        filePath: file.path,
	        name: 'music',
	        formData: { userId: this.user.id },
	        success: (uploadRes) => {
	          try {
	            // 双重解析响应（匹配Java Result结构）
	            const response = JSON.parse(uploadRes.data || '{}')
	            
	            // 结构校验（对应您的Result类字段）
	            if (response.code === '200') { // 字符串类型匹配
	              resolve(response.data) // 对应data字段
	            } else {
	              reject({ 
	                code: response.code || 'UNKNOWN_ERROR',
	                msg: response.msg || '操作失败' // 对应msg字段
	              })
	            }
	          } catch (e) {
	            reject({ code: 'PARSE_ERROR', msg: '响应解析失败' })
	          }
	        },
	        fail: (err) => {
	          reject({ code: 'NETWORK_ERROR', msg: err.errMsg })
	        }
	      })
	    })
	
	    // 后续逻辑保持原有格式
	    await this.getPersonListByUserId()
	    uni.showToast({ title: '歌曲导入成功' })
	
	  } catch (err) {
	    // 错误处理匹配Result结构
	    const errorMsg = err.msg || 
	                    (err.code === '401' ? '用户未认证' : '') || 
	                    (err.code === '413' ? '文件过大' : '') || 
	                    '未知错误'
	                    
	    console.error(`[${err.code}] ${errorMsg}`)
	    uni.showToast({ 
	      title: `导入失败: ${errorMsg}`,
	      icon: 'none',
	      duration: 3000
	    })
	  } finally {
	    uni.hideLoading()
	    this.showFilePicker = false
	  }
	},
	
	
	// 音乐文件上传错误处理
	handleUploadError(e) {
	  console.error('文件选择失败:', e)
	  uni.showToast({ title: '文件选择失败', icon: 'none' })
	},		
	
	
	// 音乐播放控制，暂停则停止，播放则播放（暂停逻辑还没做好）
	handlePlayControl() {
	  // 状态切换放到最后以确保同步
	  const targetState = !this.isPlaying;
	
	  // 处理首次播放的特殊情况
	  if (typeof this.currentIndex === 'undefined') {
	    this.currentIndex = 0;
	    this.playThis(this.currentIndex);
	    return;
	  }
	
	  // 核心控制逻辑
	  if (targetState) {
	    this.resumePlayback();
	  } else {
	    this.pausePlayback();
	  }
	
	  // 最后更新状态
	  this.isPlaying = targetState;
	},
	
	
	// 新增暂停方法
	pausePlayback() {
	  if (this.audioElement && !this.audioElement.paused) {
	    try {
	      this.audioElement.pause();
	      // 小程序API兼容（如果实际需要）
	      // uni.pauseBackgroundAudio();
	    } catch (e) {
	      console.error('暂停失败:', e);
	    }
	  }
	},
	
	
	// 新增恢复播放方法
	resumePlayback() {
	  if (this.audioElement) {
	    const playPromise = this.audioElement.play();
	    
	    playPromise.catch(error => {
	      console.warn('恢复播放失败:', error);
	      this.showPlayButton = true;
	    });
	  } else {
	    // 音频实例不存在时重新加载
	    this.playThis(this.currentIndex);
	  }
	},
	
	// 将音乐时长从秒转换到分秒标准格式
	formatDuration(sec) {
	  const m = Math.floor(sec / 60);
	  const s = sec % 60;
	  return `${m}:${String(s).padStart(2, '0')}`;
	},
	
	
	// 检查当前用户是否有播放列表，没有则创建
	async createListByUserId() {
	  try {
	    const res = await axios.post('/music/createListByUserId');
	    if (res.code === '200') {
	      //uni.showToast({ title: '列表创建成功', icon: 'success' });
	      this.getListByUserId();
	    } else {
	      uni.showToast({ title: res.data.message || '操作失败', icon: 'none' });
	    }
	  } catch (err) {
	    uni.showToast({ title: '网络错误，请稍后重试', icon: 'none' });
	  }
	},
	
	
	// 得到用户当前播放列表和历史播放列表
	async getListByUserId() {
	  try {
	    const res = await axios.get('/music/getListByUserId');
	    if (res.code === '200') {
	      const data = res.data || {};
	      // 处理当前播放列表
	      this.nowPlaylist = {
	        id: data.nowPlayListId,
	        songs: (data.nowPlayListMusics || []).map(m => {
			  const song = {
			          id: m.id,
			          musicId: m.musicId,
			          title: m.title,
			          type: m.type,
			          location: m.location,
			          url: m.musicUrl,
			          duration: Number(m.duration),
			          ifNow: m.ifNow,
			          ifFavorite: m.ifFavorite
			        };
			        
			        // 当ifNow为true时设置当前歌曲
			        if (song.ifNow) {
			          this.currentSong = { ...song }; // 使用扩展运算符创建新对象
					  this.currentIndex = song.location;
					  this.duration = song.duration;
			        }
			        
			        return song;
	        })
	      };
	      // 处理历史播放列表
	      this.historyPlaylist = {
	        id: data.historyPlayListId,
	        songs: (data.historyPlayListMusics || []).map(m => ({
	          id: m.id,
	          musicId: m.musicId,
	          title: m.title,
	          type: m.type,
	          location: m.location,
	          url: m.musicUrl,
	          duration: Number(m.duration),
	          ifNow: m.ifNow,
	          ifFavorite: m.ifFavorite
	        }))
	      };
	    }
	  } catch (e) {
	    uni.showToast({ title: '加载列表失败', icon: 'none' });
	  }
	},
	
	
	// 根据索引播放当前音频
	playThis(index) {
	  this.currentIndex = index;
	  const song = this.nowPlaylist.songs[index];
	  
	  // 增加URL验证
	  if (!song.url) {
	    console.error('歌曲URL不存在')
	    return
	  }
	  
	  this.loadAudio(song.url);
	},
	
	
	/*根据url加载音频
	loadAudio(url) {
	  // 销毁旧音频实例
	  if (this.audioElement) {
	    this.audioElement.pause()
	    this.audioElement.removeEventListener('ended', this.nextSong)
	    this.audioElement = null
	  }
	
	  try {
	    // 创建新实例
	    this.audioElement = new Audio(url)
	    console.log('音频对象创建成功:', this.audioElement)
		
		// ✅ 新增元数据加载监听
		this.audioElement.addEventListener('loadedmetadata', () => {
		    this.duration = this.audioElement.duration;
		});
		
		// ✅ 新增播放进度监听
		this.audioElement.addEventListener('timeupdate', () => {
		    if (!this.isSeeking) { // 防止拖拽时产生冲突
		    this.currentTime = this.audioElement.currentTime;
		    }
		});
	    
	    // 增加预加载
	    this.audioElement.preload = 'auto'
	    
	    // 错误监听
	    this.audioElement.addEventListener('error', (e) => {
	      console.error('音频加载错误:', e.target.error)
	    })
	
	    // 播放尝试
	    const playPromise = this.audioElement.play()
	    
	    if (playPromise !== undefined) {
	      playPromise
	        .then(() => {
	          console.log('程序化播放成功')
	          this.isPlaying = true
	        })
	        .catch(error => {
	          console.warn('自动播放被阻止，需要用户手势:', error)
	          this.$set(this, 'showPlayButton', true)
	        })
	    }
	    
	    this.audioElement.addEventListener('ended', this.nextSong)
	    
	  } catch (e) {
	    console.error('音频初始化异常:', e)
	  }
	},*/
	
	
	loadAudio(url) {
	  // 旧实例销毁逻辑（如前述优化）
	  if (this.audioElement) {
	    // 统一管理需要移除的事件监听器
	    const eventsToRemove = {
	      'ended': this.nextSong,
	      'loadedmetadata': this.handleMetadata,
	      'timeupdate': this.handleTimeUpdate,
	      'error': this.handleAudioError
	    };
	  
	    Object.entries(eventsToRemove).forEach(([event, handler]) => {
	      this.audioElement.removeEventListener(event, handler);
	    });
	  
	    // 更彻底的资源释放
	    this.audioElement.pause();
	    this.audioElement.removeAttribute('src');
	    this.audioElement.load();
	    this.audioElement = null;
	  }
	  try {
	    this.audioElement = new Audio(url);
	    this.audioElement.preload = 'auto';
	    this.audioElement.setAttribute('playsinline', '');
	
	    // 统一管理事件监听
	    const eventHandlers = {
	      'loadedmetadata': () => {
	        this.duration = Math.floor(this.audioElement.duration);
	        this.$emit('duration-update', this.duration);
	      },
	      'timeupdate': this.handleTimeUpdate,
	      'ended': this.nextSong,
	      'error': (e) => {
	        console.error('音频错误:', e.target.error.code);
	        this.$emit('error', e.target.error);
	      },
	      'stalled': () => this.isLoading = true,
	      'canplaythrough': () => this.isLoading = false
	    };
	
	    Object.entries(eventHandlers).forEach(([event, handler]) => {
	      this.audioElement.addEventListener(event, handler);
	    });
	
	    // 自动播放尝试（带状态回退）
	    this.attemptAutoplay();
	
	  } catch (e) {
	    console.error('音频初始化失败:', e);
	    this.$emit('error', e);
	  }
	},
	
	
	// 新增时间更新处理器
	  handleTimeUpdate() {
	    if (!this.isSeeking) {
	      // ✅ 必须使用响应式更新
	      this.$set(this, 'currentTime', Math.floor(this.audioElement.currentTime));
	      
	      // 调试用日志（确认事件触发）
	      console.log('[进度更新]', this.currentTime, '/', this.duration); 
	    }
	  },
	
	
	  // 新增元数据处理
	  handleMetadata() {
	    this.$set(this, 'duration', Math.floor(this.audioElement.duration));
	  },
	
	
	// 新增独立方法
	attemptAutoplay() {
	  this.audioElement.play()
	    .then(() => {
	      this.isPlaying = true;
	      this.showPlayButton = false;
	    })
	    .catch(error => {
	      if (error.name === 'NotAllowedError') {
	        console.info('需要用户交互后才能播放');
	        this.showPlayButton = true;
	      }
	      this.isPlaying = false;
	    });
	},
	
	
	// 得到用户收藏的所有音乐，展示在个人导入音乐模块中
	async getPersonListByUserId() {
	  try {
	    const res = await axios.get('/music/list');
	    if (res.code === '200') {
	      const data = res.data || {};
	     // 数据格式转换
	    this.personPlaylist = data.map(music => ({
		  id: music.musicId,
	      name: music.title,
	      duration: this.formatDuration(music.duration), // 转换秒数为时间格式
	      genre: music.type,
		  url: music.musicUrl
	    }));
	    }
	  } catch (e) {
	    uni.showToast({ title: '加载列表失败', icon: 'none' });
	  }
	},
	
	
	// 将音乐添加至播放列表
	async handleAddClick(song) {
	      try {
	        // 显示加载状态
	        uni.showLoading({ title: '添加中...', mask: true })
	        
	        // 构造符合后端接口的请求体
	        const requestBody = {
	          musicId: song.id,        // 根据实际数据结构调整
	          title: song.title,        // 字段映射
	          type: song.genre,
	          musicUrl: song.url       // 确保字段名与后端Music类一致
	        };
	
	        // 调用后端接口
	        const res = await axios.post('/music/playlist/add',requestBody);
	        // 处理响应
	        if (res.code === '200') {
	          uni.showToast({ title: '添加成功', icon: 'success' });
	          
	          // 更新播放列表（根据实际场景选择方案）
	          //await this.refreshPlaylist();  // 方案1：重新拉取最新数据
			  await this.getListByUserId()
	          
	          // 方案2：前端本地插入（保持与后端逻辑一致）
	          // this.insertSongLocal(song, res.data.location); 
	        } else {
	          throw new Error(res.msg || '添加失败');
	        }
	      } catch (err) {
	        console.error('添加失败:', err);
	        uni.showToast({
	          title: err.message || '添加到播放列表失败',
	          icon: 'none',
	          duration: 3000
	        });
	      } finally {
	        uni.hideLoading();
	      }
	    },
	
	
	    // 刷新播放列表数据
	    async refreshPlaylist() {
	      try {
			const res = await axios.get('/music/getListByUserId');
	        this.nowPlaylist = res.data;
	      } catch (e) {
	        console.error('刷新列表失败:', e);
	      }
	    },
	
	
    // 显示播放列表			  
    togglePlay() {
      if (!this.audioElement) return;
      this.isPlaying = !this.isPlaying;
      this.isPlaying ? this.audioElement.play() : this.audioElement.pause();
    },
    togglePlaylist() {
      this.showPlaylist = !this.showPlaylist;
    },
	
	
	// 播放下一首歌（暂未实现）
    nextSong() {
      const len = this.nowPlaylist.songs.length;
      this.currentIndex = (this.currentIndex + 1) % len;
	  this.currentSong = this.nowPlaylist.songs[this.currentIndex];
      this.playThis(this.currentIndex);
    },
	
	
	//切换为历史列表（暂未实现）
    playHistory(idx) {
      const song = this.historyPlaylist.songs[idx];
      const existIdx = this.nowPlaylist.songs.findIndex(s => s.id === song.id);
      if (existIdx === -1) {
        this.nowPlaylist.songs.unshift(song);
        this.currentIndex = 0;
      } else {
        this.currentIndex = existIdx;
        this.loadAudio(this.nowPlaylist.songs[existIdx].url);
      }
    }
  },
  created() {
	this.initializeUser();
    this.createListByUserId();
	this.getPersonListByUserId();
  }
};
</script>

<style lang="scss" scoped>
/* 播放列表滚动区域样式：scroll-view 需要固定高度才能滚动 */
.playlist-scroll {
  height: 500rpx;
  padding-right: 10rpx;
}

/* H5 环境下生效的滚动条美化（小程序会忽略） */
.playlist-scroll {
  overflow-y: auto;
  scroll-behavior: smooth;
}
.playlist-scroll::-webkit-scrollbar {
  width: 8rpx;
}
.playlist-scroll::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 4rpx;
}
.popup-list {
  max-height: 60vh;
  overflow-y: auto;
}

.popup-close {
  margin-top: 30rpx;
  background: #4a90e2;
  color: white;
  border-radius: 50rpx;
}

/* 表头样式 */
.popup-header {
  display: flex;
  padding: 20rpx 0;
  border-bottom: 2rpx solid #eee;
  font-weight: bold;
}

.popup-header text {
  display: flex;
    padding: 20rpx 0;
    background: #f8f8f8;
    border-radius: 8rpx;
    position: sticky;
    top: 0;
    z-index: 1;
}

.header-name { flex: 4; }
.header-duration { flex: 2; }
.header-genre { flex: 2; }
.header-action { flex: 1; }

.popup-item text {
  padding: 0 10rpx;
}

.item-name { flex: 4; }
.item-duration { flex: 2; }
.item-genre { flex: 2; }
/* 方案二样式 */
.item-action {
  padding: 8rpx;  /* 增加触摸区域 */
  border-radius: 50%;
  transition: all 0.2s;
}

/* 点击态效果 */
.item-action:active {
  background-color: rgba(74, 144, 226, 0.1);
}

.action-icon {
  color: #4a90e2;
  transition: color 0.2s;
}

.action-icon:active {
  color: #2b6cb0;
}

/* 新增滚动区域样式 */
/* 自定义滚动条样式 */
.scroll-list ::-webkit-scrollbar {
  width: 6rpx;          /* 滚动条宽度 */
  background: #f5f5f5;  /* 轨道颜色 */
}

.scroll-list ::-webkit-scrollbar-thumb {
  background: #c1c1c1;  /* 滑块颜色 */
  border-radius: 4rpx;
}

.scroll-list {
  height: 50vh;         /* 固定滚动区域高度 */
  margin-top: 20rpx;
  overscroll-behavior: contain; /* 阻止滚动链 */
  -webkit-overflow-scrolling: touch;
}


/* 新增导入按钮样式 */
.import-wrapper {
  position: absolute;
  top: 20rpx;
  right: 20rpx;
  display: flex;
  align-items: center;
  padding: 8rpx 16rpx;
  background: #f0f7ff;
  border-radius: 40rpx;
  z-index: 2;
}

.import-text {
  font-size: 24rpx;
  color: #4a90e2;
  margin-left: 8rpx;
}

.popup-content {
 position: relative;
   width: 80vw;          /* 控制弹窗宽度 */
   max-height: 70vh;      /* 最大高度为视口70% */
   overflow-y: auto;      /* 启用垂直滚动 */
   background: #ffffff;
   border-radius: 16rpx;
   padding: 32rpx;
   box-shadow: 0 8rpx 40rpx rgba(0,0,0,0.12);
    touch-action: none; /* 禁用默认触摸行为 */
}

.popup-title {
  /* 保持原有样式 */
    display: block;
    font-size: 36rpx;
    font-weight: 600;
    color: #333;
    margin-bottom: 24rpx;
}

/* 滚动列表项保持原有样式 */
.popup-item {
  display: flex;
  align-items: center;
  padding: 25rpx 0;
  border-bottom: 1rpx solid #f5f5f5;
}
.container { padding: 20rpx; background: #f5f5f5; }
.recommend-card { background: #fff; border-radius: 16rpx; padding: 30rpx; box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.1);
  .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40rpx;
    .title { font-size: 36rpx; font-weight: 600; color: #333; }
    .date { font-size: 28rpx; color: #666; }
  }
}
.time-section {
  .time-item { margin-bottom: 30rpx;
    &.night { padding-bottom: 30rpx; border-bottom: 1rpx solid #eee; }
    .label { display: block; font-size: 28rpx; color: #999; margin-bottom: 16rpx; }
    .time-group { display: flex; align-items: center; gap: 20rpx; }
    .time { font-size: 48rpx; font-weight: 500; color: #2c3e50; }
    .separator { color: #ccc; font-size: 36rpx; }
    .duration { display: block; font-size: 24rpx; color: #666; margin-top: 12rpx; }
  }
}
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24rpx; margin-top: 40rpx;
  .card { background: #fff; border-radius: 12rpx; padding: 32rpx; text-align: center; box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.08);
    .icon-box { width: 100rpx; height: 100rpx; border-radius: 24rpx; display: flex; align-items: center; justify-content: center; margin: 0 auto 20rpx;
      .iconfont { font-size: 50rpx; color: #fff; }
    }
    .card-title { display: block; font-size: 32rpx; color: #333; margin-bottom: 8rpx; }
    .card-desc { font-size: 24rpx; color: #888; }
  }
}
.iconfont { font-family: 'iconfont' !important; font-style: normal; }
.player-bar { position: fixed; bottom: 0; left: 0; right: 0; background: #fff; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); z-index: 1000;
  &.expanded { height: 60vh; }
}
.player-controls { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px; background: #f5f5f5; cursor: pointer; }
.now-playing { display: flex; align-items: center;
  .song-cover { width: 40px; height: 40px; border-radius: 4px; margin-right: 12px; }
}
.control-buttons button { background: none; border: none; padding: 8px; font-size: 24px; color: #333; }
//.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.3s ease; }
//.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); }
//.playlist-panel { background: #fff; overflow-y: auto; height: calc(100% - 60px); }
/*.playlist-tabs { display: flex; border-bottom: 1px solid #eee;
  button { flex: 1; padding: 15px; background: none; border: none; border-bottom: 2px solid transparent; }
  button.active { border-bottom-color: #007aff; color: #007aff; }
}
.song-list { max-height: 100%; overflow-y: auto; }
.song-item { display: flex; align-items: center; padding: 12px 20px; border-bottom: 1px solid #eee;
  &.playing { color: #007aff; background: #f0f8ff; }
  .song-num { width: 40px; color: #666; }
  .song-title { flex: 1; margin: 0 15px; }
  .song-duration { color: #666; }
}*/

//新添加
.playlist-panel {
  background: #fff;
  border-radius: 20rpx 20rpx 0 0;
  box-shadow: 0 -4rpx 20rpx rgba(0,0,0,0.1);
}

.playlist-tabs {
  display: flex;
  padding: 20rpx;
  border-bottom: 1rpx solid #eee;
  
  button {
    flex: 1;
    font-size: 28rpx;
    color: #666;
    background: none;
    border-radius: 8rpx;
    padding: 12rpx 0;
    
    &.active {
      color: #007AFF;
      background: #f0f7ff;
    }
  }
}

.table-header {
  display: flex;
  padding: 24rpx 20rpx;
  background: #f8f8f8;
  border-bottom: 1rpx solid #eee;
  
  .header-item {
    font-size: 24rpx;
    color: #888;
    
    &.num { width: 15%; }
    &.title { width: 30%; }
    &.type { width: 20%; }
    &.favorite { width: 15%; }
    &.duration { width: 20%; }
  }
}

.song-list {
  max-height: 60vh;
  overflow-y: auto;
}

.song-item {
  display: flex;
  align-items: center;
  padding: 28rpx 20rpx;
  border-bottom: 1rpx solid #f5f5f5;
  
  &:active {
    background-color: #f8f8f8;
  }
  
  &.playing {
    background: #f0f7ff;
    .song-num,
    .song-title {
      color: #007AFF;
    }
  }
  
  > text {
    font-size: 28rpx;
    color: #333;
  }
  
  .song-num { 
    width: 15%;
    text-align: center;
  }
  
  .song-title {
    width: 25%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .song-type {
    width: 20%;
    color: #666;
  }
  
  .favorite-icon {
    width: 18%;
    display: flex;
    justify-content: center;
    
    .star-icon {
      width: 36rpx;
      height: 36rpx;
    }
  }
  
  .song-duration {
    width: 22%;
    color: #666;
  }
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}




/* 当前播放信息 */
.now-playing {
  flex: 1;
  padding: 0 20rpx;
  overflow: hidden;

  .song-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: 80vw;
  }

  .song-title {
    font-size: 32rpx;
    color: #333;
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .song-type {
    font-size: 24rpx;
    color: #888;
    margin-top: 6rpx;
  }
}

/* 播放按钮样式修正 */
.control-buttons {
  button {
    width: 80rpx;
    height: 80rpx;
    padding: 0;
    margin: 0;
    background: transparent;
    border: none;
    line-height: 1;
    
    &::after {
      border: none; /* 去除小程序默认边框 */
    }
    
    .play-icon {
      width: 60rpx;
      height: 60rpx;
      transition: transform 0.2s;
    }
    
    &:active .play-icon {
      transform: scale(0.9);
    }
  }
}
/* 新增导入按钮样式 */
.import-wrapper {
  position: absolute;
  right: 30rpx;
  top: 30rpx;
  display: flex;
  align-items: center;
  gap: 10rpx;
  padding: 12rpx 24rpx;
  background-color: #f5f7fa;
  border-radius: 40rpx;
  z-index: 999;
}

.import-text {
  font-size: 28rpx;
  color: #4a90e2;
}

/* 添加进度条样式 */
.progress-container {
  display: flex;
  align-items: center;
  width: 100%;
  margin-top: 12rpx;
}

.progress-bar {
  flex: 1;
  margin: 0 20rpx;
}

.time-text {
  font-size: 24rpx;
  color: #666;
  min-width: 80rpx;
  text-align: center;
}

/* 调整播放图标大小 */
.play-icon {
  width: 48rpx;
  height: 48rpx;
}
</style>

