use std::fs;
mod intcode;
use std::io;


fn main() {
    // part 3
    let filename: &str = "../5_input.txt";
    let contents: String = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");
    let input: Vec<i32> = contents.split(",").map(|n| n.parse().unwrap()).collect();
    let mut computer: intcode::Intcode = intcode::Intcode::new(input.clone());
    computer.set_input(1);
    let mut output: (i32, bool) = (0, false);
    while !computer.ready {
        output = computer.step();
    }
    println!("Diagnostic code: {}", output.0);

    let mut computer: intcode::Intcode = intcode::Intcode::new(input.clone());
    computer.set_input(5);
    let mut output: (i32, bool) = (0, false);
    let debug: bool = false;
    while !computer.ready{
        if debug {
            println!("{:?}", computer);
            println!("Press any key to continue...");
            io::stdin().read_line(&mut String::new()).unwrap();
        }
        output = computer.step();
    }
    if debug {
        println!("{:?}", computer);
    }
    println!("Second diagnostic code: {}", output.0);
}