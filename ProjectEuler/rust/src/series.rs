use num_bigint::BigUint;
use num_traits::One;

pub fn fibonacci(n: u64) -> BigUint {
    let mut b: BigUint = BigUint::ZERO;
    let mut a: BigUint = BigUint::one();
    let mut count: u64 = 0;

    while count < n {
        let tmp: BigUint = &a + b;
        b = a;
        a = tmp;
        count += 1;
    }

    b
}

pub fn fibonacci_vec_n(n: usize) -> Vec<BigUint> {
    let mut vec = Vec::with_capacity(n);

    let mut n_curr: BigUint = BigUint::one();
    let mut n_prev: BigUint = BigUint::ZERO;

    for _ in 0..n {
        vec.push(n_curr.clone());

        let tmp: BigUint = &n_curr + n_prev;
        n_prev = n_curr;
        n_curr = tmp;
    }

    vec
}

pub(crate) fn fibonacci_vec_lt(lt: BigUint) -> Vec<BigUint> {
    let mut vec = Vec::new();

    let mut n_prev: BigUint = BigUint::ZERO;
    let mut n_curr: BigUint = BigUint::one();

    while n_curr < lt {
        vec.push(n_curr.clone());

        let tmp: BigUint = &n_curr + n_prev;
        n_prev = n_curr;
        n_curr = tmp;
    }

    vec
}
