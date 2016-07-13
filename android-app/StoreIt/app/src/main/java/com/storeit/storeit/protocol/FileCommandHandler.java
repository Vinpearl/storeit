package com.storeit.storeit.protocol;

import com.storeit.storeit.protocol.command.FileCommand;

/**
 * Created by loulo on 23/06/2016.
 */
public interface FileCommandHandler {

    public void handleFDEL(FileCommand command);
    public void handleFADD(FileCommand command);
    public void handleFUPT(FileCommand command);
}
