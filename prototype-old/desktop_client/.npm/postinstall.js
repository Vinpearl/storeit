var platform = require('os').platform();
var exec = require('child_process').exec;

var cp = (platform === 'win32' || platform === 'win64') ? 'copy' : 'cp';

exec(cp + ' .gulp/env.json.example .gulp/env.json && gulp build');
