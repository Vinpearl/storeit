package com.storeit.storeit.protocol.command;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

/**
 * Created by loulo on 02/05/2016.
 */
public class CommandManager {

    public final static int JOIN = 0, FDEL = 1, FADD = 2, FUPT = 3;
    private static final String[] cmds = {
            "JOIN",
            "FDEL",
            "FADD",
            "FUPT"
    };

    public static int getCommandType(String cmd) {

        JsonParser parser = new JsonParser();
        JsonObject obj = parser.parse(cmd).getAsJsonObject();

        String cmdType = obj.get("command").getAsString();

        for (int i = 0; i < cmds.length; i++){
            if (cmdType.equals(cmds[i]))
                return i;
        }

        return -1;
    }
}
