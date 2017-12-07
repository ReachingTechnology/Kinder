<template>
  <div>
  <el-dialog title="提醒设置列表" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <div align="left">
      <el-button size="large"
                 @click="handleCreate()" type="success">
        添加新提醒设置
      </el-button>
      <el-button size="large" class="horizontal-btn"
                 @click="handleDelete()" type="success">
        删除选中提醒
      </el-button>
    </div>
    <br/>
    <el-table
      :data="notifySettings"
      style="width: 100%"
      @selection-change="handleSelectionChange"
      :row-class-name="tableRowClassName">
      <el-table-column
        type="index"
        sortable>
      </el-table-column>
      <el-table-column
        prop="timeTypeDisplay"
        label="时间类型"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="timeDisplay"
        label="时间"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="notifyTypeDisplay"
        label="提醒类型"
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
      <el-table-column
        type="selection"
        width="55">
      </el-table-column>
    </el-table>
    <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
  </span>
  </el-dialog>
  <edit-panel-notify-setting @showSettingEdit="showEditOver" @settingCommited="settingCommited" :edited_notify="selected_notify" :dialogVisible="showSettingEdit"></edit-panel-notify-setting>
  </div>
</template>
<script>
  import {mapGetters} from 'vuex'
//  import Util from '../store/utils'
  import ArrayUtil from '../utils/ArrayUtil'
  import EditPanelNotifySetting from './edit_panel_notify_setting.vue'
  import {NOTIFY_TIME_TYPE, NOTIFY_TYPE} from '../store/common_defs'
  import dateUtil from '../utils/DateUtil'
  import Moment from 'moment'

  export default {
    components: {EditPanelNotifySetting},
    name: 'table_notify_setting_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleSelectionChange (val) {
        this.multipleSelection = val
      },
      commitEdit () {
        this.$emit('notifySettingListCommitted', this.notifySettings)
      },
      cancelEdit () {
        this.$emit('showNotifySettingEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      handleCreate () {
        this.selected_notify = {}
        this.selected_notify.timeType = ''
        this.selected_notify.timeLength = 10
        this.selected_notify.timePoint = ''
        this.selected_notify.notifyType = ''
        this.selected_notify.notifyPriority = ''
        this.currentEditIndex = -1
        this.isCreatingNewSetting = true
        this.showSettingEdit = true
      },
      handleEdit (index, row) {
        this.selected_notify = row
        this.currentEditIndex = index
        this.isCreatingNewSetting = false
        this.showSettingEdit = true
      },
      handleDelete () {
        console.log(this.notifySettings)
        console.log(this.multipleSelection)
        for (var i = 0, len = this.multipleSelection.length; i < len; i++) {
          for (var j = 0, len2 = this.notifySettings.length; j < len2; j++) {
            if (this.notifySettings[j].timeType === this.multipleSelection[i].timeType &&
              this.notifySettings[j].timeLength === this.multipleSelection[i].timeLength &&
              this.notifySettings[j].timePoint === this.multipleSelection[i].timePoint &&
              this.notifySettings[j].notifyType === this.multipleSelection[i].notifyType &&
              this.notifySettings[j].notifyPriority === this.multipleSelection[i].notifyPriority) {
              this.notifySettings.splice(j, 1)
              break
            }
          }
        }
      },
      showEditOver () {
        this.showSettingEdit = false
      },
      settingCommited (val) {
        val.timeTypeDisplay = this.NOTIFY_TIME_TYPE[val.timeType]
        val.notifyTypeDisplay = this.NOTIFY_TYPE[val.notifyType]
        val.timePoint = dateUtil.getDatetimeSeconds(val.timePoint)
        if (val.timeType === 'specific') {
          val.timeDisplay = Moment(val.timePoint * 1000).format('H:mm')
        } else {
          val.timeDisplay = val.timeLength + ' 分钟'
        }
        if (this.isCreatingNewSetting) {
          this.notifySettings.push(val)
        } else {
          if (this.currentEditIndex >= 0) {
            this.$set(this.notifySettings, this.currentEditIndex, val)
          }
        }
        this.showSettingEdit = false
      }
    },
    watch: {
      dialogVisible: function (val, oldval) {
        if (val === true) {
          this.notifySettings = ArrayUtil.clone(this.settings)
          for (var i = 0, len = this.notifySettings.length; i < len; i++) {
            this.notifySettings[i].timeTypeDisplay = this.NOTIFY_TIME_TYPE[this.notifySettings[i].timeType]
            this.notifySettings[i].notifyTypeDisplay = this.NOTIFY_TYPE[this.notifySettings[i].notifyType]
            if (this.notifySettings[i].timeType === 'specific') {
              this.notifySettings[i].timeDisplay = this.notifySettings[i].timePoint
            } else {
              this.notifySettings[i].timeDisplay = this.notifySettings[i].timeLength + ' 分钟'
            }
          }
        }
      }
    },
    computed: {
      ...mapGetters([])
    },
    props: ['settings', 'dialogVisible'],
    created: function () {
    },
    data: function () {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        NOTIFY_TIME_TYPE: NOTIFY_TIME_TYPE,
        NOTIFY_TYPE: NOTIFY_TYPE,
        notifySettings: [],
        selected_notify: {},
        multipleSelection: [],
        showSettingEdit: false,
        isCreatingNewSetting: false,
        currentEditIndex: -1
      }
    }
  }
</script>
