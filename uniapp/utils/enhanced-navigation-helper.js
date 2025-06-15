// utils/enhanced-navigation-helper.js - 增强版导航助手
import { featureMapping, pageRelations } from '@/config/feature-mapping.js'

class EnhancedNavigationHelper {
  constructor() {
    this.navigationHistory = []
    this.performanceMetrics = {
      successfulNavigations: 0,
      failedNavigations: 0,
      averageNavigationTime: 0
    }
    this.loadNavigationHistory()
  }
  
  // 智能路由建议
  getSmartRouteRecommendations(currentContext) {
    const recommendations = []
    const currentTime = new Date()
    const hour = currentTime.getHours()
    
    // 基于时间的推荐
    if (hour >= 6 && hour <= 9) {
      recommendations.push({
        page: '/pages/food/food1',
        reason: '早餐时间，建议记录饮食',
        priority: 0.9,
        timeRelevant: true
      })
    } else if (hour >= 11 && hour <= 14) {
      recommendations.push({
        page: '/pages/food/food1',
        reason: '午餐时间，建议记录饮食',
        priority: 0.9,
        timeRelevant: true
      })
    } else if (hour >= 17 && hour <= 20) {
      recommendations.push({
        page: '/pages/food/food1',
        reason: '晚餐时间，建议记录饮食',
        priority: 0.9,
        timeRelevant: true
      })
    } else if (hour >= 21 && hour <= 23) {
      recommendations.push({
        page: '/pages/sleep/sleep',
        reason: '准备就寝，建议记录睡眠',
        priority: 0.8,
        timeRelevant: true
      })
    }
    
    // 基于使用频率的推荐
    const frequentPages = this.getFrequentlyVisitedPages()
    frequentPages.forEach(pageInfo => {
      if (!recommendations.find(r => r.page === pageInfo.page)) {
        recommendations.push({
          page: pageInfo.page,
          reason: `您经常使用此功能`,
          priority: 0.6,
          frequencyBased: true,
          visitCount: pageInfo.count
        })
      }
    })
    
    // 基于当前页面的推荐
    if (currentContext.currentPage) {
      const relatedPages = this.getRelatedPages(currentContext.currentPage)
      relatedPages.forEach(related => {
        if (!recommendations.find(r => r.page === related.page)) {
          recommendations.push({
            page: related.page,
            reason: `与当前页面相关`,
            priority: 0.5,
            contextBased: true
          })
        }
      })
    }
    
    return recommendations
      .sort((a, b) => b.priority - a.priority)
      .slice(0, 5)
  }
  
  // 获取经常访问的页面
  getFrequentlyVisitedPages() {
    const pageCount = {}
    
    this.navigationHistory
      .filter(nav => nav.type === 'success')
      .forEach(nav => {
        pageCount[nav.page] = (pageCount[nav.page] || 0) + 1
      })
    
    return Object.entries(pageCount)
      .map(([page, count]) => ({ page, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 3)
  }
  
  // 导航性能监控
  monitorNavigationPerformance() {
    const stats = this.getNavigationStats()
    
    // 如果成功率过低，记录警告
    if (stats.successRate < 0.8 && stats.totalNavigations > 10) {
      console.warn('⚠️ 导航成功率较低:', stats.successRate)
    }
    
    // 如果平均导航时间过长，记录警告
    if (stats.averageNavigationTime > 1000) {
      console.warn('⚠️ 平均导航时间过长:', stats.averageNavigationTime)
    }
    
    return stats
  }
  
  // 导航缓存管理
  manageNavigationCache() {
    const cacheKey = 'nav_cache'
    
    try {
      const cache = uni.getStorageSync(cacheKey) || {}
      const now = Date.now()
      
      // 清理过期缓存（24小时）
      Object.keys(cache).forEach(key => {
        if (now - cache[key].timestamp > 24 * 60 * 60 * 1000) {
          delete cache[key]
        }
      })
      
      uni.setStorageSync(cacheKey, cache)
    } catch (error) {
      console.error('导航缓存管理失败:', error)
    }
  }
  
  // 导航意图学习
  learnFromNavigationPattern(userInput, intentResult, navigationResult) {
    const pattern = {
      input: userInput,
      intent: intentResult.intent,
      confidence: intentResult.confidence,
      navigationSuccess: navigationResult.success,
      timestamp: Date.now(),
      context: this.getCurrentPageInfo()
    }
    
    // 存储学习模式（可用于后续优化）
    try {
      const patterns = uni.getStorageSync('nav_patterns') || []
      patterns.unshift(pattern)
      
      // 保留最近1000条模式
      const patternsToSave = patterns.slice(0, 1000)
      uni.setStorageSync('nav_patterns', patternsToSave)
    } catch (error) {
      console.error('导航模式学习失败:', error)
    }
  }
  
  // A/B测试支持
  getNavigationVariant(feature) {
    const variants = {
      animation: ['slide', 'fade', 'zoom'],
      timing: ['fast', 'normal', 'slow'],
      feedback: ['toast', 'modal', 'inline']
    }
    
    const userVariant = uni.getStorageSync('nav_variant') || {}
    
    if (!userVariant[feature] && variants[feature]) {
      // 随机分配变体
      const options = variants[feature]
      userVariant[feature] = options[Math.floor(Math.random() * options.length)]
      uni.setStorageSync('nav_variant', userVariant)
    }
    
    return userVariant[feature]
  }
  
  // 导航错误恢复
  recoverFromNavigationError(error, context) {
    console.log('🔧 尝试从导航错误中恢复:', error)
    
    const recoveryStrategies = [
      // 策略1：清理并重试
      async () => {
        console.log('策略1: 清理并重试')
        await this.clearNavigationCache()
        return await this.switchTab('/pages/index/index')
      },
      
      // 策略2：使用替代路由
      async () => {
        console.log('策略2: 使用替代路由')
        const alternatives = ['/pages/health/health', '/pages/index/index']
        for (const alt of alternatives) {
          try {
            return await this.switchTab(alt)
          } catch (e) {
            continue
          }
        }
        throw new Error('所有替代路由都失败')
      },
      
      // 策略3：重新启动应用
      async () => {
        console.log('策略3: 重新启动应用')
        return await this.reLaunch('/pages/index/index')
      }
    ]
    
    // 按序尝试恢复策略
    return this.tryRecoveryStrategies(recoveryStrategies)
  }
  
  // 尝试恢复策略
  async tryRecoveryStrategies(strategies) {
    for (let i = 0; i < strategies.length; i++) {
      try {
        const result = await strategies[i]()
        console.log(`✅ 恢复策略${i + 1}成功`)
        return result
      } catch (error) {
        console.log(`❌ 恢复策略${i + 1}失败:`, error)
        if (i === strategies.length - 1) {
          throw new Error('所有恢复策略都失败')
        }
      }
    }
  }
  
  // 清理导航缓存
  clearNavigationCache() {
    try {
      uni.removeStorageSync('nav_cache')
      uni.removeStorageSync('nav_params')
      console.log('✅ 导航缓存已清理')
    } catch (error) {
      console.error('清理导航缓存失败:', error)
    }
  }
  
  // 导航健康检查
  performHealthCheck() {
    const healthStatus = {
      timestamp: Date.now(),
      cacheStatus: 'unknown',
      storageStatus: 'unknown',
      navigationStatus: 'unknown',
      errors: []
    }
    
    try {
      // 检查缓存状态
      const cache = uni.getStorageSync('nav_cache')
      healthStatus.cacheStatus = cache ? 'healthy' : 'empty'
    } catch (error) {
      healthStatus.cacheStatus = 'error'
      healthStatus.errors.push('Cache check failed')
    }
    
    try {
      // 检查存储状态
      const testKey = 'nav_health_test'
      uni.setStorageSync(testKey, 'test')
      uni.removeStorageSync(testKey)
      healthStatus.storageStatus = 'healthy'
    } catch (error) {
      healthStatus.storageStatus = 'error'
      healthStatus.errors.push('Storage check failed')
    }
    
    try {
      // 检查导航状态
      const currentPage = this.getCurrentPageInfo()
      healthStatus.navigationStatus = currentPage ? 'healthy' : 'error'
    } catch (error) {
      healthStatus.navigationStatus = 'error'
      healthStatus.errors.push('Navigation check failed')
    }
    
    return healthStatus
  }
  
  // 导航分析报告
  generateNavigationReport() {
    const stats = this.getNavigationStats()
    const healthStatus = this.performHealthCheck()
    const recommendations = this.getSmartRouteRecommendations({})
    
    return {
      summary: {
        totalNavigations: stats.totalNavigations,
        successRate: Math.round(stats.successRate * 100),
        averageTime: Math.round(stats.averageNavigationTime),
        healthStatus: healthStatus.navigationStatus
      },
      performance: {
        successfulNavigations: stats.successfulNavigations,
        failedNavigations: stats.failedNavigations,
        averageNavigationTime: stats.averageNavigationTime
      },
      health: healthStatus,
      recommendations: recommendations.slice(0, 3),
      recentActivity: stats.recentHistory.slice(0, 5),
      generatedAt: new Date().toISOString()
    }
  }
}

export default new EnhancedNavigationHelper()能导航到指定页面
  async smartNavigateToPage(intentResult, context = {}) {
    const startTime = Date.now()
    
    try {
      console.log('🚀 开始智能导航:', intentResult)
      
      // 验证意图结果
      if (!this.validateIntentResult(intentResult)) {
        throw new Error('Invalid intent result')
      }
      
      const { pageConfig, action, parameters } = intentResult
      const navigationStrategy = this.determineNavigationStrategy(pageConfig, action, context)
      
      console.log('📋 导航策略:', navigationStrategy)
      
      // 执行导航
      const result = await this.executeNavigation(navigationStrategy, parameters)
      
      // 记录成功导航
      this.recordNavigationSuccess(intentResult, Date.now() - startTime)
      
      return {
        success: true,
        message: `已为您${result.action}${pageConfig.description}`,
        navigationTime: Date.now() - startTime,
        strategy: navigationStrategy.type
      }
      
    } catch (error) {
      console.error('❌ 智能导航失败:', error)
      
      // 记录失败导航
      this.recordNavigationFailure(intentResult, error, Date.now() - startTime)
      
      // 尝试降级策略
      const fallbackResult = await this.tryFallbackNavigation(intentResult, context)
      
      return fallbackResult || {
        success: false,
        message: '导航失败，请手动前往该页面',
        error: error.message
      }
    }
  }
  
  // 确定导航策略
  determineNavigationStrategy(pageConfig, action, context) {
    const strategies = {
      // 直接导航策略
      direct: {
        type: 'direct',
        method: pageConfig.tabBar ? 'switchTab' : 'navigateTo',
        page: pageConfig.page,
        priority: 1.0
      },
      
      // 参数化导航策略
      parameterized: {
        type: 'parameterized',
        method: 'navigateTo',
        page: pageConfig.page,
        priority: 0.9
      },
      
      // 重定向策略
      redirect: {
        type: 'redirect',
        method: 'redirectTo',
        page: pageConfig.page,
        priority: 0.7
      },
      
      // 重启策略
      relaunch: {
        type: 'relaunch',
        method: 'reLaunch',
        page: pageConfig.page,
        priority: 0.5
      }
    }
    
    // 根据当前上下文选择最佳策略
    if (context.currentPage === pageConfig.page) {
      // 当前已在目标页面，可能需要刷新或传递参数
      return strategies.parameterized
    }
    
    if (action?.parameters && Object.keys(action.parameters).length > 0) {
      // 有参数需要传递
      return strategies.parameterized
    }
    
    if (pageConfig.tabBar) {
      // TabBar页面优先使用直接导航
      return strategies.direct
    }
    
    // 默认使用直接导航
    return strategies.direct
  }
  
  // 执行导航
  async executeNavigation(strategy, parameters = {}) {
    const { method, page, type } = strategy
    
    switch (method) {
      case 'switchTab':
        return await this.switchTab(page)
        
      case 'navigateTo':
        return await this.navigateTo(page, parameters)
        
      case 'redirectTo':
        return await this.redirectTo(page, parameters)
        
      case 'reLaunch':
        return await this.reLaunch(page, parameters)
        
      default:
        throw new Error(`Unknown navigation method: ${method}`)
    }
  }
  
  // 切换TabBar页面
  async switchTab(url) {
    return new Promise((resolve, reject) => {
      uni.switchTab({
        url: url,
        success: (result) => {
          resolve({ action: '跳转到', method: 'switchTab', result })
        },
        fail: reject
      })
    })
  }
  
  // 导航到普通页面
  async navigateTo(url, params = {}) {
    return new Promise((resolve, reject) => {
      // 智能参数处理
      const processedParams = this.processNavigationParams(params)
      const queryString = this.buildQueryString(processedParams)
      const fullUrl = queryString ? `${url}?${queryString}` : url
      
      // URL长度检查和优化
      if (fullUrl.length > 1024) {
        return this.handleLongUrl(url, processedParams, resolve, reject)
      }
      
      uni.navigateTo({
        url: fullUrl,
        success: (result) => {
          resolve({ action: '进入', method: 'navigateTo', result })
        },
        fail: reject
      })
    })
  }
  
  // 重定向页面
  async redirectTo(url, params = {}) {
    return new Promise((resolve, reject) => {
      const processedParams = this.processNavigationParams(params)
      const queryString = this.buildQueryString(processedParams)
      const fullUrl = queryString ? `${url}?${queryString}` : url
      
      uni.redirectTo({
        url: fullUrl,
        success: (result) => {
          resolve({ action: '重定向到', method: 'redirectTo', result })
        },
        fail: reject
      })
    })
  }
  
  // 重新启动到指定页面
  async reLaunch(url, params = {}) {
    return new Promise((resolve, reject) => {
      const processedParams = this.processNavigationParams(params)
      const queryString = this.buildQueryString(processedParams)
      const fullUrl = queryString ? `${url}?${queryString}` : url
      
      uni.reLaunch({
        url: fullUrl,
        success: (result) => {
          resolve({ action: '重启到', method: 'reLaunch', result })
        },
        fail: reject
      })
    })
  }
  
  // 处理长URL
  handleLongUrl(url, params, resolve, reject) {
    const paramKey = `nav_params_${Date.now()}`
    
    try {
      uni.setStorageSync(paramKey, params)
      
      uni.navigateTo({
        url: `${url}?_paramKey=${paramKey}`,
        success: (result) => {
          resolve({ action: '进入', method: 'navigateTo_storage', result })
        },
        fail: reject
      })
    } catch (storageError) {
      reject(new Error(`Storage failed: ${storageError.message}`))
    }
  }
  
  // 处理导航参数
  processNavigationParams(params) {
    const processed = {}
    
    Object.entries(params).forEach(([key, value]) => {
      // 类型转换和验证
      if (value !== null && value !== undefined) {
        if (typeof value === 'object') {
          processed[key] = JSON.stringify(value)
        } else {
          processed[key] = String(value)
        }
      }
    })
    
    return processed
  }
  
  // 构建查询字符串
  buildQueryString(params) {
    return Object.entries(params)
      .filter(([key, value]) => value !== null && value !== undefined)
      .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
      .join('&')
  }
  
  // 验证意图结果
  validateIntentResult(intentResult) {
    if (!intentResult) return false
    if (!intentResult.pageConfig) return false
    if (!intentResult.pageConfig.page) return false
    
    // 检查页面是否有效
    return this.isValidPage(intentResult.pageConfig.page)
  }
  
  // 检查页面有效性
  isValidPage(page) {
    const validPages = Object.values(featureMapping).map(config => config.page)
    return validPages.includes(page)
  }
  
  // 尝试降级导航
  async tryFallbackNavigation(intentResult, context) {
    console.log('🔄 尝试降级导航策略')
    
    try {
      // 策略1：尝试相关页面
      const relatedPages = this.getRelatedPages(intentResult.intent, context)
      if (relatedPages.length > 0) {
        const fallbackPage = relatedPages[0]
        const result = await this.navigateTo(fallbackPage.page)
        return {
          success: true,
          message: `已为您跳转到相关功能：${fallbackPage.description}`,
          fallback: true
        }
      }
      
      // 策略2：返回首页
      const result = await this.switchTab('/pages/index/index')
      return {
        success: true,
        message: '已为您返回首页，请手动选择功能',
        fallback: true
      }
      
    } catch (error) {
      console.error('降级导航也失败了:', error)
      return null
    }
  }
  
  // 获取相关页面
  getRelatedPages(intent, context) {
    const relatedPages = []
    
    // 基于功能映射查找相关页面
    const currentFeature = featureMapping[intent]
    if (currentFeature && currentFeature.relatedFeatures) {
      currentFeature.relatedFeatures.forEach(relatedIntent => {
        const relatedFeature = featureMapping[relatedIntent]
        if (relatedFeature) {
          relatedPages.push(relatedFeature)
        }
      })
    }
    
    // 基于页面关系查找
    if (context.currentPage && pageRelations[context.currentPage]) {
      pageRelations[context.currentPage].related.forEach(relatedPage => {
        const feature = Object.values(featureMapping).find(f => f.page === relatedPage)
        if (feature) {
          relatedPages.push(feature)
        }
      })
    }
    
    return relatedPages.slice(0, 3) // 最多返回3个相关页面
  }
  
  // 返回上一页（增强版）
  async goBack(delta = 1, options = {}) {
    try {
      const pages = getCurrentPages()
      
      if (pages.length <= delta) {
        // 如果没有足够的历史页面，跳转到首页
        return await this.switchTab('/pages/index/index')
      }
      
      return new Promise((resolve, reject) => {
        uni.navigateBack({
          delta,
          success: resolve,
          fail: reject
        })
      })
      
    } catch (error) {
      console.error('返回操作失败:', error)
      throw error
    }
  }
  
  // 获取当前页面信息（增强版）
  getCurrentPageInfo() {
    const pages = getCurrentPages()
    if (pages.length === 0) return null
    
    const currentPage = pages[pages.length - 1]
    const previousPage = pages.length > 1 ? pages[pages.length - 2] : null
    
    return {
      current: {
        route: currentPage.route,
        options: currentPage.options,
        path: `/${currentPage.route}`,
        fullPath: this.buildFullPath(currentPage.route, currentPage.options)
      },
      previous: previousPage ? {
        route: previousPage.route,
        path: `/${previousPage.route}`
      } : null,
      stackDepth: pages.length,
      canGoBack: pages.length > 1
    }
  }
  
  // 构建完整路径
  buildFullPath(route, options) {
    if (!options || Object.keys(options).length === 0) {
      return `/${route}`
    }
    
    const queryString = Object.entries(options)
      .map(([key, value]) => `${key}=${value}`)
      .join('&')
    
    return `/${route}?${queryString}`
  }
  
  // 记录导航成功
  recordNavigationSuccess(intentResult, duration) {
    const navigation = {
      type: 'success',
      intent: intentResult.intent,
      page: intentResult.pageConfig.page,
      duration: duration,
      timestamp: Date.now(),
      confidence: intentResult.confidence
    }
    
    this.navigationHistory.unshift(navigation)
    this.performanceMetrics.successfulNavigations++
    this.updateAverageNavigationTime(duration)
    this.saveNavigationHistory()
  }
  
  // 记录导航失败
  recordNavigationFailure(intentResult, error, duration) {
    const navigation = {
      type: 'failure',
      intent: intentResult?.intent || 'unknown',
      page: intentResult?.pageConfig?.page || 'unknown',
      error: error.message,
      duration: duration,
      timestamp: Date.now(),
      confidence: intentResult?.confidence || 0
    }
    
    this.navigationHistory.unshift(navigation)
    this.performanceMetrics.failedNavigations++
    this.saveNavigationHistory()
  }
  
  // 更新平均导航时间
  updateAverageNavigationTime(duration) {
    const total = this.performanceMetrics.successfulNavigations
    const current = this.performanceMetrics.averageNavigationTime
    this.performanceMetrics.averageNavigationTime = 
      ((current * (total - 1)) + duration) / total
  }
  
  // 保存导航历史
  saveNavigationHistory() {
    try {
      // 保留最近100条记录
      const historyToSave = this.navigationHistory.slice(0, 100)
      uni.setStorageSync('enhanced_nav_history', {
        history: historyToSave,
        metrics: this.performanceMetrics,
        lastUpdate: Date.now()
      })
    } catch (error) {
      console.error('保存导航历史失败:', error)
    }
  }
  
  // 加载导航历史
  loadNavigationHistory() {
    try {
      const saved = uni.getStorageSync('enhanced_nav_history')
      if (saved && saved.history) {
        this.navigationHistory = saved.history
        this.performanceMetrics = saved.metrics || this.performanceMetrics
      }
    } catch (error) {
      console.error('加载导航历史失败:', error)
    }
  }
  
  // 清除导航历史
  clearNavigationHistory() {
    this.navigationHistory = []
    this.performanceMetrics = {
      successfulNavigations: 0,
      failedNavigations: 0,
      averageNavigationTime: 0
    }
    uni.removeStorageSync('enhanced_nav_history')
  }
  
  // 获取导航统计
  getNavigationStats() {
    return {
      ...this.performanceMetrics,
      totalNavigations: this.performanceMetrics.successfulNavigations + this.performanceMetrics.failedNavigations,
      successRate: this.performanceMetrics.successfulNavigations / 
        (this.performanceMetrics.successfulNavigations + this.performanceMetrics.failedNavigations) || 0,
      recentHistory: this.navigationHistory.slice(0, 10)
    }
  }
  
  // 获取页面参数（增强版）
  getPageParams() {
    const pages = getCurrentPages()
    if (pages.length === 0) return {}
    
    const currentPage = pages[pages.length - 1]
    const options = currentPage.options || {}
    
    // 检查是否有存储的参数
    if (options._paramKey) {
      try {
        const storedParams = uni.getStorageSync(options._paramKey)
        if (storedParams) {
          // 使用后删除存储的参数
          uni.removeStorageSync(options._paramKey)
          return { ...options, ...storedParams }
        }
      } catch (error) {
        console.error('获取存储参数失败:', error)
      }
    }
    
    return options
  }
  
  // 预加载页面
  preloadPage(page) {
    if (typeof uni.preloadPage === 'function') {
      try {
        uni.preloadPage({ url: page })
        console.log('🚀 预加载页面:', page)
      } catch (error) {
        console.error('预加载页面失败:', error)
      }
    }
  }
  
  // 批量预加载相关页面
  preloadRelatedPages(intent) {
    const feature = featureMapping[intent]
    if (feature && feature.relatedFeatures) {
      feature.relatedFeatures.forEach(relatedIntent => {
        const relatedFeature = featureMapping[relatedIntent]
        if (relatedFeature && !relatedFeature.tabBar) {
          // 只预加载非TabBar页面
          setTimeout(() => {
            this.preloadPage(relatedFeature.page)
          }, 100)
        }
      })
    }
  }
  
  // 智