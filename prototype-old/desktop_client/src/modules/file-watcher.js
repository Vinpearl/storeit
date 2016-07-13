'use strict';
import * as watch from 'watch';

export default class FileWatcher
{
    // jscs:disable disallowAnonymousFunctions

    constructor(callbacks)
    {
        this.rootDir = global.config.root;
        this.callbacks = callbacks;
        this.monitor = null;
    }

    start()
    {
        watch.createMonitor(this.rootDir, (monitor) => {
            // console.log('watching test:', global.config);
            this.monitor = monitor;
            for (let [ev, func] of this.callbacks)
            {
                this.monitor.on(ev, func);
            }
        });
    }

    stop()
    {
        if (this.monitor)
        {
            this.monitor.stop();
        }
    }
}
