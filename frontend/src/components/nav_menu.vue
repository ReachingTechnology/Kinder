<template>
  <div style="position:relative">
    <div style="width: 100%">
  <el-menu :default-active="active_menu" class="el-menu-demo" mode="horizontal" @select="handleSelect">
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
  import dateUtil from '../utils/DateUtil'
  import { DATETYPE_DAY, DATETYPE_MONTH } from '../store/common_defs'

  export default {
    methods: {
      handleSelect (key, keyPath) {
        console.log(key, keyPath)
        var params = {}
        this.active_menu = key
        switch (key) {
          case '1-1':
            this.$router.push({name: 'UserList'})
            break
          case '1-2':
            this.$router.push({name: 'RoleList'})
            break
          case '1-3':
            this.$router.push({name: 'PermissionRoleList'})
            break
          case '2-1':
            this.$router.push({name: 'DutyList'})
            break
          case '2-2':
            this.$router.push({name: 'EmergencyHandle'})
            break
          case '4':
            this.$router.push({name: 'UserDayTaskList'})
            break
          case '5-1':
            params = {
              'starttime': dateUtil.getStartOfToday(),
              'datetime_type': DATETYPE_DAY
            }
            this.$router.push({name: 'AllUserTaskExecStat', params: params})
            break
          case '5-2':
            params = {
              'starttime': dateUtil.getStartofThisMonth(),
              'datetime_type': DATETYPE_MONTH
            }
            this.$router.push({name: 'AllUserTaskExecStat', params: params})
            break
        }
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
    },
    created: function () {
      if (this.active_menu === '4') {
        this.$router.push({name: 'UserDayTaskList'})
      }
    },
    data: function () {
      return {
        active_menu: '4'
      }
    }
  }
</script>
