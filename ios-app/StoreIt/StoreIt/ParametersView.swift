//
//  ParametersView.swift
//  StoreIt
//
//  Created by Romain Gjura on 16/06/2016.
//  Copyright © 2016 Romain Gjura. All rights reserved.
//

import Foundation


import UIKit

class ParametersView: UIViewController {
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        self.tabBarItem = UITabBarItem(title: "Paramètres", image: nil, tag: 2)
    }
}
