<template>
  <div>
    <h2>我的工作通知</h2>
    <br/>
    <el-table
      :data="messages"
      style="width: 100%"
      :default-sort = "{prop: 'informSendTime', order: 'descending'}"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="name"
        label="消息名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="msgPriorityDisplay"
        label="消息等级"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="descr"
        label="消息内容"
        align="center">
      </el-table-column>
      <el-table-column
        prop="msgArriveTimeDisplay"
        label="消息发送时间"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="readStatus"
        label="状态"
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
          @click="handleEdit(scope.$index, scope.row)" type="success">查看详情</el-button>
          </div>
        </template>
      </el-table-column>
      <!--<el-table-column-->
      <!--type="selection"-->
      <!--width="55">-->
      <!--</el-table-column>-->
    </el-table>
    <info-panel-user-inform @showEdit="showEditOver" :dialogVisible="showEdit" :edited_inform="selectedInform"></info-panel-user-inform>
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
  import { GET_INFORM_BY_USER, CHECK_SINGLE_INFORM } from '../store/mutation_types'
  import { NOTIFY_PRIORITY} from '../store/common_defs'
  import Moment from 'moment'
  import InfoPanelUserInform from './info_panel_user_inform.vue'
  //  import Util from '../store/utils'
  //  import ObjUtil from '../utils/ObjUtil'

  export default {
    name: 'table_user_message_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleEdit (index, row) {
        this.CHECK_SINGLE_INFORM(row)
        this.showEdit = true
        this.selectedInform = row
      },
      showEditOver () {
        this.showEdit = false
      },
      ...mapActions([GET_INFORM_BY_USER, CHECK_SINGLE_INFORM])
    },
    computed: {
      ...mapGetters(['userInform']),
      messages () {
        var data = []
        for (var i = 0, len = this.userInform.length; i < len; i++) {
          var item = this.userInform[i]
          item.msgArriveTimeDisplay = Moment(item.sendTime * 1000).format('YY年M月D日 H:mm')
          item.msgPriorityDisplay = NOTIFY_PRIORITY[item.notifyPriority]
          item.readStatus = item.isNew ? '未读' : '已读'
          data.push(item)
        }
        return data
      }
    },
    created: function () {
    },
    beforeRouteEnter: function (to, from, next) {
      next(vm => {
        vm.GET_INFORM_BY_USER({'pageNum': 0})
      })
    },
    data: () => {
      return {
        showEdit: false,
        selectedInform: {},
        multipleSelection: []
      }
    },
    components: {
      InfoPanelUserInform
    }
  }
</script>
