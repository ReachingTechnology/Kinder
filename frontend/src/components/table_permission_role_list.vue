<template>
  <div>
    <h2>角色权限列表</h2>
    <div align="left">
      <el-button size="large" class="horizontal-btn"
                 @click="handleCreate()" type="success">
        添加新角色
      </el-button>
      <el-button size="large" class="horizontal-btn"
                 @click="handleDelete()" type="success">
        删除选中角色
      </el-button>
    </div>
    <br/>
    <el-table
      :data="allPermissionRole"
      style="width: 100%"
      :default-sort = "{prop: 'name', order: 'ascending'}"
      @selection-change="handleSelectionChange"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="name"
        label="角色名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="descr"
        label="角色描述"
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
    <permission-role-edit-panel @showEdit="showEidtOver" :dialogVisible="showEdit" :edited_permission_role="selectedPermissionRole" ></permission-role-edit-panel>
    <br/>
    <div align="left">
      <span>总角色数：{{ this.allPermissionRole.length }}</span>
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
  import { GET_ALL_PERMISSION_ROLE, GET_ALL_PERMISSION, REMOVE_PERMISSION_ROLES } from '../store/mutation_types'
  import PermissionRoleEditPanel from './edit_panel_permission_role.vue'
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
        this.selectedPermissionRole = {}
        console.log(this.allPermissionRole)
        for (var i = 0, len = this.allPermissionRole.length; i < len; i++) {
          if (this.allPermissionRole[i].name === row.name) {
            this.selectedPermissionRole = this.allPermissionRole[i]
            console.log(this.selectedPermissionRole)
            this.showEdit = true
            break
          }
        }
      },
      handleCreate () {
        this.selectedPermissionRole = {
          '_id': '',
          'seq': 0,
          'name': '',
          'descr': '',
          'permissions': []
        }
        this.showEdit = true
      },
      handleDelete () {
        let users = []
        for (var i = 0, len = this.multipleSelection.length; i < len; i++) {
          users.push(this.multipleSelection[i]._id)
        }
        this.REMOVE_PERMISSION_ROLES(users)
      },
      showEidtOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_PERMISSION_ROLE, GET_ALL_PERMISSION, REMOVE_PERMISSION_ROLES])
    },
    computed: {
      ...mapGetters(['allPermissionRole', 'allPermission'])
    },
    created: function () {
      this.GET_ALL_PERMISSION()
      this.GET_ALL_PERMISSION_ROLE()
    },
    data: () => {
      return {
        showEdit: false,
        selectedPermissionRole: {},
        multipleSelection: [],
        permissionList: {}
      }
    },
    components: {
      PermissionRoleEditPanel
    }
  }
</script>
