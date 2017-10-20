import Vue from 'vue'
import Router from 'vue-router'
import store from '../store/store'

import UserLogin from '../components/user_login.vue'
import UserList from '../components/table_user_list.vue'
import RoleList from '../components/table_role_list.vue'
import PermissionRoleList from '../components/table_permission_role_list.vue'
import DutyList from '../components/table_duty_list.vue'
import UserDayTaskList from '../components/table_user_day_task.vue'
import EmergencyHandle from '../components/emergency_handle.vue'
import AllUserTaskExecStat from '../components/table_all_user_task_exec_stat.vue'
import OneUserAllTaskExecStat from '../components/table_one_user_all_task_exec_stat.vue'
import OneUserOneTaskExecStat from '../components/table_one_user_one_task_exec_stat.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/login',
      name: 'userlogin',
      component: UserLogin
    },
    {
      path: '/user_list',
      name: 'UserList',
      component: UserList
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
      path: '/duty_list',
      name: 'DutyList',
      component: DutyList
    },
    {
      path: '/user_day_task_list',
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
      path: '/one_user_all_task_stat/:selectedData',
      name: 'OneUserAllTaskExecStat',
      component: OneUserAllTaskExecStat
    },
    {
      path: '/one_user_one_task_stat/:selectedData',
      name: 'OneUserOneTaskExecStat',
      component: OneUserOneTaskExecStat
    }
  ]
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

