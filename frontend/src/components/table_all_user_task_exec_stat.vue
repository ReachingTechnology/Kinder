<template>
  <div>
    <h2>幼儿园安保统计报表</h2>
    <div style="width: 100%; text-align: left">
      <el-date-picker
        v-model="dateRange"
        type="daterange"
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
  import { GET_ALL_USER_TASK_EXEC_DATA, GET_ALL_USER_TASK_EXEC_DATA_BY_DATERANGE, GET_USER_TASK_EXEC_DATA_BY_DATERANGE } from '../store/mutation_types'
  import DateRangePicker from './date_rrange_picker'
  import dateUtil from '../utils/DateUtil'
  import { DATETYPE_DAY, DATETYPE_MONTH } from '../store/common_defs'

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
        this.selectedData.startofday = dateUtil.getStartOfTheday(this.dateRange[0])
        this.selectedData.endofday = dateUtil.getStartOfTheday(this.dateRange[1])
        this.$router.push({name: 'OneUserAllTaskExecStat', params: {selectedData: this.selectedData}})
      },
      handleDaySelected () {
        var param = {dateRange: this.dateRange}
        this.computeDatetime(param)
        this.GET_ALL_USER_TASK_EXEC_DATA_BY_DATERANGE(param)
      },
      computeDatetime (param) {
        let st = param.dateRange[0]
        let et = param.dateRange[1]
        param.starttime = dateUtil.getDatetimeSeconds(st)
        param.endtime = dateUtil.getDatetimeSeconds(et)
      },
      showEditOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_USER_TASK_EXEC_DATA, GET_ALL_USER_TASK_EXEC_DATA_BY_DATERANGE, GET_USER_TASK_EXEC_DATA_BY_DATERANGE])
    },
    computed: {
      ...mapGetters(['datePickerOptionsDay', 'datePickerOptionsMonth', 'all_statistic_data']),
      datePickerOption () {
        if (this.datetime_type === DATETYPE_DAY) {
          return this.datePickerOptionsDay
        }
        if (this.datetime_type === DATETYPE_MONTH) {
          return this.datePickerOptionsMonth
        }
      },
      datetime_type () {
        return this.$route.params.datetime_type
      },
      starttime () {
        return this.$route.params.starttime
      }
    },
    created: function () {
      this.handleDaySelected()
    },
    props: [],
    data: function () {
      return {
        showEdit: false,
        selectedData: {},
        selectedDay: dateUtil.getYesterday(),
        dateRange: [dateUtil.getYesterday(), dateUtil.getToday()]
      }
    },
    components: {
      DateRangePicker
    }
  }
</script>
