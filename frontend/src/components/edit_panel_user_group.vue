<template>
  <div>
    <el-dialog title="编辑小组" :visible.sync="dialogVisible" :close-on-click-modal="false" @close="handleClose">
      <el-form :model="edited_user_group"  :label-width="formLabelWidth" :label-position="labelPosition" ref="userGroupForm" :rules="rules">
        <el-form-item label="小组名称" prop="name">
          <el-input v-model="edited_user_group.name" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="小组工作描述" :label-width="formLabelWidth" prop="cellphone">
          <el-input v-model="edited_user_group.cellphone" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item align="left">
          <div>
            <div style="display: inline-block;">
              <el-button @click="editLeader">选择负责人</el-button>
            </div>
            <div style="display: inline-block;">
              <span>  {{ leaderName }}</span>
            </div>
          </div>
        </el-form-item>
        <el-form-item align="left">
          <el-button @click="editMember">选择小组成员</el-button>
        </el-form-item>
        <el-form-item align="left">
          <el-button @click="editDuty">编辑职责</el-button>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
  </span>
    </el-dialog>
    <tree-user-select @selectedUser="selectUserOver" @showEdit="showEditOver" title="选择负责人" :dialogVisible="showLeaderEdit" :selectedUser="leader"></tree-user-select>
    <tree-user-select @selectedUser="selectUserOver" @showEdit="showEditOver" title="选择小组成员" :dialogVisible="showMemberEdit" :selectedUser="members"></tree-user-select>
    <tree-duty-select @dutySelected="selectDutyOver" @showEdit="showEditOver" :dialogVisible="showDutyEdit" :selectedDuties="userGroupDuties"></tree-duty-select>
  </div>
</template>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { UPSERT_USER_GROUP } from '../store/mutation_types'
  import Util from '../store/utils'
  import ArrayUtil from '../utils/ArrayUtil'
  import TreeUserSelect from './tree_user_select.vue'
  import TreeDutySelect from './tree_duty_select.vue'
  import ObjUtil from '../utils/ObjUtil'
  import { DUTY_CAT_PREFIX } from '../store/common_defs'

  export default {
    components: {TreeUserSelect, TreeDutySelect},
    name: 'user_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        this.current_edited_user_group = ObjUtil.clone(this.edited_user_group)
        this.$refs['userGroupForm'].validate((valid) => {
          if (valid) {
            this.UPSERT_USER_GROUP(this.current_edited_user_group)
            this.edited_user_group = this.current_edited_user_group
            this.$emit('showEdit', false)
          }
        })
      },
      cancelEdit () {
        this.$refs['userGroupForm'].resetFields()
        this.$emit('showEdit', false)
      },
      editLeader () {
        this.leader = []
        this.leader.push(this.edited_user_group.leader)
        this.showLeaderEdit = true
      },
      editMember () {
        this.members = []
        this.members = this.edited_user_group.members
        if (!ArrayUtil.in_array(this.edited_user_group.leader, this.edited_user_group.members)) {
          this.edited_user_group.members.push(this.edited_user_group.leader)
        }
        this.showMemberEdit = true
      },
      editDuty () {
        if (this.edited_user_group.duty === undefined) {
          this.edited_user_group.duty = []
        }
        this.userGroupDuties = this.edited_user_group.duty
        this.showDutyEdit = true
      },
      handleClose () {
        this.cancelEdit()
      },
      showEditOver () {
        if (this.showLeaderEdit) {
          this.showLeaderEdit = false
        } else if (this.showMemberEdit) {
          this.showMemberEdit = false
        } else if (this.showDutyEdit) {
          this.showDutyEdit = false
        }
      },
      selectUserOver (user) {
        if (this.showLeaderEdit) {
          if (user.length > 0) {
            this.edited_user_group.leader = user[0]
          } else {
            this.edited_user_group.leader = ''
          }
          this.showLeaderEdit = false
        } else if (this.showMemberEdit) {
          this.edited_user_group.members = user
          this.showMemberEdit = false
        }
      },
      selectDutyOver (duty) {
        if (this.showDutyEdit) {
          var result = []
          for (var i = 0, len = duty.length; i < len; i++) {
            if (duty[i].indexOf(DUTY_CAT_PREFIX) < 0) {
              result.push(duty[i])
            }
          }
          this.edited_user_group.duty = result
          this.showDutyEdit = false
        }
      },
      ...mapActions([ UPSERT_USER_GROUP ])
    },
    computed: {
      ...mapGetters(['allRole', 'dutyForRoles']),
      Util () {
        return Util
      },
      leaderName () {
        return Util.getUserName(this.edited_user_group.leader)
      }
    },
    props: ['edited_user_group', 'dialogVisible'],
    watch: {
      dialogVisible: function (val, oldval) {
      }
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        rules: {
          name: [
            { required: true, message: '小组名称不能为空', trigger: 'blur' }
          ]
        },
        showLeaderEdit: false,
        showMemberEdit: false,
        showDutyEdit: false,
        current_edited_user_group: {},
        leader: [],
        members: [],
        userGroupDuties: []
      }
    }
  }
</script>
