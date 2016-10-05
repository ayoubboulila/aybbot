var express = require('express');
var app = express();
//var fs = require("fs");

app.get('/test', function (req, res) {
 //  fs.readFile( __dirname + "/" + "users.json", 'utf8', function (err, data) {
  //     console.log( data );
   //    res.end( data );
  // });


var ProxyLists = require('proxy-lists');
var res1 = [];
var options = {
  anonymityLevels: ['elite'],
  sourcesWhiteList: ['incloak']
};

// `gettingProxies` is an event emitter object.
//var gettingProxies = ProxyLists.getProxiesFromSource(options);
var gettingProxies = ProxyLists.getProxies(options);

gettingProxies.on('data', function(proxies) {
    // Received some proxies.
console.log("received some proxies");
console.log(proxies.length);
console.log(proxies[0]);
res1 = res1.concat(proxies);
//console.log(proxies);

});

gettingProxies.on('error', function(error) {
    // Some error has occurred.
    console.error(error);
});

gettingProxies.once('end', function() {
    // Done getting proxies.
console.log("done");
console.log("");
res.end(JSON.stringify(res1));
});


})

var server = app.listen(80, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("AYB proxy app listening at http://%s:%s", host, port)

})
