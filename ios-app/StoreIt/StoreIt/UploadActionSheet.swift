//
//  AlertControllerManager.swift
//  StoreIt
//
//  Created by Romain Gjura on 25/05/2016.
//  Copyright © 2016 Romain Gjura. All rights reserved.
//

import UIKit

class UploadActionSheet {
    
    let uploadActionSheet: UIAlertController
    
    init(title: String, message: String?) {
        self.uploadActionSheet = UIAlertController(title: title, message: message, preferredStyle: .ActionSheet)
    }
    
    func addActionToUploadActionSheet(title: String, style: UIAlertActionStyle, handler: ((UIAlertAction) -> Void)?) {
        let newAction: UIAlertAction = UIAlertAction(title: title, style: style, handler: handler)
        self.uploadActionSheet.addAction(newAction)
    }
}