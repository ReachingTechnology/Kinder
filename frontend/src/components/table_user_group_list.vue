<template>
  <div>
    <h2>幼儿园小组列表</h2>
    <div align="left">
      <el-button size="large"
                 @click="handleCreate()" type="success">
        添加新小组
      </el-button>
      <el-button size="large" class="horizontal-btn"
                 @click="handleDelete()" type="success">
        删除选中小组
      </el-button>
    </div>
    <br/>
    <el-table
      :data="groups"
      style="width: 100%"
      :default-sort = "{prop: '_id', order: 'ascending'}"
      @selection-change="handleSelectionChange"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="name"
        label="小组名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="descr"
        label="小组工作描述"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="leaderName"
        label="小组负责人"
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
    <user-group-edit-panel @showEdit="showEditOver" :dialogVisible="showEdit" :edited_user_group="selectedGroup"></user-group-edit-panel>
    <br/>
    <div align="left">
      <span>总小组数：{{ this.allUserGroup.length }}</span>
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
  import { GET_ALL_USER_GROUP, REMOVE_USER_GROUPS } from '../store/mutation_types'
  import UserGroupEditPanel from './edit_panel_user_group.vue'
  import Util from '../store/utils'
  import ObjUtil from '../utils/ObjUtil'

  export default {
    name: 'table_user_group_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleSelectionChange (val) {
        this.multipleSelection = val
      },
      handleEdit (index, row) {
        this.selectedGroup = {}
        for (var i = 0, len = this.allUserGroup.length; i < len; i++) {
          if (this.allUserGroup[i]._id === row._id) {
            this.selectedGroup = ObjUtil.clone(this.allUserGroup[i])
            this.showEdit = true
            break
          }
        }
      },
      handleCreate () {
        this.selectedGroup = {
          '_id': '',
          'name': '',
          'descr': '',
          'leader': '',
          'leaderName': '',
          'members': []
        }
        this.showEdit = true
      },
      handleDelete () {
        let users = []
        for (var i = 0, len = this.multipleSelection.length; i < len; i++) {
          users.push(this.multipleSelection[i]._id)
        }
        this.REMOVE_USER_GROUPS(users)
      },
      showEditOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_USER_GROUP, REMOVE_USER_GROUPS])
    },
    computed: {
      ...mapGetters(['allUserGroup']),
      groups () {
        var data = []
        for (var i = 0, len = this.allUserGroup.length; i < len; i++) {
          var item = this.allUserGroup[i]
          item.leaderName = Util.getUserName(this.allUserGroup[i].leader)
          data.push(item)
        }
        return data
      }
    },
    created: function () {
      this.GET_ALL_USER_GROUP()
    },
    data: () => {
      return {
        showEdit: false,
        selectedGroup: {},
        multipleSelection: []
      }
    },
    components: {
      UserGroupEditPanel
    }
  }
</script>
