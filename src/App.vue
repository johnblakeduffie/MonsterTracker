<template>
  <div id="app">
    <v-app id="inspire">
      <LootViewer :monster="selectedMonster" :monsterDrops="drops" v-model="showLootViewer" />
      <v-toolbar id="monsterTitle">
        <v-row>
          <v-toolbar-title class="ma-2" text>MONSTERTRACKER</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn class="ma-2" text>Home</v-btn>
          <v-btn class="ma-2" text :disabled="true">Trending Monsters</v-btn>
          <v-btn class="ma-2" id="collectMonsters" @click="getMonsters" text :disabled="true">Minigames</v-btn>
        </v-row>
      </v-toolbar>
      <v-parallax id="jadParallax" height="400" dark src="./assets/hydra.png">
        <v-row align="center" justify="center">
          <v-col class="justify-center" id="titleBlock" cols="12">
            <h1 class="display-1 font-weight-thin mb-4" id="monstertracker">MONSTERTRACKER</h1>
            <h4 class="subheading" id="subheading"> Discover the most profitable monsters in OSRS </h4>
          </v-col>
        </v-row>
      </v-parallax>

      <v-card id="infoCard" width="1400" class="mx-auto" justify="center" align="center" >
        <v-container fluid>
          <div class="search-wrapper">
            <v-toolbar>
              <v-spacer></v-spacer>
              <input type="text" placeholder="Enter Total Kills.." />
              <v-spacer></v-spacer>
              <input type="text" v-model="search" placeholder="Search Monster.." />
              <v-spacer></v-spacer>
              <v-btn class="ma-2" outlined :disabled="true">Filters</v-btn>
              <v-spacer></v-spacer>
            </v-toolbar>
          </div>

          <v-row>
            <v-col v-for="monster in monsterList" :key="monster.name" :cols="2">
              <v-card class="card" id="monsterCard" dark max-width="250">
                <v-img
                  :src="getImage(monster.name)"
                  class="white--text align-end"
                  gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                  height="160px"
                  max-width="250px"
                ></v-img>

                <v-divider></v-divider>

                <v-flex text-xs-center>
                  <h1 id="monsterName" class="monsterName" v-text="monster.name"></h1>
                </v-flex>

                <v-chip id="incomeChip" color="green" outlined pill>+{{Number(monster.grossIncomePerKill).toLocaleString()}}</v-chip>

                

                <v-card-actions>
                  <v-flex text-xs-center>
                    <v-btn outlined v-on:click="getMonsterDrops(monster.name)" @click.stop="selectedMonster = monster" width="150">View Loot</v-btn>
                  </v-flex>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>

          <scroll-loader :loader-method="getImagesInfo" :loader-disable="disable"></scroll-loader>

        </v-container>
      </v-card>
    </v-app>
  </div>
</template>


<script type="text/javascript">
class Monster {
  constructor(name, src, grossIncomePerKill, dropList) {
    this.name = name;
    this.src = src;
    this.grossIncomePerKill = grossIncomePerKill;
    this.dropList = dropList;
  }
}

import LootViewer from "./components/LootViewer";
import ScrollLoader from "vue-scroll-loader";
import axios from "axios";
import Vue from "vue";
import monsterImages from "@/assets/monsterList.json";


Vue.use(ScrollLoader);

export default {
  created() {
    
  },
  
  data: () => ({
    //scroll loader data
    loadMore: true,
    page: 1,
    pageSize: 30,
    images: [],
    masks: [],

    selectedMonster: {},
    killCount: 1,
    showLootViewer: false,
    itemPrices: {},
    search: '',
    drops: [],
    monsterList: [
      new Monster(
        "Zulrah",
        "https://oldschool.runescape.wiki/images/b/bc/Zulrah_%28serpentine%29.png?29a54",
        10000000
      ),
      new Monster(
        "Cerberus",
        "https://oldschool.runescape.wiki/images/4/45/Cerberus.png?47f4c",
        5000000
      ),
      new Monster(
        "Skotizo",
        "https://oldschool.runescape.wiki/images/a/a8/Skotizo.png?dc8b8",
        4000000
      ),
      new Monster(
        "Zalcano",
        "https://oldschool.runescape.wiki/images/3/30/Zalcano.png?6244d",
        3500000
      ),
      new Monster(
        "Vorkath",
        "https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb",
        3000000
      ),
      new Monster(
        "Alchemical Hydra",
        "https://oldschool.runescape.wiki/images/a/a3/Alchemical_Hydra.png?925dd",
        2500000
      ),
      new Monster(
        "Something",
        "https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb",
        2000000
      ),
      new Monster(
        "Zulrah",
        "https://oldschool.runescape.wiki/images/b/bc/Zulrah_%28serpentine%29.png?29a54",
        10000000
      ),
      new Monster(
        "Cerberus",
        "https://oldschool.runescape.wiki/images/4/45/Cerberus.png?47f4c",
        5000000
      ),
      new Monster(
        "Skotizo",
        "https://oldschool.runescape.wiki/images/a/a8/Skotizo.png?dc8b8",
        4000000
      ),
      new Monster(
        "Zalcano",
        "https://oldschool.runescape.wiki/images/3/30/Zalcano.png?6244d",
        3500000
      ),
      new Monster(
        "Vorkath",
        "https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb",
        3000000
      ),
      new Monster(
        "Alchemical Hydra",
        "https://oldschool.runescape.wiki/images/a/a3/Alchemical_Hydra.png?925dd",
        2500000
      ),
      new Monster(
        "Something",
        "https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb",
        2000000
      ),
      new Monster(
        "Zulrah",
        "https://oldschool.runescape.wiki/images/b/bc/Zulrah_%28serpentine%29.png?29a54",
        10000000
      ),
      new Monster(
        "Cerberus",
        "https://oldschool.runescape.wiki/images/4/45/Cerberus.png?47f4c",
        5000000
      ),
      new Monster(
        "Skotizo",
        "https://oldschool.runescape.wiki/images/a/a8/Skotizo.png?dc8b8",
        4000000
      ),
      new Monster(
        "Zalcano",
        "https://oldschool.runescape.wiki/images/3/30/Zalcano.png?6244d",
        3500000
      ),
      new Monster(
        "Vorkath",
        "https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb",
        3000000
      ),
      new Monster(
        "Alchemical Hydra",
        "https://oldschool.runescape.wiki/images/a/a3/Alchemical_Hydra.png?925dd",
        2500000
      ),
      new Monster(
        "Something",
        "https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb",
        2000000
      ),
      new Monster(
        "Zulrah",
        "https://oldschool.runescape.wiki/images/b/bc/Zulrah_%28serpentine%29.png?29a54",
        10000000
      ),
      new Monster(
        "Cerberus",
        "https://oldschool.runescape.wiki/images/4/45/Cerberus.png?47f4c",
        5000000
      ),
      new Monster(
        "Skotizo",
        "https://oldschool.runescape.wiki/images/a/a8/Skotizo.png?dc8b8",
        4000000
      ),
      new Monster(
        "Zalcano",
        "https://oldschool.runescape.wiki/images/3/30/Zalcano.png?6244d",
        3500000
      ),
      new Monster(
        "Vorkath",
        "https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb",
        3000000
      ),
      new Monster(
        "Alchemical Hydra",
        "https://oldschool.runescape.wiki/images/a/a3/Alchemical_Hydra.png?925dd",
        2500000
      ),
      new Monster(
        "Something",
        "https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb",
        2000000
      )
    ],
  }),
  components: {
    LootViewer,
  },
  computed: {
    // filteredList() {
    //   return this.monsterList.filter(monster => {
    //     return monster.name.toLowerCase().includes(this.search.toLowerCase());
    //   });
    // }
  },

  methods: {
    getImage(name) {
      return monsterImages[name];
    },
    getImagesInfo() {
      axios
        .get("http://localhost:8000/sortedProfit/", {
          params: {
            page: this.page++,
            per_page: this.pageSize,
            //client_id: 'e874834b096dcd107c232fe4b0bb521158b62e486580c988b0a75cb0b77a2abe'
          },
        })
        .then((res) => {
          //this.images.concat(res.data)
          //this.images.push("https://oldschool.runescape.wiki/images/6/6d/Vorkath%27s_head_detail.png?e82eb")
          // Stop scroll-loader
          //res.data.length < this.pageSize && (this.loadMore = false)
          res.data && (this.images = [...this.images, ...res.data]);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    watch: {
      page(value) {
        this.disable = value > 10;
      },
    },

    getMonsters: function () {
     fetch("http://localhost:8000/sortedProfit/")
      .then((response) => response.json())
      .then((data) => {
        this.monsterList = data;
      });
    },
    getMonsterDrops: function (name) {
      // var monster = {};
      // monster = monsterQuery.getMonster(name);
      // console.log(monster);
      // return monster.dropList;
      fetch("http://localhost:8000/monster/" + name + "/")
        .then((response) => response.json())
        .then((data) => {
          console.log(data.dropList);
          this.drops = data.dropList;
          this.showLootViewer = true;
          //return data.dropList;
        });
    },
    checkMonsters: function () {
      console.log(JSON.parse(JSON.stringify(this.monsterList)));
    },
  },
  mounted() {
    this.getMonsters();
    this.getImagesInfo();
  },
};
</script>

<style lang="scss">
//Scroll Loader
// .card {
//   animation-duration: 1s;
//   animation-fill-mode: both;
//   animation-name: fadeInUp;
// }



body {
  background-color: black;
  font-family: "Roboto", sans-serif;
  text-align: center;
  font-weight: 300;
  font-size: 20px;
}

#infoCard {
  background-color: black;
  margin-top: 0.55rem;
}

#incomeChip {
  margin-bottom: 0.55rem;
}

.v-parallax {
  margin-bottom: 0.55rem;
}

.monsterName {
  margin-top: 0.55rem;
}

.v-chip {
  margin-top: 0.55rem;
  margin-right: 0.2rem;
  
}

input {
      padding: 4px 12px;
      color: rgba(255, 250, 250, 0.884);
      border: 1px solid rgba(255, 252, 252, 0.966);
      transition: .15s all ease-in-out;
      &:focus {
        transform: scale(1.05);
      }
      
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10%) scale(0.9);
  }

  to {
    opacity: 1;
    transform: translateY(0%) scale(1);
  }
}

#monsterCard {
  margin-top: 0.3rem;
  font-size: 10px;
  animation-duration: 1s;
  //animation-fill-mode: both;
  animation-name: fadeInUp;
  transition: .15s all ease-in-out;
  &:hover {
      transform: scale(1.1);
      box-shadow: rgba(0, 0, 0, 0.117647) 0px 1px 6px, rgba(0, 0, 0, 0.117647) 0px 1px 4px;
    }  
}

.search-wrapper {
  margin-bottom: 0.55rem;
}

.searchBar {
  border-radius: 25px;
}

#monsterTitle {
  margin-top: 1.5rem;
  //margin-bottom: 0.55rem;
  font-size: 20px;
}
</style>