use itertools::Itertools;

pub struct MappingRange {
    pub src_range_start: u64,
    pub dst_range_start: u64,
    pub range_len: u64,
}

impl MappingRange {
    fn has_src(self: &MappingRange, source: u64) -> bool {
        return self.src_range_start <= source && source < (self.src_range_start + self.range_len);
    }

    pub fn get_dst(self: &MappingRange, source: u64) -> Option<u64> {
        return if self.has_src(source) {
            Some((source - self.src_range_start) + self.dst_range_start)
        } else {
            None
        };
    }
}

pub struct SrcToDstMap {
    pub range_info: Vec<MappingRange>,
}

impl SrcToDstMap {
    pub fn map_source(self: &SrcToDstMap, source: u64) -> u64 {
        for range in &self.range_info {
            let destination = range.get_dst(source);
            match destination {
                Some(i) => return i,
                None => {}
            }
        }

        return source;
    }
}

pub struct Input {
    pub seeds: Vec<u64>,
    pub chained_maps: Vec<SrcToDstMap>,
}


impl Input {
    pub fn total_seeds_to_consider(self: &Input) -> u64 {
        self.seeds.chunks(2).map(|c| c[1]).sum()
    }

    // pub fn for_all_part_2_seeds<T>(self, dostuff: dyn Fn(u64) -> T) {
    //     return 
    
    // }

    pub fn get_location(self: &Input, seed: u64) -> u64 {
        self.chained_maps.iter().fold(seed, |prev: u64, map: &SrcToDstMap| map.map_source(prev))
    }
}
