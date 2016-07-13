'use strict';
import * as crypto from 'crypto';
import * as fs from 'fs';
import * as path from 'path';

const CHUNK_SIZE = 10 * 1024 * 1024; // 10MB
const FILE_TYPES = {
    directory: 0,
    regular: 1,
    link: 2
};
const HASH_FMT = {
    type: 'sha256',
    enc: 'hex'
};

class BasicFileModel
{
    // jscs:disable disallowAnonymousFunctions

    constructor(filePath, parentDir=null)
    {
        let relPath = path.relative(global.config.root, filePath);
        this.data = {
            // jscs:disable requireCamelCaseOrUpperCaseIdentifiers
            path: './' + relPath.replace(/\\/g, '/'),
            metadata: '',
            unique_hash: '',
            kind: null,
            chunks_hashes: [],
            files: []
        };
        this.absPath = filePath;
        this.parentDir = parentDir;
    }


    hashDigest(hash)
    {
        // jscs:disable requireCamelCaseOrUpperCaseIdentifiers
        this.data.unique_hash = hash.digest(HASH_FMT.enc);
    }

    printLast()
    {
        console.log('chunk hash:', this.data.chunks_hashes.slice(-1)[0]);
    }

    parentHashUpdate()
    {
        // jscs:disable requireCamelCaseOrUpperCaseIdentifiers
        if (this.parentDir) this.parentDir.hashUpdate(this.data.unique_hash);
    }

    get()
    {
        return this.data;
    }
}

export class FileModel extends BasicFileModel
{
    // jscs:disable disallowAnonymousFunctions

    constructor(filePath, parentDir)
    {
        super(filePath, parentDir);
        this.data.kind = FILE_TYPES.regular;
    }

    hashCalculate()
    {
        return new Promise((resolve) =>
        {
            let fd = fs.createReadStream(this.absPath);
            let hash = crypto.createHash(HASH_FMT.type);

            fd.on('end', () => {
                this.hashDigest(hash);
                this.parentHashUpdate();
                resolve();
            });

            fd.on('readable', () => {
                let chunk = null;
                while ((chunk = fd.read(CHUNK_SIZE)) !== null)
                {
                    this.chunkAdd(chunk);
                    hash.update(chunk);
                }
            });
        });
    }

    chunkAdd(chunk)
    {
        // jscs:disable requireCamelCaseOrUpperCaseIdentifiers
        let chunkHash = crypto.createHash(HASH_FMT.type)
            .update(chunk).digest(HASH_FMT.enc);
        this.data.chunks_hashes.push(chunkHash);
    }
}

export class DirModel extends BasicFileModel
{
    // jscs:disable disallowAnonymousFunctions

    constructor(filePath, parentDir)
    {
        super(filePath, parentDir);
        this.data.kind = FILE_TYPES.directory;
        this.hash = crypto.createHash(HASH_FMT.type);
    }

    hashCalculate()
    {
        return new Promise((resolve) =>
        {
            let files = fs.readdirSync(this.absPath);
            const nbFiles = files.length;
            if (nbFiles === 0)
                resolve();

            let count = 0;
            for (let filename of files)
            {
                this.entryParse(filename).then(() =>
                {
                    if (++count === nbFiles)
                    {
                        this.hashDigest(this.hash);
                        this.parentHashUpdate();
                        resolve();
                    }
                });
            }
        });
    }

    entryParse(filename)
    {
        let absPath = path.join(this.absPath, filename);

        let stats = fs.lstatSync(absPath);
        let entry = null;
        if (stats.isDirectory())
            entry = new DirModel(absPath, this);
        else
            entry = new FileModel(absPath, this);
        this.data.files.push(entry.get());
        return entry.hashCalculate();
    }

    hashUpdate(data)
    {
        // console.log('data', data);
        this.hash.update(data);
    }
}
