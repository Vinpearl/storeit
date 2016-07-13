//
//  PListManager.swift
//  StoreIt
//
//  Created by Romain Gjura on 17/06/2016.
//  Copyright © 2016 Romain Gjura. All rights reserved.
//

import Foundation
import Plist

class PListManager {
    
    private var plist: Plist?
    private let path: String
    
    init() {
		
        let rootPath = NSSearchPathForDirectoriesInDomains(NSSearchPathDirectory.DocumentDirectory, .UserDomainMask, true)[0]
        let plistPathInDocument = rootPath.stringByAppendingString("/storeit_data.plist")
        let fileManager = NSFileManager.defaultManager()
        
        if (!fileManager.fileExistsAtPath(plistPathInDocument)){
            plist = nil
            
        } else {
            plist = Plist(path: plistPathInDocument)
        }
        
        self.path = plistPathInDocument
    }
    
    func addValueForKey(key: String, value: String) {
        let data: NSMutableDictionary
        
        if (plist != nil) {
        	data = NSMutableDictionary(contentsOfFile: self.path)!
        } else {
            data = NSMutableDictionary()
        }
        
        data.setObject(value, forKey: key)
        data.writeToFile(path, atomically: true)
        self.plist = Plist(path: path)
	}
    
    func getValueWithKey(key: String) -> String {
        return self.plist?[key].string ?? "None"
    }
}
