<template>
  <div style="position:relative">
    <div style="width: 100%">
  <el-menu default-active="1" class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <el-submenu index="1" v-show="hasUserCategoryPermission || Util.hasCategoryPermission('PERMISSION_CATEGORY_ROLE') || Util.hasCategoryPermission('PERMISSION_CATEGORY_PERMISSIONROLE')">
      <template slot="title">系统管理</template>
      <el-menu-item index="1-1" v-show="Util.hasCategoryPermission('PERMISSION_CATEGORY_USER')">人员管理</el-menu-item>
      <el-menu-item index="1-2" v-show="Util.hasCategoryPermission('PERMISSION_CATEGORY_ROLE')">岗位管理</el-menu-item>
      <el-menu-item index="1-3" v-show="Util.hasCategoryPermission('PERMISSION_CATEGORY_PERMISSIONROLE')">角色权限管理</el-menu-item>
    </el-submenu>
    <el-submenu index="2">
      <template slot="title">任务管理</template>
      <el-menu-item index="2-1" v-show="Util.hasPermission('PERMISSION_TASK_EDIT_USER_TASK')">日常岗位职责列表</el-menu-item>
      <el-menu-item index="2-2">突发事件处理流程</el-menu-item>
    </el-submenu>
    <el-menu-item index="3" v-show="Util.hasPermission('PERMISSION_TASK_QUERY_USER_LOCATION')">员工定位</el-menu-item>
    <el-menu-item index="4">日常职责</el-menu-item>
    <el-submenu index="5" v-show="Util.hasPermission('PERMISSION_TASK_QUERY_ALL')">
      <template slot="title">信息管理</template>
      <el-menu-item index="5-1">日信息报告</el-menu-item>
      <el-menu-item index="5-2">月信息报告</el-menu-item>
    </el-submenu>
    <!--<el-menu-item index="6">报表输出</el-menu-item>-->
    <el-menu-item index="7">关于我园</el-menu-item>
    <el-menu-item index="8">系统退出</el-menu-item>
  </el-menu>
    </div>
    <div style="position:absolute; top: 50%; height: 40px; right:10px; margin-top: -10px">
    <span>当前用户 {{ user.name }} （{{ userRoleName }}）</span>
    </div>
  </div>
</template>
<script>
  import {mapGetters} from 'vuex'
  import Util from '../store/utils'

  export default {
    methods: {
      handleSelect (key, keyPath) {
        console.log(key, keyPath)
        this.$emit('menuSelect', key)
      },
      handleOpen (key, keyPath) {
        console.log(key, keyPath)
      },
      handleClose (key, keyPath) {
        console.log(key, keyPath)
      }
    },
    computed: {
      ...mapGetters(['user']),
      userRoleName () {
        return Util.getRoleName(this.user.role)
      },
      Util () {
        return Util
      },
      hasUserCategoryPermission () {
        return Util.hasCategoryPermission('PERMISSION_CATEGORY_USER')
      }
    }
  }
</script>
