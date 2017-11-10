<template>
  <div id="app" style="height: 100%" class="layout">
    <div class="header">
      <div class="logo">
        幼儿园安保系统
      </div>
    </div>
    <div class="content">
      <div class="body">
        <mobile-table-user-day-task v-show="user._id != '' && selectedTab == 'today_task'"></mobile-table-user-day-task>
      </div>
    </div>
    <div class="footer">
      <mu-paper class="bottomFixed">
        <mu-bottom-nav :value="selectedTab" @change="handleTabChange">
          <mu-bottom-nav-item value="today_task" title="今日任务"/>
          <mu-bottom-nav-item value="task_info" title="任务统计"/>
          <mu-bottom-nav-item value="user_center" title="用户中心"/>
        </mu-bottom-nav>
      </mu-paper>
      <!--<mu-tabs :value="activeTab" shift @change="handleTabChange">-->
        <!--<mu-tab value="today_task" icon="" title="今日任务"/>-->
        <!--<mu-tab value="task_info" icon="" title="任务统计"/>-->
        <!--<mu-tab value="user_center" icon="" title="用户中心"/>-->
      <!--</mu-tabs>-->
    </div>

  </div>
  <!--<div >-->
    <!--<mt-header fixed title="幼儿园安保系统"></mt-header>-->
    <!---->
    <!--<mt-tabbar v-model="selected" @input="selectTab">-->
      <!--<mt-tab-item id="today_task">-->
        <!--&lt;!&ndash;<img slot="icon" src="../assets/100x100.png">&ndash;&gt;-->
        <!--今日任务-->
      <!--</mt-tab-item>-->
      <!--<mt-tab-item id="task_info">-->
        <!--&lt;!&ndash;<img slot="icon" src="../assets/100x100.png">&ndash;&gt;-->
        <!--任务统计-->
      <!--</mt-tab-item>-->
      <!--<mt-tab-item id="user">-->
        <!--&lt;!&ndash;<img slot="icon" src="../assets/100x100.png">&ndash;&gt;-->
        <!--用户-->
      <!--</mt-tab-item>-->
    <!--</mt-tabbar>-->

    <!--<mobile-user-login></mobile-user-login>-->
  <!--</div>-->
</template>

<script>
  import { Tabbar, TabItem, Header } from 'mint-ui'
  import MobileTableUserDayTask from '../../components/table_user_day_task.vue'
  import { mapGetters, mapActions } from 'vuex'
  import { GET_ALL_USER_TASK_EXEC_DATA, USER_LOGOUT } from '../../store/mutation_types'
  import MobileUserLogin from '../../components/mobile/mobile_user_login.vue'
  export default {
    name: 'app',
    components: {
      Tabbar, TabItem, Header, MobileUserLogin, MobileTableUserDayTask
    },
    computed: {
      ...mapGetters(['datePickerOptionsDay', 'datePickerOptionsMonth', 'user'])
    },
    data: () => {
      return {
        selectedTab: 'today_task'
      }
    },
    methods: {
      ...mapActions([GET_ALL_USER_TASK_EXEC_DATA, USER_LOGOUT]),
      handleTabChange: function (id) {
        this.selectedTab = id
      }
    }
  }
</script>
<style scoped>
   .layout{
     background-color: rgb(236, 236, 236);
     height: 100%;
   }

  .header{
    background-color: #7e57c2;
  }

  .logo{
    font-size: 24px;
    color: white;
    display: inline-block;
    padding: 10px 20px;
  }

  .nav{
    display: inline-block;
    width: calc(100% - 150px);
    margin: 0 auto;
  }

  .tab{
    margin: 0 auto;
    width: 400px;
    background-color: rgba(0, 0, 0, 0);
  }

  .content{
    width: 90%;
    margin: 0 auto;
    height: auto;
  }

  .breadcrumb{
    margin: 10px 0;
  }

  .body{
    background-color: white;
    border-radius: 5px;
    height: auto;
  }

  .footer{
    padding: 20px 0;
    text-align: center;
    margin-bottom: 0px;
  }

   .bottomFixed{
     position: fixed;
     width: 100%;
     left: 0;
     bottom: 0;
     z-index:1000;
   }
  /*.bottom_bar_title {*/
    /*color: white;*/
  /*}*/
</style>
