// Creating European map
let obj = {};
if(localStorage.getItem("array").length > 1){    
    let colored = localStorage.getItem("array").split(",");
    colored.forEach(function(country){
        obj[country] = {fillKey: "COMPLETED"}
    });
}else{
    obj[localStorage.getItem("array")] = {fillKey: "COMPLETED"};
}

var map = new Datamap({
    element: document.getElementById('map'),
    responsive: true,
    scope: 'world',
    fills: {
        'COMPLETED': '#209CEE',
        defaultFill: '#dddddd'
    },
    data: obj,
    geographyConfig: {
        borderWidth: 0.5,
        highlightFillColor:'rgba(32, 156, 238, 0.5)',
        highlightBorderColor: 'none',
        highlightBorderWidth: 0,
    },
    setProjection: function(element, options) {
        var projection = d3.geo.equirectangular()
            .center([10, 52])
            .rotate([4.4, 0])
            .scale(300)
            .translate([element.offsetWidth / 2, element.offsetHeight / 2]);

            var path = d3.geo.path()
                .projection(projection);

        return {path: path, projection: projection};
    }
});

window.addEventListener('resize', function() {
    map.resize();
});