<template>
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
      <el-form-item label="性别" :required="true">
        <el-select v-model="edited_user.sex">
          <el-option label="男" value="Male"></el-option>
          <el-option label="女" value="Female"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="员工岗位" prop="role">
        <el-select v-model="edited_user.role" placeholder="选择岗位" :disabled="!Util.hasCategoryPermission('PERMISSION_CATEGORY_USER')">
          <el-option v-for="item in allRole" :label="item.name" :value="item._id"/>
        </el-select>
      </el-form-item>
      <el-form-item label="出生日期">
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
</template>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { UPSERT_USER_ACCOUNT } from '../store/mutation_types'
  import Util from '../store/utils'
  export default {
    components: {},
    name: 'user_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        this.$refs['userForm'].validate((valid) => {
          console.log('validation')
          console.log(valid)
          if (valid) {
            console.log('call upsert: edit user:')
            console.log(this.edited_user)
            this.UPSERT_USER_ACCOUNT(this.edited_user)
            this.$emit('showEdit', false)
          }
        })
      },
      cancelEdit () {
//        this.$refs['userForm'].resetFields()
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      ...mapActions([ UPSERT_USER_ACCOUNT ])
    },
    computed: {
      ...mapGetters(['allRole']),
      Util () {
        return Util
      }
    },
    props: ['edited_user', 'dialogVisible', 'isCreating'],
    created: function () {
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
            { required: true, message: '请选择员工岗位', trigger: 'blur' }
          ]
        }
      }
    }
  }
</script>
