<template>
  <el-dialog title="选择职责" :visible.sync="dialogVisible" :close-on-click-modal="false" @close="handleClose">
    <el-tree
      align="left"
      :data="dutyTree"
      ref="tree"
      show-checkbox
      node-key="id"
      default-expand-all
      :default-checked-keys="selectedDuties"
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
  export default {
    components: {},
    name: 'duty_select_tree',
    methods: {
      commitEdit () {
        this.$emit('dutySelected', this.$refs.tree.getCheckedKeys(true))
      },
      cancelEdit () {
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      }
    },
    computed: {
      ...mapGetters(['allRole', 'allDutyCategory', 'allDuty']),
      Util () {
        return Util
      },
      dutyTree () {
        var tree = []
        for (var i = 0, len = this.allDutyCategory.length; i < len; i++) {
          var node = {}
          node.id = this.allDutyCategory[i]._id
          node.label = this.allDutyCategory[i].name
          node.children = []
          for (var j = 0, len2 = this.allDuty.length; j < len2; j++) {
            if (this.allDuty[j].category === node.id) {
              var childNode = {}
              childNode.id = this.allDuty[j]._id
              childNode.label = this.allDuty[j].name
              node.children.push(childNode)
            }
          }
          tree.push(node)
        }
        return tree
      }
    },
    props: ['selectedDuties', 'dialogVisible'],
    updated: function () {
      this.$refs.tree.setCheckedKeys(this.selectedDuties)
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        selectedDuties: [],
        defaultProps: {
          children: 'children',
          label: 'label'
        }
      }
    }
  }
</script>
