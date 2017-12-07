<template>
  <div>
  <el-dialog title="编辑提醒" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <el-form :model="current_notify" :label-width="formLabelWidth" :label-position="labelPosition" ref="roleForm"
             >
      <el-form-item align="left" label="时间类型" prop="_id">
        <el-select v-model="current_notify.timeType">
          <el-option value="before" :label="NOTIFY_TIME_TYPE['before']"/>
          <el-option value="after" :label="NOTIFY_TIME_TYPE['after']"/>
          <el-option value="specific" :label="NOTIFY_TIME_TYPE['specific']"/>
        </el-select>
      </el-form-item>
      <el-form-item align="left" label="时间长度" prop="name" v-show="current_notify.timeType === 'before' || current_notify.timeType === 'after'">
        <el-input v-model="current_notify.timeLength" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item align="left" label="具体时间" :label-width="formLabelWidth" v-show="current_notify.timeType === 'specific'">
        <el-time-picker
          v-model="current_notify.timePoint"
          placeholder="选择时间">
        </el-time-picker>
      </el-form-item>
      <el-form-item align="left" label="提醒类型">
        <el-select v-model="current_notify.notifyType">
          <el-option :label="NOTIFY_TYPE['message_queue']" value="message_queue"/>
          <el-option :label="NOTIFY_TYPE['system_alarm']" value="system_alarm"/>
          <el-option :label="NOTIFY_TYPE['short_message']" value="short_message"/>
        </el-select>
      </el-form-item>
      <el-form-item align="left" label="提醒等级">
        <el-select v-model="current_notify.notifyPriority">
          <el-option :label="NOTIFY_PRIORITY['high']" value="high"/>
          <el-option :label="NOTIFY_PRIORITY['middle']" value="middle"/>
          <el-option :label="NOTIFY_PRIORITY['low']" value="low"/>
        </el-select>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
  </span>
  </el-dialog>
  </div>
</template>
<script>
  import {mapGetters} from 'vuex'
//  import Util from '../store/utils'
  import ObjUtil from '../utils/ObjUtil'
  import {NOTIFY_TIME_TYPE, NOTIFY_TYPE, NOTIFY_PRIORITY} from '../store/common_defs'
  export default {
    components: {},
    name: 'edit_panel_notify_setting',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        this.$emit('settingCommited', this.current_notify)
      },
      cancelEdit () {
        this.$refs['roleForm'].resetFields()
        this.$emit('showSettingEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      }
    },
    watch: {
      dialogVisible: function (val, oldval) {
        if (val === true) {
          this.current_notify = ObjUtil.clone(this.edited_notify)
        }
      }
    },
    computed: {
      ...mapGetters([])
    },
    props: ['edited_notify', 'dialogVisible'],
    created: function () {
    },
    data: function () {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        NOTIFY_TIME_TYPE: NOTIFY_TIME_TYPE,
        NOTIFY_TYPE: NOTIFY_TYPE,
        NOTIFY_PRIORITY: NOTIFY_PRIORITY,
        current_notify: {}
      }
    }
  }
</script>
