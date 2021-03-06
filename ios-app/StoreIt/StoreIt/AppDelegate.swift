//
//  AppDelegate.swift
//  StoreIt
//
//  Created by Romain Gjura on 14/03/2016.
//  Copyright © 2016 Romain Gjura. All rights reserved.
//

import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?
    
    var connectionType: ConnectionType? = nil
    var networkManager: NetworkManager? = nil
    var connectionManager: ConnectionManager? = nil
    var fileManager: FileManager? = nil
    var navigationManager: NavigationManager? = nil
    var ipfsManager: IpfsManager? = nil
    let plistManager: PListManager = PListManager()
    
    func application(application: UIApplication, didFinishLaunchingWithOptions launchOptions: [NSObject: AnyObject]?) -> Bool {
        let navigationController = self.window?.rootViewController as! UINavigationController
        let loginView = navigationController.viewControllers[0] as! LoginView

		loginView.connectionType = self.connectionType
        loginView.networkManager = self.networkManager
        loginView.connectionManager = self.connectionManager
        loginView.fileManager = self.fileManager
        loginView.ipfsManager = self.ipfsManager
        loginView.plistManager = self.plistManager
        
        return FBSDKApplicationDelegate.sharedInstance().application(application, didFinishLaunchingWithOptions: launchOptions)
    }

    func application(application: UIApplication, openURL url: NSURL, sourceApplication: String?, annotation: AnyObject) -> Bool {
        let navigationController = self.window?.rootViewController as! UINavigationController
        let loginView = navigationController.viewControllers[0] as! LoginView

        if (loginView.connectionType != nil
            && loginView.connectionType! == ConnectionType.GOOGLE) {
            loginView.connectionManager?.handleRedirectUrl(url)
        }
        else if (loginView.connectionType != nil
            && loginView.connectionType! == ConnectionType.FACEBOOK) {
            return FBSDKApplicationDelegate.sharedInstance().application(application, openURL: url, sourceApplication: sourceApplication, annotation: annotation)
        }
        return true
    }
    
    func applicationWillResignActive(application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and throttle down OpenGL ES frame rates. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(application: UIApplication) {
        // Called as part of the transition from the background to the inactive state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }


}

