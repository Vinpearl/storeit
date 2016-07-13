pub enum Level {
    VERBOSE,
    DEBUG,
    INFO,
    WARN,
    ERROR
}

pub fn log(level: Level, msg: &str) {
    println!("log: {}", msg)
}

pub fn verbose(msg: &str) {
    log(Level::VERBOSE, msg)
}

pub fn debug(msg: &str) {
    log(Level::DEBUG, msg)
}

pub fn info(msg: &str) {
    log(Level::INFO, msg)
}

pub fn warn(msg: &str) {
    log(Level::ERROR, msg)
}

pub fn error(msg: &str) {
    log(Level::ERROR, msg)
}
