use walkdir::WalkDir;
use std::thread;
use std::time::Duration;
use console::Term;


// main function walks _drafts directory and prints out the file names
fn main() {
    let term = Term::stdout();
    let mut count = 0;
    let mut files = Vec::new();
    for entry in WalkDir::new("../_drafts") {
        let entry = entry.unwrap();
        if entry.path().is_file() {
            files.push(entry.path().to_str().unwrap().to_string());
        }
    }
    loop {
        term.clear_screen().unwrap();
        term.write_line(&format!("{} files found", files.len())).unwrap();
        for file in &files {
            term.write_line(&format!("{}: {}", count, file)).unwrap();
            count += 1;
        }
        thread::sleep(Duration::from_secs(1));
    }
}