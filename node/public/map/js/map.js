function MAP(){
  this.lines = {};
  this.points = {};
  this.map = null;
  this.init();
}

MAP.prototype.init = function(){
  var _this = this;
  if(this.map === null){
    $("<div id='map'></div>").css({"width": "100%","height": "100%"}).appendTo(".left");
    var myLatLng = {lat: 25.037099758499775, lng: 121.52270889282227};
    this.map = new google.maps.Map(document.getElementById('map'), {
      center: myLatLng,
      zoom: 13
    });
    this.map.addListener('tilesloaded',function(){
      var counter = 0;
      var bound = _this.map.getBounds();
      for(var i in _this.points){
        if (!bound.contains(_this.points[i].getPosition())){
          _this.points[i].setMap(null);
          _this.lines[i].setMap(null);
        }else{
          _this.points[i].setMap(_this.map);
          _this.lines[i].setMap(_this.map);
          counter += 1;
        }
      }
      $("#counter").text(counter);
    });
  }
};

MAP.prototype.addPointWithGPS = function(busid,gps,data){
  if( busid in this.points){
    this.points[busid].setPosition(gps);
    this.points[busid].data = data;
  }else{
    var point = new google.maps.Marker({
      "position": gps,
      "map": this.map,
      "title": data.busid,
      "data": data
    });
    var _this = this;
    point.addListener('mouseover',function(){
      $("#bus_id").text(this.data.busid);
      $("#route").text(this.data.routeid);
      $("#recordAt").text(getDateString(new Date(this.data.datatime)));
      _this.lines[this.data.busid].setOptions({"strokeColor": "#9bc53d"});
    });
    point.addListener('mouseout',function(){
      $("#bus_id").text("");
      $("#route").text("");
      $("#recordAt").text("");
      _this.lines[this.data.busid].setOptions({"strokeColor": "#011936"});
    });
    this.points[busid] = point;
  }
};

MAP.prototype.addBusPositionWithGPS = function(busid,gps){
  if ( busid in this.lines ){
    this.lines[busid].getPath().push(new google.maps.LatLng(gps.lat,gps.lng));
  }else {
    this.lines[busid] = new google.maps.Polyline({
      path: [gps],
      geodesic: true,
      strokeColor: '#011936',
      strokeOpacity: 1,
      strokeWeight: 2,
      map: this.map
    });
  }
};

MAP.prototype.clean = function(){
  for(var i in this.points){
    this.points[i].setMap(null);
  }
  this.points = [];
  for(var j in this.lines){
    this.lines[j].setMap(null);
  }
  this.lines = [];
};



function resizeAllElements(){
  var contentHeight = $(window).height()-100;
  $(".left").css("height",contentHeight+"px");
  $(".right").css("height",contentHeight+"px");
}

function addMap(){
  resizeAllElements();
  CRV_MAP = new MAP();
  plotLastestPos();
}

function completeTwoDigits(d){
  return (+d<10)?"0"+d:d;
}

function getDateString(d){
  var month = completeTwoDigits(d.getMonth()+1);
  var date = completeTwoDigits(d.getDate());
  var hour = completeTwoDigits(d.getHours());
  var min = completeTwoDigits(d.getMinutes());
  var sec = completeTwoDigits(d.getSeconds());
  return d.getFullYear()+"-"+month+"-"+date+" "+hour+":"+min+":"+sec;
}

function plotLastestPos(){
  $.ajax({
    "url": "http://crvomg.cloudapp.net/map/api/buses?etlAt=lastest"
  }).done(function(res){
    if (200 == +res.code){
      for(var i in res.data){
        var poi_rawdata = res.data[i];
        var gps = {"lat": +poi_rawdata.latitude,"lng": +poi_rawdata.longitude};
        CRV_MAP.addPointWithGPS(poi_rawdata.busid,gps,poi_rawdata);
        CRV_MAP.addBusPositionWithGPS(poi_rawdata.busid,gps);
      }
      $("#etlAt").text("ETL: "+ getDateString(new Date(res.data[0].etl_time)));
    }
  });
  timer = 60;
  setTimeout(function(){plotLastestPos();}, 60000);
}

var CRV_MAP = null;
var timer = 0;

$(function(){
  setInterval(function(){timer -= 1;$("#timer").text(timer);},1000);
  $("#cleanMap").click(function(){
    CRV_MAP.clean();
  });
  $("#refreshMap").click(function(){
    plotLastestPos();
  });
});
