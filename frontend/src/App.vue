<template>
  <div id="app">
    <user-login  v-show="user._id == ''"></user-login>
    <nav-menu v-show="user._id != ''" @menuSelect="menuSelected"></nav-menu>
    <keep-alive>
      <router-view v-show="user._id != ''"></router-view>
    </keep-alive>
    <warning-dialog @choice="handleQuitChoice" :dialogVisible="showWarningDialog" :title="warningDialogTitle" :content="warningDialogContent"></warning-dialog>
  </div>
</template>

<script>
  import UserLogin from './components/user_login.vue'
  import NavMenu from './components/nav_menu.vue'
  import { mapGetters, mapActions } from 'vuex'
  import { GET_ALL_USER_ACCOUNT, GET_ALL_ROLE, GET_ALL_DUTY, GET_ALL_PERMISSION, GET_ALL_PERMISSION_ROLE, GET_ALL_DATA, USER_LOGOUT } from './store/mutation_types'
  import WarningDialog from './components/warning_dialog.vue'
  export default {
    name: 'app',
    components: {
      WarningDialog,
      UserLogin,
      NavMenu
    },
    computed: {
      ...mapGetters(['datePickerOptionsDay', 'datePickerOptionsMonth', 'user', 'backend_uri'])
    },
    data: () => {
      return {
        showWarningDialog: false,
        warningDialogTitle: '退出登录',
        warningDialogContent: '确认退出当前登录吗？'
      }
    },
    created: function () {
      this.user._id = '000001'
      this.user.role = ['ROLE_0001', 'ROLE_0004']
      this.user.name = 'zhanghao'
      this.GET_ALL_PERMISSION_ROLE()
      this.GET_ALL_PERMISSION()
      this.GET_ALL_USER_ACCOUNT()
      this.GET_ALL_ROLE()
      this.GET_ALL_DUTY()
    },
    methods: {
      ...mapActions([GET_ALL_USER_ACCOUNT, GET_ALL_ROLE, GET_ALL_DUTY, GET_ALL_PERMISSION, GET_ALL_PERMISSION_ROLE, GET_ALL_DATA, USER_LOGOUT]),
      menuSelected: function (key) {
        console.log('menu selected:' + key)
        this.menuKey = key
        switch (key) {
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
