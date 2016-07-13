extern crate time;
extern crate hyper;

use std;
use std::sync::{RwLock, RwLockReadGuard, RwLockWriteGuard};
use std::collections::HashMap;
use self::time::Tm;

use database;
use serialize;
use user;
use file;
use api;
use chunks;

pub struct User {
    pub ip : std::net::SocketAddr,
    pub database_id : i32,
    pub username : String,
    pub last_ping : Tm,
    pub root: serialize::File,
    pub http_port: String,
}

impl User {

    pub fn process_tree(&mut self,
                        sdata: &serialize::ServerData,
                        user_vision: &serialize::File) {

        let mut new_tree = self.root.clone();

        self.process_subtree(sdata, user_vision, &mut new_tree);
        self.root = new_tree;
    }

    fn process_subtree(&self,
                       sdata: &serialize::ServerData,
                       user_vision: &serialize::File,
                       server_vision: &mut serialize::File) {

        // TODO: use some hashmaps for files
        for file_u in user_vision.files.as_ref().unwrap() {

            let mut found = false;

            for file_s in server_vision.files.as_mut().unwrap().iter_mut() {
                if file_s.path == file_u.path {

                    if file_u.unique_hash != file_s.unique_hash {

                        // TODO: handle the case where a directory
                        // has been transformed into a file
                        if file_u.kind == 0 && file_s.kind == 0 {
                            self.process_subtree(sdata, file_u, file_s);
                        }

                        if {
                            let (who_is_most_recent, file_most_recent) =
                            file::get_most_recent(file_u, file_s);

                            api::update_file(&self,
                                             sdata,
                                             &who_is_most_recent,
                                             file_most_recent);

                            who_is_most_recent
                        } == file::Who::Server {

                            // TODO: do this only if the client responds OK
                            file_s.unique_hash = file_u.unique_hash.clone();
                        }

                    }
                    found = true;
                    break;
                }
            }

            if !found {
                api::add_file(self, sdata, &file::Who::Server, file_u);
                server_vision.files.as_mut().unwrap().push(file_u.clone());
            }
        }

        for ref file_s in server_vision.files.as_ref().unwrap() {

            let mut found = false;

            for ref file_u in user_vision.files.as_ref().unwrap() {
                if file_s.path == file_u.path {
                    found = true;
                    break;
                }
            }

            if !found {
                api::add_file(self, sdata, &file::Who::Client, file_s);
            }
        }

    }

    pub fn refresh_timestamp(&mut self) {
        println!("DEBUG: updating user {}'s timestamp", self.username);
        self.last_ping = time::now();
    }
}

pub struct Users {
    pub users_map : RwLock<HashMap<String, User>>,
}

impl Users {

    pub fn new() -> Users {
        Users {
            users_map: RwLock::new(HashMap::new())
        }
    }

    pub fn get_available_user<'a>(users: &'a HashMap<String, user::User>,
                                  without_chunk: &str,
                                  chunks: &chunks::Chunks)
        -> Option<&'a user::User> {

            for (_, user) in users.iter() {
                if !chunks.has_user_chunk(without_chunk, &user.username) {
                    return Some(&user);
                }
            }
            None
    }


    pub fn add(&self, user: User) {

        // don't unwrap in the future
        let mut guard = self.users_map.write().unwrap();

        // try maybe to use lifetimes instead of allocating a new string as key
        (*guard).insert(user.username.clone(), user);
    }

    pub fn remove(&self, username: &str) {

        let mut guard = self.users_map.write().unwrap();

        (*guard).remove(username);
    }

    pub fn exists(&self, username: &str) -> bool {
        let guard = self.get_read_guard();

        match (*guard).get(username) {
            None => false,
            Some(_) => true,
        }
    }

    pub fn get_read_guard(&self)
        -> RwLockReadGuard<HashMap<String, User>> {

            self.users_map.read().unwrap()
        }

    pub fn get_write_guard(&self)
        -> RwLockWriteGuard<HashMap<String, User>> {

            self.users_map.write().unwrap()
        }

    /* TODO: succeed this someday 
       pub fn get(&self, name: &str) -> Option<&'a User> {

       let mut guard : RwLockReadGuard<'a, _> = self.get_read_guard();

       let gotten = (*guard).get(name);
       gotten
       }
       */
}

pub fn make_new_user_from_db(request: &hyper::server::Request,
                             username: &str) -> Option<User> {

    let user: database::User = match database::get_user(username) {
        Some(u) => u,
        None => return None
    };

    println!("DEBUG: on server, user has tree: {}", user.file_tree);

    Some(User {
        ip: request.remote_addr,
        database_id: 42,
        username: username.to_string(),
        last_ping: self::time::now(),
        root: serialize::decode_tree(user.file_tree.as_ref()).unwrap(),
        http_port: "0".to_string(),
    })
}

pub fn credentials(request: &hyper::server::Request, users: &user::Users)
-> Option<String> {

    let auth_option
        : Option<&hyper::header::Authorization<hyper::header::Basic>>
        = request.headers.get();

    let (username, password) = match auth_option {
        None => {
            error!("User has no authentication in http header");
            return None;
        }
        Some(ref header) => {
            let password : &str = match header.password {
                None => {
                    error!("User {} has not entered a password", header.username);
                    return None;
                }
                Some(ref pass) => pass
            };
            (header.username.as_ref(), password)
        }
    };

    if users.exists(username) {
        return Some(String::from(username));
    }

    match database::get_user(username) {
        // TODO: check for password
        Some(_) => Some(String::from(username)),
        None => {
            error!("user {} doesn't exists in database", username);
            None
        }
    }
}
