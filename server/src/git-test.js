import * as gitutil from './git.js'
import fs from 'fs'
import {logger} from './log.js'
import * as proc from 'child_process'

const runTest = () => {
  try {
    fs.mkdirSync('/tmp/storeit-users')
  }
  catch (e) {
    logger.info('cannot mkdir users, you should probably ignore this message')
  }

  gitutil.setUsersDir('/tmp/storeit-users/')

  gitutil.addUser('sevauk', (repo) => {
    logger.info(repo)
  })
}

proc.exec('rm -r /tmp/storeit-users', (err) => {
  runTest()
  if (err) {
    logger.info('rm failed')
  }
})
