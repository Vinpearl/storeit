'use strict';
import express from 'express';

export default class HttpListener
{
    // jscs:disable disallowAnonymousFunctions

    constructor()
    {
        this.router = express();
        this.routesDefine();
        this.listening = false;
        this.port = global.config.clientPort;
    }

    start()
    {
        this.server = this.router.listen(this.port);
        this.server.on('listening', () => {
            this.listening = true;
            this.host = this.server.address().address;
            this.port = this.server.address().port;

            console.log('storeit client listening at http://%s/%s',
                this.host, this.port);
        });
        this.server.on('error', () => {
            ++this.port;
            console.log('port %s busy, trying %s', this.port - 1, this.port);
            this.start();
        });
    }

    stop()
    {
        if (this.listening)
        {
            this.server.close();
            console.log('storeit client closed connection');
        }
    }

    routesDefine()
    {
        this.router.get('/session/ping', this.getPing.bind(this));
        this.router.delete('/data/store', this.deleteStore.bind(this));
        this.router.post('/data/store', this.postStore.bind(this));
        this.router.put('/data/store', this.putStore.bind(this));
        this.router.delete('/data/tree', this.deleteTree.bind(this));
        this.router.post('/data/tree', this.postTree.bind(this));
        this.router.put('/data/tree', this.putTree.bind(this));
    }

    getPing(req, res)
    {
        res.end();
    }

    deleteStore(req, res)
    {
        res.status(500).send({error: 'DELETE /data/store: not implemented'});
    }

    postStore(req, res)
    {
        res.status(500).send({error: 'POST /data/store: not implemented'});
    }

    putStore(req, res)
    {
        res.status(500).send({error: 'PUT /data/store: not implemented'});
    }

    deleteTree(req, res)
    {
        res.status(500).send({error: 'DELETE /data/tree: not implemented'});
    }

    postTree(req, res)
    {
        res.status(500).send({error: 'POST /data/tree: not implemented'});
    }

    putTree(req, res)
    {
        res.status(500).send({error: 'PUT /data/tree: not implemented'});
    }
}
