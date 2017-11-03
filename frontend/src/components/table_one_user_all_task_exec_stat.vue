<template>
  <div>
      <div>
        <h2 style="margin-top: 0px">用户任务统计</h2>
        <h3>用户姓名 {{ queryUser }}</h3>
        <div align="left">
          <input :disabled="true" v-model="time_range"/>
        </div>
        <br/>
        <el-table
          :data="userDaterangeTask"
          style="width: 100%"
          :default-sort="{prop: 'no', order: 'ascending'}"
          :row-class-name="tableRowClassName">
          <el-table-column
            prop="seq"
            label="序号"
            align="center">
          </el-table-column>
          <el-table-column
            prop="taskname"
            label="职责"
            align="center"
          >
          </el-table-column>
          <el-table-column
            prop="unfinish_count"
            label="任务未完成次数"
            align="center"
          >
          </el-table-column>
          <el-table-column
            label="操作"
            align="center">
            <template scope="scope">
              <div>
                <el-button
                  size="small"
                  @click="handleEdit(scope.$index, scope.row)" type="success">查看
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
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
  import {mapActions, mapGetters} from 'vuex'
  import {GET_USER_TASK_EXEC_DATA_BY_DATERANGE} from '../store/mutation_types'
  import Moment from 'moment'
  import TableOneTaskDaterangeExecStat from './table_one_user_one_task_exec_stat'
  import Util from '../store/utils'
  export default {
    name: 'table_user_daterange_task_stat',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      ...mapActions([GET_USER_TASK_EXEC_DATA_BY_DATERANGE]),
      handleEdit (index, row) {
        this.selectedTask = row
        this.selectedTask.startofday = this.selectedData.startofday
        this.selectedTask.endofday = this.selectedData.endofday
        console.log('()*()*&*_&^*(^&**)(*)(*)')
        console.log(this.selectedTask)
        this.$router.push({name: 'OneUserOneTaskExecStat', params: {selectedData: this.selectedTask}})
      },
      handleClose () {
        this.$emit('showEdit', false)
      },
      showEditOver () {
        this.showEdit = false
      }
    },
    computed: {
      ...mapGetters(['userDaterangeTask', 'user', 'datePickerOptionsDay']),
      time_range () {
        return Moment(this.selectedData.startofday * 1000).format('M月D日') + '到' + Moment(this.selectedData.endofday * 1000).format('M月D日')
      },
      queryUser () {
        return Util.getUserName(this.selectedData.userid)
      }
    },
    created: function () {
      let params = {}
      params.userid = this.selectedData.userid
      params.startofday = this.selectedData.startofday
      params.endofday = this.selectedData.endofday
      this.GET_USER_TASK_EXEC_DATA_BY_DATERANGE(params)
    },
    beforeRouteLeave: function (to, from, next) {
      this.$destroy()
      next()
    },
    props: [],
    data: function () {
      return {
        selectedData: this.$route.params.selectedData,
        selectedTask: {},
        showEdit: false
      }
    },
    components: {
      TableOneTaskDaterangeExecStat
    }
  }
</script>
