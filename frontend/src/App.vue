<template>
  <div id="app">
    <user-login  v-show="user._id == ''"></user-login>
    <nav-menu v-show="user._id != ''" @menuSelect="menuSelected"></nav-menu>
    <table-user-list v-show="user._id != '' && menuKey == '1-1'"></table-user-list>
    <table-role-list v-show="user._id != '' && menuKey == '1-2'"></table-role-list>
    <table-permission-role-list v-show="user._id != '' && menuKey == '1-3'"></table-permission-role-list>
    <table-duty-list v-show="user._id != '' && menuKey == '2-1'"></table-duty-list>
    <emergency-handle v-show="user._id != '' && menuKey == '2-2'"></emergency-handle>
    <baidu-map v-show="user._id != '' && menuKey == '3'"></baidu-map>
    <table-manage-statistic-data :datePickerOption="datePickerOption" :datetime_type="dateType" v-show="user._id != '' && menuKey == '5-1' || menuKey == '5-2'"></table-manage-statistic-data>
    <table-user-day-task v-show="user._id != '' && menuKey == '4'"></table-user-day-task>
    <introduction v-show="menuKey == '7'"></introduction>
    <warning-dialog @choice="handleQuitChoice" :dialogVisible="showWarningDialog" :title="warningDialogTitle" :content="warningDialogContent"></warning-dialog>
    <router-view></router-view>
  </div>
</template>

<script>
  import UserLogin from './components/user_login.vue'
  import TableManageStatisticData from './components/table_manage_statistic.vue'
  import NavMenu from './components/nav_menu.vue'
  import TableUserList from './components/table_user_list.vue'
  import TableRoleList from './components/table_role_list.vue'
  import TablePermissionRoleList from './components/table_permission_role_list.vue'
  import TableTaskList from './components/table_task_list.vue'
  import TableUserDayTask from './components/table_user_day_task.vue'
  import TableDutyList from './components/table_duty_list.vue'
  import EmergencyHandle from './components/emergency_handle.vue'
  import Introduction from './components/introduction.vue'
  import BaiduMap from './components/baidumap.vue'
  import dateUtil from './utils/DateUtil'
  import { mapGetters, mapActions } from 'vuex'
  import { GET_ALL_USER_ACCOUNT, GET_ALL_ROLE, GET_ALL_DATA, USER_LOGOUT } from './store/mutation_types'
  import WarningDialog from './components/warning_dialog.vue'
  export default {
    name: 'app',
    components: {
      WarningDialog,
      UserLogin,
      TableUserList,
      TableManageStatisticData,
      NavMenu,
      TableRoleList,
      TablePermissionRoleList,
      TableTaskList,
      TableDutyList,
      TableUserDayTask,
      EmergencyHandle,
      Introduction,
      BaiduMap
    },
    computed: {
      ...mapGetters(['datePickerOptionsDay', 'datePickerOptionsMonth', 'user', 'backend_uri']),
      dateType () {
        if (this.menuKey === '5-1') {
          return this.datetype_day
        }
        if (this.menuKey === '5-2') {
          return this.datetype_month
        }
      },
      datePickerOption () {
        if (this.menuKey === '5-1') {
          return this.datePickerOptionsDay
        }
        if (this.menuKey === '5-2') {
          return this.datePickerOptionsMonth
        }
      }
    },
    data: () => {
      return {
        menuKey: '4',
        datetype_day: 'date',
        datetype_month: 'month',
        showWarningDialog: false,
        warningDialogTitle: '退出登录',
        warningDialogContent: '确认退出当前登录吗？'
      }
    },
    created: function () {
//      this.user._id = '000001'
//      this.user.role = 'ROLE_0001'
//      this.user.name = 'zhanghao'
      this.GET_ALL_USER_ACCOUNT()
      this.GET_ALL_ROLE()
    },
    methods: {
      ...mapActions([GET_ALL_USER_ACCOUNT, GET_ALL_ROLE, GET_ALL_DATA, USER_LOGOUT]),
      menuSelected: function (key) {
        console.log('menu selected:' + key)
        this.menuKey = key
        var params = {}
        switch (key) {
          case '5-1':
            params = {
              'starttime': dateUtil.getStartOfToday(),
              'datetime_type': this.datetype_day
            }
            this.GET_ALL_DATA(params)
            break
          case '5-2':
            params = {
              'starttime': dateUtil.getStartofThisMonth(),
              'datetime_type': this.datetype_month
            }
            this.GET_ALL_DATA(params)
            break
          case '8':
            this.showWarningDialog = true
        }
      },
      handleQuitChoice (choice) {
        if (choice) {
          this.USER_LOGOUT()
          window.location.href = this.backend_uri
        }
        this.showWarningDialog = false
      }
    }
  }
</script>
<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 20px;
  }
</style>
