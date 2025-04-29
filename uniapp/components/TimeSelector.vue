<template>
  <view class="time-selector">
    <checkbox-group @change="handleChange">
      <view class="time-grid">
        <label 
          v-for="time in times" 
          :key="time.value" 
          class="time-item"
          :class="{selected: selected.includes(time.value)}"
        >
          <checkbox :value="time.value" :checked="selected.includes(time.value)" color="#4CAF50"/>
          <text class="label">{{ time.label }}</text>
        </label>
      </view>
    </checkbox-group>
  </view>
</template>

<script>
export default {
  props: {
    selected: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      times: [
        { label: '早晨（6-9点）', value: 'morning' },
        { label: '上午（9-12点）', value: 'forenoon' },
        { label: '午间（12-14点）', value: 'noon' },
        { label: '下午（14-18点）', value: 'afternoon' },
        { label: '晚间（18-22点）', value: 'evening' }
      ]
    }
  },
  methods: {
    handleChange(e) {
      this.$emit('change', e.detail.value)
    }
  }
}
</script>

<style scoped>
.time-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20upx;
}

.time-item {
  flex: 0 0 calc(33.3% - 14upx);
  padding: 20upx;
  border: 2upx solid #e0e0e0;
  border-radius: 12upx;
  text-align: center;
  
  &.selected {
    border-color: #4CAF50;
    background: #f0fff4;
  }
}

.label {
  font-size: 28upx;
}
</style>