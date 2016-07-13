import angular from 'angular'

const STOREIT = {
  facebookId: '615629721922275',
  googleId: ''
}

export default angular.module('storeit.constants', [])
  .constant('STOREIT', STOREIT)
  .name
