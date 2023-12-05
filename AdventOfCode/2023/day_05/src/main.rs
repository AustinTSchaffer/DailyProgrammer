#[macro_use]
extern crate lazy_static;

mod structs;

use regex::Regex;
use structs::Input;
use structs::MappingRange;
use structs::SrcToDstMap;
use rayon::prelude::*;

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

fn main() {
    let sample_input = parse_input("sample_input.txt");
    let input = parse_input("input.txt");

    println!("Part 1 (sample): {}", part_1(&sample_input));
    println!("Part 1: {}", part_1(&input));

    println!("Part 2 (sample): {}", part_2(&sample_input));
    println!("Part 2: {}", part_2(&input));
}
