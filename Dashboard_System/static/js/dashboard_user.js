var indexCount = 0
var echartEngine = undefined;

window.onload = () => {
    console.log('Hellow WOrld')
    if (localStorage.getItem("acc") != null) {
        var userData = JSON.parse(localStorage.getItem('acc'));
        var nameList = document.getElementsByClassName("ele-name");
        for (let i=0;i < nameList.length; i++) { 
            nameList[i].textContent = userData['name']
        };
    } else {
        alert('提示：請重新登錄網頁！');
        window.location.href = "/login/";
    };
    indexCount = 0;
    // realTimeData();
    function init() {
        var requests = new XMLHttpRequest();
        var url = 'http://34.211.147.93:5000/';
        requests.open('GET',url,true);
        requests.onload = () => {
            console.log('Request Status Code: ',requests.status)
            echartEngine = getStaticData(JSON.parse(requests.response)['data'])
        };
        requests.send()
    };
    return init()
};

window.onresize = function() {
    echartEngine.resize();
}

window.onclick = function(e) {
    if  (e.target.matches('#dropdown-icon')) {  
        var buttonDropDown = document.getElementById("nav-ele");
        var iconDropDown = document.getElementById("dropdown-icon");

        if (buttonDropDown.style.display === "flex") {
            buttonDropDown.style.display = "none";
            iconDropDown.style.transform = "rotate(90deg)"
        } else { //if (buttonDropDown.style.display === "none")
            buttonDropDown.style.display = "flex";
            iconDropDown.style.transform = "rotate(0deg)"
        }
    }
};

function candleTypeClassifier(open,close){
    var diff = open - close;
    if (diff > 0){ return 1 } 
    else if (diff < 0){ return -1 } 
    else { return 0 };
};

function getStaticData(dataShares){
    var categoryData = [];
    var values = [];
    var volumes = [];
    dataShares.forEach((data,index) => {
        categoryData.push(data.date)
        values.push([data.open,data.close,data.low,data.high,data.volume])
        volumes.push([index,data.volume,candleTypeClassifier(data.open,data.close)])
    });
    console.table(dataShares)        
    return plotCandleStick({
        'categoryData' : categoryData,
        'values' : values,
        'volumes' : volumes
    });
};

function pushDataRT(option,data) {
    var date = data['date'].split('+')[0]
    option.xAxis[0]['data'].push(date);
    option.xAxis[1]['data'].push(date);
    option.series[0]['data'].push([
        data['open'],data['high'],data['low'],data['close'],data['volume']
    ]);
    option.series[1]['data'].push([
        indexCount,data['volume'],
        candleTypeClassifier(data['open'],data['close'])
    ])

    var checkObj = option.series[parseInt(data['predict'])+2]['markArea']['data']
    if (checkObj.length != 0) {
        if (checkObj[checkObj.length-1].length != 2) {
            checkObj[checkObj.length-1].push({xAxis: date})
        } else {
            checkObj.push([{xAxis: date}])
        }
    } else {
        checkObj.push([{xAxis: date}])
    }
    indexCount++
}

function plotCandleStick(eachShareData){
    var upColor = '#00da3c';
    var downColor = '#ec0000';
    var echart = echarts.init(document.getElementById('dashboard-layout'));
    var option = {
        animation: false,
        legend: {
            bottom: 10,
            left: 'center',
            data: ['Dow-Jones index', 'MA5', 'MA10', 'MA20', 'MA30']
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            },
            borderWidth: 1,
            borderColor: '#ccc',
            padding: 10,
            textStyle: {
                color: '#000'
            },
            position: function (pos, params, el, elRect, size) {
                var obj = {top: 10};
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            }
            // extraCssText: 'width: 170px'
        },
        axisPointer: {
            link: {xAxisIndex: 'all'},
            label: {
                backgroundColor: '#777'
            }
        },
        toolbox: {
            show: true,
            left: 'right',
            top: 'top',
            feature: {
                dataZoom: { yAxisIndex: false },
                brush: { type: ['lineX', 'clear'] },
                saveAsImage: { show: true }
            }
        },
        brush: {
            xAxisIndex: 'all',
            brushLink: 'all',
            outOfBrush: {
                colorAlpha: 0.1
            }
        },
        visualMap: {
            show: false,
            seriesIndex: 1,
            dimension: 2,
            pieces: [{
                value: 1,
                color: downColor
            }, {
                value: -1,
                color: upColor
            }]
        },
        grid: [
            {
                left: '10%',
                right: '8%',
                height: '50%'
            },
            {
                left: '10%',
                right: '8%',
                top: '63%',
                height: '16%'
            }
        ],
        xAxis: [
            {
                type: 'category',
                data: eachShareData.categoryData,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax',
                axisPointer: {
                    z: 100
                }
            },
            {
                type: 'category',
                gridIndex: 1,
                data: eachShareData.categoryData,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                axisTick: {show: false},
                splitLine: {show: false},
                axisLabel: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax'
            }
        ],
        yAxis: [
            {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: {show: false},
                axisLine: {show: false},
                axisTick: {show: false},
                splitLine: {show: false}
            }
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 98,
                end: 100
            },
            {
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                top: '85%',
                start: 98,
                end: 100
            }
        ],
        series: [
            {
                name: 'Dow-Jones index',
                type: 'candlestick',
                data: eachShareData.values,
                itemStyle: {
                    color: upColor,
                    color0: downColor,
                    borderColor: null,
                    borderColor0: null
                },
                tooltip: {
                    formatter: function (param) {
                        param = param[0];
                        return [
                            'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                            'Open: ' + param.data[0] + '<br/>',
                            'Close: ' + param.data[1] + '<br/>',
                            'Lowest: ' + param.data[2] + '<br/>',
                            'Highest: ' + param.data[3] + '<br/>'
                        ].join('');
                    }
                }
            },
            {
                name: 'Volume',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: eachShareData.volumes
            },
            {
                name: 'Strategic1',
                type: 'line',
                markArea: {
                    itemStyle: {
                        opacity: 0.3,
                        color: 'red'
                    },
                    data: [[{xAxis:'2017-12-29 20:01:00'},{xAxis:'2017-12-29 20:43:00'}]]
                }
            },
            {
                name: 'Strategic2',
                type: 'line',
                markArea: {
                    itemStyle: {
                        opacity: 0.3,
                        color: 'blue'
                    },
                    data: [[{xAxis:'2017-12-29 21:00:00'},{xAxis:'2018-01-01 22:10:00'}]]
                }
            },
            {
                name: 'Strategic3',
                type: 'line',
                markArea: {
                    itemStyle: {
                        opacity: 0.3,
                        color: 'green'
                    },
                    data: [[{xAxis:'2018-01-01 22:16:00'},{xAxis:'2018-01-01 23:49:00'}]]
                }
            }
        ]
    }
    echart.setOption(option);
    echart.dispatchAction({
        type: 'brush',
        areas: [
            {
                brushType: 'lineX',
                coordRange: [eachShareData.categoryData[0],eachShareData.categoryData[eachShareData.categoryData.length-1]], // X 軸資料起始日及終止日
                xAxisIndex: 0
            }
        ] // areas 表示選礦集合，可以指定多個選框
        // 也可以通過 xAxisIndex 或 yAxisIndex 來指定此選框屬於直角坐標系
        // 如果沒有指定，則此選框屬於“全局選框”。不屬於任何坐標系。
        // 屬於“坐標系選框”，可以隨坐標系一起縮放平移。屬於全局的選框不行
    }); // 區域選擇相關行為
    return echart
};
// function plotCandleStick(symbol){
//     var upColor = '#00da3c';
//     var downColor = '#ec0000';
//     var echart = echarts.init(document.getElementById('dashboard-layout'));
//     var option = {
//         animation: true, // 初始化是否動態渲染
//         legend: {
//             bottom: 10, // 提示文字在網頁底部的距離
//             left: 'center', // 提示文字置中
//             data: [
//                 symbol,'Strategic1','Strategic2','Strategic3',
//                 'Strategic4','Strategic5','Strategic6','Strategic7',
//                 'Strategic8'
//             ] // 提示文字內容***
//         }, // 提示文字與網頁底部的呈現格式
//         tooltip: {
//             trigger: 'axis', // 坐标轴触发，主要在柱状图，折线图等会使用类目轴的图表中使用
//             axisPointer: {
//                 type: 'cross' // 十字准星指示器。其实是种简写，表示启用两个正交的轴的 axisPointer
//             },
//             borderWidth: 1, // 提示框的邊框寬度
//             borderColor: '#ccc', // 提示框的邊框顏色
//             padding: 10, // 提示框與內容的間隔距離  
//             textStyle: {
//                 color: '#000' // 提示框的文字顏色
//             }, // 提示框的文字格式設定
//             position: function (pos, params, el, elRect, size) {
//                 var obj = { top: 10 };
//                 // 鼠标在左侧时 tooltip 显示到右侧，鼠标在右侧时 tooltip 显示到左侧
//                 obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
//                 return obj;
//             } // 提示框的位置設定
//         }, // 提示框的設定
//         axisPointer: {
//             link: { 
//                 xAxisIndex: 'all'
//             },
//             label: {
//                 backgroundColor: '#777' // 坐標標籤的背景顏色
//             }
//         }, // 坐标轴指示器的設定。
//         toolbox: {
//             feature: {
//                 dataZoom: {
//                     yAxisIndex: false
//                     // Zoom 時僅會橫向放大，Y 軸不會影響
//                 },
//                 brush: {
//                     type: ['lineX', 'clear']
//                     // rect  是框框選擇
//                     // linex 是橫向選擇
//                     // clear 是清除選擇
//                 }
//             }
//         }, // 工具欄（右上角）的設定
//         axisPointer: {
//             link: {xAxisIndex: 'all'},
//             label: {
//                 backgroundColor: '#777'
//             }
//         },
//         brush: {
//             xAxisIndex: 'all', // 指定哪些 xAxisIndex 可以被刷选。
//             brushLink: 'all', // 不同系列间，选中的项可以联动。
//             outOfBrush: {
//                 colorAlpha: 0.1
//                 // Candle Stick 的全色與中空的顏色參數
//             }
//         }, // Highlight 時，框框內外的格式設定
//         visualMap: {
//             show: false,
//             seriesIndex: 1,
//             dimension: 2,
//             pieces: [{
//                 value: 1,
//                 color: downColor
//             }, {
//                 value: -1,
//                 color: upColor
//             }]
//         },
//         grid: [
//             {
//                 left: '10%', // 距離左邊 10% 的寬
//                 right: '8%', // 距離右邊  8% 的寬
//                 height: '50%'// 整體高度 50% 的寬
//             }, // 上網格（K 線圖比例設定）
//             {
//                 left: '10%', // 距離左邊 10% 的寬
//                 right: '8%', // 距離右邊  8% 的寬
//                 top: '63%',  // 距離上部 63% 的寬
//                 height: '16%'// 整體高度 16% 的寬（由於有兩部分，所以各 16 %）
//             } // 下網格（Volume 線圖比例設定）
//         ], // 圖表視覺的背景網格樣式設定
//         xAxis: [
//             {
//                 type: 'category', // X 軸資料類別
//                 data: [], // X 軸的資料
//                 scale: true,
//                 axisLine: { onZero: false },
//                 splitLine: {
//                     show: true, // X 軸是否顯示豎線
//                     interval: 3 // X 軸豎線每隔 4 條切 1 次
//                 }, // X 軸背景網格的豎線是否顯示
//                 min: 'dataMin',
//                 max: 'dataMax',
//                 // gridIndex: 0, // X 軸所在的 Grid 的索引（上半部的意思）
//             },
//             {
//                 type: 'category', // X 軸資料類別
//                 gridIndex: 1, // X 軸所在的 Grid 的索引（下半部的意思）
//                 data: [], // X 軸的資料
//                 scale: true,
//                 boundaryGap: false,
//                 axisLine: { onZero: false },
//                 axisTick: { show: false },
//                 splitLine: { show: false },
//                 axisLabel: { show: false },
//                 splitNumber: 20,
//                 min: 'dataMin',
//                 max: 'dataMax'
//             }
//         ], // X 軸資料輸入及呈現樣式設定（多過 2 個 X 軸就需要特別設定 offset）
//         yAxis: [
//             {
//                 scale: true, // Y 軸數據呈現是否脫離 0 的比例
//                 gridIndex: 0, // Y 軸所在的 Grid 的索引（上半部的意思）
//                 splitArea: { show: true } // Y 軸切割區域的樣式設定
//             },
//             {
//                 scale: true,
//                 gridIndex: 1, // Y 軸所在的 Grid 的索引（下半部的意思）
//                 splitNumber: 2,
//                 splitLine: { show: false }, // Y z軸是否顯示
//                 axisLabel: { show: false },
//                 axisLine: { show: false },
//                 axisTick: { show: false },
//             }
//         ], // Y 軸資料輸入及呈現樣式設定（多過 2 個 Y 軸就需要特別設定 offset）
//         dataZoom: [
//             {
//                 type: 'inside', // 縮放種類：Bar 圖
//                 xAxisIndex: [0, 1], // 縮放最多顯示幾隻 K 線
//                 start: 98, // 縮放窗口的初始化百分比
//                 end: 100
//             },
//             {
//                 show: true, // 最底部縮放 data 的欄位
//                 xAxisIndex: [0,1], // 
//                 type: 'slider', // 縮放種類：拖拉式
//                 bottom: '10%', // 距離下部 10% 的寬
//                 start: 98, // 縮放窗口的初始化百分比
//                 end: 100
//             }
//         ], // 用於區域縮放，從而能自由關注細節的數據信息，或者概覽數據正題，或者除去離散點的影響。
//         series: [
//             {
//                 name: symbol, // 提示框中的小標題
//                 type: 'candlestick',
//                 data: [], // Data 中數據列表
//                 itemStyle: {
//                     color: upColor, // 上漲 K 線顏色
//                     color0: downColor, // 下跌 K 線顏色
//                     borderColor: null, // 上漲 K 線顏色外框顏色
//                     borderColor0: null // 下跌 K 線顏色外框顏色
//                 }, // K 线图的图形样式
//                 tooltip: {
//                     formatter: function (param) {
//                         param = param[0];
//                         return [
//                             'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
//                             'Open: ' + param.data[0] + '<br/>',
//                             'Close: ' + param.data[1] + '<br/>',
//                             'Lowest: ' + param.data[2] + '<br/>',
//                             'Highest: ' + param.data[3] + '<br/>'
//                         ].join(''); // 提示框顯示的文字內容
//                     }
//                 }
//             }, // 提示框的內容設定
//             {
//                 name: 'Volume', // 提示框中的小標題
//                 type: 'bar',
//                 xAxisIndex: 1,
//                 yAxisIndex: 1,
//                 data: [] // Data 中數據列表
//             },
//             {
//                 name: 'Strategic0',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             },
//             {
//                 name: 'Strategic1',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             },
//             {
//                 name: 'Strategic2',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             },
//             {
//                 name: 'Strategic3',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             },
//             {
//                 name: 'Strategic4',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             },
//             {
//                 name: 'Strategic5',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             },
//             {
//                 name: 'Strategic6',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             },
//             {
//                 name: 'Strategic7',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             },
//             {
//                 name: 'Strategic8',
//                 type: 'line',
//                 markArea: {
//                     itemStyle: {
//                         opacity: 0.3,
//                         color: 'red'
//                     },
//                     data: []
//                 }
//             }
//         ]
//     };
//     echart.setOption(option);
//     echart.dispatchAction({
//         type: 'brush',
//         areas: [
//             {
//                 brushType: 'lineX',
//                 coordRange: [], // X 軸資料起始日及終止日 eachShareData.categoryData[0],eachShareData.categoryData[eachShareData.categoryData.length-1]
//                 xAxisIndex: 0
//             }
//         ] // areas 表示選礦集合，可以指定多個選框
//         // 也可以通過 xAxisIndex 或 yAxisIndex 來指定此選框屬於直角坐標系
//         // 如果沒有指定，則此選框屬於“全局選框”。不屬於任何坐標系。
//         // 屬於“坐標系選框”，可以隨坐標系一起縮放平移。屬於全局的選框不行
//     }); // 區域選擇相關行為
//     return echart
// };








function realTimeData() {
    let socket = new WebSocket("ws://localhost:8000/ws/symbol_channel/");
    socket.onopen = () => {
        socket.send(JSON.stringify({
            "hash_value":"2755f0e797e7c1df3c463c3fe649b8691a23e2e4aa5ea5bcfbed9ac17ffc06a4",
            "user":"wyne",
            "symbol":"ETHBTC",
            "kline_size":"5m",
            "start_date":"2021-08-01 14:45:00",
            "end_date":"2021-08-14 14:45:00"
        }))
    }
    echartEngine = plotCandleStick()

    socket.onmessage = (event) => {
        var option = echartEngine.getOption();
        var data = JSON.parse(event['data'])
        data.forEach((each) => {
            pushDataRT(option,each)
            console.log(option)
        })
        // echartEngine.clear()
        echartEngine.hideLoading()
        echartEngine.setOption(option)
    }

    socket.onerror = (error) => {
        alert(`提示：${error}`)
    }
}



