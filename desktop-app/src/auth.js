import google from 'googleapis'
import openurl from 'openurl'
import {logger} from './log.js'

let OAuth2 = google.auth.OAuth2

let oauth2Client = new OAuth2('880343271906-mjgljqga240f6sfckbnvh5c86vn9mg7r.apps.googleusercontent.com', 'Gcz-w3sC-UXzI_WyVVMiKzYy', 'http://iglu.mobi')

export let googleAuth = () => {
  let url = oauth2Client.generateAuthUrl({
    scope: 'email'
  })

  openurl.open(url)
}

export let getGoogleToken = (code, callback) => {

  oauth2Client.getToken(code, (err, tokens) => {
  // Now tokens contains an access_token and an optional refresh_token. Save them.

    if(!err) {
      callback(tokens)
    }
    else {
      logger.error(err)
    }
  })
}
