use std::env;
use std::io;
use std::io::prelude::*;
use std::fs::File;
use std::collections::HashMap;

fn main() {
    // read in file name and n
    let mut argv = env::args();
    let usage = format!("USAGE: ./{} {{file_name}} {{top_n_words}}", argv.next().unwrap());
    let fname: String = argv.next().expect(&usage);
    let n_str: String = argv.next().expect(&usage);
    let parse_int_err = format!("Failed to parse arg '{}' to an int", n_str);
    let n: usize = n_str.parse::<usize>().ok().expect(&parse_int_err);

    // read in file
    let file_open_err = format!("Failed to open {}", fname);
    let file = File::open(&fname)
                    .ok()
                    .expect(&file_open_err);
    let freader = io::BufReader::new(&file);

    // break file into words
    let lines: Vec<String> = freader.lines()
        .map(|line_result| line_result.ok().unwrap())
        .collect();
    let words = lines.iter()
        .flat_map(|line| line.split(" "))
        .filter(|word| !word.is_empty())
        .map(|word| word.to_string());

    // count words
    let mut word_count: HashMap<String, i32> = HashMap::new();
    for i in words {
        let count = word_count.entry(i).or_insert(0);
        *count += 1;
    }

    // Sort mapping
    let mut pairs: Vec<(&String, &i32)> = word_count.iter().collect();
    pairs.sort_by(|a, b| b.1.cmp(a.1));

    // Output top n
    if pairs.len() < n {
            println!("NOTE: File has fewer than {} unique words.", n);
            println!("      Only able to display {} words.", pairs.len());
    }
    for (num, pair) in pairs.iter().enumerate() {
        if num >= n {
            break;
        }
        println!("{}", pair.0)
    }
}
