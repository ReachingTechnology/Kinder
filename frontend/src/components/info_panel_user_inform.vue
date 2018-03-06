<template>
  <div>
    <el-dialog title="通知详情" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
      <el-form :model="current_inform" :label-width="formLabelWidth" :label-position="labelPosition" ref="informForm"
      >
        <el-form-item label="通知名称">
          <!--<el-input v-model="current_inform.name" disabled="true" auto-complete="off"></el-input>-->
          <span>{{ current_inform.name }}</span>
        </el-form-item>
        <el-form-item align="left" label="通知内容" :label-width="formLabelWidth">
          <!--<el-input v-model="current_inform.descr" disabled="true" auto-complete="off"></el-input>-->
          <span>{{ current_inform.descr }}</span>
        </el-form-item>
        <el-form-item align="left" label="提醒等级">
          <el-select disabled="true" v-model="current_inform.notifyPriority">
            <el-option :label="NOTIFY_PRIORITY['high']" value="high"/>
            <el-option :label="NOTIFY_PRIORITY['middle']" value="middle"/>
            <el-option :label="NOTIFY_PRIORITY['low']" value="low"/>
          </el-select>
        </el-form-item>
        <el-form-item align="left" label="通知时间" :label-width="formLabelWidth">
          <!--<el-input v-model="current_inform.sendTimeDisplay" disabled="true" auto-complete="off"></el-input>-->
          <span>{{ current_inform.sendTimeDisplay }}</span>
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
        this.$refs['informForm'].resetFields()
        this.$emit('showEdit', false)
      },
      ...mapActions([])
    },
    watch: {
      dialogVisible: function (val, oldval) {
        if (val === true) {
          this.current_inform = ObjUtil.clone(this.edited_inform)
          this.current_inform.sendTimeDisplay = Moment(this.current_inform.sendTime * 1000).format('YYYY年M月D日 H:mm')
        }
      }
    },
    computed: {
      ...mapGetters([])
    },
    props: ['edited_inform', 'dialogVisible'],
    created: function () {
    },
    data: function () {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        NOTIFY_TYPE: NOTIFY_TYPE,
        NOTIFY_PRIORITY: NOTIFY_PRIORITY,
        current_inform: {}
      }
    }
  }
</script>
