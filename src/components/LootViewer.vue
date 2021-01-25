<template>
  <v-layout row justify-center>
    <v-dialog dark v-model="show" persistent max-width="1500px">
      <v-data-table dark :headers="headers" :items="monsterDrops" sort-by="grossIncomePerKill" class="elevation-1">
        <template v-slot:top>
          <v-toolbar flat dark>
            <v-toolbar-title>{{monster.name}}</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-toolbar-title>Total Profit: {{(Math.trunc(calculatedProfit * killsPerHour)).toLocaleString()}} GP</v-toolbar-title>
            <v-divider class="mx-4" inset vertical></v-divider>
            <v-toolbar-title>Loot Per Kill: {{(Math.trunc(calculatedProfit)).toLocaleString()}} GP</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ on }">
                <v-btn color="primary" dark class="mb-2" @click="initialize">Reset</v-btn>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-btn color="primary" dark class="mb-2" v-on="on">Add Supply Cost</v-btn>
              </template>
              <v-card dark>
                <v-card-title>
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field v-model="editedItem.name" label="Item name"></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field v-model="editedItem.grossIncomePerKill" label="Quantity (Uses/Kill)"></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field v-model="editedItem.sellAvg" label="Sell Average"></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field v-model="editedItem.rarity" label="Rarity"></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field v-model="editedItem.quantityAvg" label="Quantity"></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
          <v-icon small @click="excludeItem(item)">mdi-delete</v-icon>
        </template>
        <template v-slot:no-data>
          <v-btn color="primary" @click="initialize">Reset</v-btn>
        </template>
      </v-data-table>
      <v-btn color="primary" dark class="mb-2" @click="close">Close</v-btn>
    </v-dialog>
  </v-layout>
</template>

<script>

/*class Monster {
  constructor(name, src, grossIncomePerKill, dropList) {
    this.name = name;
    this.src = src;
    this.grossIncomePerKill = grossIncomePerKill;
    this.dropList = dropList;
  }
}*/

//import $ from "jquery";
//import monsterQuery from "../scripts/monsterQuery";
export default {
  created() {},
  props: {
    value: Boolean,
    monster: Object,
    monsterDrops: Array,
    //dropList: Array,
    killsPerHour: Number
  },
  computed: {
    calculatedProfit() {
      var total = 0;
      this.monsterDrops.map(item => (total += item.grossIncomePerKill));
      return total;
    },
    /*dropList: function () {
      var Drops = {};
      this.drops = DropList;
      var monsterP = new Monster(monsterQuery.getMonster(this.monster.name));
      var monster = {};
      monster = monsterQuery.getMonster(this.monster.name);
      monsterP = monsterQuery.getMonster(this.monster.name);
      $.each(monsterP, function(key, value) {
        console.log(key);
        console.log(value);

      });

      console.log(monster);
      fetch('http://localhost:8000/monster/' + name + '/')
        .then(response => response.json())
        .then((data) => {
          //Drops = data;
          console.log(data);
          return data.dropList
      })
      console.log(monsterQuery.getMonster(this.monster.name));
      return monsterQuery.getMonster(this.monster.name);
    },*/
    show: {
      get() {
        return this.value;
      },
      set(value) {
        this.$emit("input", value);
      }
    },
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    }
  },
  data: () => ({
    monsterName: "",
    profitTotal: 0,
    dialog: false,
    headers: [
      { text: "Item", align: "start", sortable: false, value: "name" },
      { text: "Profit (gp)", value: "grossIncomePerKill" },
      { text: "Sell Average (gp)", value: "sellAvg" },
      { text: "Drop Rate (Chance/Kill)", value: "rarity" },
      { text: "Quantity (Amount/Kill)", value: "quantityAvg" },
      { text: 'Actions', value: 'action', sortable: false },
    ],
    drops: [],
    mounted() {
      fetch('http://localhost:8000/monster/' + name + '/')
        .then(response => response.json())
        .then((data) => {
        this.drops = data.dropList;
        console.log(data);
      })
    },
    removedDrops: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      grossIncomePerKill: 0,
      sellAvg: 0,
      rarity: 0,
      quantityAvg: 0
    },
    defaultItem: {
      name: "",
      grossIncomePerKill: 0,
      sellAvg: 0,
      rarity: 0,
      quantityAvg: 0
    }
  }),

  methods: {
    /*populateDropList() {
      this.dropList = monsterQuery.getMonster(this.monster.name).dropList
    },*/
    initialize() {
      //var DropList = [];
      //var mDrops = [];
      //var monsterName = this.monster.name;
      /*mDrops = monsterQuery.getMonster(this.monster.name).dropList;
      $.each(mDrops, function(monster, index) {
        if (monster === monsterName) {
          $.each(index, function(key, value) {
            
              if (typeof value.sellAvg === 'undefined') {
                console.log("Error for Drop: " + key);
              } else {
                DropList.push(value);
              }

          });
        }
      });
      this.drops = DropList;*/
      //this.drops = monsterQuery.getMonster(this.monster.name).dropList;
      //console.log("Drops for " + this.monster.name + ":");
      //console.log(this.drops);
    },

    editItem(item) {
      this.editedIndex = this.drops.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    excludeItem(item) {
      //take item out of drops
      const index = this.drops.indexOf(item);
      this.drops.splice(index, 1);


      //store drop and its index in temp array in case item should be included again
      //this.removedDrops.push(index, item);
      //console.log(removedDrops);
    },

    /*resetItem(item) {

    },*/

    /*close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },*/

    close() {
        this.show = false
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.drops[this.editedIndex], this.editedItem);
      } else {
        this.drops.push(this.editedItem);
      }
      this.close();
    }
  }
};
</script>

<style lang="scss">
body {
  background-color: black;
  font-family: "Roboto", sans-serif;
  text-align: center;
  font-weight: 300;
  font-size: 20px;
}
</style>