fn main() {
    let _guess: u32 = "42".parse().expect("Not a number!");
    // Doesn't work:
    // let guess = "42".parse().expect("Not a number!");
    println!("Hello, world!");
}
