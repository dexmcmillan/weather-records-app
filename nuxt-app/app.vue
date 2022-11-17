<template>
  <div id="app">
    <v-form class="w-full md:w-1/4">
      <v-container>
        <v-text-field
          v-model="city_search"
          label="Find your city"
        ></v-text-field>
      </v-container>
    </v-form>
    <NuxtPage :city_search="city_search" />
  </div>
</template>

<script>
  export default {
    data() {
      return {
        city_search: ""
      }
    }}
</script>