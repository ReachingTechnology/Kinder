<template>
  <div>
    <h2>我的消息列表</h2>
    <br/>
    <el-table
      :data="messages"
      style="width: 100%"
      :default-sort = "{prop: 'informSendTime', order: 'descending'}"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="msgPriorityDisplay"
        label="消息等级"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="msgContent"
        label="消息内容"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="msgArriveTimeDisplay"
        label="消息发送时间"
        align="center"
        sortable>
      </el-table-column>
      <!--<el-table-column-->
        <!--label="操作"-->
        <!--align="center">-->
        <!--<template scope="scope">-->
          <!--<div>-->
            <!--<el-button-->
              <!--size="small"-->
              <!--@click="handleEdit(scope.$index, scope.row)" type="success">消息详情</el-button>-->
          <!--</div>-->
        <!--</template>-->
      <!--</el-table-column>-->
      <!--<el-table-column-->
        <!--type="selection"-->
        <!--width="55">-->
      <!--</el-table-column>-->
    </el-table>
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
  import { GET_INFORM_BY_USER } from '../store/mutation_types'
  import InformEditPanel from './edit_panel_inform.vue'
  import { NOTIFY_PRIORITY} from '../store/common_defs'
  import Moment from 'moment'
  //  import Util from '../store/utils'
  //  import ObjUtil from '../utils/ObjUtil'

  export default {
    name: 'table_user_message_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      ...mapActions([GET_INFORM_BY_USER])
    },
    computed: {
      ...mapGetters(['userInform']),
      messages () {
        var data = []
        for (var i = 0, len = this.userInform.length; i < len; i++) {
          var item = this.userInform[i]
          if (item.notifyTimeType === 'after') {
            item.msgContent = '此消息是提醒您的工作职责"' + item.taskname + '"应该于' + Moment(item.realendtime * 1000).format('H:mm') + '完成执行.'
          } else {
            item.msgContent = '此消息是提醒您的工作职责"' + item.taskname + '"将于' + Moment(item.realstarttime * 1000).format('H:mm') + '开始执行.'
          }
          item.msgArriveTimeDisplay = Moment(item.informSendTime * 1000).format('YY年M月D日 H:mm')
          item.msgPriorityDisplay = NOTIFY_PRIORITY[item.notifyPriority]
          data.push(item)
        }
        return data
      }
    },
    created: function () {
      this.GET_INFORM_BY_USER()
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
