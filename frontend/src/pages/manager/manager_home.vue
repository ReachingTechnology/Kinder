<template>
  <div id="app">
    <user-login  v-show="user._id == ''"></user-login>
    <nav-menu v-show="user._id != ''" @menuSelect="menuSelected"></nav-menu>
    <table-user-list v-show="user._id != '' && menuKey == '1-1'"></table-user-list>
    <table-role-list v-show="user._id != '' && menuKey == '1-2'"></table-role-list>
    <table-duty-list v-show="user._id != '' && menuKey == '2-1'"></table-duty-list>
    <emergency-handle v-show="user._id != '' && menuKey == '2-2'"></emergency-handle>
    <table-manage-statistic-data :datePickerOption="datePickerOption" :datetime_type="dateType" v-show="user._id != '' && menuKey == '5-1' || menuKey == '5-2'"></table-manage-statistic-data>
    <table-user-day-task v-show="user._id != '' && menuKey == '4'"></table-user-day-task>
  </div>
</template>

<script>
  import UserLogin from '../../components/user_login.vue'
  import TableManageStatisticData from '../../components/table_all_user_task_exec_stat.vue'
  import NavMenu from '../../components/nav_menu.vue'
  import TableUserList from '../../components/table_user_list.vue'
  import TableRoleList from '../../components/table_role_list.vue'
  import TableTaskList from '../../components/table_task_list.vue'
  import TableUserDayTask from '../../components/table_user_day_task.vue'
  import TableDutyList from '../../components/table_duty_list.vue'
  import EmergencyHandle from '../../components/emergency_handle.vue'
  import dateUtil from '../../utils/DateUtil'
  import { mapGetters, mapActions } from 'vuex'
  import { GET_ALL_DATA, USER_LOGOUT } from '../../store/mutation_types'
  export default {
    name: 'app',
    components: {
      UserLogin,
      TableUserList,
      TableManageStatisticData,
      NavMenu,
      TableRoleList,
      TableTaskList,
      TableDutyList,
      TableUserDayTask,
      EmergencyHandle
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
        datetype_month: 'month'
      }
    },
    methods: {
      ...mapActions([GET_ALL_DATA, USER_LOGOUT]),
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
            this.USER_LOGOUT()
            window.location.href = this.backend_uri + '/manager.html'
        }
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
