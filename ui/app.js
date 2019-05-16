var express = require('express');
var app = express();
var cfenv = require("cfenv");
var appEnv = cfenv.getAppEnv();
var pretty = require('express-prettify');
var bodyParser = require('body-parser');

app.use(express.static(__dirname));
// used by the MindSphere OSbar
//app.use('/app-info.json', express.static('./app-info.json') , function(req, res){});
//app.use(pretty({ query: 'pretty' }));
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "GET,POST");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});
app.use(bodyParser.json({ type: 'application/json' }));

app.get("/api/getHealth", function(req, res, next) { 
  var data = {alive: 'true'};
  res.json(data); 
});

app.post("/api/iziToast",function(req, res, next) { 
  iziToast.show(req.body);
  res.json({status: 200});
});

app.listen(appEnv.port, appEnv.bind, function() {
  console.log("server starting on " + appEnv.url)
});
