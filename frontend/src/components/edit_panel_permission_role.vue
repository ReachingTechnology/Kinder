<template>
  <el-dialog title="编辑角色" :visible.sync="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <el-form :model="edited_permission_role"  :label-width="formLabelWidth" :label-position="labelPosition">
      <el-form-item label="角色名称">
        <el-input v-model="edited_permission_role.name" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="角色描述" :label-width="formLabelWidth">
        <el-input v-model="edited_permission_role.descr" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="角色权限">
        <template>
        <br/>
        <div align="left" v-for="categoryid in Object.keys(allPermission)">
          <!--<el-checkbox :indeterminate="isIndeterminate[categoryid]" v-model="permissionCategory[categoryid]" @change="(event) => {handleCheckCategoryChange(event, categoryid)}">{{ allPermission[categoryid].categoryName }}</el-checkbox>-->
          <!--<div style="margin: 15px 0;"></div>-->
          <div align="left"><span>  {{ allPermission[categoryid].categoryName }}</span></div>
          <el-checkbox-group v-model="checkedPermissions[categoryid]" @change="(value) => {handleCheckedPermissionChange(value, categoryid)}">
            <el-checkbox v-for="permission in allPermission[categoryid].permissions" :name="categoryid" :value="permission.id" :label="permission.name"></el-checkbox>
          </el-checkbox-group>
          <!--<mu-checkbox v-for="permission in allPermission[categoryid].permissions" :name="categoryid" :nativeValue="permission.id" v-model="checkedPermissions[categoryid]" :label="permission.name" @change="(value) => {handleCheckedPermissionChange(value, categoryid)}"/>-->
          <br/>
        </div>
        </template>
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
  import { UPSERT_PERMISSION_ROLE } from '../store/mutation_types'
  import Util from '../store/utils'
  export default {
    components: {},
    name: 'permission_role_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        this.edited_permission_role.permissions = []
        var keys = Object.keys(this.checkedPermissions)
        for (var i = 0, len = keys.length; i < len; i++) {
          for (var j = 0, len2 = this.checkedPermissions[keys[i]].length; j < len2; j++) {
            var permName = this.checkedPermissions[keys[i]][j]
            this.edited_permission_role.permissions.push(Util.getPermissionIdByName(permName, this.allPermission))
          }
        }
        console.log('commit upsert of a permission role')
        console.log(this.edited_permission_role)
        this.UPSERT_PERMISSION_ROLE(this.edited_permission_role)
        this.$emit('showEdit', false)
      },
      cancelEdit () {
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      handleCheckCategoryChange (event, cateogryid) {
        console.log('handleCheckCategoryChange, event:')
        console.log(event)
        this.checkedPermissions[cateogryid] = event.target.checked ? this.allofPermissions[cateogryid] : []
        console.log(this.checkedPermissions[cateogryid])
        this.isIndeterminate[cateogryid] = false
      },
      handleCheckedPermissionChange (value, categoryid) {
        console.log('handleCheckedPermissionChange, value:')
        console.log(value)
        this.checkedPermissions[categoryid] = value
      },
      ...mapActions([ UPSERT_PERMISSION_ROLE ])
    },
    watch: {
      dialogVisible: function (val, oldval) {
        if (val === true) {
          this.checkedPermissions = {}
          var keys = Object.keys(this.allPermission)
          var editedPermissionList = this.edited_permission_role.permissions
          for (var i = 0, len = keys.length; i < len; i++) {
            var categoryid = keys[i]
            var perms = []
            for (var j = 0, len2 = this.allPermission[categoryid].permissions.length; j < len2; j++) {
              var found = false
              for (var temp in editedPermissionList) {
                if (editedPermissionList[temp] === this.allPermission[categoryid].permissions[j].id) {
                  found = true
                  break
                }
              }
              if (found) {
                perms.push(this.allPermission[categoryid].permissions[j].name)
              }
            }
            this.$set(this.checkedPermissions, categoryid, perms)
          }
        }
      }
    },
    computed: {
      ...mapGetters(['allPermission']),
      allofPermissions () {
        var data = {}
        var keys = Object.keys(this.allPermission)
        for (var i = 0, len = keys.length; i < len; i++) {
          var categoryid = keys[i]
          data[categoryid] = []
          for (var j = 0; j < this.allPermission[categoryid].permissions.length; j++) {
            data[categoryid].push(this.allPermission[categoryid].permissions[j].name)
          }
        }
        return data
      }
    },
    props: ['edited_permission_role', 'dialogVisible'],
    created: function () {
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        permissionCategory: [],
        isIndeterminate: {},
        checkedPermissions: {}
      }
    }
  }
</script>
