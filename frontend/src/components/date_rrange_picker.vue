<template>
  <div class="block">
    <el-date-picker
      v-model="selectedDay"
      :type="datetime_type"
      align="left"
      placeholder="选择时间范围"
      @change="handleDaySelected"
      :picker-options="datePickerOptionsMonth">
    </el-date-picker>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        value6: '',
        value7: '',
        selectedDay: new Date()
      }
    },
    props: ['datetime_type']
  }
</script>
