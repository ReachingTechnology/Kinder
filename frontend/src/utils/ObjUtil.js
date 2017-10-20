/**
 * Created by HOZ on 19/10/2017.
 */
function _ObjUtil () {
}

_ObjUtil.prototype.clone = function (obj) {
  var newobj = {}
  for (var key in obj) {
    newobj[key] = obj[key]
  }
  return newobj
}

var ObjUtil = new _ObjUtil()
export default ObjUtil
