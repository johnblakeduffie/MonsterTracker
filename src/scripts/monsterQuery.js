import $ from "jquery";


class Monster {
    constructor(name, src, grossIncomePerKill, dropList) {
        this.name = name;
        this.src = src;
        this.grossIncomePerKill = grossIncomePerKill;
        this.dropList = dropList
    }
}

var sortedProfit = []

$(document).ready(function () {
    $.getJSON('http://localhost:8000/sortedProfit/').then(function (json) {

        sortedProfit = json;
    });
});

export default {
    getSortedProfit() {
        return sortedProfit;
    },
    getMonster(name) {
        var monsterP = new Monster();
        //var monsterP = null;
        $.getJSON('http://localhost:8000/monster/' + name + '/').then( function (json) {
            monsterP.name = json["name"];
            monsterP.src = "https://oldschool.runescape.wiki/images/b/bc/Zulrah_%28serpentine%29.png?29a54";
            monsterP.grossIncomePerKill = json["grossIncomePerKill"];
            monsterP.dropList = json["dropList"];
            monsterP.dropList = json.dropList
        });
        return monsterP;
    }
}