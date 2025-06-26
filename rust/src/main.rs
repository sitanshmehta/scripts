use std::fs;
use std::fs::{File, OpenOptions};
use std::io;
use std::io::Read;
use std::os::unix;
use std::path::Path;

fn cat(path: &Path) -> io::Result<String> {
    let mut f = File::open(path)?;
    let mut s = String::new();
    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
}

fn main() {
    println!("Hello, world!");
}
