import angular from 'angular'

import FileExplorerController from './file_explorer_controller.js'
import FilesService from './files_service.js'
import {html as template} from './file_explorer.jade!'
import './file_explorer.css!'

let fileExplorerComponent = {
  template,
  controller: FileExplorerController,
  controllerAs: 'vm',
}

const DEPENDENCIES = []
export default angular.module('storeit.app.file-explorer', DEPENDENCIES)
  .service('FilesService', FilesService)
  .component('fileExplorer', fileExplorerComponent)
  .name
