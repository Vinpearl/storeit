package com.storeit.storeit.protocol;

/**
 * Created by loulo on 24/03/2016.
 */
public interface StoreitHandler {

    public void handleCHSEND(int send, String hash, String ip, int port);

}