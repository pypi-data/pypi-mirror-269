extern crate unidecode;
use pyo3::prelude::*;
use unidecode::unidecode;
extern crate rayon;
use std::collections::HashMap;
use std::collections::HashSet;
use rayon::prelude::*;

#[derive(Debug)]
/// The ```ClosestMatch``` struct stores informations about the dictionary of known words
/// and the different sizes for the bags of words.
pub struct ClosestMatch {
    substrings: HashMap<String, HashSet<String>>,
    substring_sizes: Vec<usize>,
}

#[derive(Debug)]
struct SplitWord {
    word: String,
    substrings: HashSet<String>,
}

#[derive(Debug)]
struct ScoreValue {
    word: String,
    score: f32,
}

fn split_word(word: String, sizes: &Vec<usize>) -> SplitWord {
    let mut substrings: HashSet<String> = HashSet::new();
    for size in sizes {
        if *size > word.len() {
            continue;
        }
        for x in 0..(word.len() - size + 1) {
            let sub = word[x..(x + size)].to_string();
            substrings.insert(sub);
        }
    }
    return SplitWord {
               word: word,
               substrings: substrings,
           };
}

fn evaluate(word_subs: &HashSet<String>,
            possible: String,
            possible_subs: &HashSet<String>)
            -> ScoreValue {
    let mut count = 0;
    let len_sum = word_subs.len() + possible_subs.len();
    for sub in word_subs {
        if possible_subs.contains(sub) {
            count += 1;
        }
    }
    let score = (count as f32) / (len_sum as f32);
    return ScoreValue {
               word: possible,
               score: score,
           };
}

fn max_score(a: ScoreValue, b: ScoreValue) -> ScoreValue {
    if a.score <= b.score {
        return b;
    }
    return a;
}

impl ClosestMatch {
    /// The function ```new``` takes a dictionary of known words with type ```Vec<String>``` and the
    /// different sizes of bag of words with type ```Vec<usize>```.
    /// It returns a ClosestMatch object.
    pub fn new(dictionary: Vec<String>, sizes: Vec<usize>) -> ClosestMatch {
        let mut substrings: HashMap<String, HashSet<String>> = HashMap::new();
        let splitwords: Vec<SplitWord> = dictionary
            .par_iter()
            .map(|possible| split_word(possible.to_lowercase(), &sizes))
            .collect();
        for splitword in splitwords {
            substrings.insert(splitword.word, splitword.substrings);
        }
        return ClosestMatch {
                   substrings: substrings,
                   substring_sizes: sizes,
               };
    }

    /// The function ```get_closest``` takes a word with type ```String``` and
    /// returns the closest word in the dictionary of known words.
    pub fn get_closest(&self, word: String) -> Option<String> {
        let word_subs = split_word(word, &self.substring_sizes).substrings;
        let best = self.substrings
            .par_iter()
            .map(|(possible, possible_subs)| {
                     evaluate(&word_subs, possible.to_lowercase(), possible_subs)
                 })
            .reduce_with(|a, b| max_score(a, b));
        match best {
            Some(expr) => Some(expr.word),
            None => None,
        }
    }
}


// Example function to find the closest match
fn find_closest_match<'a>(query: &str, options: &[&'a str]) -> Option<&'a str> {
    options.iter().min_by_key(|&option| levenshtein_distance(query, option)).cloned()
}

// Helper function to calculate Levenshtein distance
fn levenshtein_distance(s: &str, t: &str) -> usize {
    let s_chars: Vec<char> = s.chars().collect();
    let t_chars: Vec<char> = t.chars().collect();
    let s_len = s_chars.len();
    let t_len = t_chars.len();

    let mut dp = vec![vec![0; t_len + 1]; s_len + 1];
    for i in 0..=s_len {
        dp[i][0] = i;
    }
    for j in 0..=t_len {
        dp[0][j] = j;
    }

    for i in 1..=s_len {
        for j in 1..=t_len {
            let cost = if s_chars[i - 1] == t_chars[j - 1] { 0 } else { 1 };
            dp[i][j] = (dp[i - 1][j] + 1)
                .min(dp[i][j - 1] + 1)
                .min(dp[i - 1][j - 1] + cost);
        }
    }

    dp[s_len][t_len]
}

#[pyfunction]
fn closest_match<'a>(_py: Python, target: &str, candidates: Vec<&'a str>) -> Option<String> {
    let mut decoded_strings = Vec::new();
    for candidate in candidates {
        decoded_strings.push(unidecode(&candidate).to_string());
    }
    let cm = ClosestMatch::new(decoded_strings.clone(), [2, 3].to_vec());
    let closest = cm.get_closest(unidecode(target));
    for option in decoded_strings {
        if option.to_lowercase() == closest.clone()?.to_string() {
            return Some(option);
        }
    }
    None
}

#[pyfunction]
fn closest_match_distance<'a>(_py: Python, query: &str, options: Vec<&'a str>) -> Option<String> {
    let mut decoded_strings = Vec::new();
    for option in options {
        decoded_strings.push(unidecode(option).to_string());
    }
    let slice_of_string_slices: Vec<&str> = decoded_strings.iter().map(|s| s.as_str()).collect();
    let closest = find_closest_match(&unidecode(query), &slice_of_string_slices);
    
    // If a closest match is found, find the case exact match in decoded_strings
    if let Some(closest_str) = closest {
        // Iterate through decoded_strings to find the exact case match
        for option in &decoded_strings {
            if option == closest_str {
                // Return the closest match as it appears in decoded_strings
                return Some(option.clone());
            }
        }
    }
    None
}
#[pymodule]
fn fast_string_match(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(closest_match_distance, m)?)?;
    m.add_function(wrap_pyfunction!(closest_match, m)?)?;
    Ok(())
}

