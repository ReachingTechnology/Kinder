<template>
  <div>
    <h2>下发通知列表</h2>
    <div align="left">
      <el-button size="large"
                 @click="handleCreate()" type="success">
        添加新通知
      </el-button>
      <el-button v-show="Util.hasPermission('PERMISSION_INFORM_REMOVE')" size="large" class="horizontal-btn"
                 @click="handleDelete()" type="success">
        删除选中通知
      </el-button>
    </div>
    <br/>
    <el-table
      :data="informs"
      style="width: 100%"
      :default-sort = "{prop: '_id', order: 'descending'}"
      @selection-change="handleSelectionChange"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="name"
        label="通知名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="descr"
        label="通知内容"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        v-show="false"
        prop="notifyTypeDisplay"
        label="通知类型"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="notifyPriorityDisplay"
        label="通知等级"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="sendTimeDisplay"
        label="通知发送时间"
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
    <inform-edit-panel @showEdit="showEditOver" :dialogVisible="showEdit" :edited_inform="selectedInform"></inform-edit-panel>
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
  import { GET_ALL_INFORM, REMOVE_INFORMS } from '../store/mutation_types'
  import InformEditPanel from './edit_panel_inform.vue'
  import { NOTIFY_TYPE, NOTIFY_PRIORITY} from '../store/common_defs'
  import Moment from 'moment'
  import dateUtil from '../utils/DateUtil'
  import Util from '../store/utils'
  //  import ObjUtil from '../utils/ObjUtil'

  export default {
    name: 'table_inform_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleSelectionChange (val) {
        this.multipleSelection = val
      },
      handleEdit (index, row) {
        this.selectedInform = row
        this.isCreating = false
        this.showEdit = true
      },
      handleCreate () {
        this.selectedInform = {
          '_id': '',
          'name': '',
          'descr': '',
          'notifyType': 'message_queue',
          'notifyPriority': '',
          'sendTime': dateUtil.getNow(),
          'informUserList': [],
          'sender': ''
        }
        this.showEdit = true
      },
      handleDelete () {
        let informs = []
        for (var i = 0, len = this.multipleSelection.length; i < len; i++) {
          informs.push(this.multipleSelection[i]._id)
        }
        this.REMOVE_INFORMS(informs)
      },
      showEditOver () {
        this.showEdit = false
      },
      ...mapActions([GET_ALL_INFORM, REMOVE_INFORMS])
    },
    computed: {
      ...mapGetters(['allInform']),
      informs () {
        var data = []
        for (var i = 0, len = this.allInform.length; i < len; i++) {
          var item = this.allInform[i]
          item.notifyTypeDisplay = NOTIFY_TYPE[item.notifyType]
          item.notifyPriorityDisplay = NOTIFY_PRIORITY[item.notifyPriority]
          item.sendTimeDisplay = Moment(item.sendTime * 1000).format('YY年M月D日 H:mm')
          data.push(item)
        }
        return data
      },
      Util () {
        return Util
      }
    },
    created: function () {
      this.GET_ALL_INFORM()
    },
    data: () => {
      return {
        showEdit: false,
        selectedInform: {},
        multipleSelection: []
      }
    },
    components: {
      InformEditPanel
    }
  }
</script>
