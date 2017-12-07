<template>
  <div style="position:relative; overflow: visible">
    <div style="width: 100%">
  <el-menu :default-active="active_menu" class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <el-submenu index="1" v-show="hasUserCategoryPermission || Util.hasCategoryPermission('PERMISSION_CATEGORY_ROLE') || Util.hasCategoryPermission('PERMISSION_CATEGORY_PERMISSIONROLE')">
      <template slot="title">系统管理</template>
      <el-menu-item index="1-1" v-show="Util.hasCategoryPermission('PERMISSION_CATEGORY_USER')">人员管理</el-menu-item>
      <el-menu-item index="1-4" v-show="Util.hasCategoryPermission('PERMISSION_CATEGORY_USER')">小组管理</el-menu-item>
      <el-menu-item index="1-2" v-show="Util.hasCategoryPermission('PERMISSION_CATEGORY_ROLE')">岗位管理</el-menu-item>
      <el-menu-item index="1-3" v-show="Util.hasCategoryPermission('PERMISSION_CATEGORY_PERMISSIONROLE')">角色权限管理</el-menu-item>
    </el-submenu>
    <el-submenu index="2">
      <template slot="title">职责管理</template>
      <el-menu-item index="2-1" v-show="Util.hasPermission('PERMISSION_TASK_EDIT_USER_TASK')">职责类别列表</el-menu-item>
      <el-menu-item index="2-2" v-show="Util.hasPermission('PERMISSION_TASK_EDIT_USER_TASK')">岗位职责列表</el-menu-item>
      <el-menu-item index="2-3">突发事件处理流程</el-menu-item>
    </el-submenu>
    <el-menu-item index="3" v-show="Util.hasPermission('PERMISSION_TASK_QUERY_USER_LOCATION')">员工定位</el-menu-item>
    <el-submenu index="4">
      <template slot="title">职责列表</template>
      <el-menu-item index="4-1" v-show="Util.hasPermission('PERMISSION_TASK_EDIT_USER_TASK')">日常职责</el-menu-item>
      <el-menu-item index="4-2" v-show="Util.hasPermission('PERMISSION_TASK_EDIT_USER_TASK')">定期职责</el-menu-item>
      <el-menu-item index="4-3" v-show="Util.hasPermission('PERMISSION_TASK_EDIT_USER_TASK')">特定时间职责</el-menu-item>
      <el-menu-item index="4-4" v-show="Util.hasPermission('PERMISSION_TASK_EDIT_USER_TASK')">小组职责</el-menu-item>
    </el-submenu>
    <el-submenu index="5" v-show="Util.hasPermission('PERMISSION_TASK_QUERY_ALL')">
      <template slot="title">信息管理</template>
      <el-menu-item index="5-1">信息统计</el-menu-item>
      <el-menu-item index="5-2">工作审批</el-menu-item>
    </el-submenu>
    <el-submenu index="6">
      <template slot="title">安全秘书</template>
      <el-menu-item index="6-1">我的消息</el-menu-item>
      <el-menu-item index="6-2">工作通知列表</el-menu-item>
    </el-submenu>
    <el-submenu index="7">
      <template slot="title">文件管理</template>
      <el-menu-item index="7-1">文件列表</el-menu-item>
    </el-submenu>
    <el-submenu index="8">
      <template slot="title">个人中心</template>
      <el-menu-item index="8-1">修改密码</el-menu-item>
      <el-menu-item index="8-2">退出登录</el-menu-item>
    </el-submenu>
  </el-menu>
    </div>
    <div style="position:absolute; top: 50%; height: 40px; right:10px; margin-top: -10px">
      <span>当前用户 {{ user.name }} （{{ userRoleName }}）</span>
    </div>
  </div>
</template>
<script>
  import {mapGetters, mapActions} from 'vuex'
  import Util from '../store/utils'
  import dateUtil from '../utils/DateUtil'
  import { DATETYPE_DAY, DATETYPE_MONTH, DUTY_TIME_TYPE_ROUTINE, DUTY_TIME_TYPE_PERIODICAL, DUTY_TIME_TYPE_SPECIFIC, DUTY_TIME_TYPE_GROUP } from '../store/common_defs'
  import { SET_ACTIVE_MENU } from '../store/mutation_types'
  export default {
    methods: {
      handleSelect (key, keyPath) {
        console.log(key, keyPath)
        var params = {}
        this.active_menu = key
        this.SET_ACTIVE_MENU({'active_menu': this.active_menu})
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
          case '1-4':
            this.$router.push({name: 'UserGroupList'})
            break
          case '2-1':
            this.$router.push({name: 'DutyCategoryList'})
            break
          case '2-2':
            this.$router.push({name: 'DutyList'})
            break
          case '2-3':
            this.$router.push({name: 'EmergencyHandle'})
            break
          case '3':
            this.$router.push({name: 'AllUserLocation'})
            break
          case '4-1':
            this.$router.push({name: 'UserDayTaskList', params: {'timeType': DUTY_TIME_TYPE_ROUTINE}})
            break
          case '4-2':
            this.$router.push({name: 'UserDayTaskList', params: {'timeType': DUTY_TIME_TYPE_PERIODICAL}})
            break
          case '4-3':
            this.$router.push({name: 'UserDayTaskList', params: {'timeType': DUTY_TIME_TYPE_SPECIFIC}})
            break
          case '4-4':
            this.$router.push({name: 'UserDayTaskList', params: {'timeType': DUTY_TIME_TYPE_GROUP}})
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
          case '6-1':
            this.$router.push({name: 'UserMessageList'})
            break
          case '6-2':
            this.$router.push({name: 'InformList'})
            break
          case '8-1':
            this.$router.push({name: 'ChangePass'})
            break
        }
        this.$emit('menuSelect', key)
      },
      handleOpen (key, keyPath) {
        console.log(key, keyPath)
      },
      handleClose (key, keyPath) {
        console.log(key, keyPath)
      },
      ...mapActions([SET_ACTIVE_MENU])
    },
    computed: {
      ...mapGetters(['user']),
      userRoleName () {
        return Util.getRoleNames(this.user.role).join(', ')
      },
      Util () {
        return Util
      },
      hasUserCategoryPermission () {
        return Util.hasCategoryPermission('PERMISSION_CATEGORY_USER')
      }
    },
    created: function () {
      if (this.active_menu === '4-1') {
        this.$router.push({name: 'UserDayTaskList', params: {'timeType': DUTY_TIME_TYPE_ROUTINE}})
        SET_ACTIVE_MENU({'active_menu': this.active_menu})
      }
    },
    data: function () {
      return {
        active_menu: '4-1'
      }
    }
  }
</script>
