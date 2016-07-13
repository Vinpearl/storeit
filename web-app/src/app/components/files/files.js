import angular from 'angular'

import FilesController from './files_controller.js'
import {html as template} from './files.jade!'
import './files.css!'

let filesComponent = {
  template,
  controller: FilesController,
  controllerAs: 'vm',
}

const DEPENDENCIES = []
export default angular.module('storeit.app.components.files', DEPENDENCIES)
  .component('filesView', filesComponent)
  .name
