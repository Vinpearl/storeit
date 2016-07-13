import 'angular-material/angular-material.css!'

import angular from 'angular'
import 'angular-animate'
import 'angular-aria'
import 'angular-material'
import 'ngComponentRouter'

import constants from './app/core/constants.js'
import app from './app/app.js'

let coreConfig = ($locationProvider) => {
  'ngInject'
  $locationProvider.html5Mode(false) // TODO
}

let run = ($rootScope) => {
  'ngInject'
  /* eslint no-unused-vars:"off" */
  // Promise.setScheduler(cb => $rootScope.$evalAsync(cb)) // FIXME
}

const DEPENDENCIES = [
  'ngComponentRouter',
  'ngMaterial',
  constants,
  app
]
let storeit = angular.module('storeit', DEPENDENCIES)
  .config(coreConfig)
  .run(run)
  .value('$routerRootComponent', 'app')

angular.element(document).ready(() => {
  let appContainer = document.getElementById('app-container')
  angular.bootstrap(appContainer, [storeit.name])
})

export default storeit
