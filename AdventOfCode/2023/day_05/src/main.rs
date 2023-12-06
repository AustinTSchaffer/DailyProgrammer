#[macro_use]
extern crate lazy_static;

mod structs;

use rayon::collections::hash_map;
use regex::Regex;
use structs::Input;
use structs::MappingRange;
use structs::SrcToDstMap;
use rayon::prelude::*;
use rand::{seq::IteratorRandom, thread_rng};
use std::collections::HashMap;
use std::fs;

lazy_static! {
    static ref SRC_TO_DST_MAP_RE: Regex =
        Regex::new(r"(?P<dst_range_start>\d+) (?P<src_range_start>\d+) (?P<range_len>\d+)")
            .unwrap();
    static ref GREEDY_INT_RE: Regex = Regex::new(r"\d+").unwrap();
}

fn parse_input(filename: &str) -> Input {
    let contents = fs::read_to_string(filename).expect("File does not exist");
    let mut sections = contents.split("\n\n");

    let seeds = GREEDY_INT_RE
        .captures_iter(sections.next().unwrap())
        .map(|seed_str| seed_str[0].parse::<u64>().unwrap())
        .collect();

    let chained_maps = sections
        .map(|mapping_section_str| SrcToDstMap {
            range_info: SRC_TO_DST_MAP_RE
                .captures_iter(mapping_section_str)
                .map(|capture| MappingRange {
                    src_range_start: capture["src_range_start"].parse::<u64>().unwrap(),
                    dst_range_start: capture["dst_range_start"].parse::<u64>().unwrap(),
                    range_len: capture["range_len"].parse::<u64>().unwrap(),
                })
                .collect(),
        })
        .collect();

    Input {
        seeds: seeds,
        chained_maps: chained_maps,
    }
}

fn part_1(input: &Input) -> u64 {
    input.seeds.iter().map(|seed| input.get_location(*seed)).min().unwrap()
}

fn part_2(input: &Input) -> u64 {
    input.seeds
        .chunks(2)
        .par_bridge()
        .flat_map(|c| {
            c[0]..(c[0] + c[1])
        })
        .map(|seed| {
            input.get_location(seed)
        }).min().unwrap()
}

fn get_stats(input: &Input) {
    let ranges: Vec<(u64, u64)> = input.seeds
        .chunks(2)
        .map(|c| {
            (c[0], (c[0] + c[1]))
        })
        .collect();

    let min = ranges.iter().map(|(start, _)| start).min().unwrap();
    let max = ranges.iter().map(|(_, end)| end).min().unwrap();
    let total_range = max - min;
    let naive_range = input.total_seeds_to_consider();

    dbg!(min, max, total_range, naive_range);

    let mut overlapping_ranges: HashMap<u64, u64> = HashMap::new();

    let mut sorted_ranges = ranges.clone();
    sorted_ranges.sort_by(|(starta,_), (startb, _)| starta.cmp(startb));

    for (i, range) in sorted_ranges.iter().enumerate() {
        current_nesting += 1;
        overlapping_ranges.insert(range.0, current_nesting);
        let range_end = range.0 + range.1;
        let mut j = 1;
        while sorted_ranges[j].0 <= range_end {

        }
    }

}

fn main() {
    let sample_input = parse_input("sample_input.txt");
    let input = parse_input("input.txt");

    get_stats(&input);

    // println!("Part 1 (sample): {}", part_1(&sample_input));
    // println!("Part 1: {}", part_1(&input));

    // println!("Part 2 (sample): {}", part_2(&sample_input));
    // println!("Part 2: {}", part_2(&input));
}
