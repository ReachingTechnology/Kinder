/**
 * Created by HOZ on 28/08/2017.
 */
const getters = {
  active_menu: state => { return state.active_menu },
  sessionToken: state => { return state.sessionToken },
  user: state => { return state.user },
  backend_uri: state => { return state.backend_uri },
  upload_image_uri: state => { return state.upload_image_uri },
  upload_document_base_uri: state => { return state.upload_document_base_uri },
  allUser: state => { return state.allUser },
  allUserGroup: state => { return state.allUserGroup },
  allUserLocation: state => { return state.allUserLocation },
  allRole: state => { return state.allRole },
  allPermissionRole: state => { return state.allPermissionRole },
  allPermission: state => { return state.allPermission },
  allTask: state => { return state.allTask },
  allDuty: state => { return state.allDuty },
  allDutyCategory: state => { return state.allDutyCategory },
  dutyForRoles: state => { return state.dutyForRoles },
  allDocument: state => { return state.allDocument },
  allInform: state => { return state.allInform },
  userInform: state => { return state.userInform },
  userDutyNotification: state => { return state.userDutyNotification },
  underlineDutyNotification: state => { return state.underlineDutyNotification },
  newInformCount: state => { return state.newInformCount },
  newDutyNotificationCount: state => { return state.newDutyNotificationCount },
  all_statistic_data: state => { return state.all_statistic_data },
  userDayTask: state => { return state.userDayTask },
  userDaterangeTask: state => { return state.userDaterangeTask },
  taskExecDaterangeData: state => { return state.taskExecDaterangeData },
  datePickerOptionsDay: state => { return state.datePickerOptionsDay },
  datePickerOptionsMonth: state => { return state.datePickerOptionsMonth },
  changePassFail: state => { return state.changePassFail }
}
export default getters
