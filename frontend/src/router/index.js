import Vue from 'vue'
import Router from 'vue-router'
import store from '../store/store'

import UserLogin from '../components/user_login.vue'
import ChangePass from '../components/change_password_panel.vue'
import UserList from '../components/table_user_list.vue'
import UserGroupList from '../components/table_user_group_list.vue'
import RoleList from '../components/table_role_list.vue'
import PermissionRoleList from '../components/table_permission_role_list.vue'
import DutyList from '../components/table_duty_list.vue'
import DutyCategoryList from '../components/table_duty_category_list.vue'
import UserDayTaskList from '../components/table_user_day_task.vue'
import EmergencyHandle from '../components/emergency_handle.vue'
import AllUserTaskExecStat from '../components/table_all_user_task_exec_stat.vue'
import OneUserAllTaskExecStat from '../components/table_one_user_all_task_exec_stat.vue'
import OneUserOneTaskExecStat from '../components/table_one_user_one_task_exec_stat.vue'
import AllUserLocation from '../components/table_user_location_list.vue'
import InformList from '../components/table_inform_list.vue'
import UserDutyNotificationList from '../components/table_user_duty_notification_list.vue'
import UserInformList from '../components/table_user_inform_list.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/login',
      name: 'userlogin',
      component: UserLogin
    },
    {
      path: '/change_pass',
      name: 'ChangePass',
      component: ChangePass
    },
    {
      path: '/user_list',
      name: 'UserList',
      component: UserList
    },
    {
      path: '/user_group_list',
      name: 'UserGroupList',
      component: UserGroupList
    },
    {
      path: '/role_list',
      name: 'RoleList',
      component: RoleList,
      meta: {
        keepAlive: false
      }
    },
    {
      path: '/permission_role_list',
      name: 'PermissionRoleList',
      component: PermissionRoleList
    },
    {
      path: '/duty_category_list',
      name: 'DutyCategoryList',
      component: DutyCategoryList
    },
    {
      path: '/duty_list',
      name: 'DutyList',
      component: DutyList
    },
    {
      path: '/user_day_task_list/:timeType',
      name: 'UserDayTaskList',
      component: UserDayTaskList
    },
    {
      path: '/emergency_handle',
      name: 'EmergencyHandle',
      component: EmergencyHandle
    },
    {
      path: '/all_user_task_exec_stat/:datetime_type/:starttime',
      name: 'AllUserTaskExecStat',
      component: AllUserTaskExecStat
    },
    {
      path: '/one_user_all_task_stat/:userid/:startofday/:endofday',
      name: 'OneUserAllTaskExecStat',
      component: OneUserAllTaskExecStat,
      meta: {
        keepAlive: false
      }
    },
    {
      path: '/one_user_one_task_stat/:selectedData',
      name: 'OneUserOneTaskExecStat',
      component: OneUserOneTaskExecStat,
      meta: {
        keepAlive: false
      }
    },
    {
      path: '/user_location',
      name: 'AllUserLocation',
      component: AllUserLocation,
      meta: {
        keepAlive: false
      }
    },
    {
      path: '/inform',
      name: 'InformList',
      component: InformList,
      meta: {
        keepAlive: false
      }
    },
    {
      path: '/user_duty_notification/:type',
      name: 'UserDutyNotificationList',
      component: UserDutyNotificationList,
      meta: {
        keepAlive: false
      }
    },
    {
      path: '/underline_duty_notification/:type',
      name: 'UnderlineDutyNotificationList',
      component: UserDutyNotificationList,
      meta: {
        keepAlive: false
      }
    },
    {
      path: '/user_inform',
      name: 'UserInformList',
      component: UserInformList,
      meta: {
        keepAlive: false
      }
    }
  ]
  // mode: 'history',
  // base: '/'
})
/**
 * 登录钩子函数
 * to 即将要进入的目标 路由对象
 * from 当前导航正要离开的路由
 * next 一定要调用该方法来 resolve 这个钩子
 * next() 进行管道中的下一个钩子 如果全部钩子执行完了，则状态就是 confirmed （确认的）
 */
router.beforeEach((to, from, next) => {
  console.log('router.beforeeach:' + to.fullPath)
  console.log(to.params)

  // if (to.meta.requireAuth) { // 判断该路由是否需要登录权限
  //   if (store.state.sessionToken) { // 通过vuex state获取当前的token是否存在
  //     next()
  //   } else {
  //     next({
  //       path: '/login',  // 跳转到登录页面
  //       query: { redirect: to.fullPath } // 将跳转的路由path作为参数，用于登录成功后回到登录前页面
  //     })
  //   }
  // } else {
  //   next()
  // }
  if (store.state.user === '') {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
})

export default router

