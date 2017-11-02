<template>
  <el-dialog title="编辑岗位" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <el-form :model="edited_role" :label-width="formLabelWidth" :label-position="labelPosition" ref="roleForm"
             :rules="rules">
      <el-form-item label="岗位编号" prop="_id">
        <el-input v-model="edited_role._id" auto-complete="off" :disabled="!isCreating"></el-input>
      </el-form-item>
      <el-form-item label="岗位名称" prop="name">
        <el-input v-model="edited_role.name" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="岗位描述" :label-width="formLabelWidth">
        <el-input v-model="edited_role.descr" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="直接汇报岗位">
        <el-select v-model="edited_role.upper_role" placeholder="选择岗位">
          <el-option label="无" :value="ROOT_ROLE"/>
          <el-option v-for="item in allRole" :label="item.name" :value="item._id"/>
        </el-select>
      </el-form-item>
      <el-form-item label="角色权限">
        <el-checkbox-group v-model="checkedPermissionRoleNames" @change="handleCheckedPermissionRoleChange">
          <el-checkbox v-for="role in allPermissionRole" :name="role.name" :label="role.name"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
  </span>
  </el-dialog>
</template>
<script>
  import {mapActions, mapGetters} from 'vuex'
  import {UPSERT_ROLE} from '../store/mutation_types'
  import Util from '../store/utils'
  import ObjUtil from '../utils/ObjUtil'
  import { ROOT_ROLE } from '../store/common_defs'

  export default {
    components: {},
    name: 'role_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        this.current_edited_role = ObjUtil.clone(this.edited_role)
        this.$refs['roleForm'].validate((valid) => {
          if (valid) {
            this.current_edited_role.permissionRoleNames = this.checkedPermissionRoleNames
            this.current_edited_role.permissionRoles = []
            for (var j = 0; j < this.checkedPermissionRoleNames.length; j++) {
              var permRole = Util.getPermissionRoleByName(this.checkedPermissionRoleNames[j])
              this.current_edited_role.permissionRoles.push(permRole._id)
            }
            this.UPSERT_ROLE(this.current_edited_role)
            this.edited_role = this.current_edited_role
            this.$emit('showEdit', false)
          }
        })
      },
      cancelEdit () {
        this.$refs['roleForm'].resetFields()
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      handleCheckedPermissionRoleChange (value) {
        console.log('handleCheckedPermissionRoleChange, value:')
        console.log(value)
        this.checkedPermissionRoleNames = value
      },
      ...mapActions([UPSERT_ROLE])
    },
    watch: {
      dialogVisible: function (val, oldval) {
        if (val === true) {
          this.checkedPermissionRoleNames = this.edited_role.permissionRoleNames
        }
      }
    },
    computed: {
      ...mapGetters(['allRole', 'allPermissionRole']),
      ROOT_ROLE () {
        return ROOT_ROLE
      }
    },
    props: ['edited_role', 'dialogVisible', 'isCreating'],
    created: function () {
    },
    data: function () {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        checkedPermissionRoleNames: [],
        rules: {
          _id: [
            {required: true, message: '岗位编号不能为空', trigger: 'blur'}
          ],
          name: [
            {required: true, message: '岗位名称不能为空', trigger: 'blur'}
          ]
        },
        current_edited_role: {}
      }
    }
  }
</script>
