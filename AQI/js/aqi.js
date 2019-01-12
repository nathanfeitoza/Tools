//var mymap = L.map('mapid').setView([37.7, 100.9], 4, );
var basemaps = {
    Light: L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoid3B5MTk5NSIsImEiOiJjamp4empwZDMxZjZxM2tvOHVwN2Qxb3p1In0.kvDhZ_fJg20bohQnjL0gxQ', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.light',
        accessToken: 'pk.eyJ1Ijoid3B5MTk5NSIsImEiOiJjamp4empwZDMxZjZxM2tvOHVwN2Qxb3p1In0.kvDhZ_fJg20bohQnjL0gxQ'
    }),
    Streets: L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoid3B5MTk5NSIsImEiOiJjamp4empwZDMxZjZxM2tvOHVwN2Qxb3p1In0.kvDhZ_fJg20bohQnjL0gxQ', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.streets',
        accessToken: 'pk.eyJ1Ijoid3B5MTk5NSIsImEiOiJjamp4empwZDMxZjZxM2tvOHVwN2Qxb3p1In0.kvDhZ_fJg20bohQnjL0gxQ'
    })
};

var groups = {
    cities: new L.LayerGroup(),
    kriging: new L.LayerGroup()
};

var groupedOverlays = {
    "Layers": {
        "Cities": groups.cities,
        "Kriging Interpolation": groups.kriging
    }
};


// add clip image
$.getJSON('single-china.json').done(function (data) {
    let lonMax = 135.0879,
        lonMin = 73.4766,
        latMax = 53.5693,
        latMin = 18.1055;
    let anchors = [
        [latMax, lonMin],
        [latMax, lonMax],
        [latMin, lonMax],
        [latMin, lonMin]
    ];
    let boundry = data;
    L.imageTransform('aqi.png', anchors, {
        clip: boundry,
        opacity: 0.8
    }).addTo(groups.kriging);

});


function classifyAQI(value) {
    value = parseInt(value);
    if (value <= 50) {
        return '#149718';
    } else if (value <= 100) {
        return '#fd9827';
    } else if (value <= 200) {
        return '#fc3946';
    } else {
        return '#973f97';
    }
}

function parseDate(date) {
    date = date.split(' ');
    date[1] = date[1].substr(0, date[1].length - 2);
    let year = new Date().getFullYear();
    date.push('GMT+08:00');
    date.push(year);
    date = date.join(' ');
    date = new Date(date);
    res = date.getFullYear() + '/' + (date.getMonth()+1) + '/' + date.getDate() + ' ' + date.getHours() + ':00';
    return res;
}

// add marker layer
$.getJSON('data.json').done(function (data) {
    let index = Math.floor(Math.random() * 100);
    let selectedDate = parseDate(data[index]['utime']);
    $('h3 span').text('更新时间: ' + selectedDate);
    //console.log(data);
    let reg = /\((.+)\)/;
    for (item of data) {
        //console.log(item.lat);
        L.marker([item.lat, item.lon], {
            icon: L.BeautifyIcon.icon({
                iconShape: 'circle-dot',
                iconStyle: "opacity: 0.8",
                iconSize: [8, 8],
                borderWidth: 4,
                borderColor: classifyAQI(item.aqi)
            }),
            title: reg.exec(item.city)[1] + ': ' + item.aqi + '\n更新时间: ' + parseDate(item.utime)
        }).addTo(groups.cities);
    }
});

var mymap = L.map('mapid', {
    center: [36.9, 105.9],
    zoom: 4,
    layers: [basemaps.Light, groups.cities]
});

let layerControl = L.control.groupedLayers(basemaps, groupedOverlays).addTo(mymap);






/*let baselayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoid3B5MTk5NSIsImEiOiJjamp4empwZDMxZjZxM2tvOHVwN2Qxb3p1In0.kvDhZ_fJg20bohQnjL0gxQ', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoid3B5MTk5NSIsImEiOiJjamp4empwZDMxZjZxM2tvOHVwN2Qxb3p1In0.kvDhZ_fJg20bohQnjL0gxQ'
});*/

// add china layer
/*
$.getJSON('js/china.json').done(function (data) {
    L.geoJSON(data, {
        style: function (feature) {
            return {
                color: 'red',
                weight: 1,
                fillColor: 'rgba(51, 136, 255, 0.28)'
            };
        }
    }).bindPopup(function (layer) {
        return layer.feature.properties.name;
    }).addTo(mymap);
    
});*/


