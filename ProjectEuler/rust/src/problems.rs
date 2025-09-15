use crate::series;
use num_bigint::{BigUint};
use num_traits::FromPrimitive;
use num_integer::Integer;

pub fn p1() -> u64 {
    let mut sum: u64 = 0;

    for n in 1..1000 {
        if n % 3 == 0 || n % 5 == 0{
            sum += n;
        }
    }

    sum
}

pub fn p2() -> BigUint {
    let mut sum: BigUint = BigUint::ZERO;

    for n in series::fibonacci_vec_lt(BigUint::from_u64(4_000_000_u64).unwrap()) {
        if n.is_even() {
            sum += n;
        }
    }

    sum
}

pub fn p3() -> u64 {
    0    
}
