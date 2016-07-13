pub fn get_file_name(path: &str) -> String {


    let slash_idx = match path.rfind('/') {
        Some(idx) => idx,
        None => return path.to_string()
    };

    let (_, filename) = path.split_at(slash_idx);

    filename.to_string()
}
