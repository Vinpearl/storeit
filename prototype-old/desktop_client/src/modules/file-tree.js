'use strict';
import * as fs from 'fs';

import FileWatcher from './file-watcher';
import {DirModel} from './file-models';

export default class FileTree
{
    // jscs:disable disallowAnonymousFunctions

    constructor(watchCallbacks)
    {
        this.list = [];
        this.watcher = new FileWatcher(watchCallbacks);
    }

    init()
    {
        let root = new DirModel(global.config.root);
        this.list = root.get();
        return root.hashCalculate();
    }

    watch()
    {
        this.watcher.start();
    }

    unwatch()
    {
        this.watcher.stop();
    }

    static fileExists(path)
    {
        try
        {
            fs.accessSync(path, fs.R_OK | fs.W_OK);
        }
        catch (e)
        {
            return false;
        }
        return true;
    }
}
