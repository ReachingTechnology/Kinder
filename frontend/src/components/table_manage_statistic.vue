<template>
  <div>
    <h2>幼儿园安保统计报表</h2>
    <div style="width: 100%; text-align: left">
      <el-date-picker
        v-model="selectedDay"
        :type="datetime_type"
        align="left"
        placeholder="选择时间范围"
        @change="handleDaySelected"
        :picker-options="datePickerOption">
      </el-date-picker>
    </div>
    <br/>
    <el-table
      :data="all_statistic_data"
      style="width: 100%"
      :default-sort = "{prop: 'userid', order: 'ascending'}"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="userid"
        label="编号"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="username"
        label="姓名"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="role"
        label="岗位"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="unfinish_count"
        label="职责未完成项数"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center">
        <template scope="scope">
          <div>
            <el-button
              size="small"
              @click="handleEdit(scope.$index, scope.row)" type="success">查看</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <table-user-datarange-task-stat @showEdit="showEditOver" :dialogVisible="showEdit" :selectedData="selectedData" ></table-user-datarange-task-stat>
  </div>
</template>
<style>
  .el-table .info-row {
    background: #c9e5f5;
  }

  .el-table .positive-row {
    background: #e2f0e4;
  }
</style>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { GET_ALL_DATA, GET_USER_TASK_EXEC_DATA_BY_DATERANGE } from '../store/mutation_types'
  import DateRangePicker from './date_rrange_picker'
  import TableUserDatarangeTaskStat from './table_user_daterange_task_stat'
  import dateUtil from '../utils/DateUtil'
  export default {
    name: 'table_manage_unfinished_data',
    methods: {
      tableRowClassName (row, index) {
        let item = row
        if (item.unfinish_count > 0) {
          return 'info-row'
        }
        return ''
      },
      handleEdit (index, row) {
        this.selectedData = {}
        this.selectedData.userid = row.userid
        if (this.datetime_type === 'month') {
          this.selectedData.startofday = dateUtil.getStartofMonthofTheDay(this.selectedDay)
          let daycount = dateUtil.getDayCountOfTheMonth(this.selectedDay)
          this.selectedData.endofday = this.selectedData.startofday + 3600 * 24 * daycount
          let startofToday = dateUtil.getStartOfToday()
          if (this.selectedData.endofday > startofToday) {
            console.log('this month')
            this.selectedData.endofday = startofToday
          }
        } else {
          this.selectedData.startofday = dateUtil.getStartOfTheday(this.selectedDay)
          this.selectedData.endofday = this.selectedData.startofday + 3600 * 24
        }
        let params = {}
        params.userid = this.selectedData.userid
        params.startofday = this.selectedData.startofday
        params.endofday = this.selectedData.endofday
        this.GET_USER_TASK_EXEC_DATA_BY_DATERANGE(params)
        this.showEdit = true
      },
      handleDaySelected () {
        let params = {
          'starttime': this.datetime_type === 'month' ? dateUtil.getStartofMonthofTheDay(this.selectedDay) : dateUtil.getStartOfTheday(this.selectedDay),
          'datetime_type': this.datetime_type
        }
        this.GET_ALL_DATA(params)
      },
      showEditOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_DATA, GET_USER_TASK_EXEC_DATA_BY_DATERANGE])
    },
    computed: {
      ...mapGetters(['all_statistic_data'])
    },
    mounted: function () {
    },
    props: ['datetime_type', 'datePickerOption'],
    data: () => {
      return {
        showEdit: false,
        selectedData: {},
        selectedDay: new Date()
      }
    },
    components: {
      DateRangePicker,
      TableUserDatarangeTaskStat
    }
  }
</script>
