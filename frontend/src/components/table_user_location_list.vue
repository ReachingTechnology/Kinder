<template>
  <div>
    <h2>员工位置</h2>
    <br/>
    <el-table
      :data="userLocations"
      style="width: 100%"
      :default-sort = "{prop: '_id', order: 'ascending'}"
      @selection-change="handleSelectionChange"
      :row-class-name="tableRowClassName">
      <el-table-column
        prop="user_name"
        label="员工名"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="location_display"
        label="位置"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        prop="update_time_display"
        label="位置更新时间"
        align="center"
        sortable>
      </el-table-column>
      <el-table-column
        label="操作"
        align="center">
        <template scope="scope">
          <div>
            <el-button
              size="small"
              :disabled="scope.row.locationLat === 0 && scope.row.locationLng === 0"
              @click="handleShowInMap(scope.$index, scope.row)" type="success">地图中查看</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<style>
  .el-table .info-row {
    background: #c9e5f5;
  }

  .el-table .positive-row {
    background: #e2f0e4;
  }
</style>
<script>
  import { mapActions, mapGetters } from 'vuex'
  import { GET_ALL_USER_LOCATION } from '../store/mutation_types'
  import RoleEditPanel from './edit_panel_role.vue'
  import Util from '../store/utils'
  import Moment from 'moment'

  export default {
    name: 'table_user_location_list',
    methods: {
      tableRowClassName (row, index) {
        return ''
      },
      handleSelectionChange (val) {
        this.multipleSelection = val
      },
      handleShowInMap (index, row) {
        this.$router.push({name: 'ShowLocation', params: {lat: row.locationLat, lng: row.locationLng}})
      },
      ...mapActions([GET_ALL_USER_LOCATION])
    },
    computed: {
      ...mapGetters(['allUser', 'allUserLocation']),
      userLocations () {
        var data = []
        for (var i = 0, len = this.allUser.length; i < len; i++) {
          var user = this.allUser[i]
          var location = {user_id: user._id, user_name: user.name, location_display: '未知', update_time: 0, locationLat: 0, locationLng: 0}
          for (var j = 0, len2 = this.allUserLocation.length; j < len2; j++) {
            if (this.allUserLocation[j].user_id === location.user_id) {
              location.location_display = Util.getLocationDisplay(this.allUserLocation[j].locationLat, this.allUserLocation[j].locationLng)
              location.locationLat = this.allUserLocation[j].locationLat
              location.locationLng = this.allUserLocation[j].locationLng
              location.update_time = this.allUserLocation[j].update_time
              if(location.update_time > 0) {
                location.update_time_display = Moment(location.update_time * 1000).format('MM-DD H:mm')
              } else {
                location.update_time_display = ''
              }
            }
          }
          data.push(location)
        }
        return data
      }
    },
    created: function () {
      this.GET_ALL_USER_LOCATION()
    },
    beforeRouteUpdate: function (to, from, next) {
      this.GET_ALL_USER_LOCATION()
      next()
    },
    beforeRouteEnter: function (to, from, next) {
      next(vm => { vm.GET_ALL_USER_LOCATION() })
    },
    data: () => {
      return {
        showEdit: false,
        selectedRole: {},
        multipleSelection: [],
        isCreating: false
      }
    },
    components: {
      RoleEditPanel
    }
  }
</script>
