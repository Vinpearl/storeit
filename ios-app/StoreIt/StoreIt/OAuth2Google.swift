//
//  OAuth2Google2.swift
//  StoreIt
//
//  Created by Romain Gjura on 06/05/2016.
//  Copyright © 2016 Romain Gjura. All rights reserved.
//

import Foundation
import p2_OAuth2

class OAuth2Google : OAuth2 {
    
    private let oauth2: OAuth2CodeGrant
    
    init() {
        oauth2 = OAuth2CodeGrant(settings: [
                "client_id": "929129451297-scre09deafvcfip9tvkefoe590uenv9l.apps.googleusercontent.com",
                "authorize_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://www.googleapis.com/oauth2/v3/token",
                "scope": "profile email",
                "redirect_uris": ["com.googleusercontent.apps.929129451297-scre09deafvcfip9tvkefoe590uenv9l:/oauth-storeit"],
            ])
        onFailureOrAuthorizeAddEvents()
    }
    
    func authorize(context: AnyObject) {
  		oauth2.authorizeEmbeddedFrom(context)
    }
    
    func handleRedirectUrl(url: NSURL) {
        oauth2.handleRedirectURL(url)
    }
    
    func forgetTokens() {
        oauth2.forgetTokens()
    }
    
    func onFailureOrAuthorizeAddEvents() {
        let appDelegate = UIApplication.sharedApplication().delegate as! AppDelegate
        let navigationController = appDelegate.window?.rootViewController as! UINavigationController
        let loginView = navigationController.viewControllers[0] as! LoginView

        oauth2.onAuthorize = { parameters in
            print("[ConnexionManager] Did authorize with parameters: \(parameters)")
            
            loginView.initConnection(loginView.host, port: loginView.port, path: "/Users/gjura_r/Desktop/demo/", allItems: [:])
            
            while (loginView.networkManager?.isConnected() == false) {
                usleep(1)
            }
            
            loginView.networkManager?.join("gg", accessToken: self.oauth2.accessToken!, completion: nil)
            loginView.performSegueWithIdentifier("StoreItSynchDirSegue", sender: nil)
        }
        oauth2.onFailure = { error in
            if let error = error {
                print("[ConnexionManager] Authorization failure: \(error)")
                
                loginView.logout()
            }
        }
    }
    
}