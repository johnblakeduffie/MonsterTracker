import $ from "jquery";

class Monster {
    constructor(title, src, profit) {
        this.title = title;
        this.src = src;
        this.profit = profit;
    }
}

var itemPrices = {};
var monsterDrops = {};
//var monsterProfit = {};
//var monsterDropProfit = {};
var sortedMonsterProfit = [];
var killsPerHour = 1000;

$(document).ready(function () {

    //var keepGoing = 1;

    $.getJSON('https://rsbuddy.com/exchange/summary.json', function (json) {
        itemPrices = json;
        getDrops();
    });

    function lookupPrice(drop) {
        var sell;
        $.each(itemPrices, function (i, item) {
            var item_name = item["name"];
            if (item_name === drop) {
                var item_sell = item["sell_average"];
                /*if (item_sell == 0) {
                    console.log(item_name + ": Need to lookup price on different API\n");
                }*/
                sell = item_sell;
            }
        });
        return sell;
    }

    function getDrops() {
        $.getJSON('https://www.osrsbox.com/osrsbox-db/monsters-complete.json', function (data) {
            console.log("Successfully accessed monster database\n");
            $.each(data, function (i, item) {
                var dropList = {};
                var monster = item["name"];
                $.each(item["drops"], function (key, value) {
                    var drop = {};
                    var id = value["id"]; // Can use for getting pictures later
                    var dropItem = value["name"];
                    var rarity = value["rarity"];
                    var quantity = value["quantity"];
                    var sell;
                    if (drop == 'Coins') {
                        sell = 1;
                    } else {
                        sell = lookupPrice(dropItem);
                    }
                    drop = {
                        id: id,
                        item: dropItem,
                        rarity: rarity,
                        quantity: quantity,
                        sell_average: sell
                    };
                    dropList[dropItem] = drop;
                });
                monsterDrops[monster] = dropList;
            });
            calculateProfit();
        });
        //checkMonsterDrops();
    }

    function calculateProfit() {
        $.each(monsterDrops, function (monster, item) {
            var totalProfit = 0.0;
            var profitList = {};
            $.each(item, function (key, value) {
                var quantityAvg = 0.0;
                //console.log("Monster: " + monster + " Drop: " + value['item']);
                try {
                    var sellAverage = parseFloat(value.sell_average);
                    var quantity = value.quantity;
                    var rarity = value.rarity;
                    var item = value.item;
                    var profit;

                    if (quantity.includes("-")) {
                        var quantityRange = quantity.split('-');
                        quantityAvg = (parseInt(quantityRange[0]) + parseInt(quantityRange[1])) / 2;
                    } else {
                        quantityAvg = parseFloat(quantity);
                    }

                    profit = rarity * sellAverage * quantityAvg;

                    if (profit >= 0) {
                        totalProfit += rarity * sellAverage * quantityAvg;
                        profitList[item] = rarity * sellAverage * quantityAvg;
                        monsterDrops[monster][item].profit = rarity * sellAverage * quantityAvg;
                    } else {
                        totalProfit += 0;
                    }
                } catch (e) {
                    totalProfit += 0;
                }

            });
            monsterDropProfit[monster] = profitList;
            monsterProfit[monster] = totalProfit * killsPerHour;
            sortedMonsterProfit.push([monster, totalProfit * killsPerHour]);
            var monsterP = new Monster(
                monster,
                "https://oldschool.runescape.wiki/images/b/bc/Zulrah_%28serpentine%29.png?29a54",
                parseInt(totalProfit * killsPerHour),
            );
            sortedMonsterProfit.push(monsterP);
        });
        checkMonsterDropProfit();
        checkMonsterDrops();
        sortMonsterProfit();
        checkSortedMonsterProfit();
    }

    /*function checkMonsterDropProfit() {
        console.log(JSON.parse(JSON.stringify(monsterDropProfit)));
    }*/

    /*function checkMonsterProfit() {
        console.log(JSON.parse(JSON.stringify(monsterProfit)));
    }*/

    function checkSortedMonsterProfit() {
        console.log(JSON.parse(JSON.stringify(sortedMonsterProfit)));
    }

    function checkMonsterDrops() {
        console.log(monsterDrops);
    }

    function sortMonsterProfit() {
        /*sortedMonsterProfit.sort(function (a, b) {
            return b[1] - a[1];
        });*/
        sortedMonsterProfit.sort((a, b) => (parseInt(a.profit) < parseInt(b.profit)) ? 1 : -1)
    }

    /*function checkPrices() {
        console.log(itemPrices);
    }*/

    // Uses static monster database to get monsters and their drops
    // calculations will be made using monster database and the real-time price data from Grand Exchange API

});

export default {
    getKillsPerHour() {
        return killsPerHour;
    },
    /*setKillsPerHour() {
    
    },*/
    getSortedMonsterProfit() {
        return sortedMonsterProfit;
    },
    getMonsterDrops() {
        return monsterDrops;
    }
}


