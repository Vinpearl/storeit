package com.storeit.storeit.utils;

import android.content.Context;
import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.util.Log;

import com.google.gson.Gson;
import com.storeit.storeit.protocol.StoreitFile;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;

/**
 * Handle file creation and deletion
 */
public class FilesManager {
    private File mDataDir;
    private StoreitFile mRootFile;
    private static final String LOGTAG = "FilesManager";
    private String storageLocation;

    public FilesManager(Context ctx, StoreitFile rootFile) {

        SharedPreferences SP = PreferenceManager.getDefaultSharedPreferences(ctx);
        storageLocation = SP.getString("pref_key_storage_location", "");

        if (storageLocation.equals("")) {
            File path[] = ctx.getExternalFilesDirs(null);
            storageLocation = path[0].getAbsolutePath();
        }

        mDataDir = new File(storageLocation);


        File jsonFile = new File(storageLocation + "/storeit.json");
        if (!jsonFile.exists()) {
            Log.d(LOGTAG, "Creating root json file");
            try {
                if (!jsonFile.createNewFile()) {
                    Log.v(LOGTAG, "Error creating .storeit");
                }
                FileWriter fw = new FileWriter(jsonFile);
                Gson gson = new Gson();
                fw.write(gson.toJson(rootFile, StoreitFile.class));
                fw.close();
            } catch (IOException e) {
                e.printStackTrace();
            }

        } else {
            StoreitFile currentRoot;
            StringBuilder text = new StringBuilder();
            String line;

            try {
                BufferedReader br;
                br = new BufferedReader(new FileReader(jsonFile));
                while ((line = br.readLine()) != null) {
                    text.append(line);
                    text.append('\n');
                }

                Gson gson = new Gson();
                currentRoot = gson.fromJson(text.toString(), StoreitFile.class);
                compareRoot(currentRoot, rootFile);

                FileWriter fw = new FileWriter(jsonFile, false);
                fw.write(gson.toJson(rootFile, StoreitFile.class));
                fw.close();

            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        mRootFile = rootFile;
    }

    // Delete a directory and its content
    public static boolean deleteContents(File dir) {
        File[] files = dir.listFiles();
        boolean success = true;
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    success &= deleteContents(file);
                }
                if (!file.delete()) {
                    Log.e(LOGTAG, "Failed to delete " + file);
                    success = false;
                }
            }
        }
        return success;
    }

    // Recursively compare new tree with existing tree
    public void recursiveCmp(StoreitFile existingFile, StoreitFile newRoot) {

        if (!existingFile.getPath().equals("/storeit")) { // Don't delete root
            StoreitFile f = getFileByHash(existingFile.getIPFSHash(), newRoot); // Look for the actual file
            if (f == null) { // If the file doesn't exist anymore
                File fileToDelete = new File(mDataDir.getAbsolutePath() + File.separator + existingFile.getIPFSHash());
                if (fileToDelete.exists()) {
                    if (existingFile.isDirectory()) { // Delete directory
                        deleteContents(fileToDelete);
                    } else { // Delete file
                        if (!fileToDelete.delete()) {
                            Log.e(LOGTAG, "Error while deleting " + fileToDelete);
                        }
                    }
                }
            }
        }

        for (Map.Entry<String, StoreitFile> entry : existingFile.getFiles().entrySet()) {
            if (entry.getValue().isDirectory()) {
                recursiveCmp(entry.getValue(), newRoot);
            }
        }
    }

    public void compareRoot(StoreitFile currentRoot, StoreitFile newRoot) {
        recursiveCmp(currentRoot, newRoot);
    }

    public boolean exist(StoreitFile file) {

        File requestedFile = new File(mDataDir.getAbsolutePath() + File.separator + file.getIPFSHash());
        return requestedFile.exists();
    }

    public StoreitFile getRoot() {
        return mRootFile;
    }

    public String getFolderPath() {
        return mDataDir.getPath();
    }

    private StoreitFile recursiveSearch(String hash, StoreitFile root) {
        if (root.getIPFSHash().equals(hash))
            return root;

        for (Map.Entry<String, StoreitFile> entry : root.getFiles().entrySet()) {
            if (entry.getValue().getIPFSHash().equals(hash))
                return entry.getValue();
            else if (entry.getValue().isDirectory())
                recursiveSearch(hash, entry.getValue());
        }
        return null;
    }

    public StoreitFile getFileByHash(String hash, StoreitFile file) {
        return recursiveSearch(hash, file);
    }

    private StoreitFile getParentFile(StoreitFile root, String parentPath) {

        if (root.getPath().equals(parentPath)) {
            return root;
        }

        for (Map.Entry<String, StoreitFile> entry : root.getFiles().entrySet()) {
            if (entry.getValue().isDirectory()) {
                return getParentFile(entry.getValue(), parentPath);
            }
        }

        return null;
    }

    public void saveJson() {
        File jsonFile = new File(storageLocation + "/storeit.json");

        try {
            if (!jsonFile.exists()) {
                if (!jsonFile.createNewFile()) {
                    Log.v(LOGTAG, "Error creating .storeit");
                }
            }
            FileWriter fw = new FileWriter(jsonFile, false);
            Gson gson = new Gson();
            fw.write(gson.toJson(mRootFile, StoreitFile.class));
            fw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void removeFile(StoreitFile file) {
        File parentFile = new File(file.getPath());
        String parentPath = parentFile.getParentFile().getAbsolutePath();

        StoreitFile parent = getParentFile(mRootFile, parentPath);
        if (parent != null) {
            parent.getFiles().remove(file.getFileName());

            File fileToDelete = new File(mDataDir.getAbsolutePath() + File.separator + file.getIPFSHash());
            if (fileToDelete.exists()) {
                if (!fileToDelete.delete()) {
                    Log.e(LOGTAG, "Error while deleting " + fileToDelete);
                }
            }
            saveJson();
        }
    }

    public void addFile(StoreitFile file, StoreitFile parent) {
        StoreitFile p = getFileByHash(parent.getIPFSHash(), mRootFile);
        if (p != null) {
            p.addFile(file);
            saveJson();
        }

    }

    public void addFile(StoreitFile file) {

        File parentFile = new File(file.getPath());
        String parentPath = parentFile.getParentFile().getAbsolutePath();

        StoreitFile parent = getParentFile(mRootFile, parentPath);
        if (parent != null) {
            parent.addFile(file);
            saveJson();
        }
    }

    public void updateFile(StoreitFile file) {
        StoreitFile toUpdate = getFileByHash(file.getIPFSHash(), mRootFile);

        if (toUpdate != null) {
            toUpdate.setFiles(file.getFiles());
            toUpdate.setIsDir(file.isDirectory());
            toUpdate.setMetadata(file.getMetadata());
            toUpdate.setPath(file.getPath());
        }
    }
}
