/**
 * Created by HOZ on 28/08/2017.
 */
export const SET_ACTIVE_MENU = 'SET_ACTIVE_MENU'

export const GET_ALL_USER_TASK_EXEC_DATA = 'GET_ALL_USER_TASK_EXEC_DATA'
export const GET_ALL_USER_TASK_EXEC_DATA_BY_DATERANGE = 'GET_ALL_USER_TASK_EXEC_DATA_BY_DATERANGE'

// user login/logout
export const GET_CURRENT_USER = 'GET_CURRENT_USER'
export const USER_LOGIN = 'USER_LOGIN'
export const USER_LOGOUT = 'USER_LOGOUT'
export const USER_CHANGE_PASS = 'USER_CHANGE_PASS'

// user account
export const UPSERT_USER_ACCOUNT = 'UPSERT_USER_ACCOUNT'
export const GET_ALL_USER_ACCOUNT = 'GET_ALL_USER_ACCOUNT'
export const REMOVE_USERS = 'REMOVE_USERS'

// user group
export const GET_ALL_USER_GROUP = 'GET_ALL_USER_GROUP'
export const UPSERT_USER_GROUP = 'UPSERT_USER_GROUP'
export const REMOVE_USER_GROUPS = 'REMOVE_USER_GROUPS'

// role
export const GET_ALL_ROLE = 'GET_ALL_ROLE'
export const UPSERT_ROLE = 'UPSERT_ROLE'
export const REMOVE_ROLES = 'REMOVE_ROLES'

// permission role
export const GET_ALL_PERMISSION_ROLE = 'GET_ALL_PERMISSION_ROLE'
export const UPSERT_PERMISSION_ROLE = 'UPSERT_PERMISSION_ROLE'
export const GET_ALL_PERMISSION = 'GET_ALL_PERMISSION'
export const REMOVE_PERMISSION_ROLES = 'REMOVE_PERMISSION_ROLES'

// duty
export const GET_ALL_DUTY = 'GET_ALL_DUTY'
export const GET_DUTY_BY_USER = 'GET_DUTY_BY_USER'
export const UPSERT_DUTY = 'UPSERT_DUTY'
export const REMOVE_DUTIES = 'REMOVE_DUTIES'
export const GET_ALL_DUTY_CATEGORY = 'GET_ALL_DUTY_CATEGORY'
export const UPSERT_DUTY_CATEGORY = 'UPSERT_DUTY_CATEGORY'
export const REMOVE_DUTY_CATEGORIES = 'REMOVE_DUTY_CATEGORIES'

// task exec
export const COMMIT_TASK_EXEC_INFO = 'COMMIT_TASK_EXEC_INFO'
export const GET_TASK_EXEC_DATA_BY_DATE = 'GET_TASK_EXEC_DATA_BY_DATE'
export const GET_USER_TASK_EXEC_DATA_BY_DATERANGE = 'GET_USER_TASK_EXEC_DATA_BY_DATERANGE'
export const GET_ONE_TASK_EXEC_DATA_BY_DATERANGE = 'GET_ONE_TASK_EXEC_DATA_BY_DATERANGE'

// user location
export const GET_ALL_USER_LOCATION = 'GET_ALL_USER_LOCATION'
export const UPSERT_USER_LOCATION = 'UPSERT_USER_LOCATION'

// inform
// duty
export const GET_ALL_INFORM = 'GET_ALL_INFORM'
export const GET_DUTY_NOTIFICATION_BY_USER = 'GET_DUTY_NOTIFICATION_BY_USER'
export const GET_UNDERLINE_DUTY_NOTIFICATION_BY_USER = 'GET_UNDERLINE_DUTY_NOTIFICATION_BY_USER'
export const GET_INFORM_BY_USER = 'GET_INFORM_BY_USER'
export const UPSERT_INFORM = 'UPSERT_INFORM'
export const REMOVE_INFORMS = 'REMOVE_INFORMS'
export const GET_NEW_DUTY_NOTIFICATION_COUNT = 'GET_NEW_DUTY_NOTIFICATION_COUNT'
export const GET_NEW_INFORM_COUNT = 'GET_NEW_INFORM_COUNT'
export const CHECK_SINGLE_NOTIFICATION = 'CHECK_SINGLE_NOTIFICATION'
export const CHECK_SINGLE_INFORM = 'CHECK_SINGLE_INFORM'
