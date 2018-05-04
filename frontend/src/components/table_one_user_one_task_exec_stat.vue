<template>
  <div>
    <div>
      <h2 style="margin-top: 0px">用户任务 {{ selectedData.taskname }} 统计</h2>
      <h3>用户姓名 {{ queryUser }}</h3>
      <div align="left">
        <el-tag>{{time_range}}</el-tag>
      </div>
      <br/>
      <el-table
        :data="tasks"
        style="width: 100%"
        :default-sort="{prop: 'no', order: 'ascending'}"
        :row-class-name="tableRowClassName">
        <el-table-column
          prop="startofdayDisplay"
          label="日期"
          align="center">
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
            <el-button
              size="mini"
              type="danger"
              @click="handleEdit(scope.$index, scope.row)">编辑任务
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <br/>
      <div align="left" class="no-print">
        <el-button size="large" class="horizontal-btn"
                   @click="handlePrint" type="success">
          打印
        </el-button>
      </div>
    </div>
    <div id="print_area" class="no-screen">
      <div id="print">
        <h1>用户单项任务统计</h1>
        <h3>用户姓名: {{queryUser}}  | 任务: {{selectedData.taskname}}</h3>
        <h3>{{time_range}}</h3>
        <table>
          <thead>
          <tr>
            <th> 日期 </th>
            <th> 实际完成时间 </th>
            <th> 备注 </th>
            <th> 完成状态 </th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="data in tasks">
            <td> {{data.startofdayDisplay}} </td>
            <td> {{data.realendtimeDisplay}} </td>
            <td> {{data.comment}} </td>
            <td> {{data.finish_status_display}} </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  <edit-panel-user-day-task @showEdit="showEditOver" :dialogVisible="showEdit" :edited_task="selectedTask" :selectedDay="selectedDay"></edit-panel-user-day-task>
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
  import {mapActions, mapGetters} from 'vuex'
  import {GET_ONE_TASK_EXEC_DATA_BY_DATERANGE, PRINT} from '../store/mutation_types'
  import Moment from 'moment'
  import EditPanelUserDayTask from './edit_panel_user_day_task.vue'
  import {
    TASK_STATUS_UNFINISHED,
    TASK_STATUS_DELAYED,
    TASK_STATUS
  } from '../store/common_defs'
  import Util from '../store/utils'
  export default {
    name: 'table_user_day_task',
    methods: {
      tableRowClassName (row, index) {
        let item = row
        if (item.finish_status === TASK_STATUS_UNFINISHED || item.finish_status === TASK_STATUS_DELAYED) {
          return 'info-row'
        }
        return ''
      },
      ...mapActions([GET_ONE_TASK_EXEC_DATA_BY_DATERANGE, PRINT]),
      handleEdit (index, row) {
        this.selectedDay = new Date(row.startofday * 1000)
        this.selectedTask = row
        this.selectedTask.name = row.taskname
        this.showEdit = true
      },
      handleClose () {
        this.$emit('showEdit', false)
      },
      showEditOver () {
        this.showEdit = false
      },
      handlePrint () {
        let allContent = document.documentElement.innerHTML
        let printContent = document.getElementById('print_area').innerHTML
        this.PRINT({all: allContent, print: printContent})
        return true
      }
    },
    computed: {
      ...mapGetters(['taskExecDaterangeData', 'user', 'datePickerOptionsDay']),
      time_range () {
        return Moment(this.selectedData.startofday * 1000).format('M月D日') + '到' + Moment(this.selectedData.endofday * 1000).format('M月D日')
      },
      tasks () {
        var data = []
        console.log(this.selectedData)
        console.log(this.taskExecDaterangeData)
        for (var i = 0, len = this.taskExecDaterangeData.length; i < len; i++) {
          var item = this.taskExecDaterangeData[i]
          item.executetime = Moment(item.starttime * 1000).format('H:mm') + ' 到 ' + Moment(item.endtime * 1000).format('H:mm')
          item.realendtimeDisplay = item.realendtime === 0 ? '' : Moment(item.realendtime * 1000).format('M月D日 H:mm')
          item.finish_status_display = TASK_STATUS.get(item.finish_status)
          console.log('完成状态')
          console.log(item.finish_status)
          console.log(item.finish_status_display)
          item.startofdayDisplay = Moment(item.startofday * 1000).format('M月D日')
          item.taskname = this.selectedData.taskname
          item.taskid = this.selectedData.taskid
          item.userid = this.selectedData.userid
          data.push(item)
        }
        return data
      },
      queryUser () {
        return Util.getUserName(this.selectedData.userid)
      }
    },
    mounted: function () {
      console.log('%%%%%%%%%%%%%%^^^^^^^^^^^^^^^')
      console.log(this.selectedData)
      this.GET_ONE_TASK_EXEC_DATA_BY_DATERANGE(this.selectedData)
    },
    beforeRouteLeave: function (to, from, next) {
      this.$destroy()
      next()
    },
    props: [],
    data: function () {
      return {
        selectedDay: new Date(),
        selectedUser: '000001',
        showEdit: false,
        selectedTask: {},
        selectedData: this.$route.params.selectedData
      }
    },
    components: {
      EditPanelUserDayTask
    }
  }
</script>
