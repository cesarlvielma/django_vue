<template>
  <v-app>
    <v-main>
      <UserComponent/>
    </v-main>
  </v-app>
</template>

<script>
import UserComponent from './components/UserComponent.vue'

export default {
  name: 'App',

  components: {
    UserComponent,
  },

  data: () => ({
    //
  }),
}
</script>
