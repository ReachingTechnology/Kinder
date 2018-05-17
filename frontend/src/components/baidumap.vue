<template>
  <div>
    <!--<baidu-map class="map" :center="{lng: 116.3086, lat: 39.935846}" :zoom="18">-->
    <!--<baidu-map class="map" :center="{lng: longitude, lat: latitude}" :zoom="18">-->
      <!--&lt;!&ndash;<bm-geolocation anchor="BMAP_ANCHOR_BOTTOM_RIGHT" :showAddressBar="true" :autoLocation="true" @locationSuccess="onLocationReady"></bm-geolocation>&ndash;&gt;-->
      <!--<bm-marker :position="{lng: longitude, lat: latitude}" :dragging="true" animation="BMAP_ANIMATION_BOUNCE">-->
        <!--<bm-label :content="getLocationClicked ? '我在这里':'幼儿园位置'" :labelStyle="{color: 'green', fontSize : '24px'}" :offset="{width: -35, height: 30}"/>-->
      <!--</bm-marker>-->
    <!--</baidu-map>-->
    <div id="allmap">
    </div>
  </div>
</template>
<script>
//  import {BMap} from 'http://developer.baidu.com/map/jsdemo/demo/convertor.js'
  export default {
    methods: {
      onLocationReady (result) {
        console.log('baidu********************')
        console.log(result.point)
        alert('检测到员工位置信息：经度 ' + result.point.lng + '，纬度 ' + result.point.lat)
      },
      getLocation () {
        this.getLocationClicked = true
        navigator.geolocation.getCurrentPosition(this.translateLoc)
      },
      translateLoc (position) {
        console.log('baidu********************  translateLoc')
        var currentLat = position.coords.latitude
        var currentLon = position.coords.longitude
        var gpsPoint = new BMap.Point(currentLon, currentLat)
        BMap.Convertor.translate(gpsPoint, 0, this.setBaiduPoint)
      },
      setBaiduPoint (point) {
        console.log('this is baidu point')
        console.log(point)
        this.longitude = point.lng
        this.latitude = point.lat
      },
      showMap () {
        this.map = undefined
        this.map = new BMap.Map('allmap')
        var point = new BMap.Point(this.lng, this.lat)
        console.log('$$$$$', this.lng, this.lat)
        this.map.setCurrentCity('北京')
        this.map.centerAndZoom(point, 14)
        var mk = new BMap.Marker(point)
        this.map.addOverlay(mk)
        this.map.panTo(point)
        this.map.enableScrollWheelZoom(true)
      }
    },
    mounted: function () {
//      // 添加带有定位的导航控件
//      var navigationControl = new BMap.NavigationControl({
//        // 靠左上角位置
//        anchor: BMAP_ANCHOR_TOP_LEFT,
//        // LARGE类型
//        type: BMAP_NAVIGATION_CONTROL_LARGE,
//        // 启用显示定位
//        enableGeolocation: true
//      });
//      map.addControl(navigationControl);
//      // 添加定位控件
//      var geolocationControl = new BMap.GeolocationControl();
//      geolocationControl.addEventListener("locationSuccess", function(e){
//        // 定位成功事件
//        var address = '';
//        address += e.addressComponent.province;
//        address += e.addressComponent.city;
//        address += e.addressComponent.district;
//        address += e.addressComponent.street;
//        address += e.addressComponent.streetNumber;
//        alert("当前定位地址为：" + address);
//      });
//      geolocationControl.addEventListener("locationError",function(e){
//        // 定位失败事件
//        alert(e.message);
//      });
//      map.addControl(geolocationControl);
    },
    beforeRouteEnter: function (to, from, next) {
      next(vm => { vm.showMap() })
    },
    beforeRouteLeave: function (to, from, next) {
      this.$destroy()
      next()
    },
    data () {
      return {
        lng: this.$route.params.lng,
        lat: this.$route.params.lat,
        getLocationClicked: false,
        map: undefined
      }
    }
  }
</script>
<style>
  /* The container of BaiduMap must be set width & height. */
  #allmap {
    width: 100%;
    height: 400px;
  }
</style>
