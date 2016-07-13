var gitutil = require('./gitutil.js')
var fs = require('fs')
var ipfs = require('./ipfs.js')
var path = require('path')

var exclude_files = []

function isDir(path) {
  try {
    return fs.lstatSync(pathFrom + filename).isDirectory()
  } catch (e) {
    return false
  }
}

function makeDir(path) {
  try {
    fs.mkdirSync(path)
  } catch (e) {
    console.error("2: ignore " + path + " (" + e + ")")
  }
}

function syncDirs(filename, pathFrom, pathToUpdate, isGit) {

  // TODO: handle weird cases when file already exists in target

  // TODO: don't match .gitsomestuff
  if (filename.startsWith('.git') || exclude_files.indexOf(filename) !== -1) {
    return
  }

  try {
    var isdir = fs.lstatSync(pathFrom + filename).isDirectory()
  } catch (e) {
    isRemove = true
    var targetIsDir = isDir(pathToUpdate + filename)
    if (targetIsDir) {
      fs.rmdir(pathToUpdate + filename)
    } else {
      try {
        fs.unlinkSync(pathToUpdate + filename)

        if (!isGit) {
          putFileInGit(filename, "rm")
        }
      } catch(e) {
        console.error("1: ignore " + filename + " " + e)
      }
    }
    return
  }

  if (isdir) {
    makeDir(pathToUpdate + filename)
  } else {
    exclude_files.push(filename)

    if (!isGit) {
      putFileInGit(filename, "add")
    } else {
      addFileFromGit(filename)
    }
  }
}

function putFileInGit(filename, action) {

  if (action == "rm") {
    gitutil.commit(filename, action)
  } else {

    ipfs.hostFile(gitutil.getUserPath() + filename, function(hash) {
      console.log("added " + hash + " to ipfs (" + filename + ")")
      fs.writeFile(gitutil.getRepo() + "/" + filename, hash, {flag: 'w+'}, function(err) {
        if (err) {
          return console.error(err)
        }

        gitutil.commit(filename)

        exclude_files = exclude_files.slice(exclude_files.indexOf(filename), 1)
      })
    })
  }

}

function prepareUserDir() {

  makeDir(gitutil.getUserPath())
}

function addAllFromGit(done) {

  var recursive = require('recursive-readdir');

  // FIXME handle submodules, better handle the .git exception
  recursive(gitutil.getRepo(), ['.git'], function (err, files) {

    files.sort(function(a, b){
      return a.length - b.length;
    })

    // TODO: use something like map
    for (var i = 0; i < files.length; i++) {
      files[i] = files[i].replace(gitutil.getRepo(), gitutil.getUserPath())
    }


    // Files is an array of filename
    files.forEach(function(file) {

      const dir = path.dirname(file)

      var tree = ''
      dir.split('/').forEach(function(d) {
          tree += d + '/'
          console.log('mkdir: ' + tree)
          makeDir(tree)
      })

      addFileFromGit(file.substring(gitutil.getUserPath().length))
    })
    done()
  })

}

function poll() {

  gitutil.prepareRepo(function() {

    console.log("watching " + gitutil.getUserPath())

    prepareUserDir()
    addAllFromGit(function() {

      fs.watch(gitutil.getUserPath(), {recursive: true}, function(event, filename) {
        syncDirs(filename, gitutil.getUserPath(), gitutil.getRepo(), false)
      })

    })

    fs.watch(gitutil.getRepo(), {recursive: true}, function(event, filename) {
      syncDirs(filename, gitutil.getRepo(), gitutil.getUserPath(), true)
    })

  })

  setInterval(pullEverySecond, 1000)

}

function addFileFromGit(hashFilename) {

  const targetPath = gitutil.getUserPath() + "/" + hashFilename

  if (isDir(hashFilename)) {
    makeDir(targetPath)
    return
  }
  const hashPath = gitutil.getRepo() + "/" + hashFilename
  var hash = fs.readFileSync(hashPath)
  console.log("hash for " + hashPath + " is " + hash)
  console.log("loading this at " + targetPath)
  ipfs.getFile(hash, targetPath)
  console.log("done")
}


function pullEverySecond() {
  gitutil.pull()
}

module.exports = {
  poll: poll
}
