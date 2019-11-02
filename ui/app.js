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
  res.header("Access-Control-Allow-Credentials", "true");
  next();
});

app.listen(appEnv.port, '0.0.0.0', function() {
  console.log("server starting on " + appEnv.url)
});
