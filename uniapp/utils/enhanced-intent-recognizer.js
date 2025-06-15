// utils/enhanced-intent-recognizer.js - 增强版意图识别器
class EnhancedIntentRecognizer {
  constructor() {
    this.initializeData()
    this.initializeNLP()
  }

  // 初始化数据配置
  initializeData() {
    // 意图分类定义
    this.intentCategories = {
      NAVIGATION: 'navigation',        // 导航类
      RECORD: 'record',               // 记录类
      QUERY: 'query',                 // 查询类
      REMINDER: 'reminder',           // 提醒类
      ANALYSIS: 'analysis',           // 分析类
      GENERAL: 'general'              // 通用类
    }

    // 功能映射配置
    this.featureConfig = {
      health: {
        keywords: ['健康', '管理', '体检', '医疗', '病症', '症状', '诊断'],
        aliases: ['身体健康', '健康状况', '医疗健康'],
        page: '/pages/health/health',
        tabBar: true,
        category: this.intentCategories.NAVIGATION,
        weight: 1.0,
        description: '健康管理功能'
      },
      sport: {
        keywords: ['运动', '锻炼', '健身', '跑步', '游泳', '骑行', '瑜伽', '篮球', '足球', '网球'],
        aliases: ['体育运动', '体育锻炼', '体能训练', '有氧运动'],
        page: '/pages/sport/sport',
        tabBar: false,
        category: this.intentCategories.RECORD,
        weight: 1.0,
        description: '运动记录功能'
      },
      food: {
        keywords: ['饮食', '吃饭', '食物', '营养', '餐饮', '用餐', '进餐', '早餐', '午餐', '晚餐'],
        aliases: ['膳食', '餐食', '饮食管理', '营养管理'],
        page: '/pages/food/food1',
        tabBar: false,
        category: this.intentCategories.RECORD,
        weight: 1.0,
        description: '饮食记录功能'
      },
      sleep: {
        keywords: ['睡眠', '睡觉', '休息', '入睡', '失眠', '安眠', '作息'],
        aliases: ['睡眠管理', '作息管理', '睡眠质量'],
        page: '/pages/sleep/sleep',
        tabBar: false,
        category: this.intentCategories.RECORD,
        weight: 1.0,
        description: '睡眠记录功能'
      },
      body: {
        keywords: ['身体', '体重', '身高', 'BMI', '体脂', '肌肉', '骨量', '基础代谢'],
        aliases: ['身体信息', '体型数据', '身体指标'],
        page: '/pages/index/index',
        tabBar: true,
        category: this.intentCategories.QUERY,
        weight: 1.0,
        description: '身体信息查看'
      },
      blog: {
        keywords: ['博客', '文章', '分享', '日记', '笔记', '心得'],
        aliases: ['健康博客', '文章分享', '健康日记'],
        page: '/pages/blog/blog',
        tabBar: true,
        category: this.intentCategories.NAVIGATION,
        weight: 1.0,
        description: '健康博客功能'
      }
    }

    // 动作词典
    this.actionWords = {
      navigate: ['去', '到', '进入', '打开', '访问', '查看', '浏览'],
      record: ['记录', '添加', '输入', '录入', '保存', '登记', '填写'],
      query: ['查询', '查看', '显示', '获取', '了解', '知道', '看看'],
      update: ['修改', '更新', '编辑', '改变', '调整'],
      delete: ['删除', '移除', '清除', '取消']
    }

    // 时间词典
    this.timeWords = {
      today: ['今天', '今日', '现在', '当前'],
      yesterday: ['昨天', '昨日'],
      tomorrow: ['明天', '明日'],
      thisWeek: ['这周', '本周', '这星期', '本星期'],
      thisMonth: ['这个月', '本月'],
      morning: ['早上', '上午', '晨'],
      afternoon: ['下午', '午后'],
      evening: ['晚上', '傍晚', '黄昏'],
      night: ['夜晚', '深夜', '夜里']
    }

    // 否定词典
    this.negativeWords = ['不', '别', '没', '非', '无', '停止', '取消', '关闭']

    // 疑问词典
    this.questionWords = ['什么', '怎么', '如何', '为什么', '哪里', '哪个', '什么时候', '多少']
  }

  // 初始化NLP处理
  initializeNLP() {
    // 中文分词的简单实现
    this.stopWords = new Set(['的', '了', '在', '是', '我', '你', '他', '她', '它', '们', '这', '那', '有', '和', '或'])
  }

  // 主要意图识别方法
  recognizeIntent(userInput, context = {}) {
    try {
      console.log('🔍 开始意图识别:', userInput)
      
      // 预处理用户输入
      const processedInput = this.preprocessInput(userInput)
      console.log('📝 预处理结果:', processedInput)
      
      // 特征提取
      const features = this.extractFeatures(processedInput, context)
      console.log('🎯 提取特征:', features)
      
      // 规则匹配
      const ruleBasedResult = this.ruleBasedMatching(processedInput, features, context)
      console.log('📋 规则匹配结果:', ruleBasedResult)
      
      // 语义匹配
      const semanticResult = this.semanticMatching(processedInput, features, context)
      console.log('🧠 语义匹配结果:', semanticResult)
      
      // 结果融合
      const finalResult = this.fuseResults([ruleBasedResult, semanticResult], context)
      console.log('✅ 最终识别结果:', finalResult)
      
      return finalResult
    } catch (error) {
      console.error('❌ 意图识别失败:', error)
      return this.createDefaultResult()
    }
  }

  // 预处理用户输入
  preprocessInput(input) {
    const processed = {
      original: input,
      normalized: input.toLowerCase().trim(),
      tokens: [],
      cleanedText: '',
      hasNegation: false,
      hasQuestion: false
    }

    // 去除特殊字符但保留中文
    processed.cleanedText = processed.normalized.replace(/[^\u4e00-\u9fa5a-zA-Z0-9\s]/g, ' ')

    // 简单分词（按字分词，可后续优化）
    processed.tokens = this.simpleTokenize(processed.cleanedText)

    // 检测否定词
    processed.hasNegation = this.negativeWords.some(word => processed.normalized.includes(word))

    // 检测疑问词
    processed.hasQuestion = this.questionWords.some(word => processed.normalized.includes(word))

    return processed
  }

  // 简单分词
  simpleTokenize(text) {
    // 移除停用词并按空格分割
    return text.split(/\s+/)
      .filter(token => token.length > 0 && !this.stopWords.has(token))
      .concat(this.extractChinese(text))
  }

  // 提取中文词汇
  extractChinese(text) {
    const chineseWords = []
    
    // 提取所有关键词
    Object.values(this.featureConfig).forEach(config => {
      config.keywords.forEach(keyword => {
        if (text.includes(keyword)) {
          chineseWords.push(keyword)
        }
      })
      
      if (config.aliases) {
        config.aliases.forEach(alias => {
          if (text.includes(alias)) {
            chineseWords.push(alias)
          }
        })
      }
    })

    return [...new Set(chineseWords)]
  }

  // 特征提取
  extractFeatures(processedInput, context) {
    const features = {
      actionType: this.extractActionType(processedInput),
      timeContext: this.extractTimeContext(processedInput),
      targetFeature: this.extractTargetFeature(processedInput),
      parameters: this.extractParameters(processedInput),
      confidence: 0,
      contextualClues: this.extractContextualClues(context)
    }

    return features
  }

  // 提取动作类型
  extractActionType(processedInput) {
    for (const [action, words] of Object.entries(this.actionWords)) {
      if (words.some(word => processedInput.normalized.includes(word))) {
        return action
      }
    }
    
    // 默认推断
    if (processedInput.hasQuestion) {
      return 'query'
    }
    
    return 'navigate'
  }

  // 提取时间上下文
  extractTimeContext(processedInput) {
    for (const [timeType, words] of Object.entries(this.timeWords)) {
      if (words.some(word => processedInput.normalized.includes(word))) {
        return timeType
      }
    }
    return null
  }

  // 提取目标功能
  extractTargetFeature(processedInput) {
    const matches = []
    
    Object.entries(this.featureConfig).forEach(([feature, config]) => {
      let score = 0
      
      // 关键词匹配
      config.keywords.forEach(keyword => {
        if (processedInput.normalized.includes(keyword)) {
          score += 1
        }
      })
      
      // 别名匹配
      if (config.aliases) {
        config.aliases.forEach(alias => {
          if (processedInput.normalized.includes(alias)) {
            score += 0.8
          }
        })
      }
      
      if (score > 0) {
        matches.push({ feature, score, config })
      }
    })
    
    return matches.sort((a, b) => b.score - a.score)
  }

  // 提取参数
  extractParameters(processedInput) {
    const params = {}
    
    // 提取数字
    const numbers = processedInput.original.match(/\d+/g)
    if (numbers) {
      params.numbers = numbers.map(n => parseInt(n))
    }
    
    // 提取特定模式
    const patterns = {
      weight: /(\d+(?:\.\d+)?)\s*(?:kg|公斤|斤)/i,
      height: /(\d+(?:\.\d+)?)\s*(?:cm|厘米|米)/i,
      time: /(\d{1,2}):(\d{2})/g
    }
    
    Object.entries(patterns).forEach(([key, pattern]) => {
      const match = processedInput.original.match(pattern)
      if (match) {
        params[key] = match[1]
      }
    })
    
    return params
  }

  // 提取上下文线索
  extractContextualClues(context) {
    return {
      currentPage: context.currentPage || null,
      timeOfDay: this.getTimeOfDay(),
      userHistory: context.userHistory || [],
      lastAction: context.lastAction || null
    }
  }

  // 规则匹配
  ruleBasedMatching(processedInput, features, context) {
    const results = []
    
    // 直接功能匹配
    if (features.targetFeature && features.targetFeature.length > 0) {
      const topMatch = features.targetFeature[0]
      
      const confidence = this.calculateRuleConfidence(
        topMatch.score,
        features.actionType,
        features.timeContext,
        context
      )
      
      results.push({
        type: 'rule_based',
        intent: topMatch.feature,
        confidence: confidence,
        action: this.determineAction(features.actionType, topMatch.config),
        pageConfig: topMatch.config,
        parameters: features.parameters,
        reason: '基于关键词直接匹配'
      })
    }
    
    // 上下文匹配
    const contextualMatch = this.matchByContext(processedInput, context)
    if (contextualMatch) {
      results.push(contextualMatch)
    }
    
    return results.sort((a, b) => b.confidence - a.confidence)[0] || null
  }

  // 语义匹配
  semanticMatching(processedInput, features, context) {
    const results = []
    
    // 基于语义相似度的匹配
    Object.entries(this.featureConfig).forEach(([feature, config]) => {
      const similarity = this.calculateSemanticSimilarity(
        processedInput.tokens,
        [...config.keywords, ...(config.aliases || [])]
      )
      
      if (similarity > 0.3) {
        const confidence = similarity * 0.8 + (features.contextualClues.currentPage === config.page ? 0.2 : 0)
        
        results.push({
          type: 'semantic',
          intent: feature,
          confidence: confidence,
          action: this.determineAction(features.actionType, config),
          pageConfig: config,
          parameters: features.parameters,
          reason: '基于语义相似度匹配'
        })
      }
    })
    
    return results.sort((a, b) => b.confidence - a.confidence)[0] || null
  }

  // 计算语义相似度
  calculateSemanticSimilarity(tokens, keywords) {
    if (tokens.length === 0 || keywords.length === 0) return 0
    
    let totalSimilarity = 0
    let maxSimilarity = 0
    
    tokens.forEach(token => {
      keywords.forEach(keyword => {
        const similarity = this.stringSimilarity(token, keyword)
        maxSimilarity = Math.max(maxSimilarity, similarity)
        totalSimilarity += similarity
      })
    })
    
    // 综合最大相似度和平均相似度
    const avgSimilarity = totalSimilarity / (tokens.length * keywords.length)
    return (maxSimilarity * 0.7 + avgSimilarity * 0.3)
  }

  // 字符串相似度计算
  stringSimilarity(str1, str2) {
    if (str1 === str2) return 1.0
    if (str1.includes(str2) || str2.includes(str1)) return 0.8
    
    const longer = str1.length > str2.length ? str1 : str2
    const shorter = str1.length > str2.length ? str2 : str1
    
    if (longer.length === 0) return 1.0
    
    const editDistance = this.levenshteinDistance(longer, shorter)
    return (longer.length - editDistance) / longer.length
  }

  // 编辑距离
  levenshteinDistance(str1, str2) {
    const matrix = Array(str2.length + 1).fill().map(() => Array(str1.length + 1).fill(0))
    
    for (let i = 0; i <= str1.length; i++) matrix[0][i] = i
    for (let j = 0; j <= str2.length; j++) matrix[j][0] = j
    
    for (let j = 1; j <= str2.length; j++) {
      for (let i = 1; i <= str1.length; i++) {
        const cost = str1[i - 1] === str2[j - 1] ? 0 : 1
        matrix[j][i] = Math.min(
          matrix[j - 1][i] + 1,     // deletion
          matrix[j][i - 1] + 1,     // insertion
          matrix[j - 1][i - 1] + cost // substitution
        )
      }
    }
    
    return matrix[str2.length][str1.length]
  }

  // 结果融合
  fuseResults(results, context) {
    const validResults = results.filter(result => result !== null)
    
    if (validResults.length === 0) {
      return this.createDefaultResult()
    }
    
    if (validResults.length === 1) {
      return validResults[0]
    }
    
    // 多结果融合策略
    const ruleResult = validResults.find(r => r.type === 'rule_based')
    const semanticResult = validResults.find(r => r.type === 'semantic')
    
    if (ruleResult && ruleResult.confidence > 0.7) {
      return ruleResult
    }
    
    if (semanticResult && semanticResult.confidence > 0.6) {
      return semanticResult
    }
    
    // 选择置信度最高的结果
    return validResults.sort((a, b) => b.confidence - a.confidence)[0]
  }

  // 计算规则置信度
  calculateRuleConfidence(matchScore, actionType, timeContext, context) {
    let confidence = Math.min(matchScore / 2, 1.0)
    
    // 动作类型加权
    if (actionType === 'navigate') confidence *= 1.1
    if (actionType === 'record') confidence *= 1.0
    if (actionType === 'query') confidence *= 0.9
    
    // 时间上下文加权
    if (timeContext) confidence *= 1.1
    
    // 当前页面上下文
    if (context.currentPage && context.currentPage !== '/pages/aihelper/aihelper') {
      confidence *= 0.9
    }
    
    return Math.min(confidence, 1.0)
  }

  // 确定具体行动
  determineAction(actionType, config) {
    const actionMap = {
      navigate: 'navigate_to_page',
      record: 'open_record_page',
      query: 'show_info_page',
      update: 'navigate_to_page',
      delete: 'show_delete_options'
    }
    
    return {
      type: actionMap[actionType] || 'navigate_to_page',
      page: config.page,
      tabBar: config.tabBar,
      description: config.description
    }
  }

  // 上下文匹配
  matchByContext(processedInput, context) {
    // 基于当前时间的智能推荐
    const hour = new Date().getHours()
    
    if (processedInput.normalized.includes('记录') || processedInput.normalized.includes('添加')) {
      if (hour >= 6 && hour <= 10) {
        return this.createContextResult('food', '早餐时间推荐饮食记录', 0.6)
      } else if (hour >= 11 && hour <= 14) {
        return this.createContextResult('food', '午餐时间推荐饮食记录', 0.6)
      } else if (hour >= 17 && hour <= 20) {
        return this.createContextResult('food', '晚餐时间推荐饮食记录', 0.6)
      } else if (hour >= 21 && hour <= 23) {
        return this.createContextResult('sleep', '睡前推荐睡眠记录', 0.6)
      }
    }
    
    return null
  }

  // 创建上下文结果
  createContextResult(feature, reason, confidence) {
    const config = this.featureConfig[feature]
    if (!config) return null
    
    return {
      type: 'contextual',
      intent: feature,
      confidence: confidence,
      action: this.determineAction('record', config),
      pageConfig: config,
      parameters: {},
      reason: reason
    }
  }

  // 创建默认结果
  createDefaultResult() {
    return {
      type: 'default',
      intent: 'general_help',
      confidence: 0.3,
      action: {
        type: 'show_help',
        description: '显示帮助信息'
      },
      pageConfig: null,
      parameters: {},
      reason: '无法识别具体意图，提供通用帮助'
    }
  }

  // 获取当前时段
  getTimeOfDay() {
    const hour = new Date().getHours()
    if (hour >= 6 && hour < 12) return 'morning'
    if (hour >= 12 && hour < 18) return 'afternoon' 
    if (hour >= 18 && hour < 22) return 'evening'
    return 'night'
  }

  // 获取智能建议
  getSmartSuggestions(context = {}) {
    const suggestions = []
    const timeOfDay = this.getTimeOfDay()
    const hour = new Date().getHours()
    
    // 基于时间的建议
    if (timeOfDay === 'morning') {
      suggestions.push(
        { text: '记录早餐', intent: 'food', confidence: 0.8 },
        { text: '晨练打卡', intent: 'sport', confidence: 0.7 }
      )
    } else if (timeOfDay === 'afternoon') {
      suggestions.push(
        { text: '记录午餐', intent: 'food', confidence: 0.8 },
        { text: '查看健康数据', intent: 'body', confidence: 0.6 }
      )
    } else if (timeOfDay === 'evening') {
      suggestions.push(
        { text: '记录晚餐', intent: 'food', confidence: 0.8 },
        { text: '晚间运动', intent: 'sport', confidence: 0.7 }
      )
    } else {
      suggestions.push(
        { text: '准备睡眠记录', intent: 'sleep', confidence: 0.8 },
        { text: '查看今日总结', intent: 'body', confidence: 0.6 }
      )
    }
    
    // 基于上下文的建议
    if (context.currentPage && context.currentPage !== '/pages/aihelper/aihelper') {
      suggestions.push({ text: '返回首页', intent: 'body', confidence: 0.5 })
    }
    
    return suggestions.slice(0, 3)
  }

  // 意图验证
  validateIntent(result, context) {
    if (!result || result.confidence < 0.3) {
      return false
    }
    
    // 检查页面是否存在
    if (result.pageConfig && !this.isValidPage(result.pageConfig.page)) {
      return false
    }
    
    // 检查上下文合理性
    if (context.currentPage === result.pageConfig?.page && result.action?.type === 'navigate_to_page') {
      return false // 不应该导航到当前页面
    }
    
    return true
  }

  // 检查页面有效性
  isValidPage(page) {
    const validPages = [
      '/pages/index/index',
      '/pages/health/health', 
      '/pages/food/food1',
      '/pages/sport/sport',
      '/pages/sleep/sleep',
      '/pages/blog/blog',
      '/pages/me/me'
    ]
    
    return validPages.includes(page)
  }

  // 学习和优化接口（可扩展）
  learnFromFeedback(userInput, expectedIntent, actualResult) {
    // 这里可以实现学习机制，调整权重和规则
    console.log('学习反馈:', { userInput, expectedIntent, actualResult })
    // TODO: 实现机器学习逻辑
  }

  // 调试信息
  getDebugInfo(userInput, result) {
    return {
      input: userInput,
      preprocessed: this.preprocessInput(userInput),
      result: result,
      timestamp: new Date().toISOString()
    }
  }
}

export default new EnhancedIntentRecognizer()