use serialize;

#[derive(PartialEq)]
pub enum Who {
    Server,
    Client,
}

/*
 * returns the most recently modified file, and if it is on the server
 * metadata or in the client tree
 */
pub fn get_most_recent<'a>(user:   &'a serialize::File,
                           server: &'a serialize::File)
    -> (Who, &'a serialize::File) {

        // TODO: don't unwrap
        let timestamp_user = user.metadata.parse::<i32>().unwrap();
        let timestamp_server = server.metadata.parse::<i32>().unwrap();

        // TODO: metadata shoud become timestamp
        // TODO: handle conflict when timestamps are exactly the same
        if timestamp_user < timestamp_server {
            (Who::Server, server)
        } else {
            (Who::Client, user)
        }
}
