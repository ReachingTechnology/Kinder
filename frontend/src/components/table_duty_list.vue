<template>
  <div>
    <h2>幼儿园岗位职责列表</h2>
    <div align="left" style="width:100%">
      <el-button size="large" class="horizontal-btn"
                 @click="handleCreate()" type="success">
        添加新职责
      </el-button>
      <el-button size="large" class="horizontal-btn"
                 @click="handleDelete()" type="success">
        删除选中职责
      </el-button>
      <div class="horizontal-btn-right" id="select_role">
      <el-form>
      <el-form-item label="选择岗位">
        <el-select v-model="currentRoleId" >
          <el-option label="所有" :value="ROOT_ROLE"></el-option>
          <el-option v-for="role in allRole" :label="role.name" :value="role._id"></el-option>
        </el-select>
      </el-form-item>
      </el-form>
      </div>
    </div>
    <br/>
    <el-table
      :data="duties"
      style="width: 100%"
      :default-sort = "{prop: '_id', order: 'ascending'}"
      @selection-change="handleSelectionChange"
      :row-class-name="tableRowClassName">
      <!--<el-table-column-->
        <!--prop="_id"-->
        <!--label="职责编号"-->
        <!--align="center"-->
        <!--sortable>-->
      <!--</el-table-column>-->
      <el-table-column
        prop="name"
        label="职责名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="descr"
        label="职责描述"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="categoryName"
        label="职责类别"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="roleNames_display"
        label="相关岗位"
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
    <duty-edit-panel @showEdit="showEditOver" :isCreating="isCreating" :dialogVisible="showEdit" :edited_duty="selectedDuty" ></duty-edit-panel>
  </div>
</template>
<style>
  .el-table .info-row {
    background: #c9e5f5;
  }

  .el-table .positive-row {
    background: #e2f0e4;
  }

  .horizontal-btn {
    display: inline-block;
  }

  .horizontal-btn-right {
    display: inline-block;
    float: right;
  }

  #select_role .el-form-item__label {
    display: inline-block;
  }

  #select_role .el-form-item__content {
    display: inline-block;
  }

</style>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { GET_ALL_DUTY, REMOVE_DUTIES } from '../store/mutation_types'
  import DutyEditPanel from './edit_panel_duty.vue'
  import Util from '../store/utils'
  import Moment from 'moment'
  import dateUtil from '../utils/DateUtil'
  import { ROOT_ROLE, DUTY_TIME_TYPE_SPECIFIC } from '../store/common_defs'

  export default {
    name: 'table_duty_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleSelectionChange (val) {
        this.multipleSelection = val
      },
      getDutiesForRole (roleid) {
        this.currentDutyList = []
        if (roleid === this.ROOT_ROLE) {
          this.currentDutyList = this.allDuty
        } else {
          for (var i = 0, len = this.allDuty.length; i < len; i++) {
            var rolesForDuty = this.allDuty[i].roles
            if (rolesForDuty.indexOf(roleid) >= 0) {
              this.currentDutyList.push(this.allDuty[i])
            }
          }
        }
      },
      handleDutyChange (command) {
        this.getDutiesForRole(command)
      },
      handleEdit (index, row) {
        this.selectedDuty = {}
        for (var i = 0, len = this.allDuty.length; i < len; i++) {
          if (this.allDuty[i]._id === row._id) {
            this.selectedDuty = this.allDuty[i]
            this.selectedDuty.selectedWeekDays = []
            this.selectedDuty.selectedMonthDays = []
            if (this.selectedDuty.notify_user === undefined) {
              this.selectedDuty.notify_user = false
            }
            if (this.selectedDuty.notify_user_setting_list === undefined) {
              this.selectedDuty.notify_user_setting_list = []
            }
            if (this.selectedDuty.notify_manager === undefined) {
              this.selectedDuty.notify_manager = false
            }
            if (this.selectedDuty.notify_manager_setting_list === undefined) {
              this.selectedDuty.notify_manager_setting_list = []
            }
            this.isCreating = false
            this.showEdit = true
            console.log(this.selectedDuty)
            break
          }
        }
      },
      handleCreate () {
        let startofyesterday = dateUtil.getStartOfToday() - 3600 * 24
        let timeRangeStart = new Date((startofyesterday + 8 * 3600) * 1000)
        let timeRangeEnd = new Date((startofyesterday + 9 * 3600) * 1000)
        let dateRangeStart = new Date()
        let dateRangeEnd = dateRangeStart
        this.selectedDuty = {
          '_id': '',
          'name': '',
          'descr': '',
          'category': '',
          'starttime': '',
          'endtime': '',
          'timeRange': [timeRangeStart, timeRangeEnd],
          'dateRange': [dateRangeStart, dateRangeEnd],
          'roles': [],
          'selectedRoleNames': [],
          'timeType': '',
          'periodType': '',
          'periodDate': [],
          'selectedWeekDays': [],
          'selectedMonthDays': [],
          'notify_user': false,
          'notify_manager': false,
          'notify_user_setting_list': [],
          'notify_manager_setting_list': []
        }
        this.isCreating = true
        this.showEdit = true
      },
      handleDelete () {
        let duties = []
        for (var i = 0, len = this.multipleSelection.length; i < len; i++) {
          duties.push(this.multipleSelection[i]._id)
        }
        this.REMOVE_DUTIES(duties)
      },
      showEditOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_DUTY, REMOVE_DUTIES])
    },
    computed: {
      ...mapGetters(['allRole', 'allDuty', 'dutyForRoles']),

      duties () {
        var data = this.dutyForRoles[this.currentRoleId]
        if (data === undefined) {
          data = this.allDuty
        }
        for (var i = 0, len = data.length; i < len; i++) {
          var duty = data[i]
          duty.selectedRoleNames = []
          for (var j = 0, len2 = duty.roles.length; j < len2; j++) {
            var rolename = Util.getRoleName(duty.roles[j])
            duty.selectedRoleNames.push(rolename)
          }
          duty.roleNames_display = duty.selectedRoleNames.join(',')
          if (duty.timeType === DUTY_TIME_TYPE_SPECIFIC) {
            let st = new Date(duty.starttime * 1000)
            let et = new Date(duty.endtime * 1000)
            duty.dateRange = [st, et]
          } else {
            let st = new Date(duty.starttime * 1000)
            let et = new Date(duty.endtime * 1000)
            duty.timeRange = [st, et]
          }
          duty.categoryName = Util.getDutyCategoryNameById(duty.category)
        }
        return data
      },
      ROOT_ROLE () {
        return ROOT_ROLE
      }
    },
    created: function () {
      this.GET_ALL_DUTY()
    },
    data: () => {
      return {
        showEdit: false,
        selectedDuty: {},
        currentRoleId: '',
        currentDutyList: this.duties,
        multipleSelection: [],
        isCreating: false
      }
    },
    components: {
      DutyEditPanel
    }
  }
</script>
