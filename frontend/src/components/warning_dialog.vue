<template>
  <el-dialog :title="title" :visible="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <span>{{ content }}</span>
    <span slot="footer" class="dialog-footer">
    <el-button @click="handleCancel">取消</el-button>
    <el-button type="primary" @click="handleOk">确认</el-button>
  </span>
  </el-dialog>
</template>
<script>
  export default {
    components: {},
    name: 'warning_dialog',
    methods: {
      handleOk () {
        this.$emit('choice', true)
      },
      handleCancel () {
        this.$emit('choice', false)
      },
      handleClose () {
        console.log('handlecoloe')
        this.$emit('choice', false)
      }
    },
    props: ['title', 'content', 'dialogVisible']
  }
</script>
