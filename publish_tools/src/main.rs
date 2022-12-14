use walkdir::WalkDir;

fn main() {
    // list files in ../../_drafts folder
    let mut drafts = Vec::new();
    for entry in WalkDir::new("../_drafts") {
        let entry = entry.unwrap();
        if entry.file_type().is_file() {
            drafts.push(entry.path().to_str().unwrap().to_string());
        }
    }
    // print drafts
    for draft in drafts {
        println!("{}", draft);
    }
}
