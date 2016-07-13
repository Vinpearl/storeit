import hello from 'hellojs'

export default class AuthController
{
  constructor(Facebook, Auth) {
    'ngInject'

    this.facebook = Facebook
    this.auth = Auth
    hello.on('auth.login', () => this.getProfile('facebook'))
  }

  login(profile) {
    console.log(profile) // TODO
    this.auth.login()
      .then(() => this.$router.navigate(['FileExplorer']))
      .catch(err => console.error(err))
  }

  oauth(network) {
    this[network].login()
  }

  getProfile(network) {
    this[network].api('/me').then((res) => this.login(res))
  }
}
