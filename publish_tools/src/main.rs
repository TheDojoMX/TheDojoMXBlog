use walkdir::WalkDir;
use std::thread;
use std::time::Duration;
use console::Term;



fn main() -> Result<T, E> {
    // list files in ../../_drafts folder
    let mut drafts = Vec::new();
    let term = Term::stdout();

    for entry in WalkDir::new("../_drafts") {
        let entry = entry.unwrap();
        if entry.file_type().is_file() {
            drafts.push(entry.path().to_str().unwrap().to_string());
        }
    }
    // print drafts
    for draft in drafts {
        term.write_line(&draft);
    }
    thread::sleep(Duration::from_millis(2000));
    term.clear_line()?;
}
