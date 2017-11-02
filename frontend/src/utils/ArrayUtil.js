/**
 * Created by HOZ on 19/10/2017.
 */
function _ArrayUtil () {
}

_ArrayUtil.prototype.in_array = function (obj, array) {
  if (obj === undefined || array === undefined) {
    return false
  }
  for (var i = 0, len = array.length; i < len; i++) {
    if (obj === array[i]) {
      return true
    }
  }
  return false
}
_ArrayUtil.prototype.diff = function (arr1, arr2) {
  return arr1.filter(function (i) { return arr2.indexOf(i) < 0 })
}
_ArrayUtil.prototype.remove = function (obj, arr) {
  var index = arr.indexOf(obj)
  if (index > -1) {
    arr.splice(index, 1)
  }
}
var ArrayUtil = new _ArrayUtil()
export default ArrayUtil
