<template>
  <el-dialog title="编辑任务" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <el-form :model="edited_duty"  :label-width="formLabelWidth" :label-position="labelPosition" ref="dutyForm" :rules="rules">
      <!--<el-form-item label="任务编号" v-show="edited_duty._id == '' ? false : true">-->
      <!--<el-input v-model="edited_duty._id" auto-complete="off" :disabled="true"></el-input>-->
      <!--</el-form-item>-->
      <el-form-item label="任务名称" prop="name">
        <el-input v-model="edited_duty.name" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="任务描述" :label-width="formLabelWidth">
        <el-input v-model="edited_duty.descr" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="选择任务时间" prop="timeRange">
        <el-time-picker
          is-range
          v-model="edited_duty.timeRange"
          placeholder="选择时间区间">
        </el-time-picker>
      </el-form-item>
      <el-form-item label="相关岗位" prop="selectedRoleNames">
        <el-checkbox-group v-model="selectedRoleNames" @change="handleCheckedRolesChange">
          <el-checkbox v-for="item in allRole" :label="item.name" :key="item._id"></el-checkbox>
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
  import { mapActions, mapGetters } from 'vuex'
  import { UPSERT_DUTY } from '../store/mutation_types'
  import dateUtil from '../utils/DateUtil'
  import Util from '../store/utils'
  export default {
    components: {},
    name: 'duty_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleCheckedRolesChange (value) {
        console.log('check role changed!!')
        console.log(value)
        this.edited_duty.roles = []
        for (var i = 0, len = value.length; i < len; i++) {
          let id = Util.getRoleId(value[i], this.allRole)
          this.edited_duty.roles.push(id)
        }
        this.edited_duty.roleNames = value
      },
      computeDatetime () {
//        alert('haha')
        let st = this.edited_duty.timeRange[0]
        let et = this.edited_duty.timeRange[1]
        let startofyesterday = dateUtil.getStartOfToday() - 3600 * 24
        console.log('before converting time: st:' + st + '; et:' + et)
        this.edited_duty.starttime = dateUtil.getDatetimeSeconds(st) - startofyesterday
        this.edited_duty.endtime = dateUtil.getDatetimeSeconds(et) - startofyesterday
        console.log('after converting time: st:' + this.edited_duty.starttime + '; et:' + this.edited_duty.endtime)
        console.log('call upsert: edit duty:' + this.edited_duty)
      },
      commitEdit () {
        this.$refs['dutyForm'].validate((valid) => {
          console.log('validation')
          console.log(valid)
          if (valid) {
            this.computeDatetime()
            this.UPSERT_DUTY(this.edited_duty)
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
      ...mapActions([ UPSERT_DUTY ])
    },
    computed: {
      ...mapGetters(['allRole'])
    },
//    watch: {
//      dialogVisible: function (val, oldval) {
//        console.log('dialog visible watched')
//        if (val) {
//          this.$refs['dutyForm'].validate()
//        }
//      }
//    },
    props: ['edited_duty', 'dialogVisible', 'selectedRoleNames'],
    created: function () {
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        selectedRoleName: [],
        rules: {
          name: [
            { required: true, message: '职责名称不能为空', trigger: 'blur' }
          ],
//          timeRange: [
//            { type: 'date', required: true, message: '请选择执行时间', trigger: 'blur' }
//          ],
          selectedRoleNames: [
            { type: 'array', required: true, message: '请至少选择一个岗位', trigger: 'blur' }
          ]
        }
      }
    }
  }
</script>
