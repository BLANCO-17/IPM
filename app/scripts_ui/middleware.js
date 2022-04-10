const colorThief = new ColorThief();
var $ = jQuery = require("jquery");

var _MonthlyData = {};

function setCharts(data_obj){
    const labels = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
      ];
      var ctx = document.getElementById('myChart').getContext('2d');
      var ctx2 = document.getElementById('myChart2').getContext('2d');
      var ctx3 = document.getElementById('myChart3').getContext('2d');
      
      var ctx4 = document.getElementById('myChart4').getContext('2d');                
      
      var grad = ctx.createLinearGradient(0, 0, 0, 300);
      grad.addColorStop(0, 'rgba(255,255,255, 0.5)');
      grad.addColorStop(1, 'rgba(5, 142, 239, 0.1)');

    
      const hodl_data = {
        labels: labels,
        datasets: [{                                
          borderColor: 'rgb(255, 255, 255)',
          data: Object.values(data_obj.hodl),
          pointRadius: 0,
          fill: true,
          backgroundColor: grad
        }]
      };
      const invst_data = {
        labels: labels,
        datasets: [{                                
          borderColor: 'rgb(255, 255, 255)',
          data: Object.values(data_obj.investment),
          pointRadius: 0,
          fill: true,
          backgroundColor: grad
        }]
      };
      const netgain_data = {
        labels: labels,
        datasets: [{                                
          borderColor: 'rgb(255, 255, 255)',
          data: Object.values(data_obj.netgain),
          pointRadius: 0,
          fill: true,
          backgroundColor: grad
        }]
      };
    
      const config_hodl = {
        type: 'line',
        data: hodl_data,
        options: {
            scales: {
                  x: {
                      grid: {
                          display: false,
                          drawBorder: false
                      },
                      ticks:{
                          display: false
                      }
                  },
                  y: {
                      grid: {
                          display: false,
                          drawBorder: false
                      },
                      ticks:{
                          display: false
                      }
                  }
              },
              plugins :{
                  legend: {
                      display: false
                  }
              }
          }
      };
      const config_invst = {
        type: 'line',
        data: invst_data,
        options: {
            scales: {
                  x: {
                      grid: {
                          display: false,
                          drawBorder: false
                      },
                      ticks:{
                          display: false
                      }
                  },
                  y: {
                      grid: {
                          display: false,
                          drawBorder: false
                      },
                      ticks:{
                          display: false
                      }
                  }
              },
              plugins :{
                  legend: {
                      display: false
                  }
              }
          }
      };
      const config_netgain = {
        type: 'line',
        data: netgain_data,
        options: {
            scales: {
                  x: {
                      grid: {
                          display: false,
                          drawBorder: false
                      },
                      ticks:{
                          display: false
                      }
                  },
                  y: {
                      grid: {
                          display: false,
                          drawBorder: false
                      },
                      ticks:{
                          display: false
                      }
                  }
              },
              plugins :{
                  legend: {
                      display: false
                  }
              }
          }
      };
      
      const myChart = new Chart(ctx, config_invst);
      const myChart2 = new Chart(ctx2, config_hodl);
      const myChart3 = new Chart(ctx3, config_netgain);

      var myChart4 = new Chart(ctx4, {
        type: 'bar',
        // options: {
        //     scales: {
        //           x: {
        //               grid: {
        //                   display: false,
        //                   drawBorder: false
        //               }
        //           },
        //           y: {
        //               grid: {
        //                   display: false,
        //                   drawBorder: false
        //               }
        //           }
        //       }
        //     },
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            datasets: [{ 
                data: Object.values(data_obj.investment),
                label: "Invested",
                borderColor: "rgb(62,149,205)",
                backgroundColor: "rgb(62,149,205,0.1)",
                borderWidth:2
            }, { 
                data: Object.values(data_obj.netgain),
                label: "Net Return",
                borderColor: "rgb(60,186,159)",
                backgroundColor: "rgb(60,186,159,0.1)",
                borderWidth:2
            }, { 
                data: Object.values(data_obj.hodl),
                label: "Hodl",
                borderColor: "rgb(255,165,0)",
                backgroundColor:"rgb(255,165,0,0.1)",
                borderWidth:2
            }
            ]
        },
    });
      
}

function setTableData(element, logo){
    
    item = element.split('_')[0]
    cur = element.split('_')[1]
    
    // col = colorThief.getColor(logo)
    // var r = col[0];
    // var g = col[1];
    // var b = col[2];

    // fetch("http:/127.0.0.1:5000/fromapp/getMonthlyData?item="+item+"&cur="+cur)
    fetch("http:/127.0.0.1:5000/fromapp/getMonthlyData")
    .then(data => data.text())
    .then((data) => {
        data = JSON.parse(data)
        // console.log(data[item+'/'+cur])
        let month_table = document.getElementById("month_table");
        month_table.innerHTML = ""

        let thead = `<thead>
                        <tr>
                            <th><h1>Month</h1></th>
                            <th><h1>Invested</h1></th>
                            <th><h1>Net Returns</h1></th>
                            <th><h1>Hodl Value</h1></th>
                        </tr>
                    </thead>`
        month_table.innerHTML = thead;
        var row = month_table.insertRow();
        
        for(var i=1; i<13; i++){
            row.insertCell().innerHTML = i
            row.insertCell().innerHTML = data[item+'/'+cur]['cost'][i]
            row.insertCell().innerHTML = data[item+'/'+cur]['netgain'][i]
            row.insertCell().innerHTML = data[item+'/'+cur]['hodl'][i]                        
            var row = month_table.insertRow();
            // console.log(data[item+'/'+cur]['cost'][i])
        }
    })

    fetch("http:/127.0.0.1:5000/fromapp/getMonthlyData?item="+item+"&cur="+cur)
    .then(data => data.text())
    .then((data) => {
        data = JSON.parse(data)[item+'/'+cur].trades
        let trade_table = document.getElementById("trade_table");
        trade_table.innerHTML = ""

        let thead = `<thead>
                        <tr>
                            <th><h1>Trade No</h1></th>
                            <th><h1>Invested</h1></th>
                            <th><h1>Shares</h1></th>
                            <th><h1>Net Returns</h1></th>
                            <th><h1>Month</h1></th>
                        </tr>
                    </thead>`
        trade_table.innerHTML = thead;
        var row = trade_table.insertRow();
        // console.log(data))
        for(var i=1; i<=Object.keys(data).length; i++){
            var trade = "trade "+i;
            row.insertCell().innerHTML = "Trade "+ i
            row.insertCell().innerHTML = data[trade]['cost']
            row.insertCell().innerHTML = data[trade]['shares']                       
            row.insertCell().innerHTML = data[trade]['gain']
            row.insertCell().innerHTML = data[trade]['month']                       
            var row = trade_table.insertRow();
            // console.log(data[item+'/'+cur]['cost'][i])
        }
    })
    document.getElementById("report_heading").textContent = item.toUpperCase()+" REPORT"
}

function Init_Items(element){
    let logo = document.createElement('img')
    logo.classList.add("item_con-logo");
    logo.id = element+'_m_logo';
    logo.src = "http://127.0.0.1:5000/fromapp/getItemLogo?item="+element.split('_', 1);

    logo.addEventListener("click", function(){
        setTableData(element, logo)
    });
    document.getElementById("m_item_con").appendChild(logo);
}

async function startup(){   
    var nums=0; 
    nums = await fetch("http://127.0.0.1:5000/fromapp/getItemList")
    .then(data => data.text())
    .then((data) => {
        data = JSON.parse(data).data
        // console.log(data.crypto);
        // nums = data.crypto.length
        createCards(data.crypto);
        data.crypto.forEach(element => {
            // console.log(element)
            Init_Items(element);
        });
        return data.crypto.length;
    })
    .catch(error => {
        console.log(error);
        console.log("Waiting for backend.");
    });

    setFng();
    
    fetch("http://127.0.0.1:5000/fromapp/getChartsData")
    .then(data => data.text())
    .then((data)=> {
        data = JSON.parse(data)
        // console.log(Object.values(data.hodl))
        setCharts(data);
    })
    .catch(error => {
        console.log(error)
    })

    refreshCardsData();

    // setTimeout(sliderFunc, 1000);    
    sliderFunc(nums);
    
};


function setFng(){
    fetch('https://api.alternative.me/fng/?limit=1')
        .then(data => data.text())
        .then((data) => {
            data = JSON.parse(data).data;
            // console.log(data[0].value);
            var Gauge = require("svg-gauge");
            var col;
            var gauge2 = Gauge(
            document.getElementById("gauge"),
            {
                min: 0,
                max: 100,
                dialStartAngle: 180,
                dialEndAngle: 0,
                value: data[0].value,
                viewBox: "0 0 100 57",
                color: function(value) {
                    
                    if(value < 20) {
                        col = "#e45734";                    
                    }else if(value < 40) {
                        col = "#d07733";
                    }else if(value < 60) {
                        col = "#f6de41"
                    }else  if(value < 80) {
                        col = "#aee940";
                    }else{
                        col = "#5dcf1f";
                    }
                    return col;
                }
            });
            document.getElementById("gauge_classification").textContent = data[0].value_classification.toUpperCase();            
            document.getElementById("gauge_classification").style.backgroundColor = col;
        });
}

function createCards(itemList){
    var count=0
    itemList.forEach(element => {

        element = element.replace('_', '/');
        item = element.split("/", 1)
        // console.log(element.toUpperCase());

        if(!document.getElementById(element+"_card")){

            let new_ele = document.createElement('div');
            new_ele.classList.add('assetCard');
            new_ele.id = element+"_card";

            // <div class="assetCard" id="${element}_card">
            let card = `
                <div class="card-data">
                    <div style="display: inline-flex; flex-flow: row;">
                        <span class="card-data-name">${element.toUpperCase()}</span>
                        
                        <span class="card-data-priceChange-perc up" id="${element}_pc">
                        <i class="fa fa-caret-down" id="${element}_indic"></i>
                        </span>
                    </div>
                    <div class="card-data-div">
                        <span class="card-data-price" id="${element}_price">000</span>
                        <span class="card-data-priceChange up" id="${element}_pd">-+0</span>                                
                    </div><br>
                    <div class="card-data-div">
                        <span class="card-data-share">SHARES</span>
                        <span id="${element}_share" style="font-size: 125%; white-space: nowrap;" >0.0</span>
                    </div>
                    <div class="card-data-div">
                        <span class="card-data-cost">SPENT</span>
                        <span id="${element}_cost" style="font-size: 125%; white-space: nowrap;">0.0</span>
                    </div>
                    <div class="card-data-div">
                        <span class="card-data-hodl">HODL</span>
                        <span id="${element}_hodl" style="font-size: 125%; white-space: nowrap;">0.0</span>
                    </div>
                    <div class="card-data-div">
                        <span class="card-data-gain">NET GAIN</span>
                        <span id="${element}_net" style="font-size: 125%; white-space: nowrap;">0.0</span>
                    </div>
                </div>
                <div class="card-logo">
                    <img id="${item}_logo" class="card-itemlogo" src="http://127.0.0.1:5000/fromapp/getItemLogo?item=${item}" alt="">                
                </div>
                `

            let delbtn = document.createElement('div')
            delbtn.classList.add("delbtn")
            delbtn.innerHTML = `<i class="fa-solid fa-trash-can" style="filter: invert(100%);"></i>`

            delbtn.addEventListener("click", function(){
                console.log("delete function");
            });
            
            new_ele.innerHTML = card;
            new_ele.appendChild(delbtn);
            document.getElementById('assetCon').appendChild(new_ele);

            let short_con = document.getElementById('items_shorts');
            let short_div = document.createElement('div');
            short_div.classList.add("item");
            
            if (count == 0){
                short_div.classList.add('active')
            }
            else if(count == 1){
                short_div.classList.add('next')
            }
            else if(count == itemList.length-1){
                short_div.classList.add('prev')
            }
            // console.log(document.getElementsByClassName('item'))
            short_div.id = element+'_short';
            let html_code = `
                <img src="http://127.0.0.1:5000/fromapp/getItemLogo?item=${item}">
                <div class="details">
                    <span class="content" id="${element}_short_price">123456</span>
                    <span class="content up" id="${element}_short_change">-4500</span>
                    <span class="content up" id="${element}_short_pc"></span>
                </div>
                    `
                    // <i class="fa fa-caret-down" id="${element}_short_indic"></i>

            short_div.innerHTML = html_code;

            short_con.appendChild(short_div);
            
            const img = document.createElement('img');
            img.src = 'http://127.0.0.1:5000/fromapp/getItemLogo?item='+item;
            // console.log('http://127.0.0.1:5000/fromapp/getItemLogo?item='+item)
                    
            setTimeout(function(){
                col = colorThief.getColor(img)
                var r = col[0];
                var g = col[1];
                var b = col[2];
                document.getElementById(element+"_card").style.backgroundColor = `rgba(${r}, ${g}, ${b}, 0.40)`;
                
                document.getElementById(element+'_card').addEventListener("mouseover", function(){                            
                    document.getElementById(element+"_card").style.backgroundColor = `rgba(${r}, ${g}, ${b}, 0.65)`;                
                })
                document.getElementById(element+'_card').addEventListener("mouseout", function(){                                
                    document.getElementById(element+"_card").style.backgroundColor = `rgba(${r}, ${g}, ${b}, 0.40)`;
                });
            }, 
            3000);
    }
    count++;
    });
    
}

function sliderFunc(max){
    const slider = document.getElementsByClassName("items");
    const slides = document.getElementsByClassName("item");
    const button = document.getElementsByClassName("button");    

    let current = 0;
    let prev = slides.length-1;
    let next = 1;
    console.log(slides.length)
    for (let i = 0; i < button.length; i++) {
        button[i].addEventListener("click", () => i == 0 ? gotoPrev() : gotoNext());
    }

    const gotoPrev = () => current > 0 ? gotoNum(current - 1) : gotoNum(slides.length - 1);

    const gotoNext = () => current < max ? gotoNum(current + 1) : gotoNum(0);

    const gotoNum = number => {
        current = number;
        prev = current - 1;
        next = current + 1;
        for (let i = 0; i < slides.length; i++) {
            slides[i].classList.remove("active");
            slides[i].classList.remove("prev");
            slides[i].classList.remove("next");
        }

        if (next == max) {
            next = 0;
        }

        if (prev == -1) {
            prev = max-1;
        }
        if(current == slides.length){
            current = 0;
            next = 1;
        }
        // console.log(prev, current, next)
        slides[current].classList.add("active");
        slides[prev].classList.add("prev");
        slides[next].classList.add("next");
    }
}

function refreshCardsData(){
    fetch("http://127.0.0.1:5000/fromapp/getItemList")
    .then(data => data.text())
    .then( async (data) => {
        ItemList = JSON.parse(data).data
        // console.log(data);
        // createCards(data.crypto);
        let Itemdata = await getItemDetails();
        total_invst = 0.0;
        total_net_gain = 0.0;
        total_net_value = 0.0;
        
        ItemList.crypto.forEach( (item) => {
            
            if(!document.getElementById(item.replace('_', '/')+'_card')){
                createCards([item]);
            }
            let element = item.replace('_', '/');
            let hodl = Number((Itemdata[element].prices[0]*Itemdata[element].shares).toFixed(2));
            
            total_invst += Itemdata[element].cost;
            total_net_gain += Itemdata[element].netgain;
            total_net_value += hodl;
            // console.log(element)
            document.getElementById(element+'_price').textContent = Itemdata[element].prices[1];
            document.getElementById(element+'_share').textContent = ": " + Itemdata[element].shares;
            document.getElementById(element+'_cost').textContent = ": " + Itemdata[element].cost;
            document.getElementById(element+'_net').textContent = ": " + Itemdata[element].netgain;
            document.getElementById(element+'_hodl').textContent = ": " + hodl;
            document.getElementById(element+'_pd').textContent = Itemdata[element].change.indic + Itemdata[element].change.diff;
            let indicator = document.getElementById(element+'_pc');
            // let caret = 
            // indicator.textContent = Itemdata[element].change.indic + Itemdata[element].change.percentage;
            
            //setting shorts item elements
            document.getElementById(element+'_short_price').textContent = Itemdata[element].prices[1];
            document.getElementById(element+'_short_change').textContent = Itemdata[element].change.indic + Itemdata[element].change.diff;
            document.getElementById(element+'_short_pc').textContent = Itemdata[element].change.percentage + "%";

            // console.log(document.getElementById(element+'_short_indic'))            
            
            if(Itemdata[element].change.indic == '+'){
                indicator.classList.replace('down', 'up');
                document.getElementById(element+"_pd").classList.replace('down', 'up');
                document.getElementById(element+'_indic').classList.replace('fa-caret-down', 'fa-caret-up');
                
                // document.getElementById(element+'_short_indic').classList.replace('fa-caret-down', 'fa-caret-up');
                document.getElementById(element+'_short_change').classList.replace('down', 'up');
                document.getElementById(element+'_short_pc').classList.replace('down', 'up');
            }
            else{
                indicator.classList.replace('up', 'down');
                document.getElementById(element+"_pd").classList.replace('up', 'down');
                document.getElementById(element+'_indic').classList.replace('fa-caret-up', 'fa-caret-down');

                // document.getElementById(element+'_short_indic').classList.replace('fa-caret-up', 'fa-caret-down');
                document.getElementById(element+'_short_change').classList.replace('up', 'down');
                document.getElementById(element+'_short_pc').classList.replace('up', 'down');
            }
            document.getElementById(element+'_indic').textContent = ' ' + Itemdata[element].change.percentage + " %";

            document.getElementById('total_invst').textContent = "$"+total_invst.toLocaleString("en-US");
            document.getElementById('net_value').textContent = "$"+total_net_value.toLocaleString("en-US");
            document.getElementById('net_profit').textContent = "$"+total_net_gain.toLocaleString("en-US");

            // id="${element}_short_price"
            
            
        })
    })
    .catch(error => {
        console.log(error);
    });
}

async function getItemDetails(){
    let out = await fetch("http://127.0.0.1:5000/fromapp/getCardStructure")
    .then(data => data.text())
    .then((data) => {
        data = JSON.parse(data).ItemObject
        return data;
        // console.log(data['btc/usd']);
        // createCards(data.crypto);        
    })
    .catch(error => {
        console.log(error);
    });
    return out;
}

function addItemRequest(){

    let item = document.getElementById('item_select').value;
    let cur = document.getElementById('cur_select').value;
    let shares = document.getElementById('item_qty').value;
    let cost = document.getElementById('item_price').value;
    let price = document.getElementById('item_price').value;
    let month = document.getElementById('month_select').value;

    let url = 'http://127.0.0.1:5000/toapp/addTradeItem?';

    dict = {
        "item": item+"&",
        "cur": cur+"&",
        "cost": cost+"&",
        "shares": shares+"&",
        "price": price+"&",
        "month": month+"&",
        "type": "cryp"
    }
    // "testing": "on"

    for(var key in dict){
        url += key + "=" + dict[key];
        // console.log(key+" - "+dict[key]);
    }
    
    fetch(url)
    .then(data => data.text())
    .then((data) => {
        data = JSON.parse(data)
        console.log(data)
        
        //Create Newly added element
        let obj = item +'_'+ cur;
        createCards([obj]);
        Init_Items(obj);        
        // if data.request == 200{

        // }
    })

    toggle_addWindow();
}

startup();
// setInterval(rotate_icons, 50);

// setInterval(refreshCardsData, 10000);