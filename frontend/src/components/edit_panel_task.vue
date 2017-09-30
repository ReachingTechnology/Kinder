<template>
  <el-dialog title="编辑任务" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <el-form :model="edited_task"  :label-width="formLabelWidth" :label-position="labelPosition">
      <el-form-item label="任务编号" v-show="edited_task._id == '' ? false : true">
        <el-input v-model="edited_task._id" auto-complete="off" :disabled="true"></el-input>
      </el-form-item>
      <el-form-item label="任务名称">
        <el-input v-model="edited_task.name" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="任务描述" :label-width="formLabelWidth">
        <el-input v-model="edited_task.descr" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="任务类型" >
        <el-select v-model="edited_task.type">
          <el-option label="日常任务" :value="this.task_type_routine" :close-on-click-modal="false"></el-option>
          <el-option label="一般任务" :value="this.task_type_normal"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="选择任务时间">
        <el-date-picker
          v-show="edited_task.type == this.task_type_normal"
          v-model="edited_task.timeRange"
          type="datetimerange"
          placeholder="选择时间区间">
        </el-date-picker>
        <el-time-picker
          is-range
          v-show="edited_task.type == this.task_type_routine "
          v-model="edited_task.timeRange"
          placeholder="选择时间区间">
        </el-time-picker>
      </el-form-item>
      <el-form-item label="直接负责岗位">
        <el-select v-model="edited_task.upper_role" placeholder="选择岗位">
          <el-option v-for="item in allRole" :label="item.name" :value="item._id"/>
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
  import { UPSERT_TASK } from '../store/mutation_types'
  import dateUtil from '../utils/DateUtil'
  import { TASK_TYPE_NORMAL, TASK_TYPE_ROUTINE } from '../store/common_defs'
  export default {
    components: {},
    name: 'task_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      computeDatetime () {
//        alert('haha')
        let st = this.edited_task.timeRange[0]
        let et = this.edited_task.timeRange[1]
        console.log('before converting time: st:' + st + '; et:' + et)
        this.edited_task.starttime = dateUtil.getDatetimeSeconds(st)
        this.edited_task.endtime = dateUtil.getDatetimeSeconds(et)
        console.log('after converting time: st:' + this.edited_task.starttime + '; et:' + this.edited_task.endtime)
        console.log('call upsert: edit task:' + this.edited_task)
      },
      commitEdit () {
        this.computeDatetime()
        this.UPSERT_TASK(this.edited_task)
        this.$emit('showEdit', false)
      },
      cancelEdit () {
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      ...mapActions([ UPSERT_TASK ])
    },
    computed: {
      ...mapGetters(['allRole'])
    },
    props: ['edited_task', 'dialogVisible'],
    created: function () {
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        task_type_normal: TASK_TYPE_NORMAL,
        task_type_routine: TASK_TYPE_ROUTINE
      }
    }
  }
</script>
