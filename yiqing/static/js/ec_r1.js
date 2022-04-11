var ecRight1 = echarts.init(document.getElementById('r1'));

right1Option = {

    title: [
        {
            text: '省份/直辖市新增确诊TOP5',
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
            barMaxWidth: '20%',
            data: []
        }
    ]
};

right1Option && ecRight1.setOption(right1Option);