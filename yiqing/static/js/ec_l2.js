var ecLeft2 = echarts.init(document.getElementById('l2'));

left2Option = {

    title: [
        {
            text: '全国每日确诊、治愈情况',
            left: 'left',
            textStyle: {
                color: 'black'
            }
        },

    ],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#7171C6'
            }
        }
    },
    legend: {
        data: ['日确诊', '日治愈'],
        left: 'right',
        textStyle: {
            color: 'black'
        }
    },

    grid: {
        left: '4%',
        right: '6%',
        bottom: '4%',
        top: 50,
        containLabel: true
    },
    xAxis: [
        {
            type: 'category',
            data: []
        },
    ],
    yAxis: [
        {
            type: 'value',
            axisLabel: {
                show: true,
                color: 'black',
                fontSize: 12,
                formatter: function (value) {
                    if (value > 1000) {
                        value = value / 1000 + 'k';
                    }
                    return value;
                }
            },
            axisLine: {
                show: true
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#17273B',
                    width: 1,
                    type: 'solid'
                }
            }
        },
    ],
    series: [
        {
            name: '日确诊',
            type: 'line',
            //smooth: true,
            data: []
        },
        {
            name: '日治愈',
            type: 'line',
            //smooth: true,
            data: []
        },
    ]
};

left2Option && ecLeft2.setOption(left2Option);