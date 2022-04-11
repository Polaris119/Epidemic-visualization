//l1数据
function getL1Data() {
    $.ajax({
        url: '/l1',
        success: function (data){
            // console.log(data)
            left1Option.xAxis[0].data = data.date;
            left1Option.series[0].data = data.confirm;
            left1Option.series[1].data = data.heal;
            left1Option.series[2].data = data.dead;
            ecLeft1.setOption(left1Option);
        }, error: console.error('请求l1数据失败')
    })
}
getL1Data();

// l2数据
function getL2Data() {
    $.ajax({
        url: '/l2',
        success: function (data){
            // console.log(data)
            left2Option.xAxis[0].data = data.date;
            left2Option.series[0].data = data.confirm_add;
            left2Option.series[1].data = data.heal_add;
            ecLeft2.setOption(left2Option);
        }, error: console.error('请求l2数据失败')
    })
}
getL2Data();

//c1数据
function getC1Data() {
    $.ajax({
        url: '/c1',
        success: function (jsonData) {
            //分别选中各个元素并填充内容
            // console.log(jsonData);
            $('.num h1').eq(0).text(jsonData.confirm);
            $('.num h1').eq(1).text(jsonData.suspect);
            $('.num h1').eq(2).text(jsonData.heal);
            $('.num h1').eq(3).text(jsonData.dead);
        }, error: console.error('请求c1数据失败')
  })
}
getC1Data();

// c2数据
function getC2Data() {
    $.ajax({
        url: '/c2',
        success: function (jsonData) {
            // console.log(jsonData);
            mapOption.series[0].data = jsonData.key_data;
            echartsMap.setOption(mapOption);
        }, error: console.error('请求c2数据失败')
    })
}
getC2Data();

//r1数据
function getR1Data() {
    $.ajax({
        url: '/r1',
        success: function (data){
            // console.log(data)
            right1Option.xAxis[0].data = data.province;
            right1Option.series[0].data = data.confirm_add;
            ecRight1.setOption(right1Option);
        }, error: console.error('请求r1数据失败')
    })
}
getR1Data();

//r2数据
function getR2Data() {
    $.ajax({
        url: '/r2', 
        success: function (data){
            // console.log(data)
            right2Option.xAxis[0].data = data.city;
            right2Option.series[0].data = data.confirm;
            ecRight2.setOption(right2Option);
        }, error: console.error('请求r2数据失败')
    })
}
getR2Data();