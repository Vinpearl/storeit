package com.storeit.storeit.protocol.command;

/**
 * Created by loulo on 21/06/2016.
 */
public class JoinCommand {
    int uid;
    String command;
    Parameters parameters;

    public JoinCommand(int uid, String authType, String accessToken){
        this.uid = uid;
        this.command = "JOIN";
        this.parameters = new Parameters(authType, accessToken);
    }

    class Parameters{
        String authType;
        String accessToken;

        public Parameters(String authType, String accessToken){
            this.authType = authType;
            this.accessToken = accessToken;
        }
    }
}
