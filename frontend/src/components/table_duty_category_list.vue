<template>
  <div>
    <h2>职责类别列表</h2>
    <div align="left" style="width:100%">
      <el-button size="large" class="horizontal-btn"
                 @click="handleCreate()" type="success">
        添加新类别
      </el-button>
      <el-button size="large" class="horizontal-btn"
                 @click="handleDelete()" type="success">
        删除选中类别
      </el-button>
    </div>
    <br/>
    <el-table
      :data="allDutyCategory"
      style="width: 100%"
      :default-sort = "{prop: '_id', order: 'ascending'}"
      @selection-change="handleSelectionChange"
      >
      <el-table-column
        prop="name"
        label="类别名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="descr"
        label="类别描述"
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
    <duty-category-edit-panel @showEdit="showEditOver" :isCreating="isCreating" :dialogVisible="showEdit" :edited_duty_category="selectedDutyCategory" ></duty-category-edit-panel>
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

  .horizontal-btn-right {
    display: inline-block;
    float: right;
  }

  #select_role .el-form-item__label {
    display: inline-block;
  }

  #select_role .el-form-item__content {
    display: inline-block;
  }

</style>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { GET_ALL_DUTY_CATEGORY, REMOVE_DUTY_CATEGORIES } from '../store/mutation_types'
  import DutyCategoryEditPanel from './edit_panel_duty_category.vue'

  export default {
    name: 'table_duty_category_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleSelectionChange (val) {
        this.multipleSelection = val
      },
      handleEdit (index, row) {
        this.selectedDutyCategory = {}
        for (var i = 0, len = this.allDutyCategory.length; i < len; i++) {
          if (this.allDutyCategory[i]._id === row._id) {
            this.selectedDutyCategory = this.allDutyCategory[i]
            this.isCreating = false
            this.showEdit = true
            break
          }
        }
      },
      handleCreate () {
        this.selectedDutyCategory = {
          '_id': '',
          'name': '',
          'descr': ''
        }
        this.isCreating = true
        this.showEdit = true
      },
      handleDelete () {
        let dutyCategories = []
        for (var i = 0, len = this.multipleSelection.length; i < len; i++) {
          dutyCategories.push(this.multipleSelection[i]._id)
        }
        this.REMOVE_DUTY_CATEGORIES(dutyCategories)
      },
      showEditOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_DUTY_CATEGORY, REMOVE_DUTY_CATEGORIES])
    },
    computed: {
      ...mapGetters(['allDutyCategory'])
    },
    created: function () {
      this.GET_ALL_DUTY_CATEGORY()
    },
    data: () => {
      return {
        showEdit: false,
        selectedDutyCategory: {},
        multipleSelection: [],
        isCreating: false
      }
    },
    components: {
      DutyCategoryEditPanel
    }
  }
</script>
