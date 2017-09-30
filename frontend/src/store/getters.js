/**
 * Created by HOZ on 28/08/2017.
 */
const getters = {
  sessionToken: state => { return state.sessionToken },
  user: state => { return state.user },
  backend_uri: state => { return state.backend_uri },
  allUser: state => { return state.allUser },
  allRole: state => { return state.allRole },
  allPermissionRole: state => { return state.allPermissionRole },
  allPermission: state => { return state.allPermission },
  allTask: state => { return state.allTask },
  allDuty: state => { return state.allDuty },
  dutyForRoles: state => { return state.dutyForRoles },
  all_statistic_data: state => { return state.all_statistic_data },
  userDayTask: state => { return state.userDayTask },
  userDaterangeTask: state => { return state.userDaterangeTask },
  taskExecDaterangeData: state => { return state.taskExecDaterangeData },
  datePickerOptionsDay: state => { return state.datePickerOptionsDay },
  datePickerOptionsMonth: state => { return state.datePickerOptionsMonth }
}
export default getters
