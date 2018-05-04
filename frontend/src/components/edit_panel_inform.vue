<template>
  <div>
    <el-dialog title="编辑提醒" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
      <el-form :model="current_inform" :label-width="formLabelWidth" :label-position="labelPosition" ref="informForm"
      >
        <el-form-item label="通知名称">
          <el-input v-model="current_inform.name" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="通知内容" :label-width="formLabelWidth">
          <el-input v-model="current_inform.descr" auto-complete="off"></el-input>
        </el-form-item>
        <!--<el-form-item align="left">-->
          <!--<div>-->
            <!--<div style="display: inline-block">-->
              <!--<el-button @click="editInformer">选择通知发送人</el-button>-->
            <!--</div>-->
            <!--<div style="display: inline-block">-->
              <!--<span>  {{ current_inform.senderName }}</span>-->
            <!--</div>-->
          <!--</div>-->
        <!--</el-form-item>-->
        <!--<el-form-item align="left" label="通知方式">-->
          <!--<el-select v-model="current_inform.notifyType">-->
            <!--<el-option :label="NOTIFY_TYPE['message_queue']" value="message_queue"/>-->
            <!--<el-option :label="NOTIFY_TYPE['system_alarm']" value="system_alarm"/>-->
            <!--<el-option :label="NOTIFY_TYPE['short_message']" value="short_message"/>-->
          <!--</el-select>-->
        <!--</el-form-item>-->
        <el-form-item align="left" label="提醒等级">
          <el-select v-model="current_inform.notifyPriority">
            <el-option :label="NOTIFY_PRIORITY['high']" value="high"/>
            <el-option :label="NOTIFY_PRIORITY['middle']" value="middle"/>
            <el-option :label="NOTIFY_PRIORITY['low']" value="low"/>
          </el-select>
        </el-form-item>
        <el-form-item align="left" label="通知时间" :label-width="formLabelWidth">
          <el-date-picker
            v-model="current_inform.sendTime"
            type="datetime"
            placeholder="选择日期时间">
          </el-date-picker>
        </el-form-item>
        <el-form-item align="left">
          <div>
            <div style="display: inline-block;">
              <el-button @click="editInformee">选择被通知人</el-button>
            </div>
            <div style="display: inline-block;">
              <span>  {{ informeeList }}</span>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelEdit">取消</el-button>
        <el-button type="primary" @click="commitEdit">提交</el-button>
      </span>
    </el-dialog>
    <tree-user-select @selectedUser="selectInformeeOver" @showEdit="showInformeeEditOver" title="选择被通知人" :dialogVisible="showInformeeEdit" :selectedUser="current_inform.informUserList"></tree-user-select>
    <!--<tree-user-select @selectedUser="selectInformerOver" @showEdit="showInformerEditOver" title="选择通知发送人" :dialogVisible="showInformerEdit" :selectedUser="informerList"></tree-user-select>-->
  </div>
</template>
<script>
  import {mapGetters, mapActions} from 'vuex'
  import dateUtil from '../utils/DateUtil'
  import ObjUtil from '../utils/ObjUtil'
  import Util from '../store/utils'
  import {UPSERT_INFORM} from '../store/mutation_types'
  import {NOTIFY_TYPE, NOTIFY_PRIORITY} from '../store/common_defs'
  import TreeUserSelect from './tree_user_select.vue'
  export default {
    components: {TreeUserSelect},
    name: 'edit_panel_inform',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        this.current_inform.sendTime = dateUtil.getDatetimeSeconds(this.current_inform.sendTime)
        this.UPSERT_INFORM(this.current_inform)
        this.$refs['informForm'].resetFields()
        this.$emit('showEdit', false)
      },
      cancelEdit () {
        this.$refs['informForm'].resetFields()
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      editInformee () {
        this.showInformeeEdit = true
      },
      editInformer () {
        this.showInformerEdit = true
      },
      showInformeeEditOver () {
        this.showInformeeEdit = false
      },
      selectInformeeOver (user) {
        console.log(user)
        this.current_inform.informUserList = user
        this.showInformeeEdit = false
      },
      showInformerEditOver () {
        this.showInformerEdit = false
      },
      selectInformerOver (user) {
        if (user.length === 0) {
          this.current_inform.sender = ''
        } else {
          this.current_inform.sender = user[0]
        }
        this.current_inform.senderName = Util.getUserName(this.current_inform.sender)
        this.showInformerEdit = false
      },
      ...mapActions([UPSERT_INFORM])
    },
    watch: {
      dialogVisible: function (val, oldval) {
        if (val === true) {
          this.current_inform = ObjUtil.clone(this.edited_inform)
          this.current_inform.sendTime = new Date(this.current_inform.sendTime * 1000)
          this.current_inform.senderName = Util.getUserName(this.current_inform.sender)
        }
      }
    },
    computed: {
      ...mapGetters([]),
      informeeList () {
        var data = []
        var idList = this.current_inform.informUserList
        if (idList === undefined) {
          return ''
        }
        for (var i = 0, len = idList.length; i < len; i++) {
          data.push(Util.getUserName(idList[i]))
        }
        return data.join(', ')
      },
      informerList () {
        var data = []
        if (this.current_inform.sender !== '') {
          data.push(this.current_inform.sender)
        }
        return data
      }
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
        current_inform: {},
        showInformeeEdit: false,
        showInformerEdit: false
      }
    }
  }
</script>
