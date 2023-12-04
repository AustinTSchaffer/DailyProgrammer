#[macro_use]
extern crate lazy_static;

use regex::Regex;

use std::env;
use std::fs;

struct ScratcherCard {
    id: u32,
    winning_numbers: Vec<bool>,
    actual_numbers: Vec<u32>,
}

lazy_static! {
    static ref SCRATCHER_CARD_RE: Regex = Regex::new(r"Card\s{1,3}(?P<card_number>\d{1,3}):\s{1,2}(?P<winning_numbers>(\d{1,2}\s+)+)\|\s{1,2}(?P<actual_numbers>(\d{1,2}\s*)+)").unwrap();
    static ref GREEDY_INT_RE: Regex = Regex::new(r"\d+").unwrap();
}

fn parse_input(filename: &str) -> Vec<ScratcherCard> {
    let contents = fs::read_to_string(filename)
        .expect("File does not exist");

    let mut output: Vec<ScratcherCard> = Vec::new();

    for caps in SCRATCHER_CARD_RE.captures_iter(&contents) {
        let mut winning_numbers: Vec<bool> = vec![false; 100];
        let mut actual_numbers: Vec<u32> = Vec::new();

        for wn_cap in GREEDY_INT_RE.captures_iter(&caps["winning_numbers"]) {
            winning_numbers[wn_cap[0].parse::<usize>().unwrap()] = true;
        }

        for an_cap in GREEDY_INT_RE.captures_iter(&caps["actual_numbers"]) {
            actual_numbers.push(an_cap[0].parse::<u32>().unwrap())
        }

        output.push(ScratcherCard {
            id: caps["card_number"].parse::<u32>().unwrap(),
            actual_numbers,
            winning_numbers,
        })
    }

    return output;
}

fn part_1(input: &Vec<ScratcherCard>) -> u64 {
    let mut output = 0;

    for card in input {
        let mut value: u64 = 0;
        for actual_num in &card.actual_numbers {
            if card.winning_numbers[(*actual_num) as usize] {
                if value == 0 {
                    value = 1
                } else {
                    value <<= 1
                }
            }
        }
        output += value
    }

    return output;
}

fn part_2(input: &Vec<ScratcherCard>) -> u64 {
    let mut cards_generated: Vec<u64> = vec![0; input.len()];

    input.iter().rev().enumerate().for_each(|(rev_index, card)| {
        let index = input.len() - 1 - rev_index;
        cards_generated[index] = 1;

        let num_matching_numbers = 
            card.actual_numbers.iter().filter(|&&n| card.winning_numbers[n as usize]).count();

        for other_card_index in (index+1)..std::cmp::min(index + num_matching_numbers + 1, input.len()) {
            cards_generated[index] += cards_generated[other_card_index];
        }
    });

    return cards_generated.iter().sum();
}

fn main() {
    let sample_input = parse_input("sample_input.txt");
    let input = parse_input("input.txt");

    println!("Part 1 (sample): {}", part_1(&sample_input));
    println!("Part 1: {}", part_1(&input));

    println!("Part 2 (sample): {}", part_2(&sample_input));
    println!("Part 2: {}", part_2(&input));
}
