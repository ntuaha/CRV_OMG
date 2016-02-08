var express = require('express');
var router = express.Router();
// var pg = require('pg');
var promise = require('bluebird');
var options = {
    "promiseLib": promise
};
var pgp = require("pg-promise")(options);
var db = pgp("postgres://CRVomg:dataaha305@localhost/bus");

router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.get('/buses', function(req, res, next) {
  console.log(req.query.etlAt);
  if(req.query.etlAt!==undefined){
    if (req.query.etlAt == "lastest"){
        db.many("SELECT * from ${table~}",{"table": "busdata_lastest"})
          .then(function(data){
            res.json({"code": 200,"data": data});
          })
          .catch(function(error){
            res.json({"code": 500,"message": error});
            console.log(error);
          });
    }
  }else{
    res.json({"code": 200});
  }
});


module.exports = router;
