//
//  StoreItNavigationController.swift
//  StoreIt
//
//  Created by Romain Gjura on 16/06/2016.
//  Copyright © 2016 Romain Gjura. All rights reserved.
//

import UIKit

class StoreItNavigationController: UINavigationController {
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        
        self.tabBarItem = UITabBarItem(title: "Mes fichiers et dossiers", image: nil, tag: 0)
    }
    
}