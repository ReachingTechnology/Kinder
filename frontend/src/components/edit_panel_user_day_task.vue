<template>
  <el-dialog title="编辑任务" :visible.sync="dialogVisible" :close-on-click-modal="false" @close="handleClose">
    <el-form :model="edited_task"  :label-width="formLabelWidth" :label-position="labelPosition">
      <el-form-item label="任务名称">
        <el-input v-model="edited_task.name" :disabled="true" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="任务执行时间">
        <el-input v-model="edited_task.executetime" :disabled="true" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="任务实际完成时间" v-show="edited_task.realendtime !== 0">
        <el-input v-model="edited_task.realendtimeDisplay" :disabled="true" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="备注">
        <el-input type="textarea"
                  :autosize="{ minRows: 2, maxRows: 4}"
                  v-model="edited_task.comment" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="完成状态">
        <el-input v-model="edited_task.finish_status_display" :disabled="true" autoComplete="off"></el-input>
      </el-form-item>
      <el-form-item label="工作审批">
        <el-select v-model="edited_task.approve_status" :disabled="!Util.hasPermission('PERMISSION_TASK_APPROVE_TASK')" placeholder="选择审批意见">
          <el-option label="个人原因" value='0'></el-option>
          <el-option label="工作安排" value='1'></el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
  </span>
  </el-dialog>
</template>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { COMMIT_TASK_EXEC_INFO } from '../store/mutation_types'
  import dateUtil from '../utils/DateUtil'
  import Util from '../store/utils'
  export default {
    components: {},
    name: 'duty_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        var finishTime = dateUtil.getNow()
        this.edited_task.startofday = dateUtil.getStartOfTheday(this.selectedDay)
        var taskFinishInfo = {}
        taskFinishInfo.taskid = this.edited_task.taskid
        taskFinishInfo.userid = this.edited_task.userid
        taskFinishInfo.startofday = this.edited_task.startofday
        taskFinishInfo.realendtime = finishTime
        taskFinishInfo.comment = this.edited_task.comment
        taskFinishInfo.approve_status = this.edited_task.approve_status
        taskFinishInfo.approve_user = this.edited_task.approve_user
        taskFinishInfo.timeType = this.edited_task.timeType
        this.COMMIT_TASK_EXEC_INFO(taskFinishInfo)
        this.$emit('showEdit', false)
      },
      cancelEdit () {
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      ...mapActions([ COMMIT_TASK_EXEC_INFO ])
    },
    computed: {
      ...mapGetters(['allRole']),
      Util () { return Util }
    },
    props: ['edited_task', 'dialogVisible', 'selectedDay'],
    created: function () {
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        selectedRoleName: []
      }
    }
  }
</script>
