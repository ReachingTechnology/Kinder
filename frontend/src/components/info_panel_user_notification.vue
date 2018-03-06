<template>
  <div>
    <el-dialog title="职责提醒详情" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
      <el-form :model="current_notification" :label-width="formLabelWidth" :label-position="labelPosition" ref="notifyForm"
      >
        <el-form-item label="职责名称">
          <!--<el-input v-model="current_notification.name" disabled="true" auto-complete="off"></el-input>-->
          <span>{{ current_notification.taskname }}</span>
        </el-form-item>
        <el-form-item align="left" label="提醒内容" :label-width="formLabelWidth">
          <!--<el-input v-model="current_notification.descr" disabled="true" auto-complete="off"></el-input>-->
          <span>{{ current_notification.msgContent }}</span>
        </el-form-item>
        <!--<el-form-item label="职责执行时间">-->
          <!--<el-input v-model="current_notification.dutyExecTime" disabled="true" auto-complete="off"></el-input>-->
        <!--</el-form-item>-->
        <!--<el-form-item align="left" label="提醒等级">-->
          <!--<el-select v-model="current_notification.notifyPriority" disabled>-->
            <!--<el-option :label="NOTIFY_PRIORITY['high']" value="high"/>-->
            <!--<el-option :label="NOTIFY_PRIORITY['middle']" value="middle"/>-->
            <!--<el-option :label="NOTIFY_PRIORITY['low']" value="low"/>-->
          <!--</el-select>-->
        <!--</el-form-item>-->
        <el-form-item align="left" label="提醒等级">
          <span> {{ NOTIFY_PRIORITY[current_notification.notifyPriority] }} </span>
        </el-form-item>
        <el-form-item align="left" label="提醒发送时间" :label-width="formLabelWidth">
          <!--<el-input v-model="current_notification.sendTimeDisplay" disabled="true" auto-complete="off"></el-input>-->
          <span>{{ current_notification.msgArriveTimeDisplay }}</span>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleClose">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
  import {mapGetters, mapActions} from 'vuex'
  import ObjUtil from '../utils/ObjUtil'
  import {NOTIFY_TYPE, NOTIFY_PRIORITY} from '../store/common_defs'
  import Moment from 'moment'
  export default {
    components: {},
    name: 'edit_panel_inform',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleClose () {
        this.$refs['notifyForm'].resetFields()
        this.$emit('showEdit', false)
      },
      ...mapActions([])
    },
    watch: {
      dialogVisible: function (val, oldval) {
        if (val === true) {
          this.current_notification = ObjUtil.clone(this.edited_notification)
        }
      }
    },
    computed: {
      ...mapGetters([])
    },
    props: ['edited_notification', 'dialogVisible'],
    created: function () {
    },
    data: function () {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        NOTIFY_TYPE: NOTIFY_TYPE,
        NOTIFY_PRIORITY: NOTIFY_PRIORITY,
        current_notification: {}
      }
    }
  }
</script>
