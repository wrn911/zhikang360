// config/feature-mapping.js - 功能映射配置文件
export const featureMapping = {
  health: {
    keywords: ['健康', '管理', '体检', '医疗', '病症', '症状', '诊断', '治疗'],
    aliases: ['身体健康', '健康状况', '医疗健康', '健康管理'],
    page: '/pages/health/health',
    tabBar: true,
    description: '健康管理功能',
    category: 'navigation',
    weight: 1.0,
    relatedFeatures: ['body', 'sleep', 'sport'],
    icon: '💊'
  },
  
  sport: {
    keywords: ['运动', '锻炼', '健身', '跑步', '游泳', '骑行', '瑜伽', '篮球', '足球', '网球', '徒步', '爬山'],
    aliases: ['体育运动', '体育锻炼', '体能训练', '有氧运动', '无氧运动'],
    page: '/pages/sport/sport',
    tabBar: false,
    description: '运动记录功能',
    category: 'record',
    weight: 1.0,
    relatedFeatures: ['health', 'body'],
    icon: '🏃‍♀️',
    subCategories: {
      running: ['跑步', '慢跑', '晨跑'],
      fitness: ['健身', '力量训练', '举重'],
      cardio: ['有氧', '心肺', '耐力'],
      ball: ['篮球', '足球', '网球', '羽毛球']
    }
  },
  
  food: {
    keywords: ['饮食', '吃饭', '食物', '营养', '餐饮', '用餐', '进餐', '早餐', '午餐', '晚餐', '夜宵', '零食'],
    aliases: ['膳食', '餐食', '饮食管理', '营养管理', '食谱'],
    page: '/pages/food/food1',
    tabBar: false,
    description: '饮食记录功能',
    category: 'record',
    weight: 1.0,
    relatedFeatures: ['health', 'body'],
    icon: '🍎',
    subCategories: {
      meals: ['早餐', '午餐', '晚餐', '宵夜'],
      snacks: ['零食', '点心', '水果'],
      drinks: ['饮料', '水', '茶', '咖啡']
    }
  },
  
  sleep: {
    keywords: ['睡眠', '睡觉', '休息', '入睡', '失眠', '安眠', '作息', '熬夜', '早睡'],
    aliases: ['睡眠管理', '作息管理', '睡眠质量', '睡眠时间'],
    page: '/pages/sleep/sleep',
    tabBar: false,
    description: '睡眠记录功能',
    category: 'record',
    weight: 1.0,
    relatedFeatures: ['health', 'body'],
    icon: '😴',
    subCategories: {
      bedtime: ['就寝', '上床', '准备睡觉'],
      wakeup: ['起床', '醒来', '早起'],
      quality: ['睡眠质量', '深度睡眠', '浅睡']
    }
  },
  
  body: {
    keywords: ['身体', '体重', '身高', 'BMI', '体脂', '肌肉', '骨量', '基础代谢', '体型', '体检'],
    aliases: ['身体信息', '体型数据', '身体指标', '体测数据'],
    page: '/pages/index/index',
    tabBar: true,
    description: '身体信息查看',
    category: 'query',
    weight: 1.0,
    relatedFeatures: ['health', 'sport', 'food'],
    icon: '📊',
    subCategories: {
      weight: ['体重', '称重', '减重', '增重'],
      composition: ['体脂', '肌肉', '水分', '骨量'],
      metrics: ['BMI', '基础代谢', '体脂率']
    }
  },
  
  blog: {
    keywords: ['博客', '文章', '分享', '日记', '笔记', '心得', '经验', '资讯'],
    aliases: ['健康博客', '文章分享', '健康日记', '经验分享'],
    page: '/pages/blog/blog',
    tabBar: true,
    description: '健康博客功能',
    category: 'navigation',
    weight: 1.0,
    relatedFeatures: ['health'],
    icon: '📝',
    subCategories: {
      read: ['阅读', '查看', '浏览'],
      write: ['写作', '发布', '分享'],
      search: ['搜索', '查找', '寻找']
    }
  }
}

// 同义词词典 - 用于文本预处理
export const synonymDict = {
  '运动': ['锻炼', '健身', '训练', '体育'],
  '饮食': ['吃饭', '用餐', '进食', '膳食'],
  '睡眠': ['睡觉', '休息', '就寝'],
  '健康': ['养生', '保健', '康复'],
  '身体': ['体型', '身材', '体质'],
  '记录': ['登记', '录入', '添加', '保存'],
  '查看': ['查询', '浏览', '了解', '获取'],
  '管理': ['维护', '调理', '照顾']
}

// 页面关系映射 - 用于上下文推荐
export const pageRelations = {
  '/pages/aihelper/aihelper': {
    related: [
      '/pages/index/index',
      '/pages/health/health',
      '/pages/food/food1',
      '/pages/sport/sport',
      '/pages/sleep/sleep',
      '/pages/blog/blog'
    ],
    suggestions: [
      { text: '查看身体信息', feature: 'body', reason: '了解当前状态' },
      { text: '记录今日数据', feature: 'food', reason: '养成记录习惯' },
      { text: '健康管理', feature: 'health', reason: '全面健康管理' }
    ]
  },
  
  '/pages/index/index': {
    related: ['/pages/health/health', '/pages/sport/sport', '/pages/food/food1'],
    suggestions: [
      { text: '记录运动', feature: 'sport', reason: '运动有助健康' },
      { text: '记录饮食', feature: 'food', reason: '营养均衡重要' }
    ]
  },
  
  '/pages/health/health': {
    related: ['/pages/index/index', '/pages/sport/sport', '/pages/sleep/sleep'],
    suggestions: [
      { text: '查看身体数据', feature: 'body', reason: '监测健康指标' },
      { text: '运动记录', feature: 'sport', reason: '运动促进健康' }
    ]
  },
  
  '/pages/sport/sport': {
    related: ['/pages/health/health', '/pages/index/index', '/pages/food/food1'],
    suggestions: [
      { text: '记录饮食', feature: 'food', reason: '运动后需要补充营养' },
      { text: '查看身体变化', feature: 'body', reason: '运动效果监测' }
    ]
  },
  
  '/pages/food/food1': {
    related: ['/pages/health/health', '/pages/sport/sport', '/pages/index/index'],
    suggestions: [
      { text: '查看体重变化', feature: 'body', reason: '饮食影响体重' },
      { text: '计划运动', feature: 'sport', reason: '运动消耗卡路里' }
    ]
  },
  
  '/pages/sleep/sleep': {
    related: ['/pages/health/health', '/pages/index/index', '/pages/sport/sport'],
    suggestions: [
      { text: '查看健康状态', feature: 'health', reason: '睡眠影响整体健康' },
      { text: '适量运动', feature: 'sport', reason: '运动有助改善睡眠' }
    ]
  },
  
  '/pages/blog/blog': {
    related: ['/pages/health/health', '/pages/index/index'],
    suggestions: [
      { text: '健康管理', feature: 'health', reason: '学以致用' },
      { text: '查看个人数据', feature: 'body', reason: '对比学习内容' }
    ]
  }
}

// 动作类型映射
export const actionTypeMapping = {
  navigate: {
    keywords: ['去', '到', '进入', '打开', '访问', '查看', '浏览', '前往'],
    priority: 1.0,
    description: '页面导航'
  },
  record: {
    keywords: ['记录', '添加', '输入', '录入', '保存', '登记', '填写', '新增'],
    priority: 1.1,
    description: '数据记录'
  },
  query: {
    keywords: ['查询', '查看', '显示', '获取', '了解', '知道', '看看', '检查'],
    priority: 0.9,
    description: '信息查询'
  },
  update: {
    keywords: ['修改', '更新', '编辑', '改变', '调整', '更正'],
    priority: 0.8,
    description: '更新修改'
  },
  delete: {
    keywords: ['删除', '移除', '清除', '取消', '去掉'],
    priority: 0.7,
    description: '删除操作'
  },
  analyze: {
    keywords: ['分析', '统计', '报告', '总结', '评估'],
    priority: 0.9,
    description: '数据分析'
  }
}

// 时间上下文映射
export const timeContextMapping = {
  today: {
    keywords: ['今天', '今日', '现在', '当前', '今'],
    weight: 1.2,
    description: '今天'
  },
  yesterday: {
    keywords: ['昨天', '昨日', '昨'],
    weight: 1.0,
    description: '昨天'
  },
  tomorrow: {
    keywords: ['明天', '明日', '明'],
    weight: 0.9,
    description: '明天'
  },
  thisWeek: {
    keywords: ['这周', '本周', '这星期', '本星期', '这礼拜'],
    weight: 0.8,
    description: '本周'
  },
  thisMonth: {
    keywords: ['这个月', '本月', '这月'],
    weight: 0.7,
    description: '本月'
  },
  morning: {
    keywords: ['早上', '上午', '晨', '早晨', '早间'],
    weight: 1.0,
    description: '早上'
  },
  afternoon: {
    keywords: ['下午', '午后', '中午'],
    weight: 1.0,
    description: '下午'
  },
  evening: {
    keywords: ['晚上', '傍晚', '黄昏', '晚间'],
    weight: 1.0,
    description: '晚上'
  },
  night: {
    keywords: ['夜晚', '深夜', '夜里', '半夜'],
    weight: 1.0,
    description: '夜晚'
  }
}

// 情绪和语气映射
export const sentimentMapping = {
  positive: {
    keywords: ['好', '棒', '很好', '不错', '满意', '开心', '高兴'],
    weight: 1.1,
    description: '积极'
  },
  negative: {
    keywords: ['不好', '糟糕', '难受', '痛苦', '不舒服', '担心'],
    weight: 1.2,
    description: '消极'
  },
  neutral: {
    keywords: ['一般', '还行', '普通', '正常'],
    weight: 1.0,
    description: '中性'
  },
  urgent: {
    keywords: ['急', '赶紧', '快', '立即', '马上', '紧急'],
    weight: 1.3,
    description: '紧急'
  },
  questioning: {
    keywords: ['什么', '怎么', '如何', '为什么', '哪里', '哪个', '什么时候', '多少'],
    weight: 1.0,
    description: '疑问'
  }
}

// 数值和单位映射
export const numericalMapping = {
  weight: {
    units: ['kg', '公斤', '斤', 'g', '克'],
    patterns: [/(\d+(?:\.\d+)?)\s*(?:kg|公斤|斤)/i],
    defaultUnit: 'kg',
    description: '体重'
  },
  height: {
    units: ['cm', '厘米', 'm', '米'],
    patterns: [/(\d+(?:\.\d+)?)\s*(?:cm|厘米|米)/i],
    defaultUnit: 'cm',
    description: '身高'
  },
  time: {
    units: ['小时', '分钟', '秒', 'h', 'min', 's'],
    patterns: [/(\d{1,2}):(\d{2})/g, /(\d+(?:\.\d+)?)\s*(?:小时|分钟|h|min)/i],
    defaultUnit: '分钟',
    description: '时间'
  },
  calories: {
    units: ['卡', '大卡', 'kcal', 'cal'],
    patterns: [/(\d+(?:\.\d+)?)\s*(?:卡|大卡|kcal|cal)/i],
    defaultUnit: 'kcal',
    description: '热量'
  },
  distance: {
    units: ['km', '公里', 'm', '米', '步'],
    patterns: [/(\d+(?:\.\d+)?)\s*(?:km|公里|米|步)/i],
    defaultUnit: 'km',
    description: '距离'
  }
}

// 常见问题模板
export const commonQuestionTemplates = {
  dataQuery: {
    patterns: [
      '我的{feature}数据',
      '查看{feature}',
      '显示{feature}信息',
      '{feature}统计'
    ],
    intent: 'query',
    confidence: 0.8
  },
  dataRecord: {
    patterns: [
      '记录{feature}',
      '添加{feature}数据',
      '输入{feature}',
      '我要记录{feature}'
    ],
    intent: 'record',
    confidence: 0.9
  },
  dataAnalysis: {
    patterns: [
      '分析{feature}',
      '{feature}报告',
      '{feature}趋势',
      '{feature}变化'
    ],
    intent: 'analyze',
    confidence: 0.7
  },
  navigation: {
    patterns: [
      '去{feature}页面',
      '打开{feature}',
      '进入{feature}',
      '我想{feature}'
    ],
    intent: 'navigate',
    confidence: 0.8
  }
}

// 智能建议规则
export const smartSuggestionRules = {
  timeBasedSuggestions: {
    morning: [
      { feature: 'food', action: 'record', text: '记录早餐', priority: 0.9 },
      { feature: 'sport', action: 'record', text: '晨练打卡', priority: 0.7 },
      { feature: 'body', action: 'query', text: '查看体重', priority: 0.6 }
    ],
    afternoon: [
      { feature: 'food', action: 'record', text: '记录午餐', priority: 0.9 },
      { feature: 'sport', action: 'record', text: '午间运动', priority: 0.5 },
      { feature: 'health', action: 'navigate', text: '健康管理', priority: 0.6 }
    ],
    evening: [
      { feature: 'food', action: 'record', text: '记录晚餐', priority: 0.9 },
      { feature: 'sport', action: 'record', text: '晚间运动', priority: 0.8 },
      { feature: 'blog', action: 'navigate', text: '阅读健康资讯', priority: 0.5 }
    ],
    night: [
      { feature: 'sleep', action: 'record', text: '准备睡眠记录', priority: 0.9 },
      { feature: 'body', action: 'query', text: '查看今日总结', priority: 0.7 }
    ]
  },
  
  contextBasedSuggestions: {
    afterMeal: [
      { feature: 'sport', action: 'record', text: '餐后运动', priority: 0.7 },
      { feature: 'health', action: 'navigate', text: '消化建议', priority: 0.5 }
    ],
    afterExercise: [
      { feature: 'food', action: 'record', text: '补充营养', priority: 0.8 },
      { feature: 'body', action: 'query', text: '查看消耗', priority: 0.6 }
    ],
    weeklyReview: [
      { feature: 'body', action: 'analyze', text: '周度分析', priority: 0.8 },
      { feature: 'blog', action: 'navigate', text: '分享心得', priority: 0.6 }
    ]
  }
}

// 错误处理和降级策略
export const fallbackStrategies = {
  noMatch: {
    suggestions: [
      { feature: 'health', text: '健康管理', reason: '通用功能' },
      { feature: 'body', text: '查看数据', reason: '了解现状' },
      { feature: 'blog', text: '学习资讯', reason: '获取知识' }
    ],
    message: '我没有完全理解您的意思，以下是一些建议功能：'
  },
  lowConfidence: {
    threshold: 0.3,
    askForConfirmation: true,
    message: '您是想要{feature}吗？',
    alternatives: 2
  },
  ambiguous: {
    maxSuggestions: 3,
    showConfidence: true,
    message: '我理解您可能想要以下功能之一：'
  }
}

// 学习和优化配置
export const learningConfig = {
  enableLearning: true,
  feedbackWeight: 0.1,
  adaptationRate: 0.05,
  minSamplesForUpdate: 10,
  maxHistoryLength: 1000
}

// 性能优化配置
export const performanceConfig = {
  maxProcessingTime: 500, // 毫秒
  cacheSize: 100,
  enableCache: true,
  debugMode: false
}

// 导出所有配置
export default {
  featureMapping,
  synonymDict,
  pageRelations,
  actionTypeMapping,
  timeContextMapping,
  sentimentMapping,
  numericalMapping,
  commonQuestionTemplates,
  smartSuggestionRules,
  fallbackStrategies,
  learningConfig,
  performanceConfig
}