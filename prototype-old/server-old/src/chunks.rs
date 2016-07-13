use std::collections::HashMap;

// table de hash  : clef chunk-> value list<client>
// table de hash  : clef client -> value list<chunk>

pub struct Chunks {
    chunk_map : HashMap<String, Vec<String>>,
    user_map: HashMap<String, Vec<String>>
}

impl Chunks {
    pub fn new() -> Chunks {
        Chunks {
            chunk_map: HashMap::new(),
            user_map: HashMap::new()
        }
    }

    pub fn add_user(& mut self, username : &str, hash_vec : Vec<String>) {

        // If user doesn't exist create blank vec
        if !self.user_map.contains_key(username){
            self.user_map.insert(username.to_string(), hash_vec.clone());
        }
        else {
            // else copy all the hashes
            *self.user_map.get_mut(username).unwrap() = hash_vec.clone();
        }


        for hash in hash_vec{

            let h = hash.clone();
            // If chunk map doesn't contain the current hash, create empty vec
            if !self.chunk_map.contains_key(&hash) { 
                // If chunk map doesn't contain the current hash, create empty vec
                self.chunk_map.insert(hash, Vec::new());
            }
            // Add the user for this hash
            self.chunk_map.get_mut(&h).unwrap().push(username.to_string());
        }
    }

    //pub fn get_chunk_owners(&self, chunk: &str) -> Option<Vec<


    pub fn get_chunk_owners_names(&mut self, chunk : &str) -> Option<Vec<String>>{
        match self.chunk_map.get(chunk) {
            Some(c) => Some(c.to_owned()),
            None => None
        }
    }

    pub fn has_user_chunk(&self, chunk: &str, username: &str) -> bool {

        let users = self.chunk_map.get(chunk);

        match users {
            None => return false,
            Some(us) => {
                for user in us {
                    if user == username {
                        return true;
                    }
                }
            }
        }

        false
    }

    pub fn add_chunk_for_user(& mut self, username : &str, chunk : &str) {

        // chunk isn't already registered, add it
        if !self.chunk_map.contains_key(chunk) {
            self.chunk_map.insert(chunk.to_string(), Vec::new());
        }

        // Add user to chunk
        self.chunk_map.get_mut(chunk).unwrap().push(username.to_string());

        // Add chunk to user
        self.user_map.get_mut(username).unwrap().push(chunk.to_string());
    }

    //pub fn remove_chunk_for_user(& mut self, username: &str, chunk : &str){

    //}

    pub fn remove_user(&mut self, username: &str){
        if self.user_map.contains_key(username)
        {
            {
                // Get list of chunk for user
                let chunk_vec = self.user_map.get(username).unwrap();

                for chunk in chunk_vec {
                    // Get the index of the chunk in the list of chunk
                    let index = self.chunk_map.get(chunk).unwrap().iter().position(|usr| *usr == username).unwrap();
                    // Remove the chunk thanks to the index
                    self.chunk_map.get_mut(chunk).unwrap().remove(index);

                    // If the user was the last owner, remove the chunk from the chunk map
                    if self.chunk_map.get(chunk).unwrap().is_empty() {
                        self.chunk_map.remove(chunk);                   
                    }
                }
            }
            // Remove user from user map
            self.user_map.remove(username);
        }
    }

    pub fn remove_chunk(& mut self, chunk: &str){
        if self.chunk_map.contains_key(chunk){
            {
                // Get list of chunk owners
                let user_vec = self.chunk_map.get(chunk).unwrap();

                for user in user_vec {
                    // Get the index of the user in the list of users
                    let index = self.user_map.get(user).unwrap().iter().position(|c| *c == chunk).unwrap();
                    // Remove the user
                    self.user_map.get_mut(user).unwrap().remove(index);

                    // if the user doesn't have anymore chunk, delete it
                    if self.user_map.get(user).unwrap().is_empty() {
                        self.user_map.remove(user);
                    }
                }
            }
            // Remove chunk from chunk map
            self.chunk_map.remove(chunk);
        }
    }
}


// Todo : create a test module with a test directory

#[test]
fn test_chunk_manager() {

    let mut chunks_manager = Chunks::new();

    chunks_manager.add_user("adrien".to_string(), vec!["123456789".to_string(), "789ez0".to_string()].clone());
    chunks_manager.add_user("romain".to_string(), vec!["123456789".to_string(), "787dsd851".to_string()].clone());
    chunks_manager.add_user("alex".to_string(), vec!["123456789".to_string(), "5641azesd2".to_string()].clone());    
    chunks_manager.add_user("louis".to_string(), vec!["123456789".to_string(), "1234a56".to_string()].clone());


    match chunks_manager.get_chunk_owners("123456789".to_string()) {
        Some(chunks) => {
            print!("owners of [123456789] : ");
            for c in chunks {
                println!("DEBUG: {}", c);
            }
        },
        None => {
            println!("DEBUG: No chunks...");
        }
    }

    chunks_manager.add_chunk_for_user("louis".to_string(), "trololol".to_string());
    match chunks_manager.get_chunk_owners("trololol".to_string()) {
        Some(chunks) => {

            for c in chunks {
                println!("DEBUG: {}", c);
            }
        },
        None => {
            println!("DEBUG: No chunks...");
        }        
    }

    chunks_manager.remove_user("louis".to_string());
    match chunks_manager.get_chunk_owners("trololol".to_string()) {
        Some(chunks) => {
            for c in chunks {
                println!("DEBUG: ici {}", c);
            }
        },
        None => {
            println!("DEBUG: No chunks...");
        }        
    }  

    chunks_manager.remove_chunk("123456789".to_string());
    match chunks_manager.get_chunk_owners("123456789".to_string()) {
        Some(chunks) => {
            println!("DEBUG: la");
            for c in chunks {
                println!("DEBUG: ici {}", c);
            }
        },
        None => {
            println!("DEBUG: No chunks...");
        }        
    }
}
