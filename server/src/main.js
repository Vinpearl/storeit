import commander from 'commander'
import './ws.js'

commander.version('0.0.1')
  .option('-p', '--port <port>', 'set the port to listen to')
  .option('-a', '--addr <ip>', 'set the address to listen on')
  .parse(process.argv)
