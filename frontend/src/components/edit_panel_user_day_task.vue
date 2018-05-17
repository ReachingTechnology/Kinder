<template>
  <el-dialog title="编辑任务" :visible.sync="dialogVisible" :close-on-click-modal="false" @close="handleClose">
    <el-form :model="edited_task"  :label-width="formLabelWidth" :label-position="labelPosition">
      <el-form-item label="任务名称">
        <el-input v-model="edited_task.name" :disabled="true" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="任务执行时间">
        <el-input v-model="edited_task.executetime" :disabled="true" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="任务实际完成时间" v-show="edited_task.realendtime !== 0">
        <el-input v-model="edited_task.realendtimeDisplay" :disabled="true" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="备注">
        <el-input type="textarea"
                  :autosize="{ minRows: 2, maxRows: 4}"
                  v-model="edited_task.comment" auto-complete="off"></el-input>
      </el-form-item>
      <el-form-item label="完成状态">
        <el-input v-model="edited_task.finish_status_display" :disabled="true" autoComplete="off"></el-input>
      </el-form-item>
      <el-upload
        :action="upload_image_uri"
        list-type="picture-card"
        :file-list="pictures"
        :before-upload="handleBeforeUpload"
        :before-remove="handleBeforeRemove"
        :on-change="handlePictureChange"
        :on-success="handlePictureUploadSucceed"
        :on-preview="handlePictureCardPreview"
        :on-remove="handlePictureRemove">
        <i class="el-icon-plus"></i>
      </el-upload>
      <el-dialog :visible.sync="previewVisible" @close="handlePreviewClose">
        <img width="100%" :src="dialogImageUrl" alt="">
      </el-dialog>
      <br/>
      <el-form-item label="工作审批">
        <el-select v-model="edited_task.approve_status" :disabled="!Util.hasPermission('PERMISSION_TASK_APPROVE_TASK')" placeholder="选择审批意见">
          <el-option label="个人原因" value='0'></el-option>
          <el-option label="工作安排" value='1'></el-option>
        </el-select>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
    <el-button @click="cancelEdit">取消</el-button>
    <el-button type="primary" @click="commitEdit">提交</el-button>
  </span>
  </el-dialog>
  <alert-dialog @showDialogOver="handleQuitPicExceedDialog" :dialogVisible="showPicExceedDialog" :content="picExceedDialogContent" :title="picExceedDialogTitle"></alert-dialog>
  <warning-dialog @choice="handleQuitPicRemoveDialog" :dialogVisible="showPicRemoveDialog" :content="picRemoveDialogContent" :title="picRemoveDialogTitle"></warning-dialog>
</template>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { COMMIT_TASK_EXEC_INFO } from '../store/mutation_types'
  import dateUtil from '../utils/DateUtil'
  import Util from '../store/utils'
  import AlertDialog from './alert_dialog.vue'
  import WarningDialog from './warning_dialog.vue'
  export default {
    components: { AlertDialog, WarningDialog },
    name: 'duty_edit_panel',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      commitEdit () {
        this.edited_task.startofday = dateUtil.getStartOfTheday(this.selectedDay)
        var taskFinishInfo = {}
        taskFinishInfo.taskid = this.edited_task.taskid
        taskFinishInfo.userid = this.edited_task.userid
        taskFinishInfo.startofday = this.edited_task.startofday
        if (this.edited_task.realendtime === 0) {
          var finishTime = dateUtil.getNow()
          taskFinishInfo.realendtime = finishTime
        } else {
          taskFinishInfo.realendtime = this.edited_task.realendtime
        }
        taskFinishInfo.comment = this.edited_task.comment
        taskFinishInfo.approve_status = this.edited_task.approve_status
        taskFinishInfo.approve_user = this.edited_task.approve_user
        taskFinishInfo.timeType = this.edited_task.timeType
        console.log('8*******************EEEEEEE')
        console.log(this.pictures)
        taskFinishInfo.pictures = this.pictures
        this.COMMIT_TASK_EXEC_INFO(taskFinishInfo)
        this.$emit('showEdit', false)
      },
      cancelEdit () {
        this.$emit('showEdit', false)
      },
      handleClose () {
        this.cancelEdit()
      },
      handlePictureUploadSucceed (response, file, fileList) {
        if (response.data.status === 0) {
          var pic = {}
          pic.remoteUri = this.backend_uri + response.data.fileurl
          pic.localUri = ''
          pic.createTime = file.raw.lastModified / 1000
          pic.originFileName = file.name
          pic.url = pic.remoteUri
          pic.name = pic.originFileName
          this.pictures.push(pic)
        }
      },
      handlePictureRemove (file, fileList) {
        console.log(file, fileList)
        this.fileTobeRemoved = file
        this.showPicRemoveDialog = true
        return false
      },
      handlePictureCardPreview (file) {
        this.dialogImageUrl = file.url
        this.previewVisible = true
      },
      handlePictureChange (file, fileList) {
        console.log('77777777787777777777777777777')
        console.log('file:', file)
        console.log('filelist:', fileList)
        console.log('this Files:', this.pictures)
      },
      handleBeforeUpload (file) {
        if (this.pictures.length >= 6) {
          this.showPicExceedDialog = true
          return false
        }
        return true
      },
      handleBeforeRemove (file, fileList) {
        console.log('beore remove', file)
        this.fileTobeRemoved = file
        this.showPicRemoveDialog = true
        return false
      },
      handlePreviewClose () {
        this.previewVisible = false
      },
      handleQuitPicExceedDialog (a) {
        this.showPicExceedDialog = false
      },
      handleQuitPicRemoveDialog (choice) {
        this.showPicRemoveDialog = false
        if (choice) {
          // go on remove
        } else {
          // cancel remove
        }
      },
      ...mapActions([ COMMIT_TASK_EXEC_INFO ])
    },
    computed: {
      ...mapGetters(['allRole', 'upload_image_uri', 'backend_uri']),
      Util () { return Util }
    },
    props: ['edited_task', 'dialogVisible', 'selectedDay'],
    watch: {
      dialogVisible (val, oldVal) {
        if (val) {
          this.pictures = this.edited_task.pictures
          console.log('8$$$$$$$$$$$$$$$$$$EEEEEEE')
          console.log(this.pictures)
        }
      }
    },
    created: function () {
    },
    data: () => {
      return {
        formLabelWidth: '120px',
        labelPosition: 'right',
        selectedRoleName: [],
        dialogImageUrl: '',
        pictures: [],
        previewVisible: false,
        showPicExceedDialog: false,
        picExceedDialogContent: '最多能上传6张照片',
        picExceedDialogTitle: '提示',
        showPicRemoveDialog: false,
        picRemoveDialogContent: '确定要删除此照片吗？',
        picRemoveDialogTitle: '删除照片',
        fileTobeRemoved: {}
      }
    }
  }
</script>
