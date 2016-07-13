import angular from 'angular'

import auth from '../components/auth/auth.js'
import files from '../components/files/files.js'

const COMPONENTS = [
  auth,
  files,
]

export default angular.module('storeit.app.components', COMPONENTS).name
