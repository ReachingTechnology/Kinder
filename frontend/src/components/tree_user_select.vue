<template>
  <el-dialog :title="title" :visible.sync="dialogVisible" :close-on-click-modal="false" @close="handleClose">
    <el-tree
      align="left"
      :data="userTree"
      ref="tree"
      show-checkbox
      node-key="id"
      default-expand-all
      :default-checked-keys="selectedUsers"
      :props="defaultProps">
    </el-tree>
    <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
    </span>
  </el-dialog>
</template>
<script>
  import {mapGetters} from 'vuex'
  import Util from '../store/utils'
  import ArrayUtil from '../utils/ArrayUtil'
  export default {
    components: {},
    name: 'user_select_tree',
    methods: {
      commitEdit () {
        this.$emit('selectedUser', this.$refs.tree.getCheckedKeys(true))
      },
      cancelEdit () {
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      }
    },
    computed: {
      ...mapGetters(['allRole', 'allUser']),
      Util () {
        return Util
      },
      userTree () {
        var tree = []
        var listedUsers = []
        for (var i = 0, len = this.allRole.length; i < len; i++) {
          var node = {}
          node.id = this.allRole[i]._id
          node.label = this.allRole[i].name
          node.children = []
          for (var j = 0, len2 = this.allUser.length; j < len2; j++) {
            if (ArrayUtil.in_array(this.allUser[j]._id, listedUsers)) {
              continue
            }
            if (ArrayUtil.in_array(node.id, this.allUser[j].role)) {
              var subNode = {}
              subNode.id = this.allUser[j]._id
              subNode.label = this.allUser[j].name
              node.children.push(subNode)
              listedUsers.push(this.allUser[j]._id)
            }
          }
          tree.push(node)
        }
        return tree
      }
    },
    props: ['selectedUser', 'dialogVisible', 'title'],
    updated: function () {
      this.$refs.tree.setCheckedKeys(this.selectedUser)
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        selectedUsers: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        }
      }
    }
  }
</script>
