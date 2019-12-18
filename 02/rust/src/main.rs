use std::fs;
mod intcode;


fn main() {
    let filename: &str = "../2_input.txt";
    let contents: String = fs::read_to_string(filename)
        .expect("Something went wrong reading the file");
    let input: Vec<i32> = contents.split(",").map(|n| n.parse().unwrap()).collect();
    let mut computer: intcode::Intcode = intcode::Intcode::new(input.clone());
    // change values for part 1
    computer.code[1] = 12;
    computer.code[2] = 2;

    // part 1
    while !computer.ready {
        computer.step();
    }
    println!("First part answer: {}", computer.code[0]);

    // bruteforce the answer to part 2
    let expected_value = 19690720;
    let return_value = part_two(input.clone(), expected_value);
    println!("Second part answer: {}", return_value);
}


fn part_two(input: Vec<i32>, expected_value: i32) -> i32{
    let mut output = 0;
    'label: for i in 0..100{
        for j in 0..100{
            let mut computer: intcode::Intcode = intcode::Intcode::new(input.clone());
            computer.code[1] = i;
            computer.code[2] = j;
            while !computer.ready {
                computer.step();
            }
            if computer.code[0] == expected_value{
                output = 100 * computer.code[1] + computer.code[2];
                break 'label;
            }
        }
    }
    output
}