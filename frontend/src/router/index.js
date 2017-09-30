import Vue from 'vue'
import Router from 'vue-router'
import store from '../store/store'

import UserLogin from '../components/user_login.vue'
import UserDaterangeTaskStat from '../components/table_user_daterange_task_stat.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/login',
      name: 'userlogin',
      component: UserLogin
    },
    {
      path: '/user_task_stat/:selectedData',
      name: 'userTaskStat',
      component: UserDaterangeTaskStat
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

