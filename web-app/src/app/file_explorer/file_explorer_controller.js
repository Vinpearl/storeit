export default class FileExplorerController {
  constructor(FilesService, $scope) {
    'ngInject'

    this.scope = $scope
    FilesService.getFiles()
      .then((files) => {
        console.log(files)
        this.path = []
        this.root = {files}
        this.cwd = {files}
        this.scope.$apply()
      })
  }

  action(index) {
    let target = this.cwd.files[index]
    if (target.kind === 'dir') {
      this.cd(target)
    }
  }

  cd(dest) {
    this.path.push(this.cwd)
    this.cwd = dest
    console.log('path', this.path)
  }

  parent() {
    let prev = this.path.pop()
    this.cwd = prev
  }
}
