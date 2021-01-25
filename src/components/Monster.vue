<template>
      <v-card flat class="ma-3 text-xs-center">
      <v-img src="https://cdn.vuetifyjs.com/images/cards/desert.jpg" aspect- 
    ratio="2.75"></v-img>
        <v-card-title primary-title>
          <div>
            <h3 class="headline pink--text text--accent-2"> 
    {{productItem.name}}</h3>
            <div>{{productItem.description}}</div>
          </div>
        </v-card-title>
        <v-card-actions>
          <v-btn flat color="orange">Add to Cart</v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <script>
    export default {
      props: ["productItem"],
      data() {
        return {};
      }
    };
    </script>

<style>
</style>