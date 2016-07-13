'use strict';
import * as fs from 'fs';

export default class ChunksManager
{
    // jscs:disable disallowAnonymousFunctions

    constructor()
    {
        this.chunks = new Map([
            ['c945', {path:'/toto'}],
            ['5e46', {path:'/tata'}],
        ]);
    }

    addChunk(chunk)
    {
        this.chunks.push(chunk);
    }

    removeChunk(hash)
    {
        fs.unlink(this.chuncks.get(hash), (err) => {
            if (!err)
                console.log('chunk', hash, 'deleted.');
        });
    }

    getChunk(hash)
    {
        let chunk = this.chuncks.get(hash);
        return chunk;
    }
}
