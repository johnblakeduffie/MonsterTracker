<template>
  <div id="app">
    <v-app  id="inspire">
      <LootViewer :monster="selectedMonster" :monsterDrops="drops" v-model="showLootViewer" />
      <v-toolbar color="#1f263c" id="monsterTitle">
        <v-row>
          <v-toolbar-title class="ma-2" text>MONSTERTRACKER</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn class="ma-2" text>Home</v-btn>
          <v-btn class="ma-2" id="collectMonsters" @click="getMonsters" text :disabled="true">Trending Monsters</v-btn>
          <v-btn class="ma-2"  text :disabled="true">Minigames</v-btn>
        </v-row>
      </v-toolbar>

      <v-row>
        <nav>
          <v-navigation-drawer color="#1f263c" v-model="drawer" id="navDrawer" class="mx-auto" :width="200" dark permanent>
            <v-list nav>
              <v-list-item :disabled="true" router to="/">
                  <v-icon class="listIcons" color="blue" left>mdi-view-dashboard</v-icon>
                  <span>Dashboard</span>
              </v-list-item>
              <v-divider color="#15182a"></v-divider>

              <v-list-item :disabled="true" router to="/">
                  <v-icon class="listIcons" color="blue" left>mdi-view-list</v-icon>
                  <span>Loot Viewer</span>
              </v-list-item>
              <v-divider color="#15182a"></v-divider>

              <v-list-item :disabled="true" router to="/">
                  <v-icon class="listIcons" color="blue" left>mdi-chart-line</v-icon>
                  <span>History</span>
              </v-list-item>
              <v-divider color="#15182a"></v-divider>

              <v-list-item :disabled="true" router to="/">
                  <v-icon class="listIcons" color="blue" left>mdi-information</v-icon>
                  <span>Monster Stats</span>
              </v-list-item>
            </v-list>
          </v-navigation-drawer>
        </nav>

        <v-col >
            <v-container fluid>
              <div  class="search-wrapper">
                <v-toolbar color="#1f263c">
                  <input type="text" class="searchBar" v-model="search" placeholder="Search Monsters"/>
                  <v-spacer></v-spacer>
                  <v-btn class="ma-2" color="blue" outlined>Filters</v-btn>
                  <v-btn class="ma-2" color="blue" :disabled="visibleMonsters<=monstersPerPage" @click.stop="decrementMonsters">Previous</v-btn>
                  <v-btn class="ma-2" color="blue" @click.stop="incrementMonsters">Next</v-btn>
                </v-toolbar>
              </div>

              <v-row>
                  <v-col v-for="monster in filteredList" :key="monster.name" :cols="2">
                    <v-card color="#1f263c" class="card" id="monsterCard" dark max-width="250" height="360">
                      <v-img
                        :src="getImage(monster.name)"
                        class="white--text align-end"
                        gradient="to bottom, rgba(0,0,0,.3), rgba(0,0,0,.5)"
                        background="white"
                        height="215px"
                        max-width="250px"
                      ></v-img>

                      <v-divider></v-divider>

                      <v-flex text-xs-center>
                        <h1 id="monsterName" class="monsterName" v-text="monster.name"></h1>
                      </v-flex>

                      <v-chip id="incomeChip" color="green accent-4" outlined pill>+{{Number(monster.grossIncomePerKill).toLocaleString()}}</v-chip>

                      <v-card-actions>
                        <v-flex text-xs-center>
                          <v-btn color="light-blue darken-2" v-on:click="getMonsterDrops(monster.name)" @click.stop="selectedMonster = monster" width="150">View Loot</v-btn>
                        </v-flex>
                      </v-card-actions>
                    </v-card>
                  </v-col>
              </v-row>
            </v-container>
          </v-col>
      </v-row>

    </v-app>
  </div>
</template>


<script type="text/javascript">
// class Monster {
//   constructor(name, src, grossIncomePerKill, dropList) {
//     this.name = name;
//     this.src = src;
//     this.grossIncomePerKill = grossIncomePerKill;
//     this.dropList = dropList;
//   }
// }

import LootViewer from "./components/LootViewer";
import monsterImages from "@/assets/monsterList.json";


export default {
  created() {
    
  },
  
  data() {
    return {
      selectedMonster: {},
      killCount: 1,
      showLootViewer: false,
      itemPrices: {},
      search: '',
      visibleMonsters: 12,
      monstersPerPage: 12,
      drops: [],
      monsterList: []
    }
  },
  components: {
    LootViewer,
  },
  computed: {
    filteredList: function(){
      var visibleMonsters = this.visibleMonsters;
      var monstersPerPage = this.monstersPerPage;
      var search = this.search;
      return this.monsterList.filter(function(monster, index) {
        if (search != '') {
          return monster.name.toLowerCase().includes(search.toLowerCase());
        } else {
          return index <= visibleMonsters - 1 && index >= visibleMonsters - monstersPerPage; 
        }
      });
    }
  },

  methods: {
    decrementMonsters() {
      this.visibleMonsters -= this.monstersPerPage;
    },
    incrementMonsters() {
      this.visibleMonsters += this.monstersPerPage;
    },
    getImage(name) {
      return monsterImages[name];
    },
    getMonsters: function () {
     fetch("http://localhost:8000/sortedProfit/")
      .then((response) => response.json())
      .then((data) => {
        this.monsterList = data;
      });
    },
    getMonsterDrops: function (name) {
      fetch("http://localhost:8000/monster/" + name + "/")
        .then((response) => response.json())
        .then((data) => {
          console.log(data.dropList);
          this.drops = data.dropList;
          this.showLootViewer = true;
        });
    },
    checkMonsters: function () {
      console.log(JSON.parse(JSON.stringify(this.monsterList)));
    },
  },
  mounted() {
    this.getMonsters();
  },
};
</script>

<style lang="scss">

.listIcons {
  margin-left: .55rem;
}

.searchBar {
  width: 400px;
  background-color: #101220;
}

.totalKillsBar {
  width: 200px;
  background-color: #15182a;
}

#inspire {
  background-color: #151620;
}


body {
  background-color:#151620;
  font-family: "Roboto", sans-serif;
  text-align: center;
  font-weight: 300;
  font-size: 20px;
}

#infoCard {
  margin-top: 1.55rem;
}

#incomeChip {
  margin-bottom: 0.55rem;
}

.v-parallax {
  margin-bottom: 0.55rem;
}

#navDrawer {
  margin-top: .8rem;
}

.monsterName {
  margin-top: .55rem;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.v-chip {
  color:#15182a;
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
  margin-top: 1.0rem;
  font-size: 20px;
}
</style>