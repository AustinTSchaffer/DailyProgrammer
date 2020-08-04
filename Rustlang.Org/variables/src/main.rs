#![allow(unused_variables)]
#![allow(unused_mut)]
#![allow(dead_code)]
fn main() {
    // Constants
    const MAX_POINTS: u32 = 100_000;

    // Mutability
    let mut x = 5;
    println!("The value of x is: {}", x);
    x = 6;
    println!("The value of x is: {}", x);

    // Shadowing
    let x = x + 1;
    let x = x * 2;
    println!("The value of x is: {}", x);

    let spaces = "   ";
    let spaces = spaces.len();
    println!("The value of spaces is: {}", spaces);

    let mut spaces = "      ";
    let spaces = spaces.len();
    println!("The value of spaces is: {}", spaces);
}
