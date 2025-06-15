// utils/enhanced-ai-service.js - 增强版AI服务
class EnhancedAIService {
  constructor() {
    this.baseUrl = 'http://10.27.246.45:8000'
    this.requestQueue = []
    this.isProcessingQueue = false
    this.cache = new Map()
    this.retryConfig = {
      maxRetries: 3,
      retryDelay: 1000,
      backoffFactor: 2
    }
    this.performanceMetrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      averageResponseTime: 0,
      cacheHits: 0
    }
  }
  
  // 增强的会话列表获取
  async getSessions(options = {}) {
    const cacheKey = 'sessions_list'
    
    try {
      // 执行健康检查
    const healthStatus = await this.performHealthCheck()
    
    if (healthStatus.status === 'healthy') {
      console.log('✅ 智能重连成功')
      return true
    } else {
      console.log('❌ 智能重连失败')
      return false
    }
  }
  
  // 获取服务状态报告
  generateServiceReport() {
    const performance = this.getPerformanceStats()
    
    return {
      summary: {
        status: performance.successRate > 0.8 ? 'good' : 'poor',
        totalRequests: performance.totalRequests,
        successRate: Math.round(performance.successRate * 100),
        averageResponseTime: Math.round(performance.averageResponseTime)
      },
      performance: performance,
      cache: {
        size: this.cache.size,
        hitRate: Math.round(performance.cacheHitRate * 100)
      },
      recommendations: this.generateServiceRecommendations(performance),
      generatedAt: new Date().toISOString()
    }
  }
  
  // 生成服务建议
  generateServiceRecommendations(performance) {
    const recommendations = []
    
    if (performance.successRate < 0.8) {
      recommendations.push({
        type: 'warning',
        message: '服务成功率较低，建议检查网络连接',
        action: 'checkNetwork'
      })
    }
    
    if (performance.averageResponseTime > 3000) {
      recommendations.push({
        type: 'warning',
        message: '响应时间较长，建议清理缓存',
        action: 'clearCache'
      })
    }
    
    if (performance.cacheHitRate < 0.3 && performance.totalRequests > 10) {
      recommendations.push({
        type: 'info',
        message: '缓存命中率较低，建议优化缓存策略',
        action: 'optimizeCache'
      })
    }
    
    if (this.cache.size > 100) {
      recommendations.push({
        type: 'info',
        message: '缓存数据较多，建议定期清理',
        action: 'cleanupCache'
      })
    }
    
    return recommendations
  }
  
  // 自动优化服务
  async autoOptimizeService() {
    console.log('🔧 开始自动优化服务...')
    
    const performance = this.getPerformanceStats()
    
    // 如果缓存过大，清理旧缓存
    if (this.cache.size > 50) {
      this.cleanupOldCache()
    }
    
    // 如果成功率过低，尝试重连
    if (performance.successRate < 0.5 && performance.totalRequests > 5) {
      await this.intelligentReconnect()
    }
    
    // 如果响应时间过长，调整超时设置
    if (performance.averageResponseTime > 5000) {
      this.retryConfig.maxRetries = Math.max(1, this.retryConfig.maxRetries - 1)
    }
    
    console.log('✅ 服务优化完成')
  }
  
  // 清理旧缓存
  cleanupOldCache() {
    const now = Date.now()
    const maxAge = 5 * 60 * 1000 // 5分钟
    
    for (const [key, value] of this.cache.entries()) {
      if (now - value.timestamp > maxAge) {
        this.cache.delete(key)
      }
    }
    
    console.log(`🧹 清理了过期缓存，当前缓存大小: ${this.cache.size}`)
  }
  
  // 批量操作支持
  async batchOperations(operations) {
    const results = []
    const concurrency = 3 // 最大并发数
    
    for (let i = 0; i < operations.length; i += concurrency) {
      const batch = operations.slice(i, i + concurrency)
      const batchPromises = batch.map(async (operation) => {
        try {
          const result = await this.executeOperation(operation)
          return { success: true, result, operation }
        } catch (error) {
          return { success: false, error: error.message, operation }
        }
      })
      
      const batchResults = await Promise.all(batchPromises)
      results.push(...batchResults)
    }
    
    return results
  }
  
  // 执行单个操作
  async executeOperation(operation) {
    switch (operation.type) {
      case 'getSessions':
        return await this.getSessions(operation.options)
      
      case 'getHistory':
        return await this.getSessionHistory(
          operation.sessionId, 
          operation.page, 
          operation.pageSize, 
          operation.options
        )
      
      case 'deleteSession':
        return await this.deleteSession(operation.sessionId, operation.options)
      
      case 'updateTitle':
        return await this.updateSessionTitle(
          operation.sessionId, 
          operation.title, 
          operation.options
        )
      
      default:
        throw new Error(`Unknown operation type: ${operation.type}`)
    }
  }
  
  // 数据同步
  async syncData(options = {}) {
    console.log('🔄 开始数据同步...')
    
    try {
      const operations = [
        { type: 'getSessions', options: { useCache: false } }
      ]
      
      const results = await this.batchOperations(operations)
      const sessionsResult = results.find(r => r.operation.type === 'getSessions')
      
      if (sessionsResult && sessionsResult.success) {
        console.log('✅ 数据同步成功')
        return {
          success: true,
          syncedAt: Date.now(),
          sessionsCount: sessionsResult.result.length
        }
      } else {
        throw new Error('会话数据同步失败')
      }
      
    } catch (error) {
      console.error('❌ 数据同步失败:', error)
      return {
        success: false,
        error: error.message,
        syncedAt: Date.now()
      }
    }
  }
  
  // 离线支持
  async handleOfflineMode() {
    console.log('📱 进入离线模式')
    
    // 保存当前缓存到本地存储
    try {
      const cacheData = {}
      for (const [key, value] of this.cache.entries()) {
        cacheData[key] = value
      }
      
      uni.setStorageSync('ai_service_offline_cache', {
        cacheData,
        timestamp: Date.now()
      })
      
      console.log('💾 离线缓存已保存')
    } catch (error) {
      console.error('离线缓存保存失败:', error)
    }
  }
  
  // 恢复在线模式
  async handleOnlineMode() {
    console.log('🌐 恢复在线模式')
    
    try {
      // 恢复离线缓存
      const offlineCache = uni.getStorageSync('ai_service_offline_cache')
      if (offlineCache && offlineCache.cacheData) {
        for (const [key, value] of Object.entries(offlineCache.cacheData)) {
          this.cache.set(key, value)
        }
        console.log('📥 离线缓存已恢复')
      }
      
      // 同步数据
      await this.syncData()
      
      // 清理离线缓存
      uni.removeStorageSync('ai_service_offline_cache')
      
    } catch (error) {
      console.error('在线模式恢复失败:', error)
    }
  }
  
  // 错误分类和处理
  categorizeError(error) {
    if (error.message.includes('timeout')) {
      return {
        category: 'timeout',
        severity: 'medium',
        retryable: true,
        userMessage: '请求超时，请检查网络连接'
      }
    }
    
    if (error.message.includes('network')) {
      return {
        category: 'network',
        severity: 'high',
        retryable: true,
        userMessage: '网络连接异常，请检查网络设置'
      }
    }
    
    if (error.message.includes('401') || error.message.includes('403')) {
      return {
        category: 'auth',
        severity: 'high',
        retryable: false,
        userMessage: '认证失败，请重新登录'
      }
    }
    
    if (error.message.includes('500')) {
      return {
        category: 'server',
        severity: 'high',
        retryable: true,
        userMessage: '服务器异常，请稍后重试'
      }
    }
    
    return {
      category: 'unknown',
      severity: 'medium',
      retryable: false,
      userMessage: '发生未知错误，请联系技术支持'
    }
  }
  
  // 智能错误处理
  async handleError(error, context = {}) {
    const errorInfo = this.categorizeError(error)
    
    console.log('🚨 错误处理:', errorInfo)
    
    // 记录错误
    this.recordError(error, errorInfo, context)
    
    // 根据错误类型采取相应措施
    switch (errorInfo.category) {
      case 'timeout':
      case 'network':
        if (errorInfo.retryable) {
          // 自动重试
          return await this.autoRetryAfterError(context)
        }
        break
        
      case 'auth':
        // 尝试刷新认证
        return await this.refreshAuthentication()
        
      case 'server':
        // 等待后重试
        await this.sleep(2000)
        if (errorInfo.retryable) {
          return await this.autoRetryAfterError(context)
        }
        break
    }
    
    return {
      success: false,
      error: errorInfo,
      fallback: true
    }
  }
  
  // 记录错误
  recordError(error, errorInfo, context) {
    const errorRecord = {
      error: error.message,
      category: errorInfo.category,
      severity: errorInfo.severity,
      context,
      timestamp: Date.now(),
      stackTrace: error.stack
    }
    
    try {
      const errorLog = uni.getStorageSync('ai_service_errors') || []
      errorLog.unshift(errorRecord)
      
      // 保留最近50条错误记录
      const trimmedLog = errorLog.slice(0, 50)
      uni.setStorageSync('ai_service_errors', trimmedLog)
    } catch (logError) {
      console.error('错误记录失败:', logError)
    }
  }
  
  // 错误后自动重试
  async autoRetryAfterError(context) {
    console.log('🔄 错误后自动重试...')
    
    try {
      // 清理可能有问题的缓存
      this.clearAllCache()
      
      // 等待一段时间
      await this.sleep(1000)
      
      // 执行健康检查
      const health = await this.performHealthCheck()
      
      if (health.status === 'healthy') {
        console.log('✅ 自动重试成功')
        return { success: true, retried: true }
      } else {
        console.log('❌ 自动重试失败')
        return { success: false, retried: true }
      }
      
    } catch (retryError) {
      console.error('自动重试异常:', retryError)
      return { success: false, retried: true, error: retryError.message }
    }
  }
  
  // 刷新认证
  async refreshAuthentication() {
    console.log('🔑 尝试刷新认证...')
    
    try {
      // 这里应该实现认证刷新逻辑
      // 暂时返回需要重新登录的提示
      return {
        success: false,
        needRelogin: true,
        message: '认证已过期，请重新登录'
      }
    } catch (error) {
      console.error('认证刷新失败:', error)
      return {
        success: false,
        error: error.message
      }
    }
  }
  
  // 获取错误统计
  getErrorStats() {
    try {
      const errorLog = uni.getStorageSync('ai_service_errors') || []
      const stats = {
        totalErrors: errorLog.length,
        errorsByCategory: {},
        errorsBySeverity: {},
        recentErrors: errorLog.slice(0, 5)
      }
      
      errorLog.forEach(error => {
        stats.errorsByCategory[error.category] = 
          (stats.errorsByCategory[error.category] || 0) + 1
        stats.errorsBySeverity[error.severity] = 
          (stats.errorsBySeverity[error.severity] || 0) + 1
      })
      
      return stats
    } catch (error) {
      console.error('获取错误统计失败:', error)
      return { totalErrors: 0, errorsByCategory: {}, errorsBySeverity: {} }
    }
  }
}

export default new EnhancedAIService()检查缓存
      if (options.useCache !== false && this.cache.has(cacheKey)) {
        const cached = this.cache.get(cacheKey)
        if (Date.now() - cached.timestamp < 30000) { // 30秒缓存
          this.performanceMetrics.cacheHits++
          return cached.data
        }
      }
      
      const startTime = Date.now()
      const token = uni.getStorageSync('xm-user')?.token
      
      const response = await this.makeRequest({
        url: `${this.baseUrl}/session/list`,
        method: 'GET',
        header: { 'token': token },
        timeout: options.timeout || 10000
      })
      
      if (response.statusCode === 200) {
        const sessions = response.data.sessions || []
        
        // 缓存结果
        this.cache.set(cacheKey, {
          data: sessions,
          timestamp: Date.now()
        })
        
        this.recordRequestSuccess(Date.now() - startTime)
        return sessions
      }
      
      throw new Error(`HTTP ${response.statusCode}: ${response.data?.message || 'Unknown error'}`)
      
    } catch (error) {
      console.error('获取会话列表失败:', error)
      this.recordRequestFailure()
      
      // 尝试从缓存返回旧数据
      if (this.cache.has(cacheKey)) {
        console.log('使用缓存的会话数据')
        return this.cache.get(cacheKey).data
      }
      
      return []
    }
  }
  
  // 增强的会话历史获取
  async getSessionHistory(sessionId, page = 1, pageSize = 10, options = {}) {
    const cacheKey = `history_${sessionId}_${page}_${pageSize}`
    
    try {
      // 检查缓存
      if (options.useCache !== false && this.cache.has(cacheKey)) {
        const cached = this.cache.get(cacheKey)
        if (Date.now() - cached.timestamp < 60000) { // 1分钟缓存
          this.performanceMetrics.cacheHits++
          return cached.data
        }
      }
      
      const startTime = Date.now()
      const token = uni.getStorageSync('xm-user')?.token
      
      const response = await this.makeRequest({
        url: `${this.baseUrl}/session/${sessionId}/history`,
        method: 'GET',
        header: { 'token': token },
        data: { page, page_size: pageSize },
        timeout: options.timeout || 15000
      })
      
      if (response.statusCode === 200) {
        const history = response.data.history || []
        
        // 缓存结果
        this.cache.set(cacheKey, {
          data: history,
          timestamp: Date.now()
        })
        
        this.recordRequestSuccess(Date.now() - startTime)
        return history
      }
      
      throw new Error(`HTTP ${response.statusCode}: ${response.data?.message || 'Unknown error'}`)
      
    } catch (error) {
      console.error('获取历史消息失败:', error)
      this.recordRequestFailure()
      
      // 尝试从缓存返回数据
      if (this.cache.has(cacheKey)) {
        console.log('使用缓存的历史数据')
        return this.cache.get(cacheKey).data
      }
      
      return []
    }
  }
  
  // 删除会话（带确认和恢复）
  async deleteSession(sessionId, options = {}) {
    try {
      const startTime = Date.now()
      const token = uni.getStorageSync('xm-user')?.token
      
      // 在删除前备份会话信息（如果需要的话）
      if (options.backup) {
        await this.backupSession(sessionId)
      }
      
      const response = await this.makeRequest({
        url: `${this.baseUrl}/session/${sessionId}`,
        method: 'DELETE',
        header: { 'token': token },
        timeout: options.timeout || 10000
      })
      
      if (response.statusCode === 200) {
        // 清除相关缓存
        this.clearSessionCache(sessionId)
        this.recordRequestSuccess(Date.now() - startTime)
        return true
      }
      
      throw new Error(`HTTP ${response.statusCode}: ${response.data?.message || 'Delete failed'}`)
      
    } catch (error) {
      console.error('删除会话失败:', error)
      this.recordRequestFailure()
      return false
    }
  }
  
  // 备份会话
  async backupSession(sessionId) {
    try {
      const history = await this.getSessionHistory(sessionId, 1, 100, { useCache: false })
      const backup = {
        sessionId,
        history,
        timestamp: Date.now()
      }
      
      const backups = uni.getStorageSync('session_backups') || []
      backups.unshift(backup)
      
      // 保留最近10个备份
      const backupsToSave = backups.slice(0, 10)
      uni.setStorageSync('session_backups', backupsToSave)
      
      console.log('会话已备份:', sessionId)
    } catch (error) {
      console.error('备份会话失败:', error)
    }
  }
  
  // 智能聊天接口（支持意图上下文）
  async chatWithAI(message, context = {}, options = {}) {
    try {
      const startTime = Date.now()
      const token = uni.getStorageSync('xm-user')?.token
      
      // 构建增强的请求数据
      const requestData = {
        message,
        context: this.enhanceContext(context),
        timestamp: Date.now(),
        requestId: this.generateRequestId(),
        clientInfo: this.getClientInfo()
      }
      
      // 如果有意图分析结果，添加到请求中
      if (context.intentAnalysis) {
        requestData.intentHint = {
          recognizedIntent: context.intentAnalysis.recognizedIntent,
          confidence: context.intentAnalysis.confidence,
          suggestedAction: context.intentAnalysis.suggestedAction
        }
      }
      
      const response = await this.makeRequest({
        url: `${this.baseUrl}/chat`,
        method: 'POST',
        header: {
          'token': token,
          'Content-Type': 'application/json'
        },
        data: requestData,
        timeout: options.timeout || 30000
      })
      
      if (response.statusCode === 200) {
        this.recordRequestSuccess(Date.now() - startTime)
        return this.processAIResponse(response.data, context)
      }
      
      throw new Error(`HTTP ${response.statusCode}: ${response.data?.message || 'AI service error'}`)
      
    } catch (error) {
      console.error('AI服务调用失败:', error)
      this.recordRequestFailure()
      
      // 返回降级响应
      return this.getFallbackResponse(message, context)
    }
  }
  
  // 增强上下文信息
  enhanceContext(context) {
    return {
      ...context,
      deviceInfo: {
        platform: uni.getSystemInfoSync().platform,
        version: uni.getSystemInfoSync().version,
        screenWidth: uni.getSystemInfoSync().screenWidth,
        screenHeight: uni.getSystemInfoSync().screenHeight
      },
      appInfo: {
        version: '1.0.0', // 应用版本
        environment: 'production', // 环境
        features: ['health', 'sport', 'food', 'sleep', 'blog'] // 可用功能
      },
      sessionInfo: {
        startTime: context.sessionStart || Date.now(),
        messageCount: context.messageCount || 0,
        lastActivity: Date.now()
      }
    }
  }
  
  // 处理AI响应
  processAIResponse(response, context) {
    const processed = {
      success: true,
      message: response.message || response.answer || '',
      actions: response.actions || [],
      suggestions: response.suggestions || [],
      metadata: {
        responseTime: response.responseTime,
        model: response.model,
        confidence: response.confidence
      }
    }
    
    // 如果AI回复包含意图信息，进行处理
    if (response.detectedIntent) {
      processed.detectedIntent = response.detectedIntent
    }
    
    // 如果AI回复包含推荐操作，转换为标准格式
    if (response.recommendedActions) {
      processed.actions = response.recommendedActions.map(action => ({
        type: 'navigate',
        text: action.text,
        page: action.page,
        isTabBar: action.isTabBar || false,
        description: action.description
      }))
    }
    
    return processed
  }
  
  // 获取降级响应
  getFallbackResponse(message, context) {
    const fallbackResponses = [
      {
        trigger: ['健康', '管理'],
        response: '抱歉服务暂时不可用，您可以点击下方按钮进入健康管理页面。',
        actions: [{
          type: 'navigate',
          text: '进入健康管理',
          page: '/pages/health/health',
          isTabBar: true
        }]
      },
      {
        trigger: ['运动', '锻炼'],
        response: '网络连接异常，建议您直接进入运动记录页面。',
        actions: [{
          type: 'navigate',
          text: '进入运动记录',
          page: '/pages/sport/sport',
          isTabBar: false
        }]
      },
      {
        trigger: ['饮食', '吃饭'],
        response: '系统繁忙，您可以直接进入饮食记录页面。',
        actions: [{
          type: 'navigate',
          text: '进入饮食记录',
          page: '/pages/food/food1',
          isTabBar: false
        }]
      }
    ]
    
    // 尝试匹配降级响应
    for (const fallback of fallbackResponses) {
      if (fallback.trigger.some(keyword => message.includes(keyword))) {
        return {
          success: true,
          message: fallback.response,
          actions: fallback.actions,
          fallback: true
        }
      }
    }
    
    // 默认降级响应
    return {
      success: false,
      message: '抱歉，AI服务暂时不可用，请稍后重试或手动选择功能。',
      actions: [{
        type: 'navigate',
        text: '返回首页',
        page: '/pages/index/index',
        isTabBar: true
      }],
      fallback: true
    }
  }
  
  // 带重试的网络请求
  async makeRequest(config) {
    this.performanceMetrics.totalRequests++
    
    for (let attempt = 0; attempt <= this.retryConfig.maxRetries; attempt++) {
      try {
        return await this.executeRequest(config)
      } catch (error) {
        console.log(`请求失败 (尝试 ${attempt + 1}/${this.retryConfig.maxRetries + 1}):`, error.message)
        
        if (attempt === this.retryConfig.maxRetries) {
          throw error
        }
        
        // 计算重试延迟
        const delay = this.retryConfig.retryDelay * Math.pow(this.retryConfig.backoffFactor, attempt)
        await this.sleep(delay)
      }
    }
  }
  
  // 执行网络请求
  executeRequest(config) {
    return new Promise((resolve, reject) => {
      uni.request({
        ...config,
        success: resolve,
        fail: reject
      })
    })
  }
  
  // 休眠函数
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
  
  // 更新会话标题（带缓存更新）
  async updateSessionTitle(sessionId, title, options = {}) {
    try {
      const startTime = Date.now()
      const token = uni.getStorageSync('xm-user')?.token
      
      const response = await this.makeRequest({
        url: `${this.baseUrl}/session/${sessionId}/title`,
        method: 'PUT',
        header: {
          'token': token,
          'Content-Type': 'application/json'
        },
        data: { title },
        timeout: options.timeout || 10000
      })
      
      if (response.statusCode === 200) {
        // 更新缓存中的会话标题
        this.updateSessionTitleInCache(sessionId, title)
        this.recordRequestSuccess(Date.now() - startTime)
        return true
      }
      
      throw new Error(`HTTP ${response.statusCode}: ${response.data?.message || 'Update failed'}`)
      
    } catch (error) {
      console.error('更新会话标题失败:', error)
      this.recordRequestFailure()
      return false
    }
  }
  
  // 更新缓存中的会话标题
  updateSessionTitleInCache(sessionId, newTitle) {
    const cacheKey = 'sessions_list'
    if (this.cache.has(cacheKey)) {
      const cached = this.cache.get(cacheKey)
      const sessions = cached.data
      const sessionIndex = sessions.findIndex(s => s.id === sessionId)
      
      if (sessionIndex !== -1) {
        sessions[sessionIndex].title = newTitle
        this.cache.set(cacheKey, {
          data: sessions,
          timestamp: cached.timestamp
        })
      }
    }
  }
  
  // 清除会话相关缓存
  clearSessionCache(sessionId) {
    const keysToDelete = []
    
    for (const key of this.cache.keys()) {
      if (key.includes(sessionId)) {
        keysToDelete.push(key)
      }
    }
    
    keysToDelete.forEach(key => this.cache.delete(key))
    
    // 清除会话列表缓存以强制刷新
    this.cache.delete('sessions_list')
  }
  
  // 清除所有缓存
  clearAllCache() {
    this.cache.clear()
    console.log('所有AI服务缓存已清除')
  }
  
  // 生成请求ID
  generateRequestId() {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }
  
  // 获取客户端信息
  getClientInfo() {
    try {
      const systemInfo = uni.getSystemInfoSync()
      return {
        platform: systemInfo.platform,
        version: systemInfo.version,
        model: systemInfo.model,
        brand: systemInfo.brand,
        screenWidth: systemInfo.screenWidth,
        screenHeight: systemInfo.screenHeight
      }
    } catch (error) {
      return { platform: 'unknown' }
    }
  }
  
  // 记录请求成功
  recordRequestSuccess(responseTime) {
    this.performanceMetrics.successfulRequests++
    this.updateAverageResponseTime(responseTime)
  }
  
  // 记录请求失败
  recordRequestFailure() {
    this.performanceMetrics.failedRequests++
  }
  
  // 更新平均响应时间
  updateAverageResponseTime(responseTime) {
    const total = this.performanceMetrics.successfulRequests
    const current = this.performanceMetrics.averageResponseTime
    this.performanceMetrics.averageResponseTime = 
      ((current * (total - 1)) + responseTime) / total
  }
  
  // 获取性能统计
  getPerformanceStats() {
    return {
      ...this.performanceMetrics,
      successRate: this.performanceMetrics.successfulRequests / 
        (this.performanceMetrics.successfulRequests + this.performanceMetrics.failedRequests) || 0,
      cacheHitRate: this.performanceMetrics.cacheHits / this.performanceMetrics.totalRequests || 0,
      cacheSize: this.cache.size
    }
  }
  
  // 健康检查
  async performHealthCheck() {
    try {
      const startTime = Date.now()
      const response = await this.makeRequest({
        url: `${this.baseUrl}/health`,
        method: 'GET',
        timeout: 5000
      })
      
      const responseTime = Date.now() - startTime
      
      return {
        status: response.statusCode === 200 ? 'healthy' : 'unhealthy',
        responseTime,
        timestamp: Date.now(),
        serverInfo: response.data || {}
      }
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
        timestamp: Date.now()
      }
    }
  }
  
  // 服务监控
  async monitorService() {
    const healthCheck = await this.performHealthCheck()
    const performance = this.getPerformanceStats()
    
    return {
      health: healthCheck,
      performance,
      cache: {
        size: this.cache.size,
        hitRate: performance.cacheHitRate
      },
      timestamp: Date.now()
    }
  }
  
  // 智能重连
  async intelligentReconnect() {
    console.log('🔄 开始智能重连...')
    
    // 清除缓存
    this.clearAllCache()
    
    // 重置性能指标
    this.performanceMetrics = {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      averageResponseTime: 0,
      cacheHits: 0
    }
    
    //