/**
 * Created by HOZ on 28/08/2017.
 */
import axios from 'axios'
import { GET_ALL_DATA, USER_LOGIN, USER_LOGOUT,
  GET_DUTY_BY_USER, UPSERT_USER_ACCOUNT, GET_ALL_USER_ACCOUNT, REMOVE_USERS,
  GET_ALL_ROLE, UPSERT_ROLE, REMOVE_ROLES,
  GET_ALL_PERMISSION_ROLE, UPSERT_PERMISSION_ROLE, GET_ALL_PERMISSION, REMOVE_PERMISSION_ROLES,
  GET_ALL_TASK, UPSERT_TASK, COMMIT_TASK_EXEC_INFO, GET_TASK_EXEC_DATA_BY_DATE, GET_USER_TASK_EXEC_DATA_BY_DATERANGE, GET_ONE_TASK_EXEC_DATA_BY_DATERANGE,
  GET_ALL_DUTY, UPSERT_DUTY, REMOVE_DUTIES } from './mutation_types'
// import dateUtil from '../utils/DateUtil'

// axios.defaults.baseURL = 'https://47.94.192.237:7070'
axios.defaults.baseURL = 'https://127.0.0.1:7070'
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
axios.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest'
// axios.defaults.headers.post['Content-Type'] = 'application/json'

const actions = {
  [ USER_LOGIN ]: function (store, param) {
    axios.post('/user/user_login', param)
      .then(function (response) {
        console.log('user login')
        console.log(response.data)
        store.commit('SET_USER', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ USER_LOGOUT ]: function (store, param) {
    var data = {}
    data._id = ''
    data.name = ''
    store.commit('SET_USER', data)
  },
  [ GET_ALL_DATA ]: function (store, param) {
    'use strict'
    axios.post('/manager/query_all_by_time', param)
    // axios.get('/manager/query_all_by_time?starttime=' + param['starttime'] + '&endtime=' + param['endtime'])
      .then(function (response) {
        console.log('get all statistic data')
        console.log(response.data)
        store.commit('SET_ALL_STATISTIC_DATA', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ UPSERT_USER_ACCOUNT ]: function (store, param) {
    'use strict'
    console.log('user birthday:' + param.birthday)

    axios.post('/management/upsert_user', param)
      .then(function (response) {
        axios.get('/management/query_all_user')
          .then(function (response) {
            store.commit('SET_ALL_USER_ACCOUNT', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ GET_ALL_USER_ACCOUNT ]: function (store, param) {
    'use strict'
    axios.get('/management/query_all_user')
      .then(function (response) {
        console.log('get all user:')
        console.log(response.data)
        store.commit('SET_ALL_USER_ACCOUNT', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ REMOVE_USERS ]: function (store, param) {
    axios.post('/management/remove_user', param)
      .then(function (response) {
        console.log('remove users:' + param)
        console.log(response.data)
        axios.get('/management/query_all_user')
          .then(function (response) {
            store.commit('SET_ALL_USER_ACCOUNT', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
  },
  [ GET_ALL_ROLE ]: function (store, param) {
    'use strict'
    console.log('get all role!!!')
    axios.get('/management/query_all_role')
      .then(function (response) {
        console.log('get all roles')
        store.commit('SET_ALL_ROLE', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ UPSERT_ROLE ]: function (store, param) {
    'use strict'
    axios.post('/management/upsert_role', param)
      .then(function (response) {
        console.log(response.data)
        axios.get('/management/query_all_role')
          .then(function (response) {
            console.log('get all roles')
            store.commit('SET_ALL_ROLE', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ REMOVE_ROLES ]: function (store, param) {
    axios.post('/management/remove_role', param)
      .then(function (response) {
        console.log('remove roles:' + param)
        console.log(response.data)
        axios.get('/management/query_all_role')
          .then(function (response) {
            store.commit('SET_ALL_ROLE', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
  },
  [ GET_ALL_PERMISSION_ROLE ]: function (store, param) {
    'use strict'
    console.log('get all permission role!!!')
    axios.get('/management/query_all_permission_role')
      .then(function (response) {
        console.log('get all permission roles')
        store.commit('SET_ALL_PERMISSION_ROLE', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ UPSERT_PERMISSION_ROLE ]: function (store, param) {
    'use strict'
    axios.post('/management/upsert_permission_role', param)
      .then(function (response) {
        console.log(response.data)
        axios.get('/management/query_all_permission_role')
          .then(function (response) {
            console.log('get all permission roles')
            store.commit('SET_ALL_PERMISSION_ROLE', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ REMOVE_PERMISSION_ROLES ]: function (store, param) {
    'use strict'
    axios.post('/management/remove_permission_role', param)
      .then(function (response) {
        console.log(response.data)
        axios.get('/management/query_all_permission_role')
          .then(function (response) {
            console.log('get all permission roles')
            store.commit('SET_ALL_PERMISSION_ROLE', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ GET_ALL_PERMISSION ]: function (store, param) {
    'use strict'
    axios.get('/management/query_all_permission')
      .then(function (response) {
        console.log('et all permission')
        console.log(response.data)
        store.commit('SET_ALL_PERMISSION', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ GET_ALL_DUTY ]: function (store, param) {
    'use strict'
    axios.get('/management/query_all_duty')
      .then(function (response) {
        console.log('get all duty')
        store.commit('SET_ALL_DUTY', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ GET_DUTY_BY_USER ]: function (store, param) {
    'use strict'
    axios.post('/duty/query_duty_by_user', {'userid': store.state.user['id']})
      .then(function (response) {
        console.log('get data by user:')
        console.log(response.data)
        store.commit('SET_USER_DUTY_DATA', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ UPSERT_DUTY ]: function (store, param) {
    'use strict'
    axios.post('/management/upsert_duty', param)
      .then(function (response) {
        console.log(response.data)
        axios.get('/management/query_all_duty')
          .then(function (response) {
            console.log('get all duties')
            store.commit('SET_ALL_DUTY', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ REMOVE_DUTIES ]: function (store, param) {
    axios.post('/management/remove_duty', param)
      .then(function (response) {
        console.log('remove duties:' + param)
        console.log(response.data)
        axios.get('/management/query_all_duty')
          .then(function (response) {
            store.commit('SET_ALL_DUTY', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
  },
  [ GET_ALL_TASK ]: function (store, param) {
    'use strict'
    axios.get('/management/query_all_task')
      .then(function (response) {
        console.log('get all tasks')
        store.commit('SET_ALL_TASK', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ UPSERT_TASK ]: function (store, param) {
    'use strict'
    axios.post('/management/upsert_task', param)
      .then(function (response) {
        console.log(response.data)
        axios.get('/management/query_all_task')
          .then(function (response) {
            console.log('get all tasks')
            store.commit('SET_ALL_TASK', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ COMMIT_TASK_EXEC_INFO ]: function (store, param) {
    'use strict'
    axios.post('/user/commit_task_exec_info', param)
      .then(function (response) {
        console.log(response.data)
        let newparam = {}
        newparam.userid = param.userid
        newparam.startofday = param.startofday
        axios.post('/user/get_task_exec_info_by_date', newparam)
          .then(function (response) {
            store.commit('SET_USER_DUTY_EXEC_DATA', response.data)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ GET_TASK_EXEC_DATA_BY_DATE ]: function (store, param) {
    console.log('GET_TASK_EXEC_DATA_BY_DATE')
    console.log(param)
    axios.post('/user/get_task_exec_info_by_date', param)
      .then(function (response) {
        console.log(response.data)
        console.log('update user duty data')
        store.commit('SET_USER_DUTY_EXEC_DATA', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ GET_USER_TASK_EXEC_DATA_BY_DATERANGE ]: function (store, param) {
    console.log('GET_USER_TASK_EXEC_DATA_BY_DATERANGE')
    console.log(param)
    axios.post('/user/get_user_task_exec_info_by_daterange', param)
      .then(function (response) {
        store.commit('SET_USER_TASK_EXEC_DATA_BY_DATERANGE', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  [ GET_ONE_TASK_EXEC_DATA_BY_DATERANGE ]: function (store, param) {
    console.log('GET_ONE_TASK_EXEC_DATA_BY_DATERANGE')
    console.log(param)
    axios.post('/user/get_one_task_exec_info_by_daterange', param)
      .then(function (response) {
        store.commit('SET_ONE_TASK_EXEC_DATA_BY_DATERANGE', response.data)
      })
      .catch(function (error) {
        console.log(error)
      })
  }
}
export default actions
