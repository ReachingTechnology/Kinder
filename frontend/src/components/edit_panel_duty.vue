<template>
  <div>
  <el-dialog title="编辑任务" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <el-form :model="current_edited_duty"  :label-width="formLabelWidth" :label-position="labelPosition" ref="dutyForm" :rules="rules">
      <el-form-item label="任务名称" prop="name">
        <el-input v-model="current_edited_duty.name" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="任务描述" :label-width="formLabelWidth">
        <el-input v-model="current_edited_duty.descr" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item align="left" label="任务类别" :required="true">
        <el-select v-model="current_edited_duty.category">
          <el-option v-for="cat in allDutyCategory" :label="cat.name" :value="cat._id"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="执行时间类型" align="left" :label-width="formLabelWidth">
        <el-select v-model="current_edited_duty.timeType">
          <el-option label="日常" :value="DUTY_TIME_TYPE_ROUTINE"></el-option>
          <el-option label="定期" :value="DUTY_TIME_TYPE_PERIODICAL"></el-option>
          <el-option label="特定时间" :value="DUTY_TIME_TYPE_SPECIFIC"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item align="left" label="定期类型" @change="handlePeriodTypeChanged" v-show="isTimeTypePeriod()">
        <el-select v-model="current_edited_duty.periodType">
          <el-option label="每周" :value="DUTY_PERIOD_TYPE_WEEK"></el-option>
          <el-option label="每月" :value="DUTY_PERIOD_TYPE_MONTH"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item align="left" label="选择日期" prop="selectedWeekDays" v-show="isPeriodTypeWeek()">
        <el-checkbox-group v-model="current_edited_duty.selectedWeekDays" @change="handleCheckedWeekDaysChange">
          <el-checkbox label="周一" key="DUTY_PERIOD_WEEK_0"></el-checkbox>
          <el-checkbox label="周二" key="DUTY_PERIOD_WEEK_1"></el-checkbox>
          <el-checkbox label="周三" key="DUTY_PERIOD_WEEK_2"></el-checkbox>
          <el-checkbox label="周四" key="DUTY_PERIOD_WEEK_3"></el-checkbox>
          <el-checkbox label="周五" key="DUTY_PERIOD_WEEK_4"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item align="left" label="选择日期" prop="selectedMonthDays" v-show="isPeriodTypeMonth()">
        <el-checkbox-group v-model="current_edited_duty.selectedMonthDays" @change="handleCheckedMonthDaysChange">
          <el-checkbox v-for="i in 31" :label="i + ''" :key="DUTY_PERIOD_MONTH_PREFIX + i" :value="DUTY_PERIOD_MONTH_PREFIX + i"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item align="left" label="选择日期" prop="dateRange" v-show="isTimeTypeSpecific()">
        <el-date-picker
          v-model="current_edited_duty.dateRange"
          type="daterange"
          placeholder="选择日期范围">
        </el-date-picker>
      </el-form-item>
      <el-form-item align="left" label="选择任务时间" prop="timeRange" v-show="!isTimeTypeSpecific()">
        <el-time-picker
          is-range
          v-model="current_edited_duty.timeRange"
          placeholder="选择时间区间">
        </el-time-picker>
      </el-form-item>
      <el-form-item align="left" label="消息提醒" prop="notify_user">
        <div>
          <el-switch align="left" style="display: inline-block"
            v-model="current_edited_duty.notify_user"
            >
          </el-switch>
          <el-button align="right" style="display: inline-block" v-show="current_edited_duty.notify_user" @click="editNotifyUser">设置</el-button>
        </div>
      </el-form-item>
      <el-form-item align="left" label="职责完成情况提醒" prop="notify_manager">
        <div>
          <el-switch style="display: inline-block"
            v-model="current_edited_duty.notify_manager">
          </el-switch>
          <el-button style="display: inline-block" v-show="current_edited_duty.notify_manager" @click="editNotifyManager">设置</el-button>
        </div>
      </el-form-item>
      <el-form-item align="left" label="相关岗位" prop="selectedRoleNames">
        <el-checkbox-group v-model="current_edited_duty.selectedRoleNames" @change="handleCheckedRolesChange">
          <el-checkbox v-for="item in allRole" :label="item.name" :key="item._id"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
  </span>
  </el-dialog>
  <table-notify-setting-list @notifySettingListCommitted="notifySettingListCommitted" @showNotifySettingEdit="showEditOver" :settings="this.current_edited_duty.notify_user_setting_list" :dialogVisible="showEditNotifyUser"></table-notify-setting-list>
    <table-notify-setting-list @notifySettingListCommitted="notifySettingListCommitted" @showNotifySettingEdit="showEditOver" :settings="this.current_edited_duty.notify_manager_setting_list" :dialogVisible="showEditNotifyManager"></table-notify-setting-list>
  </div>
</template>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { UPSERT_DUTY } from '../store/mutation_types'
  import dateUtil from '../utils/DateUtil'
  import Util from '../store/utils'
  import ObjUtil from '../utils/ObjUtil'
  import ArrayUtil from '../utils/ArrayUtil'
  import TableNotifySettingList from './table_notify_setting_list.vue'
  import { WEEK_DAYS, DUTY_TIME_TYPE_ROUTINE, DUTY_TIME_TYPE_PERIODICAL, DUTY_TIME_TYPE_SPECIFIC, DUTY_PERIOD_TYPE_WEEK, DUTY_PERIOD_TYPE_MONTH, DUTY_PERIOD_MONTH_PREFIX } from '../store/common_defs'

  export default {
    components: {TableNotifySettingList},
    name: 'duty_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      isTimeTypeSpecific () {
        return this.current_edited_duty.timeType === DUTY_TIME_TYPE_SPECIFIC
      },
      isTimeTypePeriod () {
        return this.current_edited_duty.timeType === DUTY_TIME_TYPE_PERIODICAL
      },
      isPeriodTypeMonth () {
        return this.current_edited_duty.timeType === DUTY_TIME_TYPE_PERIODICAL && this.current_edited_duty.periodType === DUTY_PERIOD_TYPE_MONTH
      },
      isPeriodTypeWeek () {
        return this.current_edited_duty.timeType === DUTY_TIME_TYPE_PERIODICAL && this.current_edited_duty.periodType === DUTY_PERIOD_TYPE_WEEK
      },
      handlePeriodTypeChanged (value) {
        this.current_edited_duty.periodType = value
      },
      handleCheckedRolesChange (value) {
        this.current_edited_duty.roles = []
        for (var i = 0, len = value.length; i < len; i++) {
          let id = Util.getRoleId(value[i])
          this.current_edited_duty.roles.push(id)
        }
      },
      handleCheckedWeekDaysChange (value) {
        console.log('handleCheckedWeekDaysChange')
        console.log(value)
        this.current_edited_duty.selectedWeekDays = value
      },
      handleCheckedMonthDaysChange (value) {
        this.current_edited_duty.selectedMonthDays = value
      },
      computeDatetime (duty) {
        if (duty.timeType === DUTY_TIME_TYPE_SPECIFIC) {
          let st = duty.dateRange[0]
          let et = duty.dateRange[1]
          duty.starttime = dateUtil.getDatetimeSeconds(st)
          duty.endtime = dateUtil.getDatetimeSeconds(et)
          console.log('for specific time, start:')
          console.log(duty.starttime)
        } else {
          let st = duty.timeRange[0]
          let et = duty.timeRange[1]
          let startofyesterday = dateUtil.getStartOfToday() - 3600 * 24
          console.log(startofyesterday)
          console.log('&&&&&&')
          console.log(dateUtil.getDatetimeSeconds(st))
          duty.starttime = dateUtil.getDatetimeSeconds(st) - startofyesterday
          duty.endtime = dateUtil.getDatetimeSeconds(et) - startofyesterday
          console.log('for other time, start:')
          console.log(duty.starttime)
        }
      },
      getPeriodDate (periodType, labels) {
        var result = []
        if (periodType === DUTY_PERIOD_TYPE_WEEK) {
          for (var i = 0, len = labels.length; i < len; i++) {
            result.push(WEEK_DAYS[labels[i]])
          }
        } else if (periodType === DUTY_PERIOD_TYPE_MONTH) {
          for (var j = 0, len2 = labels.length; j < len2; j++) {
            result.push(DUTY_PERIOD_MONTH_PREFIX + labels[j])
          }
        }
        return result
      },
      getLabels (periodType, periodDate) {
        var result = []
        if (periodType === DUTY_PERIOD_TYPE_WEEK) {
          var keys = Object.keys(WEEK_DAYS)
          for (var i = 0, len = keys.length; i < len; i++) {
            if (ArrayUtil.in_array(WEEK_DAYS[keys[i]], periodDate)) {
              result.push(keys[i])
            }
          }
        } else if (periodType === DUTY_PERIOD_TYPE_MONTH) {
          for (var j = 0, len2 = periodDate.length; j < len2; j++) {
            result.push(periodDate[j].substr(17))
          }
        }
        return result
      },
      commitEdit () {
        this.edited_duty = ObjUtil.clone(this.current_edited_duty)
        this.$refs['dutyForm'].validate((valid) => {
          if (valid) {
            this.computeDatetime(this.edited_duty)
            if (this.edited_duty.timeType === DUTY_TIME_TYPE_PERIODICAL) {
              if (this.edited_duty.periodType === DUTY_PERIOD_TYPE_WEEK) {
                this.edited_duty.periodDate = this.getPeriodDate(this.edited_duty.periodType, this.edited_duty.selectedWeekDays)
              } else {
                this.edited_duty.periodDate = this.getPeriodDate(this.edited_duty.periodType, this.edited_duty.selectedMonthDays)
              }
            }
            this.UPSERT_DUTY(this.edited_duty)
            this.current_edited_duty = this.edited_duty
            this.$emit('showEdit', false)
          }
        })
      },
      cancelEdit () {
        this.$refs['dutyForm'].resetFields()
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      editNotifyUser () {
        this.showEditNotifyUser = true
      },
      editNotifyManager () {
        this.showEditNotifyManager = true
      },
      showEditOver () {
        if (this.showEditNotifyUser) {
          this.showEditNotifyUser = false
        }
        if (this.showEditNotifyManager) {
          this.showEditNotifyManager = false
        }
      },
      notifySettingListCommitted (val) {
        if (this.showEditNotifyUser) {
          this.current_edited_duty.notify_user_setting_list = val
          this.showEditNotifyUser = false
        }
        if (this.showEditNotifyManager) {
          this.current_edited_duty.notify_manager_setting_list = val
          this.showEditNotifyManager = false
        }
      },
      ...mapActions([ UPSERT_DUTY ])
    },
    computed: {
      ...mapGetters(['allRole', 'allDutyCategory'])
    },
    watch: {
      dialogVisible: function (val, oldval) {
        if (val) {
          this.current_edited_duty = ObjUtil.clone(this.edited_duty)
          if (this.current_edited_duty.timeType === DUTY_TIME_TYPE_PERIODICAL) {
            if (this.edited_duty.periodType === DUTY_PERIOD_TYPE_WEEK) {
              this.current_edited_duty.selectedWeekDays = this.getLabels(this.edited_duty.periodType, this.edited_duty.periodDate)
            } else {
              this.current_edited_duty.selectedMonthDays = this.getLabels(this.edited_duty.periodType, this.edited_duty.periodDate)
            }
          } else {
            this.current_edited_duty.selectedWeekDays = []
            this.current_edited_duty.selectedMonthDays = []
          }
        }
      }
    },
    props: ['edited_duty', 'dialogVisible'],
    created: function () {
    },
    data: function () {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        rules: {
          name: [
            { required: true, message: '职责名称不能为空', trigger: 'blur' }
          ]
//          selectedRoleNames: [
//            { type: 'array', required: true, message: '请至少选择一个岗位', trigger: 'blur' }
//          ]
        },
        current_edited_duty: {},
        DUTY_TIME_TYPE_ROUTINE: DUTY_TIME_TYPE_ROUTINE,
        DUTY_TIME_TYPE_PERIODICAL: DUTY_TIME_TYPE_PERIODICAL,
        DUTY_TIME_TYPE_SPECIFIC: DUTY_TIME_TYPE_SPECIFIC,
        DUTY_PERIOD_TYPE_WEEK: DUTY_PERIOD_TYPE_WEEK,
        DUTY_PERIOD_TYPE_MONTH: DUTY_PERIOD_TYPE_MONTH,
        DUTY_PERIOD_MONTH_PREFIX: DUTY_PERIOD_MONTH_PREFIX,
        showEditNotifyUser: false,
        showEditNotifyManager: false
      }
    }
  }
</script>
