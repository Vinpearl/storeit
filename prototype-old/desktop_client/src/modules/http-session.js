'use strict';
import request from 'request';
import Filetree from './file-tree';

export default class HttpSession
{
    // jscs:disable disallowAnonymousFunctions

    constructor()
    {
        this.connected = false;
        this.request = request.defaults({
            baseUrl: `http://${global.config.host}:${global.config.port}`,
            auth: {
                user: global.config.username,
                pass: global.config.password
            },
        });
    }

    join(filelist)
    {
        let url = `/session/join?port=${global.config.clientPort}`;
        this.post(url, filelist, (err, res) => {
            if (!err && res.statusCode === 200)
            {
                console.log('join success.');
                this.connected = true;
            }
            else
            {
                console.log('join fail:', err);
            }
        });
    }

    leave()
    {
        if (!this.connected)
            return;

        this.post('/session/leave', (err, res) => {
            if (!err && res.statusCode === 200)
            {
                console.log('Session closed with status');
                this.connected = false;
            }
            else
                console.log('leave fail');
        });
    }

    fileCreated(filename, stat)
    {
        this.fileUpdateSend('PUT', filename, stat);
    }

    fileChanged(filename, stat)
    {
        this.fileUpdateSend('POST', filename, stat);
    }

    fileUpdateSend(method, filename, stat)
    {
        let file = Filetree.makeFileInfo(filename, stat);
        let action = method === 'PUT' ? 'added' : 'updated';
        this.req(method, '/data/tree', file, (err, res) => {
            if (!err && res.statusCode === 200)
                console.log('file', filename, 'successfully', action);
            else // if error
            {
                let msg = `file ${filename} not ${action}.`;
                if (res.statusCode === 401)
                    console.error(msg, 'Storage full.');
                else // 409
                    console.error(msg, 'File already exists.');
            }
        });
    }

    fileRemoved(filename)
    {
        let data = {
            // jscs:disable requireCamelCaseOrUpperCaseIdentifiers
            file_path: filename
        };
        this.del('/data/tree', data, (res) => {
            console.log('file', filename, 'removed with code', res.statusCode);
        });
    }

    post(uri, data, cb)
    {
        this.req('POST', uri, data, cb);
    }

    put(uri, data, cb)
    {
        this.req('PUT', uri, data, cb);
    }

    del(uri, data, cb)
    {
        this.req('DELETE', uri, data, cb);
    }

    req(method, uri, data, cb)
    {
        let options = {
            method,
            uri
        };
        if (method === 'GET')
            return;
        else if (method === 'DELETE')
        {
            options.useQuerystring = true;
            options.qs = data;
        }
        else
        {
            options.json = true;
            options.body = data;
        }
        this.request(options, cb);
    }
}
