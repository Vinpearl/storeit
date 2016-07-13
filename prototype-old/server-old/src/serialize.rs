use rustc_serialize::json;
use std::sync::{Arc, RwLock};
use user;
use chunks;
use serialize;
use path;

/*
 * The json datastructures involved in the requests
 */
#[derive(RustcDecodable, RustcEncodable, Clone)]
#[derive(Debug)]
pub struct File {
    pub path : String,
    pub metadata : String,
    pub unique_hash : String,
    pub kind : i16,
    pub chunks_hashes : Option<Vec<String>>,

    //TODO: make it a hashmap with file name as a key
    pub files : Option<Vec<File>>,
}

impl File {

    fn append_to_dir(path: &mut[&str],
                     target_tree: &mut serialize::File,
                     add_tree: &serialize::File) -> bool
    {
        if path.len() <= 1 {
            println!("adding {} to {}", path[0], target_tree.path);
            true
        } else {

            match target_tree.files.as_mut() {
                None => false,
                Some(ref mut f) => {

                    for file in f.iter_mut() {

                        if path::get_file_name(&file.path) == path[0] {

                            match path.split_first_mut() {
                                None => {
                                    return false
                                }
                                Some(tpl) => {
                                  return File::append_to_dir(tpl.1, file, add_tree);
                                }
                            }
                        }
                    }
                    false
                }
            }
        }
    }

    pub fn add_file(&mut self, added_tree: &serialize::File) -> bool {

        let mut path = added_tree.path.split('/').collect::<Vec<&str>>();

        //let path = match path {
        //    None => {
        //        error!("a path {} was invalid", added_tree.path);
        //        return false;
        //    }
        //    Some(slice) => slice
        //};

        File::append_to_dir(&mut path, self, added_tree)
    }
}

// TODO: put in main
pub struct ServerData {
    pub users : Arc<user::Users>,
    pub chunks : RwLock<chunks::Chunks>,
}

pub fn decode_tree(json: &str) -> Result<File, json::DecoderError> {
    json::decode(json)
}

pub fn tree_to_json(tree: &File) -> Result<String, json::EncoderError> {
    json::encode(tree)
}

