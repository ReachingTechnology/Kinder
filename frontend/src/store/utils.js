/**
 * Created by HOZ on 07/09/2017.
 */
import { PERMISSIONS, PERMISSION_CATEGORIES } from './common_defs'
import state from './state'

function _Util () {
}
_Util.prototype.getUserName = function (userId) {
  for (var i = 0, len = state.allUser.length; i < len; i++) {
    if (state.allUser[i]._id === userId) {
      return state.allUser[i].name
    }
  }
  return ''
}
_Util.prototype.getRoleName = function (roleId) {
  for (var i = 0, len = state.allRole.length; i < len; i++) {
    if (state.allRole[i]._id === roleId) {
      return state.allRole[i].name
    }
  }
  return ''
}
_Util.prototype.getRoleId = function (roleName, allRole) {
  for (var i = 0, len = allRole.length; i < len; i++) {
    if (allRole[i].name === roleName) {
      return allRole[i]._id
    }
  }
  return ''
}
_Util.prototype.getPermissionIdByName = function (name, allPermission) {
  var keys = Object.keys(allPermission)
  for (var i = 0; i < keys.length; i++) {
    var perms = allPermission[keys[i]].permissions
    for (var j = 0; j < perms.length; j++) {
      if (perms[j].name === name) {
        return perms[j].id
      }
    }
  }
  return ''
}
_Util.prototype.getPermissionRoleByName = function (name) {
  for (var i = 0; i < state.allPermissionRole.length; i++) {
    if (name === state.allPermissionRole[i].name) {
      return state.allPermissionRole[i]
    }
  }
  return null
}
_Util.prototype.getPermissionRoleById = function (id) {
  for (var i = 0; i < state.allPermissionRole.length; i++) {
    if (id === state.allPermissionRole[i]._id) {
      return state.allPermissionRole[i]
    }
  }
  return null
}
_Util.prototype.hasPermission = function (permission) {
  var permissionid = PERMISSIONS[permission]
  var roleid = state.user.role
  for (var i = 0; i < state.allRole.length; i++) {
    var role = state.allRole[i]
    if (role._id === roleid) {
      var permissionRoles = role.permissionRoles
      for (var j = 0; j < permissionRoles.length; j++) {
        var permissionRole = this.getPermissionRoleById(permissionRoles[j])
        if (permissionRole) {
          for (var k = 0; k < permissionRole.permissions.length; k++) {
            if (permissionRole.permissions[k] === permissionid) {
              // console.log('return true:' + permission)
              return true
            }
          }
        }
      }
    }
  }
  // console.log('return false:' + permission)
  return false
}
_Util.prototype.hasCategoryPermission = function (categoryname) {
  var categoryid = PERMISSION_CATEGORIES[categoryname]
  var roleid = state.user.role
  var permissionList = state.allPermission[categoryid] === undefined ? [] : state.allPermission[categoryid].permissions
  for (var i = 0; i < state.allRole.length; i++) {
    var role = state.allRole[i]
    if (role._id === roleid) {
      var permissionRoles = role.permissionRoles
      for (var j = 0; j < permissionRoles.length; j++) {
        var permissionRole = this.getPermissionRoleById(permissionRoles[j])
        if (permissionRole) {
          for (var k = 0; k < permissionRole.permissions.length; k++) {
            for (var m = 0; m < permissionList.length; m++) {
              if (permissionRole.permissions[k] === permissionList[m].id) {
                // console.log('return true:' + categoryname)
                return true
              }
            }
          }
        }
      }
    }
  }
  // console.log('return false:' + categoryname)
  return false
}
var Util = new _Util()
export default Util