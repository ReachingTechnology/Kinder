<template>
  <div>
    <h2>{{title}}</h2>
    <div align="left" style="margin-left: 10px" v-show="Util.hasPermission('PERMISSION__FILE_UPLOAD')">
      <el-upload
        class="upload-demo"
        :action="uploadUrl"
        :data="uploadParam"
        :on-change="onFileChange"
        :on-success="onFileUploadSucceed"
        :on-remove="onFileRemove"
        :show-file-list="false"
        :file-list="documentList">
        <el-button size="small" type="primary">点击上传文件</el-button>
        <!--<div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>-->
      </el-upload>
    </div>
    <br/>
    <el-table
      :data="documentList"
      style="width: 100%"
      :default-sort = "{prop: 'upload_time', order: 'descending'}"
      >
      <el-table-column
        prop="name"
        label="文件名称"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="sizeDisplay"
        label="文件大小"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="upload_time_display"
        label="上传时间"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center">
        <template scope="scope">
          <div style="display: inline-block">
            <el-button
              size="mini"
              type="success"
              ><a download :href="scope.row.url">下载</a></el-button>
          </div>
          <div :style="canRemove(scope.row.uploader) ? 'display: inline-block' : 'display:none'" v-show="Util.hasPermission('PERMISSION__FILE_UPLOAD')">
            <el-button
              size="mini"
              @click="onFileRemove(scope.row)" type="danger">删除</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <warning-dialog @choice="handleQuitChoice" :dialogVisible="showWarningDialog" :title="warningDialogTitle" :content="warningDialogContent"></warning-dialog>
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
  import { GET_ALL_DOCUMENT, REMOVE_DOCUMENT } from '../store/mutation_types'
  import Moment from 'moment'
  import Util from '../store/utils'
  import WarningDialog from './warning_dialog.vue'

  export default {
    name: 'table_document_list',
    components: {
      WarningDialog
    },
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      onFileChange (file, fileList) {
      },
      onFileUploadSucceed (response, file, fileList) {
        console.log('upload succeed.......')
        this.GET_ALL_DOCUMENT(this.level)
      },
      canRemove (uploaderId) {
        return uploaderId === this.user._id
      },
      onFileRemove (row) {
        this.warningDialogContent = '确认删除文件 ' + row.name + ' 吗？'
        this.showWarningDialog = true
        this.removing_file = row.id
      },
      handleQuitChoice (choice) {
        if (choice) {
          var param = {id: this.removing_file, level: this.level}
          this.REMOVE_DOCUMENT(param)
        }
        this.showWarningDialog = false
      },
      ...mapActions([GET_ALL_DOCUMENT, REMOVE_DOCUMENT])
    },
    computed: {
      ...mapGetters(['upload_document_base_uri', 'allDocument', 'user']),
      title () {
        if (this.level === 'COUNTRY') {
          return '国家政策文件'
        } else if (this.level === 'PROV&CITY') {
          return '省市指导文件'
        } else {
          return '园区工作文件'
        }
      },
      documentList () {
        var data = []
        var docList = this.allDocument[this.level]
        if (docList === undefined) {
          return []
        }
        for (var i = 0, len = docList.length; i < len; i++) {
          var doc = {}
          doc.id = docList[i]._id
          doc.name = docList[i].name
          doc.url = docList[i].url
          doc.status = 'finished'
          doc.uploader = docList[i].uploader
          doc.sizeDisplay = Math.round(docList[i].size / 1024 + 1) + 'K'
          doc.upload_time_display = Moment(docList[i].upload_time * 1000).format('YYYY年M月D日 H:mm')
          data.push(doc)
        }
        return data
      },
      uploadUrl () {
        if (this.level === 'COUNTRY') {
          return this.upload_document_base_uri + 'upload_document_country'
        } else if (this.level === 'PROV&CITY') {
          return this.upload_document_base_uri + 'upload_document_city'
        } else {
          return this.upload_document_base_uri + 'upload_document_kindergarten'
        }
      },
      Util () {
        return Util
      }
    },
    watch: {
      '$route' (to, from) {
        console.log('***********************')
        this.level = this.$route.params.level
        this.uploadParam = {level: this.level, uploader: this.user._id}
        console.log(this.level)
        this.GET_ALL_DOCUMENT(this.level)
      }
    },
    beforeRouteEnter: function (to, from, next) {
      next(vm => {
        vm.level = vm.$route.params.level
        vm.uploadParam = {level: vm.level, uploader: vm.user._id}
        vm.GET_ALL_DOCUMENT(vm.level)
      })
    },
    beforeRouteLeave: function (to, from, next) {
      this.$destroy()
      next()
    },
    mounted: function () {
      var files = document.getElementsByClassName('el-upload-list__item-name')
      console.log('^^^^^^^^^^^^^^^^^^^^^^###')
      console.log(files.length)
      for (var i = 0; i < files.length; i++) {
        console.log('^^^^^^^^^^^^^^^^^^^^^^')
        console.log(files[i])
        var name = files[i].innerHTML
        console.log(name)
        if (name === '德国.png') {
        }
      }
    },
    data: function () {
      return {
        level: this.$route.params.level,
        uploadParam: {},
        showWarningDialog: false,
        warningDialogTitle: '删除文件',
        warningDialogContent: '',
        removing_file: ''
      }
    }
  }
</script>
