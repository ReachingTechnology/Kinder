<template>
  <div align="center">
    <div style="width: 50%" >
      <el-form :model="user_login_data">
        <el-form-item label="员工编号">
          <el-input v-model="user_login_data.userid" auto-complete="on" placeholder="输入员工编号或手机号"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="user_login_data.pass" auto-complete="off"></el-input>
        </el-form-item>
        <el-button @click="cancellogin">取消</el-button>
        <el-button type="primary" @click="commitlogin">登录</el-button>
      </el-form>
    </div>
  </div>
</template>

<script>
  import { mapActions } from 'vuex'
  import { USER_LOGIN } from '../store/mutation_types'
  export default {
    name: 'app',
    components: {
    },
    computed: {
    },
    data: () => {
      return {
        user_login_data: {'userid': '', 'pass': ''}
      }
    },
    methods: {
      ...mapActions([USER_LOGIN]),
      commitlogin: function () {
        this.USER_LOGIN(this.user_login_data)
        this.user_login_data = {'userid': '', 'pass': ''}
      },
      cancellogin: function () {
        this.user_login_data = {'userid': '', 'pass': ''}
      }
    }
  }
</script>
<style scoped>

</style>
