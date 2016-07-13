extern crate std;
extern crate hyper;
extern crate time;

use user;
use http;
use serialize;
use file;
use database;

use hyper::Client;
use std::thread;
use std::sync::{Arc, RwLock, RwLockReadGuard};
use std::vec::Vec;

// time between each ping sent to a user in seconds
static PING_TIME : u32 = 5000;

/* user opening a session */
pub fn connect_user(username: &str,
                    request: &hyper::server::Request,
                    user_vision: &serialize::File,
                    client_port: &str,
                    sdata: &serialize::ServerData) {

    {
        let mut guard = sdata.chunks.write().unwrap();
        (*guard).add_user(username, Vec::new());
    }

    let mut user = user::make_new_user_from_db(request, username).unwrap();
    user.http_port = client_port.to_string();
    user.process_tree(sdata, user_vision);
    println!("DEBUG: at end of sync, user has tree on server: {:?}", user.root);
    database::save_tree_for_user(&user.username, &user.root);
    println!("DEBUG: user {} has synced and been added", &user.username);

    sdata.users.add(user);
}

fn ping_failure(user: &user::User, dead: &mut Vec<String> ) {

    error!("{} failed the ping test", user.username);

    warn!("ping test temporarily removed");

    // later, do not allocate
    dead.push(String::from(user.username.as_ref()));
}

fn send_ping(users: &user::Users) {


    let mut dead_users = vec!();

    {
        // please don't unwrap this
        // in the future, optimise by only reading first, and then writing
        let mut guard = users.users_map.write().unwrap();

        for user_tuple in &mut *guard {
            println!("DEBUG: sending ping to user: {}", user_tuple.0);

            // TODO: use IpAddr when not nightly anymore
            match http::get(&user_tuple.1.ip, "/session/ping", &user_tuple.1.http_port) {
                Err(e)      => {
                    println!("ERROR: {:?}", e);
                    ping_failure(&user_tuple.1, &mut dead_users);
                }
                Ok(res) =>
                    if res.status != hyper::status::StatusCode::Ok {
                        ping_failure(&user_tuple.1, &mut dead_users);
                    } else {
                        user_tuple.1.refresh_timestamp();
                    }
            }
        }
    }


    for name in dead_users {
        users.remove(&name);
        println!("DEBUG: {} was disconnected", name);
    }
}

pub fn handle_ping(users: Arc<user::Users>) -> thread::JoinHandle<()> {

    let child = thread::spawn(move || {

        loop {

            // is a copy of users done here ?
            send_ping(&*users);
            std::thread::sleep_ms(PING_TIME);
        }
    });

    child
}

fn build_chunk_json(chunk: &str, ip: &str) -> String {

    "{\"chunk_hash\":".to_string() + chunk + "\",\"ip_address\":" + ip + "}"
}


pub fn delete_chunk(user: &user::User, chunk: &str) {
    // TODO
    //http::delete
}

pub fn send_chunk(from: &user::User, to: &user::User, chunk: &str,
                  sdata: &serialize::ServerData) {

    println!("DEBUG: sending chunk {} from {} to {}",
             chunk, from.username, to.username);

    http::post(&to.ip,
               "/data/store?send=0",
               &build_chunk_json(chunk, &to.ip.to_string()),
               &to.http_port);

    // TODO: wait for response before this
    {
        let mut guard = sdata.chunks.write().unwrap();
        (*guard).add_chunk_for_user(&to.username, chunk);
    }

    http::post(&from.ip,
               "/data/store?send=1",
               &build_chunk_json(chunk, &from.ip.to_string()),
               &from.http_port);
}

pub fn host_chunk(user: &user::User,
                  sdata: &serialize::ServerData,
                  chunk: &str,
                  redundancy: i8) {

    let guard_users = (*sdata.users).users_map.read().unwrap();

    for i in 0..redundancy {

        let storing_user: &user::User = {

            let guard_chunks = sdata.chunks.read().unwrap();

            match user::Users::get_available_user(&*guard_users,
                                                  chunk,
                                                  &*guard_chunks) {
                Some(u) => u,
                None => {
                    println!("WARN: couldn't find enough users ({} red).", redundancy);
                    break;
                }
            }
        };


        send_chunk(user, storing_user, chunk, sdata);
    }

}

pub fn add_file(user: &user::User,
                sdata: &serialize::ServerData,
                who: &file::Who,
                file: &serialize::File) {

    match who {
        &file::Who::Server => {
            println!("DEBUG: server has registered a new file ({})",
            &file.path); 

            // TODO: handle directory stuff

            {
                let mut guard = sdata.chunks.write().unwrap();
                (*guard).add_chunk_for_user(&user.username, &file.unique_hash);
            }

            host_chunk(user, sdata, &file.unique_hash, 3);
        }
        &file::Who::Client => {
            // TODO: if it fails, we should try it again until it succeeds
            http::post(&user.ip,
                       "/data/tree",
                       &serialize::tree_to_json(file).unwrap(),
                       &user.http_port).unwrap();
        }
    }
}

pub fn remove_file(user: &user::User,
                   sdata: &serialize::ServerData,
                   who: &file::Who,
                   file: &serialize::File) {
    match who {
        &file::Who::Server => {
            println!("DEBUG: server has deleted a file");
        }
        &file::Who::Client => {
            // TODO
        }
    }
}

pub fn update_file(user: &user::User,
                   sdata: &serialize::ServerData,
                   who: &file::Who,
                   file: &serialize::File) {

    match who {
        &file::Who::Server => {
            println!("DEBUG: server noticed file update")
        }
        &file::Who::Client => {
            http::put(&user.ip,
                      "/data/tree",
                      &serialize::tree_to_json(file).unwrap(),
                      &user.http_port,
                      ).unwrap();
        }
    }
}

