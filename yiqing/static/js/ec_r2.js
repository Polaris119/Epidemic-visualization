var ecRight2 = echarts.init(document.getElementById('r2'));

right2Option = {

    title: [
        {
            text: '江苏省各城市现有确诊情况',
            left: 'left',
            textStyle: {
                color: 'black'
            }
        },

    ],
    color: ['#3398DB'],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow',
        }
    },

    xAxis: [
        {
            type: 'category',
            data: [],
            axisLabel: {
                color: 'black',
            }
        },
    ],
    yAxis: [
        {
            type: 'value',
            axisLabel: {
                color: 'black',
            }
        }
    ],
    series: [
        {
            type: 'bar', //条形图
            barMaxWidth: '7%',
            data: []
        }
    ]
};

right2Option && ecRight2.setOption(right2Option);