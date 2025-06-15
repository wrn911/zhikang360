<template>
  <view class="container" :class="currentThemeClass">
<!--    顶部导航栏
    <view class="nav-bar">
      <view class="nav-back" @click="goBack">
        <text class="nav-icon">←</text>
      </view>
      <view class="nav-title">AI答疑助手</view>
      <view class="nav-placeholder"></view>
    </view> -->
    <!-- 侧边栏 -->
    <view class="sidebar" :class="{ 'sidebar-show': showSidebar }">
      <!-- 历史会话部分 -->
      <view class="sidebar-header">
        <text class="sidebar-title">历史会话</text>
      </view>
	  <!-- ==== 侧边栏会话列表显示 ==== -->
      <scroll-view scroll-y class="history-list">
        <view v-for="session in sessions" 
              :key="session.id" 
              class="history-item"
              :class="{ 
                'active': isCurrentSession(session.id),
                [`theme-${session.agent_id || 'general'}`]: true
              }"
              @click="selectSession(session)">
          <!-- 显示会话标题和智能体信息 -->
          <view class="session-header">
            <text class="session-agent-icon">{{ session.agent_icon || '🏥' }}</text>
            <text class="session-title">{{ session.title }}</text>
          </view>
          <text class="session-agent-name">{{ session.agent_name || '健康助手' }}</text>
        </view>
      </scroll-view>
      <!-- 新对话按钮 -->
      <view class="knowledge-base-btn" @click="createNewSession">
        <text>开启新对话</text>
      </view>
<!--      <view class="user-info">
        <text>{{ userInfo.username || '' }}</text>
      </view> -->
    </view>
    
    <!-- 侧边栏遮罩层 -->
    <view class="sidebar-overlay" v-if="showSidebar" @click="closeSidebar"></view>

	<!-- 智能体选择器 -->
	<view class="agent-selector" v-if="showAgentSelector" @click="toggleAgentSelector">
	  <view class="agent-selector-content" @click.stop>
	    <view class="agent-selector-header">
	      <text class="agent-selector-title">选择AI助手</text>
	      <view class="agent-selector-close" @click="toggleAgentSelector">
	        <text>×</text>
	      </view>
	    </view>
	    <view class="agent-list">
	      <view 
	        v-for="(agent, id) in agents" 
	        :key="id" 
	        class="agent-item"
	        :class="{ 
          'agent-item-active': currentAgentId === id,
          [`agent-theme-${id}`]: true
        }"
	        @click="selectAgent(id)">
	        <view class="agent-info">
	          <text class="agent-icon">{{ agent.icon }}</text>
	          <view class="agent-details">
	            <text class="agent-name">{{ agent.name }}</text>
	            <text class="agent-description">{{ agent.description }}</text>
	          </view>
	        </view>
	        <view class="agent-check" v-if="currentAgentId === id">
	          <text>✓</text>
	        </view>
	      </view>
	    </view>
	  </view>
	</view>

    <!-- 主内容区 -->
    <view class="main-content">
      <!-- 消息列表 -->
      <scroll-view 
        class="message-list" 
        scroll-y 
        :scroll-top="scrollTop"
        @scrolltoupper="loadMoreHistory"
        :scroll-with-animation="true"
        style="height: 80%;"
        ref="messageList">
        <!-- ==== 1. 修改消息显示部分，在AI回答后添加意图操作按钮 ==== -->
        <!-- 找到消息列表中的AI消息部分，修改为： -->
        
        <view v-for="(item, index) in messages" 
              :key="index" 
              class="message-item">
          <view class="message user">
            <text>{{ item.question }}</text>
          </view>
          <view class="message ai" :class="currentThemeClass">
            <view class="ai-content-container">
              <view v-if="item.isStreaming" class="streaming-indicator">
                <view class="loading-dots">
                  <view class="dot" :class="currentThemeClass"></view>
                  <view class="dot" :class="currentThemeClass"></view>
                  <view class="dot" :class="currentThemeClass"></view>
                </view>
              </view>
              <view v-if="item.isStreaming && !item.answer" class="loading-indicator">
                <text class="loading-text">{{ currentAgent.loadingText || 'AI正在思考中...' }}</text>
              </view>
              <view v-if="item.answer" class="ai-content-wrapper">
                <view v-for="(part, pIndex) in parseThinkingContent(item.answer)" :key="pIndex">
                  <view v-if="part.type === 'thinking'" class="thinking-content" :class="currentThemeClass">
                    <view class="thinking-header">{{ currentAgent.thinkingText || '思考过程：' }}</view>
                    <zero-markdown-view themeColor="#000000" :markdown="part.content"></zero-markdown-view>
                  </view>
                  <view v-else class="answer-content">
                    <zero-markdown-view themeColor="#000000" :markdown="part.content"></zero-markdown-view>
                  </view>
                </view>
                
                <!-- ==== 新增：意图操作按钮 ==== -->
                <view v-if="item.intent && !item.isStreaming" class="intent-actions" :class="currentThemeClass">
                  <view class="intent-tip">
                    <text class="intent-tip-text">{{ currentAgent.intentTip || '💡 我发现您可能需要：' }}</text>
                  </view>
                  <button class="intent-btn" :class="currentThemeClass" @click="handleIntentAction(item.intent)">
                    <view class="intent-btn-content">
                      <text class="intent-icon">{{ item.intent.action.icon }}</text>
                      <view class="intent-text-container">
                        <text class="intent-title">{{ item.intent.action.title }}</text>
                        <text class="intent-description">{{ item.intent.action.description }}</text>
                      </view>
                      <text class="intent-arrow">→</text>
                    </view>
                  </button>
                </view>
              </view>
            </view>
          </view>
        </view>
		
        <view class="welcome-message" v-if="messages.length === 0">
          <view class="welcome-icon" :class="currentThemeClass">{{ currentAgent.icon }}</view>
          <text class="welcome-text" :class="currentThemeClass">{{ currentAgent.greeting || '嗨！我是你的助手' }}</text>
          <text class="welcome-subtext">{{ currentAgent.subGreeting || '有任何问题，请随时向我咨询' }}</text>
        </view>
        <view id="scroll-bottom" class="scroll-bottom-anchor"></view>
      </scroll-view>

      <!-- 浮动按钮区域 -->
	  <view class="floating-buttons">
	    <!-- 智能体切换按钮：仅在无会话时显示 -->
	    <button v-if="showAgentButton" class="floating-btn agent-btn" :class="currentThemeClass" @click="toggleAgentSelector">
	      <text class="floating-btn-text">{{ agents[currentAgentId].icon }} {{ agents[currentAgentId].name }}</text>
	    </button>
	    
	    <button class="floating-btn" :class="{ 'floating-btn-active': isDeepThinking, [currentThemeClass]: isDeepThinking }" @click="showDeepThinking">
	      <text class="floating-btn-text">深度思考</text>
	    </button>
	    <button class="floating-btn" @click="toggleSidebar">
	      <text class="floating-btn-text">历史对话</text>
	    </button>
	    <button class="floating-btn" @click="createNewSession">
	      <text class="floating-btn-text">新对话</text>
	    </button>
	    <button class="floating-btn" @click="goToKnowledgeBase">
	      <text class="floating-btn-text">知识库</text>
	    </button>
	  </view>

      <!-- 底部输入区域 -->
      <view class="input-area">
        <view class="input-wrapper" :class="currentThemeClass">
          <textarea
            class="input"
            v-model="inputMessage"
            :adjust-position="false"
            :cursor-spacing="20"
            :show-confirm-bar="false"
            :auto-height="true"
            :placeholder="currentAgent.placeholder || '请输入您的问题...'"
            @confirm="sendMessage"
          />
          <button class="send-btn" :class="currentThemeClass" @click="sendMessage" :disabled="!inputMessage.trim()">
            <text>发送</text>
          </button>
        </view>
      </view>

    </view>
  </view>
</template>

<script>
import zeroMarkdownView from '@/uni_modules/zero-markdown-view_2.0.5/components/zero-markdown-view/zero-markdown-view.vue';

export default {
  components: {
    zeroMarkdownView
  },
  data() {
    return {
      showSidebar: false,
      sessions: [],
      currentSession: null,
      messages: [],
      inputMessage: '',
      scrollTop: 0,
      page: 1,
      pageSize: 10,
      hasMore: true,
      userInfo: {},
      baseUrl: 'http://10.27.246.45:8000',
      isFirstMessage: true,
      isLoading: false,
      isDeepThinking: false,
      ws: null, // WebSocket 实例
      wsConnected: false,
      wsUrl: 'ws://10.27.246.45:8000/chat/ws_chat', // WebSocket 地址
      wsReconnectTimer: null,
      wsReconnectTries: 0,
	  // ==== 新增智能体相关数据 ====
	  currentAgentId: 'general',
	  showAgentSelector: false,
	  agents: {
	    'general': {
	      name: '健康助手',
	      icon: '🏥',
	      description: '提供全面的健康咨询',
        greeting: '嗨！我是你的健康助手',
        subGreeting: '有任何健康问题，请随时向我咨询',
        placeholder: '请输入您的健康问题...',
        loadingText: '正在为您分析健康问题...',
        thinkingText: '健康分析过程：',
        intentTip: '🏥 我发现您可能需要：'
	    },
	    'nutritionist': {
	      name: '营养师',
	      icon: '🥗',
	      description: '专业营养指导',
        greeting: '您好！我是您的专属营养师',
        subGreeting: '让我为您提供专业的营养指导和饮食建议',
        placeholder: '请描述您的饮食问题...',
        loadingText: '正在分析您的营养需求...',
        thinkingText: '营养分析过程：',
        intentTip: '🥗 基于营养分析，建议您：'
	    },
	    'trainer': {
	      name: '健身教练',
	      icon: '💪',
	      description: '运动健身指导',
        greeting: '加油！我是您的健身教练',
        subGreeting: '让我帮您制定科学的运动计划，达成健身目标',
        placeholder: '告诉我您的健身目标...',
        loadingText: '正在为您制定训练方案...',
        thinkingText: '训练计划分析：',
        intentTip: '💪 为了更好的训练效果，建议：'
	    },
	    'psychologist': {
	      name: '心理咨询师',
	      icon: '🧠',
	      description: '心理健康支持',
        greeting: '欢迎来到心理咨询室',
        subGreeting: '我会耐心倾听，为您提供专业的心理支持',
        placeholder: '请分享您的想法和感受...',
        loadingText: '正在理解您的情绪状态...',
        thinkingText: '心理分析过程：',
        intentTip: '🧠 基于心理评估，我建议：'
	    },
	  }
    }
  },
  computed: {
	// 智能体选择器是否显示（核心逻辑：无会话时显示）
	showAgentButton() {
	  return !this.currentSession;
	},
	
	// 获取当前会话标题
    getSessionTitle() {
      return this.currentSession && this.currentSession.title ? this.currentSession.title : '新对话'
    },

    // 获取当前智能体
    currentAgent() {
      return this.agents[this.currentAgentId] || this.agents.general;
    },

    // 获取当前主题类名
    currentThemeClass() {
      return `theme-${this.currentAgentId}`;
    }
  },
  // ==== 4. 在 onLoad 中恢复用户的智能体选择 ====
  onLoad() {
    this.connectWebSocket();
    this.loadSessions();
    
    // 恢复用户上次选择的智能体
    const savedAgent = uni.getStorageSync('selectedAgent');
    if (savedAgent && this.agents[savedAgent]) {
		this.currentAgentId = savedAgent;
    }
  },
  onUnload() {
    this.closeWebSocket();
  },
  methods: {
	// 处理意图操作
	handleIntentAction(intent) {
	  if (!intent || !intent.action) {
	    console.warn('无效的意图信息:', intent);
	    return;
	  }
	  
	  console.log('执行意图操作:', intent);
	  
	  if (intent.action.type === 'navigate') {
	    // 显示跳转提示
	    uni.showToast({
	      title: `正在跳转到${intent.action.title.replace('去', '')}...`,
	      icon: 'none',
	      duration: 1500
	    });
	    
	    // 延迟跳转，让用户看到提示
	    setTimeout(() => {
	      uni.navigateTo({
	        url: intent.action.url,
	        success: () => {
	          console.log('成功跳转到:', intent.action.url);
	        },
	        fail: (err) => {
	          console.error('跳转失败:', err);
	          uni.showToast({
	            title: '跳转失败，请检查页面是否存在',
	            icon: 'none'
	          });
	        }
	      });
	    }, 800);
	  }
	},
	
	// 智能体选择相关方法
	toggleAgentSelector() {
	  this.showAgentSelector = !this.showAgentSelector;
	},
	
	selectAgent(agentId) {
	    this.currentAgentId = agentId;
	    this.showAgentSelector = false;
	    
	    // 保存用户选择到本地存储
	    uni.setStorageSync('lastSelectedAgent', agentId);
	    
	    uni.showToast({
	      title: `已切换到${this.agents[agentId].name}`,
	      icon: 'none',
	      duration: 1500
	    });
	  },
	  
    goBack() {
      uni.navigateBack({
        delta: 1
      })
    },
    isCurrentSession(sessionId) {
      return this.currentSession && this.currentSession.id === sessionId
    },
    // 切换侧边栏
    toggleSidebar() {
      this.showSidebar = !this.showSidebar
    },
    
    // 关闭侧边栏
    closeSidebar() {
      this.showSidebar = false
    },
    
    // 跳转到知识库管理页面
    goToKnowledgeBase() {
      uni.navigateTo({
        url: '/pages/knowledgeBase/knowledgeBase'
      })
      this.showSidebar = false
    },

    // 加载会话列表
    async loadSessions() {
      try {
        const token = uni.getStorageSync('xm-user')?.token
        const res = await uni.request({
          url: `${this.baseUrl}/session/list`,
          method: 'GET',
          header: {
            'token': `${token}`
          }
        })
        if (res.statusCode === 200) {
          this.sessions = res.data.sessions
        }
      } catch (error) {
        uni.showToast({
          title: '加载会话失败',
          icon: 'none'
        })
      }
    },

    // 创建新会话 - 只清空界面
    createNewSession() {
        this.currentSession = null;
        this.messages = [];
        this.isFirstMessage = true;
        this.showSidebar = false;
        
        // ==== 新增：智能体选择器重新可用，恢复默认或上次选择 ====
        const savedAgent = uni.getStorageSync('lastSelectedAgent');
        if (savedAgent && this.agents[savedAgent]) {
          this.currentAgentId = savedAgent;
        } else {
          this.currentAgentId = 'general';
		}
    },

    // 选择会话
    async selectSession(session) {
		this.currentSession = session;
		this.messages = [];
		this.page = 1;
		this.hasMore = true;
		this.showSidebar = false;
		this.isFirstMessage = false;
		
		// ==== 新增：设置会话绑定的智能体 ====
		this.currentAgentId = session.agent_id || 'general';
		
		await this.loadHistory();
    },

    // 加载历史消息
    async loadHistory() {
      if (!this.currentSession || !this.currentSession.id) return
      
      try {
        const token = uni.getStorageSync('xm-user')
        const userToken = token ? token.token : ''
        const res = await uni.request({
          url: `${this.baseUrl}/session/${this.currentSession.id}/history`,
          method: 'GET',
          header: {
            'token': userToken
          },
          data: {
            page: this.page,
            page_size: this.pageSize
          }
        })
        if (res.statusCode === 200) {
          const newMessages = res.data.history
          if (newMessages.length < this.pageSize) {
            this.hasMore = false
          }
          this.messages = [...newMessages, ...this.messages]
        }
		
		this.scrollToBottom()
      } catch (error) {
        uni.showToast({
          title: '加载历史消息失败',
          icon: 'none'
        })
      }
    },

    connectWebSocket() {
      if (this.ws && this.wsConnected) return;
      const token = uni.getStorageSync('xm-user')?.token || '';
      this.ws = uni.connectSocket({
        url: this.wsUrl,
        header: {
          'token': token
        },
        success: () => {
          console.log('WebSocket connecting...');
        }
      });
      this.ws.onOpen(() => {
        this.wsConnected = true;
        this.wsReconnectTries = 0;
        console.log('WebSocket connected');
      });
      this.ws.onClose(() => {
        this.wsConnected = false;
        console.log('WebSocket closed');
        this.tryReconnectWebSocket();
      });
      this.ws.onError((err) => {
        this.wsConnected = false;
        console.error('WebSocket error', err);
        this.tryReconnectWebSocket();
      });
      this.ws.onMessage(this.handleWsMessage);
    },
    closeWebSocket() {
      if (this.ws) {
        this.ws.close({});
        this.ws = null;
        this.wsConnected = false;
      }
      if (this.wsReconnectTimer) {
        clearTimeout(this.wsReconnectTimer);
        this.wsReconnectTimer = null;
      }
    },
    tryReconnectWebSocket() {
      if (this.wsReconnectTries > 5) return;
      if (this.wsReconnectTimer) return;
      this.wsReconnectTries++;
      this.wsReconnectTimer = setTimeout(() => {
        this.connectWebSocket();
        this.wsReconnectTimer = null;
      }, 2000 * this.wsReconnectTries);
    },
    // ==== 2. 修改handleWsMessage方法，处理意图信息 ====
    handleWsMessage(res) {
        let data = {};
        try {
          data = typeof res.data === 'string' ? JSON.parse(res.data) : res.data;
        } catch (e) {
          console.error('WebSocket message parse error', e);
          return;
        }
        
        const messageIndex = this.messages.length - 1;
        
        if (data.error) {
          uni.showToast({ title: data.error, icon: 'none' });
          if (messageIndex >= 0) this.messages[messageIndex].isStreaming = false;
          this.isLoading = false;
          return;
        }
        
        if (data.end) {
          if (messageIndex >= 0) {
            this.messages[messageIndex].isStreaming = false;
            
            // 处理意图信息
            if (data.intent) {
              this.messages[messageIndex].intent = data.intent;
            }
          }
          
          // ==== 修改：处理新会话信息 ====
          if (this.isFirstMessage && data.session) {
            this.currentSession = {
              id: data.session.id,
              title: data.session.title,
              agent_id: data.session.agent_id || this.currentAgentId,
              agent_name: data.session.agent_name,
              agent_icon: data.session.agent_icon
            };
            // 更新当前智能体（虽然应该是一样的）
            this.currentAgentId = this.currentSession.agent_id;
            this.isFirstMessage = false;
            this.loadSessions();
          }
          
          setTimeout(() => { this.scrollToBottom(); }, 100);
          this.isLoading = false;
          return;
        }
        
        // 正常token处理
        if (messageIndex >= 0) {
          this.messages[messageIndex].isStreaming = true;
          this.messages[messageIndex].answer += data.token;
          this.$nextTick(() => { this.scrollToBottom(); });
        }
      },

    async sendMessage() {
       if (!this.inputMessage.trim() || this.isLoading) return;
       if (!this.wsConnected) {
         this.connectWebSocket();
         uni.showToast({ title: '正在连接AI服务...', icon: 'none' });
         return;
       }
       
       const question = this.inputMessage.trim();
       this.inputMessage = '';
       this.isLoading = true;
       
       // 添加问题到消息列表
       this.messages.push({
         question,
         answer: '',
         isStreaming: true,
         intent: null  // 初始化意图字段
       });
       this.scrollToBottom();
       
       // 发送消息
       const requestData = {
         question: question,
         model: this.isDeepThinking ? 'DeepSeek-R1' : 'glm-4-flash'
       };
       
	    // 检查是否有现有会话
	    if (this.currentSession && this.currentSession.id) {
			// 现有会话：发送会话ID，不发送agent_id
			requestData.session_id = this.currentSession.id;
			console.log('[DEBUG] 现有会话，session_id:', this.currentSession.id);
	    } else {
			// 新会话：发送智能体ID和标题
			requestData.agent_id = this.currentAgentId;
			if (this.isFirstMessage) {
			  requestData.title = question;
			}
			console.log('[DEBUG] 新会话，agent_id:', this.currentAgentId, 'title:', question);
	    }

       this.ws.send({
         data: JSON.stringify(requestData)
       });
    },
	
    // 深度思考
    showDeepThinking() {
      this.isDeepThinking = !this.isDeepThinking
      uni.showToast({
        title: this.isDeepThinking ? '已切换到深度思考模式' : '已切换到普通模式',
        icon: 'none'
      })
    },

	scrollToBottom() {
      // 使用nextTick确保DOM更新后再滚动
      this.$nextTick(() => {
        // 使用选择器查询尝试获取底部元素
        uni.createSelectorQuery()
          .in(this)
          .select('#scroll-bottom')
          .boundingClientRect(data => {
            if (data) {
              // 设置一个较大的值确保滚动到底部
              // 由于输入框现在固定在底部，需要确保消息完全可见
              this.scrollTop = 9999999
              
              // 延迟再次滚动以确保在复杂DOM渲染后仍能滚动到底部
              setTimeout(() => {
                this.scrollTop = this.scrollTop + 1
              }, 200)
            }
          })
          .exec()
      })
    },

    // 加载更多历史消息
    async loadMoreHistory() {
      if (!this.hasMore) return
      this.page++
      await this.loadHistory()
    },
    
    // 检查内容是否包含思考过程
    hasThinkingContent(text) {
      return text && text.includes('<think>')
    },
    
    // 解析带有思考过程的内容
    parseThinkingContent(text) {
      if (!text) return []
      
      const result = []
      let currentIndex = 0
      let startTagIndex, endTagIndex
      
      while (currentIndex < text.length) {
        // 查找下一个思考标签
        startTagIndex = text.indexOf('<think>', currentIndex)
        
        if (startTagIndex === -1) {
          // 没有更多思考标签，添加剩余内容
          if (currentIndex < text.length) {
            result.push({
              type: 'normal',
              content: text.substring(currentIndex)
            })
          }
          break
        }
        
        // 添加思考标签前的普通内容
        if (startTagIndex > currentIndex) {
          result.push({
            type: 'normal',
            content: text.substring(currentIndex, startTagIndex)
          })
        }
        
        // 查找结束标签
        endTagIndex = text.indexOf('</think>', startTagIndex)
        if (endTagIndex === -1) {
          // 没有找到结束标签，说明思考内容还在流式传输中
          // 将从开始标签到当前文本末尾的内容作为思考内容
          result.push({
            type: 'thinking',
            content: text.substring(startTagIndex + 7) // 跳过<think>标签
          })
          break
        }
        
        // 提取思考内容（不包括标签）
        const thinkingContent = text.substring(startTagIndex + 7, endTagIndex)
        result.push({
          type: 'thinking',
          content: thinkingContent
        })
        
        // 更新当前索引到结束标签之后
        currentIndex = endTagIndex + 8 // '</think>'.length = 8
      }
      
      return result
    }
  }
}
</script>

<style>
/* 基础容器样式 */
.container {
  height: 100vh;
  display: flex;
  position: relative;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  background-color: #f8fafc; /* 统一一个更柔和的浅色背景 */
}

/* ===== 现代化智能体主题样式 ===== */
/* 健康助手主题 - 现代绿色系 */
.theme-general {
  /* background: linear-gradient(135deg, #f8fffe 0%, #f0fdf4 50%, #ffffff 100%); */ /* 移除独立背景，使用container统一背景 */
}

.theme-general .welcome-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%); /* 调整渐变色，使其更鲜明 */
  -webkit-background-clip: text;
  color: transparent;
}

.theme-general .welcome-text {
  color: #065f46;
}

.theme-general .message.ai {
  border-left: 4px solid #10b981;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.08); /* 调整阴影使其更柔和 */
}

.theme-general .thinking-content {
  background: linear-gradient(135deg, rgba(236, 253, 245, 0.9) 0%, rgba(209, 250, 229, 0.75) 100%); /* 略微调整透明度 */
  border-left: 4px solid #34d399;
  backdrop-filter: blur(10px); /* 增强模糊效果 */
}

.theme-general .thinking-header {
  color: #047857;
}

.theme-general .intent-actions {
  background: linear-gradient(135deg, rgba(236, 253, 245, 0.95) 0%, rgba(220, 252, 231, 0.8) 100%);
  border-left: 4px solid #34d399;
  backdrop-filter: blur(10px);
}

.theme-general .intent-tip-text {
  color: #047857;
}

.theme-general .intent-btn,
.theme-general .send-btn,
.theme-general .agent-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25);
}

.theme-general .input-wrapper {
  border: 1px solid rgba(16, 185, 129, 0.2); /* 边框颜色稍深 */
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(16px); /* 增强模糊 */
}

.theme-general .dot {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

/* 营养师主题 - 现代橙色系 */
.theme-nutritionist {
  /* background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 50%, #ffffff 100%); */
}

.theme-nutritionist .welcome-icon {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  -webkit-background-clip: text;
  color: transparent;
}

.theme-nutritionist .welcome-text {
  color: #92400e;
}

.theme-nutritionist .message.ai {
  border-left: 4px solid #f59e0b;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.08);
}

.theme-nutritionist .thinking-content {
  background: linear-gradient(135deg, rgba(254, 243, 199, 0.9) 0%, rgba(253, 230, 138, 0.75) 100%);
  border-left: 4px solid #fbbf24;
  backdrop-filter: blur(10px);
}

.theme-nutritionist .thinking-header {
  color: #d97706;
}

.theme-nutritionist .intent-actions {
  background: linear-gradient(135deg, rgba(254, 243, 199, 0.95) 0%, rgba(254, 240, 138, 0.8) 100%);
  border-left: 4px solid #fbbf24;
  backdrop-filter: blur(10px);
}

.theme-nutritionist .intent-tip-text {
  color: #d97706;
}

.theme-nutritionist .intent-btn,
.theme-nutritionist .send-btn,
.theme-nutritionist .agent-btn {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.25);
}

.theme-nutritionist .input-wrapper {
  border: 1px solid rgba(245, 158, 11, 0.2);
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(16px);
}

.theme-nutritionist .dot {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

/* 健身教练主题 - 现代红色系 */
.theme-trainer {
  /* background: linear-gradient(135deg, #fef2f2 0%, #fecaca 50%, #ffffff 100%); */
}

.theme-trainer .welcome-icon {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  -webkit-background-clip: text;
  color: transparent;
}

.theme-trainer .welcome-text {
  color: #991b1b;
}

.theme-trainer .message.ai {
  border-left: 4px solid #ef4444;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.08);
}

.theme-trainer .thinking-content {
  background: linear-gradient(135deg, rgba(254, 226, 226, 0.9) 0%, rgba(252, 165, 165, 0.75) 100%);
  border-left: 4px solid #f87171;
  backdrop-filter: blur(10px);
}

.theme-trainer .thinking-header {
  color: #dc2626;
}

.theme-trainer .intent-actions {
  background: linear-gradient(135deg, rgba(254, 226, 226, 0.95) 0%, rgba(254, 202, 202, 0.8) 100%);
  border-left: 4px solid #f87171;
  backdrop-filter: blur(10px);
}

.theme-trainer .intent-tip-text {
  color: #dc2626;
}

.theme-trainer .intent-btn,
.theme-trainer .send-btn,
.theme-trainer .agent-btn {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.25);
}

.theme-trainer .input-wrapper {
  border: 1px solid rgba(239, 68, 68, 0.2);
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(16px);
}

.theme-trainer .dot {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

/* 心理咨询师主题 - 现代紫色系 */
.theme-psychologist {
  /* background: linear-gradient(135deg, #faf5ff 0%, #e9d5ff 50%, #ffffff 100%); */
}

.theme-psychologist .welcome-icon {
  background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  color: transparent;
}

.theme-psychologist .welcome-text {
  color: #581c87;
}

.theme-psychologist .message.ai {
  border-left: 4px solid #8b5cf6;
  box-shadow: 0 2px 8px rgba(139, 92, 246, 0.08);
}

.theme-psychologist .thinking-content {
  background: linear-gradient(135deg, rgba(243, 232, 255, 0.9) 0%, rgba(221, 214, 254, 0.75) 100%);
  border-left: 4px solid #a78bfa;
  backdrop-filter: blur(10px);
}

.theme-psychologist .thinking-header {
  color: #7c3aed;
}

.theme-psychologist .intent-actions {
  background: linear-gradient(135deg, rgba(243, 232, 255, 0.95) 0%, rgba(233, 213, 255, 0.8) 100%);
  border-left: 4px solid #a78bfa;
  backdrop-filter: blur(10px);
}

.theme-psychologist .intent-tip-text {
  color: #7c3aed;
}

.theme-psychologist .intent-btn,
.theme-psychologist .send-btn,
.theme-psychologist .agent-btn {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  box-shadow: 0 4px 14px rgba(139, 92, 246, 0.25);
}

.theme-psychologist .input-wrapper {
  border: 1px solid rgba(139, 92, 246, 0.2);
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(16px);
}

.theme-psychologist .dot {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

/* 智能体选择器现代化主题预览 */
.agent-theme-general {
  background: linear-gradient(135deg, rgba(236, 253, 245, 0.6) 0%, rgba(255, 255, 255, 0.95) 100%); /* 增强背景对比 */
  border: 2px solid #10b981;
  backdrop-filter: blur(10px);
}

.agent-theme-nutritionist {
  background: linear-gradient(135deg, rgba(254, 243, 199, 0.6) 0%, rgba(255, 255, 255, 0.95) 100%);
  border: 2px solid #f59e0b;
  backdrop-filter: blur(10px);
}

.agent-theme-trainer {
  background: linear-gradient(135deg, rgba(254, 226, 226, 0.6) 0%, rgba(255, 255, 255, 0.95) 100%);
  border: 2px solid #ef4444;
  backdrop-filter: blur(10px);
}

.agent-theme-psychologist {
  background: linear-gradient(135deg, rgba(243, 232, 255, 0.6) 0%, rgba(255, 255, 255, 0.95) 100%);
  border: 2px solid #8b5cf6;
  backdrop-filter: blur(10px);
}

/* 会话列表现代化主题样式 */
.history-item.theme-general.active {
  background: linear-gradient(135deg, rgba(236, 253, 245, 0.8) 0%, rgba(255, 255, 255, 0.95) 100%);
  border-left: 4px solid #10b981;
  backdrop-filter: blur(8px);
}

.history-item.theme-nutritionist.active {
  background: linear-gradient(135deg, rgba(254, 243, 199, 0.8) 0%, rgba(255, 255, 255, 0.95) 100%);
  border-left: 4px solid #f59e0b;
  backdrop-filter: blur(8px);
}

.history-item.theme-trainer.active {
  background: linear-gradient(135deg, rgba(254, 226, 226, 0.8) 0%, rgba(255, 255, 255, 0.95) 100%);
  border-left: 4px solid #ef4444;
  backdrop-filter: blur(8px);
}

.history-item.theme-psychologist.active {
  background: linear-gradient(135deg, rgba(243, 232, 255, 0.8) 0%, rgba(255, 255, 255, 0.95) 100%);
  border-left: 4px solid #8b5cf6;
  backdrop-filter: blur(8px);
}

/* ===== 现代化基础组件样式 ===== */
/* 侧边栏现代化样式 */
.sidebar {
  position: fixed;
  left: -80%;
  top: 0;
  width: 80%;
  max-width: 320px; /* 增加最大宽度限制 */
  height: 100vh;
  background: rgba(255, 255, 255, 0.97); /* 略微调整透明度 */
  z-index: 1000;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1); /* 调整阴影 */
  border-right: 1px solid rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(24px); /* 增强模糊 */
  -webkit-backdrop-filter: blur(24px);
}

.sidebar-show {
  left: 0;
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.2); /* 遮罩颜色加深 */
  z-index: 999;
  animation: fadeIn 0.3s forwards;
  backdrop-filter: blur(3px); /* 增强模糊 */
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.sidebar-header {
  padding: 36rpx 28rpx; /* 增加内边距 */
  border-bottom: 1px solid rgba(0, 0, 0, 0.07);
  background: rgba(248, 250, 252, 0.9); /* 调整背景透明度 */
}

.sidebar-title {
  color: #0f172a; /* 标题颜色加深 */
  font-weight: 600;
  font-size: 34rpx; /* 字体稍大 */
  letter-spacing: -0.02em;
}

.history-list {
  flex: 1;
  padding: 20rpx; /* 增加内边距 */
  height: 80%;
}

.history-item {
  padding: 22rpx 20rpx; /* 调整内边距 */
  margin-bottom: 10rpx; /* 调整外边距 */
  border-radius: 18rpx; /* 圆角稍大 */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  background: rgba(255, 255, 255, 0.8);
  border-left: 4px solid transparent; /* 边框加粗 */
  backdrop-filter: blur(10px);
}

.history-item:active {
  transform: scale(0.98);
}

.session-header {
  display: flex;
  align-items: center;
  margin-bottom: 6rpx;
}

.session-agent-icon {
  font-size: 28rpx;
  margin-right: 12rpx;
  flex-shrink: 0;
}

.session-title {
  flex: 1;
  font-size: 28rpx; /* 字体稍大 */
  font-weight: 500;
  color: #1e293b; /* 颜色加深 */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  letter-spacing: -0.015em;
}

.session-agent-name {
  font-size: 22rpx; /* 字体稍大 */
  color: #64748b; /* 颜色调整 */
  margin-left: 44rpx; /* 调整间距 */
  font-weight: 400;
}

.knowledge-base-btn {
  padding: 22rpx 28rpx;
  background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%); /* 调整渐变色 */
  color: #ffffff;
  text-align: center;
  margin: 20rpx; /* 调整外边距 */
  border-radius: 20rpx; /* 圆角稍大 */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  font-weight: 500;
  font-size: 30rpx; /* 字体稍大 */
  letter-spacing: -0.01em;
  box-shadow: 0 6px 18px rgba(99, 102, 241, 0.3); /* 调整阴影 */
}

.knowledge-base-btn:active {
  transform: scale(0.96);
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.35);
}

/* 智能体选择器现代化样式 */
.agent-selector {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.25);
  z-index: 1001;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease;
  backdrop-filter: blur(4px);
}

.agent-selector-content {
  background: rgba(255, 255, 255, 0.99);
  border-radius: 28rpx; /* 圆角稍大 */
  width: 88%; /* 宽度稍大 */
  max-width: 640rpx;
  max-height: 75vh; /* 高度稍大 */
  overflow: hidden;
  animation: slideUp 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.18); /* 调整阴影 */
  backdrop-filter: blur(24px);
}

@keyframes slideUp {
  from { 
    opacity: 0; 
    transform: translateY(40px) scale(0.96); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0) scale(1); 
  }
}

.agent-selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 36rpx 28rpx;
  border-bottom: 1px solid rgba(0, 0, 0, 0.07);
  background: rgba(248, 250, 252, 0.9);
}

.agent-selector-title {
  font-size: 34rpx;
  font-weight: 600;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.agent-selector-close {
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12rpx;
  background: rgba(0, 0, 0, 0.04);
  font-size: 32rpx;
  color: #6b7280;
  transition: all 0.2s ease;
}

.agent-selector-close:active {
  background: rgba(0, 0, 0, 0.08);
  transform: scale(0.95);
}

.agent-list {
  padding: 20rpx;
  max-height: 55vh; /* 增加最大高度 */
  overflow-y: auto;
}

.agent-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 28rpx 20rpx; /* 调整内边距 */
  margin-bottom: 14rpx;
  border-radius: 22rpx; /* 圆角稍大 */
  background: rgba(255, 255, 255, 0.85);
  border: 2px solid transparent;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  backdrop-filter: blur(10px);
}

.agent-item:active {
  transform: scale(0.98);
}

.agent-item-active {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); /* 调整阴影 */
  transform: translateY(-3rpx);
}

.agent-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.agent-icon {
  font-size: 40rpx;
  margin-right: 20rpx;
}

.agent-details {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.agent-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #1e293b;
  letter-spacing: -0.015em;
}

.agent-description {
  font-size: 24rpx;
  color: #64748b;
  font-weight: 400;
}

.agent-check {
  width: 32rpx;
  height: 32rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18rpx;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

/* 主内容区域现代化 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  position: relative;
  height: 100vh;
  overflow: hidden;
  background: transparent;
}

.message-list {
  flex: 1;
  padding: 28rpx; /* 增加内边距 */
  padding-bottom: 340rpx; /* 增加底部内边距 */
  background: transparent;
  scroll-behavior: smooth;
}

.scroll-bottom-anchor {
  height: 1rpx;
  width: 100%;
}

.message-item {
  margin-bottom: 32rpx;
}

.message {
  max-width: 85%; /* 稍宽一些 */
  padding: 22rpx 28rpx; /* 调整内边距 */
  border-radius: 24rpx; /* 圆角稍大 */
  margin-bottom: 20rpx; /* 调整外边距 */
  word-break: break-word;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  animation: messageAppear 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  font-weight: 400;
  line-height: 1.55; /* 调整行高 */
}

@keyframes messageAppear {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  margin-left: auto;
  background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
  color: #ffffff;
  border-bottom-right-radius: 10rpx; /* 圆角调整 */
  box-shadow: 0 6px 18px rgba(99, 102, 241, 0.3); /* 调整阴影 */
}

.message.ai {
  display: flex;
  align-items: flex-start;
  background: rgba(255, 255, 255, 0.99);
  border-bottom-left-radius: 10rpx;
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
}

.ai-content-container {
  width: 100%;
  position: relative;
}

.ai-content-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 16rpx;
}

.thinking-content {
  padding: 18rpx 22rpx;
  margin-bottom: 18rpx;
  border-radius: 18rpx;
  width: 100%;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05); /* 调整阴影 */
}

.thinking-header {
  font-weight: 600;
  margin-bottom: 14rpx;
  font-size: 26rpx;
  display: flex;
  align-items: center;
  letter-spacing: -0.01em;
}

.thinking-header:before {
  content: '💭';
  margin-right: 8rpx;
  font-size: 28rpx;
}

.answer-content {
  width: 100%;
  line-height: 1.6;
}

/* 现代化加载指示器 */
.streaming-indicator {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12rpx;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24rpx;
  width: 100%;
  animation: pulse 2s infinite ease-in-out;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.loading-dots {
  display: flex;
  margin-bottom: 12rpx;
  gap: 6rpx;
}

.dot {
  width: 8rpx;
  height: 8rpx;
  border-radius: 50%;
  opacity: 0.8;
  animation: dotPulse 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

.dot:nth-child(3) {
  animation-delay: 0s;
}

@keyframes dotPulse {
  0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
  40% { transform: scale(1.1); opacity: 1; }
}

.loading-text {
  font-size: 24rpx;
  color: #6b7280;
  font-weight: 400;
}

/* 现代化意图操作按钮 */
.intent-actions {
  margin-top: 20rpx;
  padding: 18rpx;
  border-radius: 18rpx;
  animation: intentButtonAppear 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes intentButtonAppear {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.intent-tip {
  margin-bottom: 12rpx;
}

.intent-tip-text {
  font-size: 26rpx;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.intent-btn {
  width: 100%;
  color: white;
  border: none;
  border-radius: 18rpx;
  padding: 0;
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.intent-btn:active {
  transform: scale(0.98);
}

.intent-btn-content {
  display: flex;
  align-items: center;
  padding: 18rpx 24rpx; /* 调整内边距 */
  width: 100%;
}

.intent-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
  flex-shrink: 0;
}

.intent-text-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.intent-title {
  font-size: 30rpx;
  font-weight: 600;
  color: white;
  margin-bottom: 4rpx; /* 增加间距 */
  letter-spacing: -0.01em;
}

.intent-description {
  font-size: 24rpx;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.35;
  font-weight: 400;
}

.intent-arrow {
  font-size: 28rpx;
  color: white;
  margin-left: 12rpx;
  flex-shrink: 0;
  font-weight: 500;
}

/* 现代化欢迎消息 */
.welcome-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 80rpx 32rpx;
  animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}

.welcome-icon {
  font-size: 96rpx; /* 图标稍大 */
  margin-bottom: 28rpx;
}

.welcome-text {
  font-size: 40rpx; /* 字体稍大 */
  font-weight: 600;
  margin-bottom: 20rpx;
  letter-spacing: -0.025em;
}

.welcome-subtext {
  color: #475569; /* 颜色调整 */
  text-align: center;
  font-size: 28rpx;
  line-height: 1.55;
  max-width: 88%;
  font-weight: 400;
}

/* 现代化浮动按钮区域 */
.floating-buttons {
  position: fixed;
  bottom: 190rpx; /* 调整位置 */
  left: 0;
  right: 0;
  display: flex;
  justify-content: flex-start;
  padding: 10rpx 20rpx; /* 调整内边距 */
  background: rgba(255, 255, 255, 0.97);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  z-index: 101;
  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);
  overflow-x: auto;
  white-space: nowrap;
}

.floating-btn {
  background: rgba(255, 255, 255, 0.92);
  color: #334155; /* 颜色调整 */
  border: 1px solid rgba(0, 0, 0, 0.09);
  border-radius: 28rpx; /* 圆角稍大 */
  padding: 14rpx 24rpx; /* 调整内边距 */
  font-size: 20rpx; /* 字体稍大 */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  flex: 0 0 auto;
  margin: 0 8rpx; /* 调整外边距 */
  min-width: 80rpx;
  backdrop-filter: blur(10px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.floating-btn:active {
  transform: scale(0.96);
  background: rgba(248, 250, 252, 0.9);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

/* 深度思考按钮激活状态 - 默认主题 */
.floating-btn-active {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
  color: white !important;
  border: 1px solid transparent !important;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25) !important;
}

.floating-btn-active .floating-btn-text {
  color: white !important;
}

/* 深度思考按钮激活状态 - 各主题样式 */
.theme-nutritionist .floating-btn-active {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
  box-shadow: 0 4px 14px rgba(245, 158, 11, 0.25) !important;
}

.theme-trainer .floating-btn-active {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.25) !important;
}

.theme-psychologist .floating-btn-active {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
  box-shadow: 0 4px 14px rgba(139, 92, 246, 0.25) !important;
}

.floating-btn-text {
  font-size: 24rpx;
  color: #334155;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.agent-btn .floating-btn-text {
  color: white;
  font-size: 20rpx;
}

/* 现代化底部输入区域 */
.input-area {
  padding: 24rpx 28rpx; /* 调整内边距 */
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.99);
  z-index: 100;
  backdrop-filter: blur(22px);
  -webkit-backdrop-filter: blur(22px);
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 16rpx; /* 增加间距 */
  padding: 10rpx; /* 调整内边距 */
  background: rgba(255, 255, 255, 0.97);
  border-radius: 32rpx; /* 圆角稍大 */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.07); /* 调整阴影 */
}

.input-wrapper:focus-within {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transform: translateY(-1rpx);
}

.input {
  flex: 1;
  min-height: 72rpx; /* 增加最小高度 */
  padding: 18rpx 24rpx; /* 调整内边距 */
  font-size: 30rpx; /* 字体稍大 */
  border: none;
  border-radius: 24rpx; /* 圆角稍大 */
  background: rgba(248, 250, 252, 0.9);
  transition: all 0.3s ease;
  color: #1e293b; /* 颜色加深 */
  font-weight: 400;
  line-height: 1.45;
}

.input:focus {
  background: rgba(248, 250, 252, 1);
  outline: none;
}

.send-btn {
  color: #ffffff;
  border: none;
  border-radius: 24rpx; /* 圆角稍大 */
  padding: 14rpx 28rpx; /* 调整内边距 */
  font-size: 28rpx; /* 字体稍大 */
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  font-weight: 500;
  letter-spacing: -0.01em;
}

.send-btn:active {
  transform: scale(0.96);
}

.send-btn[disabled] {
  background: linear-gradient(135deg, #d1d5db 0%, #9ca3af 100%) !important;
  opacity: 0.6;
  box-shadow: none !important;
  color: #6b7280 !important;
}

/* 现代化Markdown样式 */
.message.ai :deep(pre) {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); /* 调整颜色 */
  border-radius: 14rpx; /* 圆角稍大 */
  padding: 18rpx; /* 调整内边距 */
  overflow-x: auto;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.12); /* 调整阴影 */
}

.message.ai :deep(code) {
  background: rgba(99, 102, 241, 0.12); /* 背景稍深 */
  color: #4338ca; /* 颜色调整 */
  padding: 3rpx 8rpx; /* 调整内边距 */
  border-radius: 6rpx; /* 圆角稍大 */
  font-size: 25rpx; /* 字体稍大 */
}

.message.ai :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 12rpx 0;
  border-radius: 8rpx;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.message.ai :deep(th),
.message.ai :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 12rpx 16rpx;
  text-align: left;
}

.message.ai :deep(th) {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); /* 调整颜色 */
  font-weight: 600;
  color: #1e293b; /* 颜色加深 */
}

.message.ai :deep(tr:nth-child(even)) {
  background: rgba(249, 250, 251, 0.5);
}

.message.ai :deep(blockquote) {
  border-left: 4px solid #e5e7eb;
  margin: 12rpx 0;
  padding: 12rpx 16rpx;
  background: rgba(249, 250, 251, 0.5);
  border-radius: 0 8rpx 8rpx 0;
}

.message.ai :deep(h1),
.message.ai :deep(h2),
.message.ai :deep(h3) {
  color: #1f2937;
  font-weight: 600;
  letter-spacing: -0.025em;
  margin: 16rpx 0 8rpx 0;
}

.message.ai :deep(ul),
.message.ai :deep(ol) {
  padding-left: 24rpx;
  margin: 8rpx 0;
}

.message.ai :deep(li) {
  margin: 4rpx 0;
  line-height: 1.5;
}

/* 现代化响应式调整 */
@media screen and (max-width: 750px) {
  .agent-selector-content {
    width: 95%;
    border-radius: 20rpx;
  }
  
  .floating-btn {
    padding: 10rpx 16rpx;
    margin: 0 4rpx;
    min-width: 64rpx;
  }
  
  .floating-btn-text {
    font-size: 20rpx;
  }
  
  .session-agent-icon {
    font-size: 24rpx;
  }
  
  .session-title {
    font-size: 24rpx;
  }
  
  .session-agent-name {
    font-size: 18rpx;
    margin-left: 36rpx;
  }
  
  .message {
    max-width: 88%;
    padding: 16rpx 20rpx;
  }
  
  .welcome-icon {
    font-size: 72rpx;
  }
  
  .welcome-text {
    font-size: 32rpx;
  }
  
  .welcome-subtext {
    font-size: 24rpx;
  }
}

/* 深色模式适配（可选） */
@media (prefers-color-scheme: dark) {
  .container {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  }
  
  .sidebar {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
  }
  
  .sidebar-header {
    background: rgba(30, 41, 59, 0.8);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
  
  .sidebar-title {
    color: #f1f5f9;
  }
  
  .session-title {
    color: #cbd5e1;
  }
  
  .session-agent-name {
    color: #64748b;
  }
  
  .message.ai {
    background: rgba(30, 41, 59, 0.8);
    border-left-color: currentColor;
  }
  
  .welcome-subtext {
    color: #64748b;
  }
}
</style>