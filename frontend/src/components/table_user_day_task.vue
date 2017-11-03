<template>
  <div>
    <h2>日任务列表</h2>
    <div align="left">
      <el-date-picker
        v-model="selectedDay"
        type="date"
        placeholder="选择日期"
        @change="handleDaySelected"
        :picker-options="datePickerOptionsDay">
      </el-date-picker>
    </div>
    <br/>
    <el-table
      :data="dayTask"
      style="width: 100%"
      :default-sort = "{prop: 'no', order: 'ascending'}"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="seq"
        label="序号"
        align="center">
      </el-table-column>
      <el-table-column
        prop="name"
        label="职责"
        align="center"
        >
      </el-table-column>
      <el-table-column
        prop="executetime"
        label="执行时间"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="realendtimeDisplay"
        label="实际完成时间"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="comment"
        label="备注"
        align="center"
        >
      </el-table-column>
      <el-table-column
        prop="finish_status_display"
        label="完成状态"
        align="center"
        sortable
      >
      </el-table-column>
      <el-table-column
        label="操作"
        align="center"
        >
        <template scope="scope">
          <div :style="scope.row.finish_status === 'TASK_STATUS_001' ||  scope.row.finish_status === 'TASK_STATUS_000' || (scope.row.finish_status === 'TASK_STATUS_003' && scope.row.realendtime === 0)? 'display: inline-block' : 'display:none'">
            <el-button
              size="mini"
              @click="handleFinish(scope.$index, scope.row)" type="success">任务完成</el-button>
          </div>
          <div style="display: inline-block">
            <el-button
              size="mini"
              type="danger"
              @click="handleEdit(scope.$index, scope.row)">编辑任务</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <edit-panel-user-day-task @showEdit="showEditOver" :dialogVisible="showEdit" :edited_task="selectedTask" :selectedDay="selectedDay"></edit-panel-user-day-task>
    <br/>
    <div align="left">
      <span>当日未完成项数：{{ this.unfinish_total }}</span>
    </div>
  </div>
</template>
<style>
  .el-table .info-row {
    background: #c9e5f5;
  }

  .el-table .positive-row {
    background: #e2f0e4;
  }

  /*.el-button:last-child {*/
    /*float: left;*/
  /*}*/
</style>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { GET_TASK_EXEC_DATA_BY_DATE, COMMIT_TASK_EXEC_INFO } from '../store/mutation_types'
  import { TASK_STATUS, TASK_STATUS_UNFINISHED, TASK_STATUS_DELAYED, DUTY_TIME_TYPE_ROUTINE } from '../store/common_defs'
  import dateUtil from '../utils/DateUtil'
  import Moment from 'moment'
  import EditPanelUserDayTask from './edit_panel_user_day_task.vue'
//  import {BMap} from '../assets/js/baidu_convertor'
//  import {MP} from '../assets/js/baidu_map'
  export default {
    name: 'table_user_day_task',
    methods: {
      tableRowClassName (row, index) {
        let item = row
        if (item.finish_status === TASK_STATUS.get(TASK_STATUS_UNFINISHED) || item.finish_status === TASK_STATUS.get(TASK_STATUS_DELAYED)) {
          return 'info-row'
        }
        return ''
      },
      ...mapActions([GET_TASK_EXEC_DATA_BY_DATE, COMMIT_TASK_EXEC_INFO]),
      handleEdit (index, row) {
        this.selectedTask = row
        this.selectedTask.timeType = this.timeType
        this.showEdit = true
      },
      handleFinish (index, row) {
        var finishTime = dateUtil.getNow()
        row.startofday = dateUtil.getStartOfTheday(this.selectedDay)
        var taskFinishInfo = {}
        taskFinishInfo.taskid = row.taskid
        taskFinishInfo.userid = row.userid
        taskFinishInfo.startofday = row.startofday
        taskFinishInfo.realendtime = finishTime
        taskFinishInfo.comment = row.comment
        taskFinishInfo.approve_status = row.approve_status
        taskFinishInfo.approve_user = row.approve_user
        taskFinishInfo.timeType = this.timeType
        this.COMMIT_TASK_EXEC_INFO(taskFinishInfo)
//        this.getLocation()
      },
      handleDaySelected () {
        this.getTaskExecData(dateUtil.getStartOfTheday(this.selectedDay))
      },
      getTaskExecData (date) {
        var param = {}
        param['userid'] = this.user._id
        param['startofday'] = date
        param['timeType'] = this.timeType
        this.GET_TASK_EXEC_DATA_BY_DATE(param)
      },
      showEditOver () {
        this.showEdit = false
      },
      getLocation () {
        navigator.geolocation.getCurrentPosition(this.translateLoc)
      },
      translateLoc (position) {
        console.log('baidu********************  translateLoc')
        var currentLat = position.coords.latitude
        var currentLon = position.coords.longitude
        var gpsPoint = new BMap.Point(currentLon, currentLat)
        BMap.Convertor.translate(gpsPoint, 0, this.setBaiduPoint)
      },
      setBaiduPoint (point) {
        console.log('this is baidu point')
        console.log(point)
      }
    },
    computed: {
      ...mapGetters(['userDayTask', 'user', 'datePickerOptionsDay', 'active_menu']),
      dayTask () {
        var data = []
        this.unfinish_total = 0
        for (var i = 0, len = this.userDayTask.length; i < len; i++) {
          var item = this.userDayTask[i]
          item.executetime = Moment(item.starttime * 1000).format('h:mm') + ' 到 ' + Moment(item.endtime * 1000).format('h:mm')
          item.realendtimeDisplay = item.realendtime === 0 ? '' : Moment(item.realendtime * 1000).format('M月D日 hh:mm')
          item.finish_status_display = TASK_STATUS.get(item.finish_status)
          data.push(item)
          if (item.finish_status === TASK_STATUS_UNFINISHED && item.approve_status !== '1') {
            this.unfinish_total += 1
          }
        }
        return data
      },
      timeType () {
        return this.$route.params.timeType
      }
    },
    watch: {
      user: function () {
        this.getTaskExecData(dateUtil.getStartOfTheday(this.selectedDay))
      },
      active_menu: function () {
        console.log('detect active menu changed')
        this.getTaskExecData(dateUtil.getStartOfTheday(this.selectedDay))
      }
    },
    mounted: function () {
      var param = {}
      param['userid'] = this.user._id
      param['startofday'] = dateUtil.getStartOfTheday(new Date())
      param['timeType'] = DUTY_TIME_TYPE_ROUTINE
      this.GET_TASK_EXEC_DATA_BY_DATE(param)
    },
    beforeRouteLeave: function (to, from, next) {
      this.$destroy()
      next()
    },
    data: function () {
      return {
        selectedDay: new Date(),
        selectedTask: {},
        showEdit: false,
        unfinish_total: 0
      }
    },
    components: {
      EditPanelUserDayTask
    }
  }
</script>
