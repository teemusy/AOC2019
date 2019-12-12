use std::fs;

fn main() {
    let filename: &str = "../1_input.txt";
    let contents: String = fs::read_to_string(filename)
        .expect("Could not read file");
    //convert string to vec
    let input_data: Vec<&str> = contents.split("\n").collect();

    let mut total_fuel: i32 = 0;
    let mut extra_fuel: i32 = 0;
    for row in input_data{
        let mass: i32 = row.to_string().trim().parse().unwrap();
        let fuel: i32 = calc_fuel(mass);
        total_fuel = total_fuel + fuel;
        extra_fuel = extra_fuel + calc_extra(fuel);
    }

    print!("First result: {}", total_fuel);
    print!("\nSecond result: {}", total_fuel + extra_fuel);

}

fn calc_fuel(mass: i32) -> i32{
    mass / 3 - 2
}

fn calc_extra(input_fuel: i32) -> i32{
    let mut left_fuel: i32 = input_fuel;
    let mut extra_fuel: i32 = 1;
    let mut fuel: i32 = 0;
    while extra_fuel > 0 {
        extra_fuel = left_fuel / 3 - 2;
        if extra_fuel > 0{
            fuel = fuel + extra_fuel;
            left_fuel = extra_fuel;
        }
    }
    fuel
}