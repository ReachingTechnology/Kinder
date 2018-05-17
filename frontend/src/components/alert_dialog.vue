<template>
  <el-dialog :title="title" :visible="dialogVisible" @close="handleClose" :close-on-click-modal="false">
    <span>{{ content }}</span>
    <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="handleOk">确认</el-button>
  </span>
  </el-dialog>
</template>
<script>
  export default {
    components: {},
    name: 'alert_dialog',
    methods: {
      handleOk () {
        this.$emit('showDialogOver', true)
      },
      handleClose () {
        this.$emit('showDialogOver', true)
      }
    },
    props: ['title', 'content', 'dialogVisible']
  }
</script>
