<template>
  <div>
    <h2>幼儿园员工列表</h2>
    <div align="left">
      <el-button size="large" class="horizontal-btn"
                 @click="handleCreate()" type="success">
        添加新员工
      </el-button>
      <el-button size="large" class="horizontal-btn"
                 @click="handleDelete()" type="success">
        删除选中员工
      </el-button>
    </div>
    <br/>
    <el-table
      ref="userList"
      :data="users"
      style="width: 100%"
      :default-sort = "{prop: '_id', order: 'ascending'}"
      @selection-change="handleSelectionChange"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="_id"
        label="员工编号"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="cellphone"
        label="手机号"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="sex_name"
        label="性别"
        align="center"
        sortable>
        <!--<template scope="scope">-->
          <!--<el-select v-model="scope.row.sex" disabled="true">-->
            <!--<el-option label="男" value="Male"></el-option>-->
            <!--<el-option label="女" value="Female"></el-option>-->
          <!--</el-select>-->
        <!--</template>-->
      </el-table-column>
      <el-table-column
        prop="role_name"
        label="岗位"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="age"
        label="年龄"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        class="no-print"
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
    <user-edit-panel @showEdit="showEditOver" :dialogVisible="showEdit" :edited_user="selectedUser" :isCreating="isCreating"></user-edit-panel>
    <br/>
    <div align="left">
      <span>总员工数：{{ this.allUser.length }}</span>
    </div>
    <br/>
    <div align="left">
      <el-button size="large" class="horizontal-btn"
                 @click="handlePrint" type="success">
        打印
      </el-button>
    </div>
    <div id="print_area" class="no-screen">
      <div id="print">
        <h1>幼儿园员工列表</h1>
        <table>
          <thead>
          <tr>
            <th> 员工编号 </th>
            <th> 姓名 </th>
            <th> 手机号 </th>
            <th> 性别 </th>
            <th> 岗位 </th>
            <th> 年龄 </th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="data in users">
            <td> {{data._id}} </td>
            <td> {{data.name}} </td>
            <td> {{data.cellphone}} </td>
            <td> {{data.sex_name}} </td>
            <td> {{data.role_name}} </td>
            <td> {{data.age}} </td>
          </tr>
          </tbody>
        </table>
      </div>
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

  .horizontal-btn {
    display: inline-block;
  }
</style>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { GET_ALL_USER_ACCOUNT, GET_ALL_ROLE, REMOVE_USERS, PRINT } from '../store/mutation_types'
  import UserEditPanel from './edit_panel_user.vue'
  import Utils from '../store/utils'
  import ObjUtil from '../utils/ObjUtil'

  export default {
    name: 'table_user_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      toggleSelection (rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.userList.toggleRowSelection(row)
          })
        } else {
          this.$refs.userList.clearSelection()
        }
      },
      handleSelectionChange (val) {
        this.multipleSelection = val
      },
      handleEdit (index, row) {
        this.selectedUser = {}
        for (var i = 0, len = this.allUser.length; i < len; i++) {
          if (this.allUser[i]._id === row._id) {
            this.selectedUser = ObjUtil.clone(this.allUser[i])
            this.selectedUser.checkedRoleNames = []
            for (var j = 0, len2 = this.allUser[i].role.length; j < len2; j++) {
              this.selectedUser.checkedRoleNames.push(Utils.getRoleName(this.allUser[i].role[j]))
            }
            this.showEdit = true
            this.isCreating = false
            break
          }
        }
      },
      handleCreate () {
        this.selectedUser = {
          '_id': '',
          'name': '',
          'cellphone': '',
          'sex': 'Male',
          'role': [],
          'duty': [],
          'leader': '',
          'checkedRoleNames': [],
          'birthday': '',
          'password': ''
        }
        this.isCreating = true
        this.showEdit = true
      },
      showEditOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_USER_ACCOUNT, GET_ALL_ROLE, REMOVE_USERS, PRINT]),
      handleDelete () {
        let users = []
        for (var i = 0, len = this.multipleSelection.length; i < len; i++) {
          users.push(this.multipleSelection[i]._id)
        }
        this.REMOVE_USERS(users)
      },
      handlePrint () {
        let allContent = document.documentElement.innerHTML
        let printContent = document.getElementById('print_area').innerHTML
        this.PRINT({all: allContent, print: printContent})
        return true
      },
    },
    computed: {
      ...mapGetters(['allUser', 'allRole']),
      users () {
        var data = []
        for (var i = 0, len = this.allUser.length; i < len; i++) {
          var item = this.allUser[i]
          item.sex_name = item.sex === 'Male' ? '男' : '女'
          item.role_name = ''
          for (var k = 0, len1 = item.role.length; k < len1; k++) {
            let roleid = item.role[k]
            for (var j = 0, len2 = this.allRole.length; j < len2; j++) {
              if (roleid === this.allRole[j]._id) {
                item.role_name = item.role_name + this.allRole[j].name + ' '
              }
            }
          }
          data.push(item)
        }
        return data
      }
    },
    created: function () {
      this.GET_ALL_ROLE()
      this.GET_ALL_USER_ACCOUNT()
    },
    data: () => {
      return {
        showEdit: false,
        selectedUser: {},
        multipleSelection: [],
        isCreating: false
      }
    },
    components: {
      UserEditPanel
    }
  }
</script>
