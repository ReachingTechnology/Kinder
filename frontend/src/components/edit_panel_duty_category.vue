<template>
  <el-dialog title="编辑任务类别" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <el-form :model="edited_duty_category"  :label-width="formLabelWidth" :label-position="labelPosition" ref="dutyCategoryForm" :rules="rules">
      <!--<el-form-item label="任务编号" v-show="edited_duty_category._id == '' ? false : true">-->
      <!--<el-input v-model="edited_duty_category._id" auto-complete="off" :disabled="true"></el-input>-->
      <!--</el-form-item>-->
      <el-form-item label="类别名称" prop="name">
        <el-input v-model="edited_duty_category.name" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="类别描述" :label-width="formLabelWidth">
        <el-input v-model="edited_duty_category.descr" auto-complete="off"></el-input>
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
  import { UPSERT_DUTY_CATEGORY } from '../store/mutation_types'
  import ObjUtil from '../utils/ObjUtil'

  export default {
    components: {},
    name: 'duty_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        this.current_edited_duty_category = ObjUtil.clone(this.edited_duty_category)
        this.$refs['dutyCategoryForm'].validate((valid) => {
          if (valid) {
            this.UPSERT_DUTY_CATEGORY(this.current_edited_duty_category)
            this.edited_duty_category = this.current_edited_duty_category
            this.$emit('showEdit', false)
          }
        })
      },
      cancelEdit () {
        this.$refs['dutyCategoryForm'].resetFields()
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      ...mapActions([ UPSERT_DUTY_CATEGORY ])
    },
    computed: {
      ...mapGetters(['allDutyCategory'])
    },
    props: ['edited_duty_category', 'dialogVisible', 'isCreating'],
    created: function () {
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        selectedRoleName: [],
        rules: {
          name: [
            { required: true, message: '类别名称不能为空', trigger: 'blur' }
          ]
        },
        current_edited_duty_category: {}
      }
    }
  }
</script>
