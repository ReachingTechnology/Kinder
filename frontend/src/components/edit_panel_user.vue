<template>
  <div>
    <el-dialog title="编辑用户" :visible.sync="dialogVisible" :close-on-click-modal="false" @close="handleClose">
      <el-form :model="edited_user"  :label-width="formLabelWidth" :label-position="labelPosition" ref="userForm" :rules="rules">
        <el-form-item label="员工编号" prop="_id">
          <el-input v-model="edited_user._id" auto-complete="off" :disabled="!isCreating"></el-input>
        </el-form-item>
        <el-form-item label="员工姓名" prop="name">
          <el-input v-model="edited_user.name" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机号" :label-width="formLabelWidth" prop="cellphone">
          <el-input v-model="edited_user.cellphone" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item align="left" label="性别" :required="true">
          <el-select v-model="edited_user.sex">
            <el-option label="男" value="Male"></el-option>
            <el-option label="女" value="Female"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item align="left" label="员工岗位" prop="role">
          <el-checkbox-group v-model="checkedRoleNames" @change="handleCheckedRoleChange" :disabled="!Util.hasCategoryPermission('PERMISSION_CATEGORY_USER')">
            <el-checkbox v-for="role in allRole" :name="role.name" :label="role.name"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item align="left">
          <el-button @click="editDuty">编辑职责</el-button>
        </el-form-item>
        <el-form-item align="left">
          <div>
            <div style="display: inline-block;">
              <el-button @click="editLeader">直接汇报人</el-button>
            </div>
            <div style="display: inline-block;">
              <span> {{ leaderName }}</span>
            </div>
          </div>
        </el-form-item>
        <el-form-item align="left" label="出生日期">
          <el-date-picker
            v-model="edited_user.birthday"
            type="date"
            placeholder="选择出生日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="edited_user.password" placeholder="默认与手机号一致" auto-complete="off"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
  </span>
    </el-dialog>
    <tree-duty-select @showEdit="showEditOver" :edited_user="edited_user" :dialogVisible="showDutyEdit" :userDuties="userDuties"></tree-duty-select>
    <tree-user-select @selectedUser="selectUserOver" @showEdit="showEditOver" title="选择直接汇报人" :dialogVisible="showLeaderEdit" :selectedUser="leader"></tree-user-select>
  </div>
</template>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { UPSERT_USER_ACCOUNT } from '../store/mutation_types'
  import Util from '../store/utils'
  import ArrayUtil from '../utils/ArrayUtil'
  import TreeDutySelect from './tree_duty_select.vue'
  import TreeUserSelect from './tree_user_select.vue'
  import ObjUtil from '../utils/ObjUtil'

  export default {
    components: {TreeDutySelect, TreeUserSelect},
    name: 'user_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      addDutyByRole (duty, roleIds) {
        for (var i = 0, len = roleIds.length; i < len; i++) {
          var roleDuties = Util.getDutiesByRoleId(roleIds[i])
          for (var j = 0, len2 = roleDuties.length; j < len2; j++) {
            if (!ArrayUtil.in_array(roleDuties[j]._id, duty)) {
              duty.push(roleDuties[j]._id)
              console.log(duty)
            }
          }
        }
      },
      removeDutyByRole (duty, roleIds) {
        for (var i = 0, len = roleIds.length; i < len; i++) {
          var roleDuties = Util.getDutiesByRoleId(roleIds[i])
          for (var j = 0, len2 = roleDuties.length; j < len2; j++) {
            if (ArrayUtil.in_array(roleDuties[j]._id, duty)) {
              ArrayUtil.remove(roleDuties[j]._id, duty)
            }
          }
        }
      },
      handleCheckedRoleChange (value) {
        this.checkedRoleNames = value
        var oldRoles = this.edited_user.role
        this.edited_user.role = []
        for (var j = 0; j < this.checkedRoleNames.length; j++) {
          var roleid = Util.getRoleId(this.checkedRoleNames[j])
          this.edited_user.role.push(roleid)
        }
        var added = ArrayUtil.diff(this.edited_user.role, oldRoles)
        var removed = ArrayUtil.diff(oldRoles, this.edited_user.role)
        this.addDutyByRole(this.edited_user.duty, added)
        this.removeDutyByRole(this.edited_user.duty, removed)

      },
      commitEdit () {
        this.current_edited_user = ObjUtil.clone(this.edited_user)
        this.$refs['userForm'].validate((valid) => {
          if (valid) {
            this.current_edited_user.checkedRoleNames = this.checkedRoleNames
            this.UPSERT_USER_ACCOUNT(this.current_edited_user)
            this.edited_user = this.current_edited_user
            this.$emit('showEdit', false)
          }
        })
      },
      cancelEdit () {
        this.$refs['userForm'].resetFields()
        this.$emit('showEdit', false)
      },
      getDutyIdsByRole (role) {
        var result = []
        for (var i = 0, len = role.length; i < len; i++) {
          var duties = this.dutyForRoles[role[i]]
          if (duties !== undefined) {
            for (var j = 0, len2 = duties.length; j < len2; j++) {
              if (!ArrayUtil.in_array(duties[j]._id, result)) {
                result.push(duties[j]._id)
              }
            }
          }
        }
        return result
      },
      editDuty () {
        if (this.edited_user.duty === undefined || this.edited_user.duty.length === 0) {
          this.edited_user.duty = this.getDutyIdsByRole(this.edited_user.role)
        }
        this.userDuties = this.edited_user.duty
        this.showDutyEdit = true
      },
      handleClose () {
        this.cancelEdit()
      },
      showEditOver () {
        if (this.showDutyEdit) {
          this.showDutyEdit = false
        } else if (this.showLeaderEdit) {
          this.showLeaderEdit = false
        }
      },
      editLeader () {
        this.leader = []
        this.leader.push(this.edited_user.leader)
        this.showLeaderEdit = true
      },
      selectUserOver (user) {
        if (this.showLeaderEdit) {
          if (user.length > 0) {
            this.edited_user.leader = user[0]
          } else {
            this.edited_user.leader = ''
          }
          this.showLeaderEdit = false
        }
      },
      ...mapActions([ UPSERT_USER_ACCOUNT ])
    },
    computed: {
      ...mapGetters(['allRole', 'dutyForRoles']),
      Util () {
        return Util
      },
      leaderName () {
        return Util.getUserName(this.edited_user.leader)
      }
    },
    props: ['edited_user', 'dialogVisible', 'isCreating'],
    watch: {
      dialogVisible: function (val, oldval) {
        if (val === true) {
          this.checkedRoleNames = this.edited_user.checkedRoleNames
        }
      }
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        rules: {
          _id: [
            { required: true, message: '员工编号不能为空', trigger: 'blur' }
          ],
          name: [
            { required: true, message: '员工姓名不能为空', trigger: 'blur' }
          ],
          cellphone: [
            { required: true, message: '手机号不能为空', trigger: 'blur' },
            { min: 11, max: 11, message: '手机号必须是11位数字', trigger: 'blur' }
          ],
          role: [
            { type: 'array', required: true, message: '请选择员工岗位', trigger: 'blur' }
          ]
        },
        checkedRoleNames: [],
        showDutyEdit: false,
        userDuties: [],
        current_edited_user: {},
        leader: [],
        showLeaderEdit: false
      }
    }
  }
</script>
