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

var ArrayUtil = new _ArrayUtil()
export default ArrayUtil
