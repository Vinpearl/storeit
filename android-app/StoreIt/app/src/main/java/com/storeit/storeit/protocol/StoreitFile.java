package com.storeit.storeit.protocol;

import android.net.Uri;
import java.io.File;
import java.util.HashMap;

/**
 * StoreIt file object
 * Will be generated by the FileManager :D
 */
public class StoreitFile {

    private String path;
    private String IPFSHash;
    private String metadata;
    private boolean isDir;
    private HashMap<String, StoreitFile> files;

    public StoreitFile(String path, String IPFSHash, boolean isDir) {
        this.path = path;
        this.IPFSHash = IPFSHash;
        this.isDir = isDir;
        this.metadata = "";
        this.files = new HashMap<>();
    }

    public String getPath() {
        return path;
    }

    public String getFileName(){
        File file = new File(path);
        return file.getName();
    }

    public HashMap<String, StoreitFile> getFiles() {
        return files;
    }

    public void addFile(StoreitFile file) {
        Uri uri = Uri.parse(file.getPath());
        this.files.put(uri.getLastPathSegment(), file);
    }

    public String getIPFSHash() {
        return IPFSHash;
    }

    public String getMetadata(){
        return metadata;
    }

    public boolean isDirectory() {
        return isDir;
    }

    public void setIsDir(boolean isDir) {
        this.isDir = isDir;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public void setIPFSHash(String IPFSHash) {
        this.IPFSHash = IPFSHash;
    }

    public void setMetadata(String metadata) {
        this.metadata = metadata;
    }

    public void setFiles(HashMap<String, StoreitFile> files) {
        this.files = files;
    }
}
