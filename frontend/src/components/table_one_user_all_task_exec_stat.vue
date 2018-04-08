<template>
  <div>
      <div id="print_area">
        <h2 style="margin-top: 0px">用户任务统计</h2>
        <h3>用户姓名 {{ queryUser }}</h3>
        <div align="left">
          <el-tag>{{time_range}}</el-tag>
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
            class="no-print"
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
        <br/>
        <div align="left" class="no-print">
          <el-button size="large" class="horizontal-btn"
                     @click="handlePrint" type="success">
            打印
          </el-button>
        </div>
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
  import {GET_USER_TASK_EXEC_DATA_BY_DATERANGE, PRINT} from '../store/mutation_types'
  import Moment from 'moment'
  import TableOneTaskDaterangeExecStat from './table_one_user_one_task_exec_stat'
  import Util from '../store/utils'

  export default {
    name: 'table_user_daterange_task_stat',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      ...mapActions([GET_USER_TASK_EXEC_DATA_BY_DATERANGE, PRINT]),
      handleEdit (index, row) {
        this.selectedTask = row
        this.selectedTask.startofday = this.startofday
        this.selectedTask.endofday = this.endofday
        this.$router.push({name: 'OneUserOneTaskExecStat', params: {selectedData: this.selectedTask}})
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
      },
      getData () {
        let params = {}
        params.userid = this.userid
        if (typeof this.startofday === 'string') {
          params.startofday = parseInt(this.startofday)
        } else {
          params.startofday = this.startofday
        }
        if (typeof this.endofday === 'string') {
          params.endofday = parseInt(this.endofday)
        } else {
          params.endofday = this.endofday
        }
        this.GET_USER_TASK_EXEC_DATA_BY_DATERANGE(params)
      }
    },
    computed: {
      ...mapGetters(['userDaterangeTask', 'user', 'datePickerOptionsDay']),
      time_range () {
        return Moment(this.startofday * 1000).format('M月D日') + '到' + Moment(this.endofday * 1000).format('M月D日')
      }
    },
    beforeRouteEnter: function (to, from, next) {
      next(vm => {
        vm.queryUser = Util.getUserName(vm.userid)
        vm.getData()
      })
    },
    beforeRouteLeave: function (to, from, next) {
      this.$destroy()
      next()
    },
    props: [],
    data: function () {
      return {
        userid: this.$route.params.userid,
        startofday: this.$route.params.startofday,
        endofday: this.$route.params.endofday,
        selectedTask: {},
        showEdit: false,
        queryUser: ''
      }
    },
    components: {
      TableOneTaskDaterangeExecStat
    }
  }
</script>
