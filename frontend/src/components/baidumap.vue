<template>
  <div>
    <br/>
    <div align="left">
    <el-button @click="getLocation">获取当前定位</el-button>
    </div>
    <br/>
    <!--<baidu-map class="map" :center="{lng: 116.3086, lat: 39.935846}" :zoom="18">-->
    <baidu-map class="map" :center="{lng: longitude, lat: latitude}" :zoom="18">
      <!--<bm-geolocation anchor="BMAP_ANCHOR_BOTTOM_RIGHT" :showAddressBar="true" :autoLocation="true" @locationSuccess="onLocationReady"></bm-geolocation>-->
      <bm-marker :position="{lng: longitude, lat: latitude}" :dragging="true" animation="BMAP_ANIMATION_BOUNCE">
        <bm-label :content="getLocationClicked ? '我在这里':'幼儿园位置'" :labelStyle="{color: 'green', fontSize : '24px'}" :offset="{width: -35, height: 30}"/>
      </bm-marker>
    </baidu-map>
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
      }
    },
    created: function () {
//      this.getLocation()
    },
    data () {
      return {
        longitude: 116.3086,
        latitude: 39.935846,
        getLocationClicked: false
      }
    }
  }
</script>
<style>
  /* The container of BaiduMap must be set width & height. */
  .map {
    width: 100%;
    height: 400px;
  }
</style>
