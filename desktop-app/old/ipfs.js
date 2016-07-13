var ipfsAPI = require('ipfs-api')
var fs = require('fs')
ipfs = ipfsAPI('/ip4/127.0.0.1/tcp/5001')
var http = require('http');

function hostFile(path, done) {
  console.log("host " + path)

  ipfs.add([path], {recursive: false}, (err, res) => {

    if (err) {
      console.error('ipfs error: ' + err)
      return;
    }

    const added = res[0] != null ? res[0] : res
    done(added.Hash)
  })
}

function getFile(hash, path) {

  var file = fs.createWriteStream(path);
  var request = http.get("http://localhost:8080/ipfs/" + hash, function(response) {
    console.log(response)
    response.pipe(file)
  })
}

module.exports = {
  hostFile: hostFile,
  getFile: getFile
}
