<template>
  <div>
    <h2>幼儿园岗位列表</h2>
    <div align="left">
      <el-button size="large"
                 @click="handleCreate()" type="success">
        添加新岗位
      </el-button>
      <el-button size="large" class="horizontal-btn"
                 @click="handleDelete()" type="success">
        删除选中岗位
      </el-button>
    </div>
    <br/>
    <el-table
      :data="roles"
      style="width: 100%"
      :default-sort = "{prop: '_id', order: 'ascending'}"
      @selection-change="handleSelectionChange"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="_id"
        label="岗位编号"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="name"
        label="岗位名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="descr"
        label="岗位描述"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="upper_role_name"
        label="直接汇报岗位"
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
    <role-edit-panel @showEdit="showEidtOver" :dialogVisible="showEdit" :edited_role="selectedRole" :isCreating="isCreating"></role-edit-panel>
    <br/>
    <div align="left">
      <span>总岗位数：{{ this.allRole.length }}</span>
    </div>
  </div>
</template>
<style>
  .el-table .info-row {
    background: #c9e5f5;
  }

  .el-table .positive-row {
    background: #e2f0e4;
  }
</style>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { GET_ALL_ROLE, REMOVE_ROLES } from '../store/mutation_types'
  import RoleEditPanel from './edit_panel_role.vue'
  import Util from '../store/utils'
  export default {
    name: 'table_role_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleSelectionChange (val) {
        this.multipleSelection = val
      },
      handleEdit (index, row) {
        this.selectedRole = {}
        for (var i = 0, len = this.allRole.length; i < len; i++) {
          if (this.allRole[i]._id === row._id) {
            this.selectedRole = this.allRole[i]
            this.selectedRole.permissionRoleNames = []
            if (this.selectedRole.permissionRoles !== undefined) {
              for (var j = 0; j < this.selectedRole.permissionRoles.length; j++) {
                var permRole = Util.getPermissionRoleById(this.selectedRole.permissionRoles[j])
                this.selectedRole.permissionRoleNames.push(permRole.name)
              }
            }
            this.isCreating = false
            this.showEdit = true
            break
          }
        }
      },
      handleCreate () {
        this.selectedRole = {
          '_id': '',
          'name': '',
          'descr': '',
          'upper_role': '',
          'permissionRoles': []
        }
        this.isCreating = true
        this.showEdit = true
      },
      handleDelete () {
        let users = []
        for (var i = 0, len = this.multipleSelection.length; i < len; i++) {
          users.push(this.multipleSelection[i]._id)
        }
        this.REMOVE_ROLES(users)
      },
      showEidtOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_ROLE, REMOVE_ROLES])
    },
    computed: {
      ...mapGetters(['allRole']),
      roles () {
        var data = []
        for (var i = 0, len = this.allRole.length; i < len; i++) {
          var item = this.allRole[i]
          for (var j = 0, len2 = this.allRole.length; j < len2; j++) {
            if (item.upper_role === this.allRole[j]._id) {
              item.upper_role_name = this.allRole[j].name
            }
          }
          data.push(item)
        }
        return data
      }
    },
    created: function () {
      this.GET_ALL_ROLE()
    },
    data: () => {
      return {
        showEdit: false,
        selectedRole: {},
        multipleSelection: [],
        isCreating: false
      }
    },
    components: {
      RoleEditPanel
    }
  }
</script>
