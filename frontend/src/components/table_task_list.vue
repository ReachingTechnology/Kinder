<template>
  <div>
    <h2>幼儿园任务列表</h2>
    <div align="left">
      <el-button size="large"
                 @click="handleCreate()" type="success">
        添加新任务
      </el-button>
    </div>
    <br/>
    <el-table
      :data="tasks"
      style="width: 100%"
      :default-sort = "{prop: '_id', order: 'ascending'}"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="_id"
        label="任务编号"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="name"
        label="任务名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="descr"
        label="任务描述"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="type_name"
        label="任务类型"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="timeRangeShow"
        label="开始/结束时间"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="upper_role"
        label="直接负责岗位"
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
              @click="handleEdit(scope.$index, scope.row)" type="success">编辑</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <task-edit-panel @showEdit="showEidtOver" :dialogVisible="showEdit" :edited_task="selectedTask" ></task-edit-panel>
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
  import { GET_ALL_TASK } from '../store/mutation_types'
  import TaskEditPanel from './edit_panel_task.vue'
  import { TASK_TYPES, TASK_TYPE_ROUTINE } from '../store/common_defs'
  import Moment from 'moment'
  export default {
    name: 'table_task_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleEdit (index, row) {
        this.selectedTask = {}
        for (var i = 0, len = this.allTask.length; i < len; i++) {
          if (this.allTask[i]._id === row._id) {
            this.selectedTask = this.allTask[i]
            this.showEdit = true
            break
          }
        }
      },
      handleCreate () {
        this.selectedTask = {
          '_id': '',
          'name': '',
          'descr': '',
          'type': TASK_TYPE_ROUTINE,
          'starttime': '',
          'endtime': '',
          'upper_role': '',
          'timeRange': []
        }
        this.showEdit = true
      },
      showEidtOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_TASK])
    },
    computed: {
      ...mapGetters(['allRole', 'allTask']),
      tasks () {
        var data = []
        for (var i = 0, len = this.allTask.length; i < len; i++) {
          var item = this.allTask[i]
          item.type_name = TASK_TYPES.get(item.type)
          for (var j = 0, len2 = this.allRole.length; j < len2; j++) {
            if (item.upper_role === this.allRole[j]._id) {
              item.upper_role = this.allRole[j].name
            }
          }
          let st = new Date(item.starttime * 1000)
          let et = new Date(item.endtime * 1000)
          item.timeRange = [st, et]
          if (item.type === TASK_TYPE_ROUTINE) {
            item.timeRangeShow = Moment(item.starttime * 1000).format('h:mm') + ' 到 ' + Moment(item.endtime * 1000).format('h:mm')
          } else {
            item.timeRangeShow = Moment(item.starttime * 1000).format('MM-DD h:mm') + ' 到 ' + Moment(item.endtime * 1000).format('MM-DD h:mm')
          }
          data.push(item)
        }
        return data
      }
    },
    created: function () {
      this.GET_ALL_TASK()
    },
    data: () => {
      return {
        showEdit: false,
        selectedTask: {}
      }
    },
    components: {
      TaskEditPanel
    }
  }
</script>
