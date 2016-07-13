import fs from 'fs'
import {logger} from './log.js'
import * as util from './util.js'
import path from 'path'
export let usersDir = path.resolve('./users/')

// could figure out how to ES6 import this
import git from 'nodegit'

export const setUsersDir = (name) => {
  usersDir = name
}

export const copyReadme = (where, handlerFn) => {
  // FIXME: make it work async
  fs.copySync(path.resolve('./ressource/readme.txt'), where + 'readme.txt')
  handlerFn()
}

const commit = (repo, filesToAdd) => {

  const author = git.Signature.create('StoreIt Admin',
  'admin@storeit.io', 123456789, 60)

  return repo.createCommitOnHead(filesToAdd, author, author, 'automatic commit')
}

export const addUser = (name, handlerFn) => {
  const userRepoPath = `${usersDir}/${name}/`
  git.Repository.init(userRepoPath, 0).then((repo) => {

    copyReadme(userRepoPath, () => {
      commit(repo, ['readme.txt']).then(() => {
        handlerFn(repo)
      }).catch(util.logerr)
    })
  }).catch(util.logerr)
}
/*
git.addConfig('user.name', 'StoreIt server')
.addConfig('user.email', 'admin@storeit.io')

export const addUser = (name, handlerFn) => {

  const repositoryPath = `${usersDir}${name}`

  try {
    fs.mkdir(repositoryPath, (err) => {
      log.ifnerr(err, 'cannot create user', 'mkdir success', () => {
        process.chdir(repositoryPath)
        git.init((err) => {
          log.ifnerr(err, 'cannot create user', 'successfully created user directory')
        })
      })
    })
  }
  catch (err) {
    console.log(err)
  }
}
*/

// what is a file json object
export const add = (what, handlerFn) => {
}
